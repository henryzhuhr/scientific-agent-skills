#!/usr/bin/env python3
"""Build a Simplified Chinese mirror of the scientific-skills tree.

The script copies non-Markdown files as-is and translates Markdown files to
scientific-skills-zh while preserving frontmatter keys, code blocks, inline
code, links, and file structure as much as possible.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import shutil
import sqlite3
import sys
import time
from pathlib import Path
from typing import Iterable
from urllib import error, parse, request


DEFAULT_SOURCE = "scientific-skills"
DEFAULT_TARGET = "scientific-skills-zh"
DEFAULT_CACHE = ".translation_cache.sqlite3"
DEFAULT_GOOGLE_MODEL = "google-translate-gtx"
DEFAULT_OPENAI_MODEL = "gpt-4.1-mini"
DEFAULT_DEEPSEEK_MODEL = "deepseek-chat"
UNPROTECTED_GLOSSARY_TERMS = {"infographics", "phylogenetics"}
GLOSSARY_BOUNDARY = r"A-Za-z0-9_/-"
FENCED_CODE_PATTERN = re.compile(r"(^```.*?^```[ \t]*\n?|^~~~.*?^~~~[ \t]*\n?)", re.MULTILINE | re.DOTALL)
INLINE_CODE_PATTERN = re.compile(r"`[^`\n]+`")
FRONTMATTER_PATTERN = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)


SYSTEM_PROMPT = """You translate technical Markdown documentation into Simplified Chinese.
Preserve Markdown syntax exactly whenever possible. Do not translate file paths,
commands, package names, API identifiers, environment variables, URLs, model
names, placeholders such as ZXQBLOCK0QXZ, or content that is already Chinese. Output only the
translated Markdown fragment."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="Source skills directory")
    parser.add_argument("--target", default=DEFAULT_TARGET, help="Target translated directory")
    parser.add_argument(
        "--provider",
        choices=["auto", "google", "openai", "deepseek"],
        default="auto",
        help="Translation provider",
    )
    parser.add_argument("--model", default=None, help="Override the default model name")
    parser.add_argument("--cache-db", default=DEFAULT_CACHE, help="SQLite cache file")
    parser.add_argument(
        "--only-subdir",
        action="append",
        default=[],
        help="Only translate files under the given top-level skill subdirectory; repeatable",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=14000,
        help="Maximum characters per translation request",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip files whose translated target already exists",
    )
    parser.add_argument(
        "--limit-files",
        type=int,
        default=0,
        help="Translate at most N Markdown files after filtering (0 means no limit)",
    )
    parser.add_argument(
        "--shard-count",
        type=int,
        default=1,
        help="Split top-level skill directories into N shards",
    )
    parser.add_argument(
        "--shard-index",
        type=int,
        default=0,
        help="Zero-based shard index to process",
    )
    parser.add_argument(
        "--google-timeout",
        type=int,
        default=30,
        help="Per-request timeout in seconds for Google Translate",
    )
    parser.add_argument(
        "--google-retries",
        type=int,
        default=8,
        help="Maximum retry attempts for Google Translate requests",
    )
    parser.add_argument(
        "--request-delay",
        type=float,
        default=0.2,
        help="Delay in seconds before each outbound translation request",
    )
    parser.add_argument(
        "--fail-log",
        default=None,
        help="Optional file path to store relative paths that failed to translate",
    )
    parser.add_argument(
        "--normalize-existing",
        action="store_true",
        help="Normalize Markdown syntax in the target tree without translating",
    )
    return parser.parse_args()


class Cache:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS translations (
                cache_key TEXT PRIMARY KEY,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                output TEXT NOT NULL,
                created_at INTEGER NOT NULL
            )
            """
        )
        self.conn.commit()

    def get(self, cache_key: str) -> str | None:
        row = self.conn.execute(
            "SELECT output FROM translations WHERE cache_key = ?",
            (cache_key,),
        ).fetchone()
        return row[0] if row else None

    def put(self, cache_key: str, provider: str, model: str, output: str) -> None:
        self.conn.execute(
            """
            INSERT OR REPLACE INTO translations (cache_key, provider, model, output, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (cache_key, provider, model, output, int(time.time())),
        )
        self.conn.commit()


class Translator:
    def __init__(
        self,
        provider: str,
        model: str,
        cache: Cache,
        glossary_terms: list[str] | None = None,
        *,
        request_delay: float = 0.0,
        google_timeout: int = 30,
        google_retries: int = 8,
    ) -> None:
        self.provider = provider
        self.model = model
        self.cache = cache
        self.request_delay = max(request_delay, 0.0)
        self.google_timeout = google_timeout
        self.google_retries = google_retries
        self.glossary_terms = sorted(
            {term for term in (glossary_terms or []) if term not in UNPROTECTED_GLOSSARY_TERMS},
            key=len,
            reverse=True,
        )
        if provider == "google":
            self.api_key = None
            self.endpoint = "https://translate.googleapis.com/translate_a/single"
        elif provider == "openai":
            self.api_key = os.environ.get("OPENAI_API_KEY")
            self.endpoint = "https://api.openai.com/v1/chat/completions"
        elif provider == "deepseek":
            self.api_key = os.environ.get("DEEPSEEK_API_KEY")
            self.endpoint = "https://api.deepseek.com/v1/chat/completions"
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        if provider != "google" and not self.api_key:
            raise RuntimeError(f"Missing API key for provider {provider}")

    def _protect_glossary_terms(self, fragment: str) -> tuple[str, list[str]]:
        if not self.glossary_terms:
            return fragment, []

        tokens: list[str] = []
        protected = fragment

        for term in self.glossary_terms:
            pattern = re.compile(rf"(?<![{GLOSSARY_BOUNDARY}]){re.escape(term)}(?![{GLOSSARY_BOUNDARY}])", re.IGNORECASE)

            def replacer(match: re.Match[str]) -> str:
                token = f"ZXQTERM{len(tokens)}QXZ"
                tokens.append(match.group(0))
                return token

            protected = pattern.sub(replacer, protected)

        return protected, tokens

    @staticmethod
    def _restore_glossary_terms(fragment: str, tokens: list[str]) -> str:
        restored = fragment
        for index, token in enumerate(tokens):
            restored = restored.replace(f"ZXQTERM{index}QXZ", token)
        return restored

    def _cache_key(self, text: str) -> str:
        payload = f"{self.provider}\0{self.model}\0{text}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def translate_fragment(self, fragment: str, *, description_mode: bool = False) -> str:
        if not fragment.strip():
            return fragment

        protected_fragment, glossary_tokens = self._protect_glossary_terms(fragment)

        mode_prefix = "description" if description_mode else "markdown"
        cache_key = self._cache_key(f"{mode_prefix}\n{protected_fragment}")
        cached = self.cache.get(cache_key)
        if cached is not None:
            return self._restore_glossary_terms(cached, glossary_tokens)

        if self.provider == "google":
            output = self._translate_with_google(protected_fragment)
            self.cache.put(cache_key, self.provider, self.model, output)
            return self._restore_glossary_terms(output, glossary_tokens)

        if description_mode:
            user_prompt = (
                "Translate the following short technical description into Simplified Chinese. "
                "Preserve product names, package names, API names, file paths, and model names. "
                "Output only the translated description.\n\n"
                f"{protected_fragment}"
            )
        else:
            user_prompt = (
                "Translate the following Markdown fragment into Simplified Chinese.\n"
                "Rules:\n"
                "- Preserve Markdown syntax, headings, tables, links, emphasis, and list markers.\n"
                "- Do not translate placeholders like ZXQBLOCK0QXZ.\n"
                "- Do not translate file paths, commands, package names, API identifiers, environment variables, URLs, or already-Chinese text.\n"
                "- Keep the output structurally close to the input.\n"
                "- Output only the translated Markdown fragment.\n\n"
                f"{protected_fragment}"
            )

        payload = {
            "model": self.model,
            "temperature": 0.1,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        }

        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        for attempt in range(5):
            req = request.Request(self.endpoint, data=body, headers=headers, method="POST")
            try:
                with request.urlopen(req, timeout=180) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                output = data["choices"][0]["message"]["content"].strip()
                self.cache.put(cache_key, self.provider, self.model, output)
                return self._restore_glossary_terms(output, glossary_tokens)
            except error.HTTPError as exc:
                retryable = exc.code in {408, 409, 425, 429, 500, 502, 503, 504}
                if attempt == 4 or not retryable:
                    details = exc.read().decode("utf-8", errors="replace")
                    raise RuntimeError(f"API request failed ({exc.code}): {details}") from exc
                time.sleep(2**attempt)
            except error.URLError as exc:
                if attempt == 4:
                    raise RuntimeError(f"Network error: {exc}") from exc
                time.sleep(2**attempt)

        raise RuntimeError("Translation failed after retries")

    def _translate_with_google(self, fragment: str) -> str:
        payload = parse.urlencode(
            {
                "client": "gtx",
                "sl": "en",
                "tl": "zh-CN",
                "dt": "t",
                "q": fragment,
            }
        ).encode("utf-8")
        for attempt in range(self.google_retries):
            req = request.Request(
                self.endpoint,
                data=payload,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                },
            )
            try:
                if self.request_delay:
                    time.sleep(self.request_delay)
                with request.urlopen(req, timeout=self.google_timeout) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                return "".join(part[0] for part in data[0] if part and part[0])
            except Exception:
                if attempt == self.google_retries - 1:
                    raise
                time.sleep(min(20, (2**attempt) + random.random()))

        raise RuntimeError("Google translation failed after retries")


def choose_provider(provider: str, model: str | None) -> tuple[str, str]:
    if provider == "google":
        return "google", model or DEFAULT_GOOGLE_MODEL
    if provider == "openai":
        return "openai", model or DEFAULT_OPENAI_MODEL
    if provider == "deepseek":
        return "deepseek", model or DEFAULT_DEEPSEEK_MODEL

    return "google", model or DEFAULT_GOOGLE_MODEL


def should_include(path: Path, only_subdirs: set[str]) -> bool:
    if not only_subdirs:
        return True
    return bool(path.parts) and path.parts[0] in only_subdirs


def resolve_selected_subdirs(source: Path, only_subdirs: set[str], shard_count: int, shard_index: int) -> set[str]:
    if shard_count < 1:
        raise ValueError("--shard-count must be at least 1")
    if shard_index < 0 or shard_index >= shard_count:
        raise ValueError("--shard-index must be in the range [0, shard_count)")

    all_subdirs = sorted(path.name for path in source.iterdir() if path.is_dir())
    sharded_subdirs = {name for idx, name in enumerate(all_subdirs) if idx % shard_count == shard_index}
    if only_subdirs:
        return only_subdirs & sharded_subdirs
    return sharded_subdirs


def replace_scientific_root(text: str) -> str:
    return text.replace("scientific-skills/", "scientific-skills-zh/")


def read_text_with_fallback(path: Path) -> tuple[str, bool]:
    try:
        return path.read_text(encoding="utf-8"), False
    except UnicodeDecodeError:
        data = path.read_bytes()
        return data.decode("utf-8", errors="replace"), True


def write_text_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.{os.getpid()}.{random.randrange(1_000_000)}.tmp")
    try:
        temp_path.write_text(content, encoding="utf-8")
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink(missing_ok=True)


def split_frontmatter(content: str) -> tuple[str | None, str]:
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return None, content
    return match.group(1), content[match.end() :]


def translate_description_line(line: str, translator: Translator) -> str:
    match = re.match(r"^(\s*description:\s*)(.*)$", line)
    if not match:
        return line

    prefix, value = match.groups()
    value = value.rstrip()
    if not value:
        return line

    quote = ""
    stripped = value.strip()
    if stripped and stripped[0] in {'"', "'"} and stripped[-1:] == stripped[0]:
        quote = stripped[0]
        stripped = stripped[1:-1]

    translated = translator.translate_fragment(stripped, description_mode=True)
    translated = translated.replace("\n", " ").strip()
    if quote:
        return f"{prefix}{quote}{translated}{quote}"
    return f"{prefix}{translated}"


def translate_frontmatter(frontmatter: str | None, translator: Translator) -> str:
    if frontmatter is None:
        return ""

    lines = frontmatter.splitlines()
    translated_lines = [translate_description_line(line, translator) for line in lines]
    return "---\n" + "\n".join(translated_lines) + "\n---\n"


def mask_tokens(text: str, pattern: re.Pattern[str], prefix: str) -> tuple[str, list[str]]:
    tokens: list[str] = []

    def replacer(match: re.Match[str]) -> str:
        token = f"ZXQ{prefix}{len(tokens)}QXZ"
        tokens.append(match.group(0))
        return token

    return pattern.sub(replacer, text), tokens


def restore_tokens(text: str, prefix: str, tokens: Iterable[str]) -> str:
    restored = text
    for index, token in enumerate(tokens):
        restored = restored.replace(f"ZXQ{prefix}{index}QXZ", token)
    return restored


def chunk_text(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    current = ""
    for part in re.split(r"(\n\n+)", text):
        if not part:
            continue
        if len(current) + len(part) <= max_chars:
            current += part
            continue

        if current:
            chunks.append(current)
            current = ""

        if len(part) <= max_chars:
            current = part
            continue

        start = 0
        while start < len(part):
            end = min(start + max_chars, len(part))
            chunks.append(part[start:end])
            start = end

    if current:
        chunks.append(current)
    return chunks


def normalize_translated_text(text: str) -> str:
    text = re.sub(r"(?<!>)[ \t]+([，。；：！？）】》])", r"\1", text)
    text = re.sub(r"([（【《])[ \t]+", r"\1", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff\)\]】》])[ \t]+(?=[\u4e00-\u9fff])", "", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff])[ \t]+(?=[，。；：！？])", "", text)
    return text


def repair_markdown_syntax(text: str) -> str:
    repaired_lines: list[str] = []
    previous_nonempty = ""
    for line in text.splitlines():
        spaced_heading = re.match(r"^(\s*)(#(?:\s+#)+)\s*(\S.*)?$", line)
        if spaced_heading:
            level = spaced_heading.group(2).count("#")
            content = spaced_heading.group(3) or ""
            line = f"{spaced_heading.group(1)}{'#' * min(level, 6)} {content}".rstrip()
        line = re.sub(r"^(\s*)(#{1,6})([^\s#])", r"\1\2 \3", line)
        line = re.sub(r"^(\s*)(\d+)[。．、]\s*", r"\1\2. ", line)
        line = re.sub(r"^(\s*)(\d+)\.(\S)", r"\1\2. \3", line)
        line = re.sub(r"^(\s*)([-*+])(\S)", r"\1\2 \3", line)
        line = re.sub(r"^(\s*)([-*+]\s+\[[ xX]\])(\S)", r"\1\2 \3", line)
        line = re.sub(r"^(\s*>)(\S)", r"\1 \2", line)
        if re.match(r"^ ([-*+]\s+|\d+\.\s+)", line) and re.match(r"^\s{0,2}([-*+]\s+|\d+\.\s+)", previous_nonempty):
            line = " " + line
        if re.match(r"^ [^\s#>*+-]", line) and (not previous_nonempty or previous_nonempty.lstrip().startswith("#")):
            line = line.lstrip()
        repaired_lines.append(line)
        if line.strip():
            previous_nonempty = line
    return "\n".join(repaired_lines)


def normalize_existing_markdown(content: str) -> str:
    frontmatter, body = split_frontmatter(content)

    normalized_frontmatter = ""
    if frontmatter is not None:
        frontmatter_lines = [normalize_translated_text(replace_scientific_root(line)) for line in frontmatter.splitlines()]
        normalized_frontmatter = "---\n" + "\n".join(frontmatter_lines) + "\n---\n"

    masked, code_tokens = mask_tokens(body, FENCED_CODE_PATTERN, "BLOCK")
    masked, inline_tokens = mask_tokens(masked, INLINE_CODE_PATTERN, "INLINE")
    normalized_body = repair_markdown_syntax(masked)
    normalized_body = replace_scientific_root(normalized_body)
    normalized_body = normalize_translated_text(normalized_body)
    normalized_body = restore_tokens(normalized_body, "INLINE", inline_tokens)
    normalized_body = restore_tokens(normalized_body, "BLOCK", code_tokens)

    normalized = normalized_frontmatter + normalized_body
    if content.endswith("\n") and not normalized.endswith("\n"):
        normalized += "\n"
    return normalized


def translate_line_content(text: str, translator: Translator) -> str:
    stripped = text.strip()
    if not stripped:
        return text
    if re.fullmatch(r"ZXQ(?:BLOCK|INLINE)\d+QXZ", stripped):
        return text

    leading = text[: len(text) - len(text.lstrip())]
    trailing = text[len(text.rstrip()) :]
    translated = translator.translate_fragment(stripped)
    translated = normalize_translated_text(translated.replace("\n", " ").strip())
    return f"{leading}{translated}{trailing}"


def is_table_separator_line(line: str) -> bool:
    return bool(re.fullmatch(r"\s*\|?(?:\s*:?-+:?\s*\|)+\s*:?-+:?\s*\|?\s*", line))


def translate_table_line(line: str, translator: Translator) -> str:
    if is_table_separator_line(line):
        return line

    stripped = line.strip()
    if "|" not in stripped:
        return translate_line_content(line, translator)

    leading = line[: len(line) - len(line.lstrip())]
    trailing = line[len(line.rstrip()) :]
    body = stripped
    left_pipe = body.startswith("|")
    right_pipe = body.endswith("|")
    inner = body[1:-1] if left_pipe and right_pipe else body.strip("|")

    translated_cells = []
    for cell in inner.split("|"):
        if not cell.strip():
            translated_cells.append(cell)
            continue
        cell_leading = cell[: len(cell) - len(cell.lstrip())]
        cell_trailing = cell[len(cell.rstrip()) :]
        cell_text = normalize_translated_text(translator.translate_fragment(cell.strip()).replace("\n", " ").strip())
        translated_cells.append(f"{cell_leading}{cell_text}{cell_trailing}")

    rebuilt = "|".join(translated_cells)
    if left_pipe:
        rebuilt = f"|{rebuilt}"
    if right_pipe:
        rebuilt = f"{rebuilt}|"
    return f"{leading}{rebuilt}{trailing}"


def translate_markdown_line(line: str, translator: Translator) -> str:
    if not line.strip():
        return line
    if re.fullmatch(r"\s*ZXQ(?:BLOCK|INLINE)\d+QXZ\s*", line):
        return line
    if re.fullmatch(r"\s*[-*_]{3,}\s*", line):
        return line
    if is_table_separator_line(line):
        return line
    if "|" in line and line.lstrip().startswith("|"):
        return translate_table_line(line, translator)

    patterns = [
        re.compile(r"^(\s*#{1,6}\s+)(.+?)(\s*#*\s*)$"),
        re.compile(r"^(\s*[-*+]\s+\[[ xX]\]\s+)(.+)$"),
        re.compile(r"^(\s*[-*+]\s+)(.+)$"),
        re.compile(r"^(\s*\d+\.\s+)(.+)$"),
        re.compile(r"^(\s*>\s+)(.+)$"),
    ]

    for pattern in patterns:
        match = pattern.match(line)
        if match:
            prefix = match.group(1)
            content = match.group(2)
            suffix = match.group(3) if pattern.groups >= 3 else ""
            translated_content = translate_line_content(content, translator).strip()
            return f"{prefix}{translated_content}{suffix}"

    return translate_line_content(line, translator)


def translate_body(body: str, translator: Translator, max_chars: int) -> str:
    masked, code_tokens = mask_tokens(body, FENCED_CODE_PATTERN, "BLOCK")
    masked, inline_tokens = mask_tokens(masked, INLINE_CODE_PATTERN, "INLINE")

    translated_parts = []
    for chunk in chunk_text(masked, max_chars):
        protected_chunk, newline_tokens = mask_tokens(chunk, re.compile(r"\n+"), "NL")
        translated_chunk = translator.translate_fragment(protected_chunk)
        translated_parts.append(restore_tokens(translated_chunk, "NL", newline_tokens))

    translated = "".join(translated_parts)

    translated = restore_tokens(translated, "INLINE", inline_tokens)
    translated = repair_markdown_syntax(translated)
    translated = restore_tokens(translated, "BLOCK", code_tokens)
    return normalize_translated_text(translated)


def translate_markdown(content: str, translator: Translator, max_chars: int) -> str:
    frontmatter, body = split_frontmatter(content)
    translated = translate_frontmatter(frontmatter, translator) + translate_body(body, translator, max_chars)
    translated = replace_scientific_root(translated)
    translated = normalize_translated_text(translated)
    if content.endswith("\n") and not translated.endswith("\n"):
        translated += "\n"
    return translated


def normalize_existing_tree(target: Path) -> int:
    files = sorted(target.rglob("*.md"))
    for file_path in files:
        original, used_fallback = read_text_with_fallback(file_path)
        if used_fallback:
            print(f"[warn] decode fallback used for {file_path.relative_to(target)}")
        normalized = normalize_existing_markdown(original)
        if normalized != original:
            write_text_atomic(file_path, normalized)
            print(f"[normalized] {file_path.relative_to(target)}")
    print(f"Normalized {len(files)} markdown files.")
    return len(files)


def iter_source_files(source: Path, only_subdirs: set[str]) -> tuple[list[Path], list[Path]]:
    markdown_files: list[Path] = []
    passthrough_files: list[Path] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(source)
        if not should_include(rel, only_subdirs):
            continue
        if path.suffix.lower() == ".md":
            markdown_files.append(path)
        else:
            passthrough_files.append(path)
    return markdown_files, passthrough_files


def build_glossary_terms(source: Path) -> list[str]:
    return sorted({path.name for path in source.iterdir() if path.is_dir()})


def copy_passthrough(files: Iterable[Path], source: Path, target: Path) -> None:
    for path in files:
        rel = path.relative_to(source)
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)


def translate_files(
    markdown_files: list[Path],
    source: Path,
    target: Path,
    translator: Translator,
    *,
    max_chars: int,
    skip_existing: bool,
    limit_files: int,
) -> list[Path]:
    processed = 0
    total = len(markdown_files) if limit_files <= 0 else min(len(markdown_files), limit_files)
    effective_max_chars = min(max_chars, 1800) if translator.provider == "google" else max_chars
    failures: list[Path] = []
    for path in markdown_files:
        if limit_files > 0 and processed >= limit_files:
            break

        rel = path.relative_to(source)
        dest = target / rel
        if skip_existing and dest.exists():
            print(f"[skip] {rel}")
            continue

        try:
            text = path.read_text(encoding="utf-8")
            translated = translate_markdown(text, translator, effective_max_chars)
            write_text_atomic(dest, translated)

            processed += 1
            print(f"[{processed}/{total}] translated {rel}")
        except Exception as exc:
            failures.append(rel)
            print(f"[error] {rel}: {exc}")

    return failures


def main() -> int:
    args = parse_args()
    source = Path(args.source)
    target = Path(args.target)
    if not source.exists():
        raise FileNotFoundError(f"Source directory not found: {source}")

    provider, model = choose_provider(args.provider, args.model)
    cache = Cache(Path(args.cache_db))
    translator = Translator(
        provider,
        model,
        cache,
        glossary_terms=build_glossary_terms(source),
        request_delay=args.request_delay,
        google_timeout=args.google_timeout,
        google_retries=args.google_retries,
    )
    only_subdirs = resolve_selected_subdirs(source, set(args.only_subdir), args.shard_count, args.shard_index)

    markdown_files, passthrough_files = iter_source_files(source, only_subdirs)
    print(f"Using provider={provider} model={model}")
    print(f"Shard: {args.shard_index + 1}/{args.shard_count}")
    print(f"Markdown files: {len(markdown_files)}")
    print(f"Passthrough files: {len(passthrough_files)}")

    if args.normalize_existing:
        normalize_existing_tree(target)
        return 0

    target.mkdir(parents=True, exist_ok=True)
    copy_passthrough(passthrough_files, source, target)
    failures = translate_files(
        markdown_files,
        source,
        target,
        translator,
        max_chars=args.max_chars,
        skip_existing=args.skip_existing,
        limit_files=args.limit_files,
    )

    if args.fail_log:
        fail_log_path = Path(args.fail_log)
        fail_log_path.write_text("\n".join(str(path) for path in failures) + ("\n" if failures else ""), encoding="utf-8")

    if failures:
        print(f"Completed with {len(failures)} failed file(s).")
        return 1

    print("Completed with no translation failures.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        raise SystemExit(130)