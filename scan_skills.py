#!/usr/bin/env python3
"""Scan all skills for security issues and produce SECURITY.md."""

import argparse
import os
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv() -> None:
        return None

from skill_scanner import SkillScanner
from skill_scanner.core.analyzers import (
    BehavioralAnalyzer,
    LLMAnalyzer,
    TriggerAnalyzer,
)
from skill_scanner.core.loader import SkillLoadError
from skill_scanner.core.models import Report
from skill_scanner.core.scan_policy import ScanPolicy

load_dotenv()

DEFAULT_SKILLS_DIR = "scientific-skills"
DEFAULT_OUTPUT_FILE = "SECURITY.md"


TRANSLATIONS = {
    "en": {
        "report_title": "# Security Scan Report",
        "generated": "**Generated:** {value}  ",
        "skills_scanned": "**Skills scanned:** {value}  ",
        "total_findings": "**Total findings:** {value}  ",
        "headline": "**Critical:** {critical} | **High:** {high} | **Safe skills:** {safe}/{total}",
        "summary": "## Summary",
        "table_skill": "Skill",
        "table_severity": "Severity",
        "table_findings": "Findings",
        "table_safe": "Safe",
        "table_duration": "Duration",
        "detailed_findings": "## Detailed Findings",
        "file": "File",
        "remediation": "Remediation",
        "no_findings": "No findings to report — all skills passed.",
    },
    "zh": {
        "report_title": "# 安全扫描报告",
        "generated": "**生成时间：** {value}  ",
        "skills_scanned": "**扫描技能数：** {value}  ",
        "total_findings": "**发现总数：** {value}  ",
        "headline": "**严重：** {critical} | **高危：** {high} | **安全技能：** {safe}/{total}",
        "summary": "## 汇总",
        "table_skill": "技能",
        "table_severity": "严重级别",
        "table_findings": "发现数",
        "table_safe": "安全",
        "table_duration": "耗时",
        "detailed_findings": "## 详细发现",
        "file": "文件",
        "remediation": "修复建议",
        "no_findings": "没有需要报告的发现，所有技能均通过扫描。",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-dir",
        default=DEFAULT_SKILLS_DIR,
        help="Directory containing skills to scan",
    )
    parser.add_argument(
        "--output-file",
        default=DEFAULT_OUTPUT_FILE,
        help="Markdown report path to write",
    )
    parser.add_argument(
        "--lang",
        choices=sorted(TRANSLATIONS.keys()),
        default="en",
        help="Report language",
    )
    return parser.parse_args()


def build_scanner() -> SkillScanner:
    policy = ScanPolicy.from_preset("balanced")
    policy.llm_analysis.max_instruction_body_chars = 75_000
    policy.llm_analysis.max_referenced_file_chars = 75_000
    policy.llm_analysis.max_code_file_chars = 75_000
    policy.llm_analysis.max_total_prompt_chars = 500_000
    llm_model = os.getenv("SKILL_SCANNER_LLM_MODEL", "anthropic/claude-sonnet-4-6")
    llm_key = os.getenv("SKILL_SCANNER_LLM_API_KEY")

    analyzers = [
        BehavioralAnalyzer(),
        TriggerAnalyzer(),
    ]
    if llm_key:
        analyzers.append(LLMAnalyzer(model=llm_model, api_key=llm_key, policy=policy))
    else:
        print("SKILL_SCANNER_LLM_API_KEY not set; running without LLM analysis.")

    scanner = SkillScanner(
        analyzers=analyzers,
        policy=policy,
    )
    return scanner


def severity_badge(sev: str) -> str:
    icons = {
        "CRITICAL": "🔴",
        "HIGH": "🟠",
        "MEDIUM": "🟡",
        "LOW": "🔵",
        "INFO": "⚪",
        "SAFE": "🟢",
    }
    return f"{icons.get(sev, '⚫')} {sev}"


def generate_report(report, lang: str = "en") -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = []
    t = TRANSLATIONS[lang]

    lines.append(t["report_title"])
    lines.append("")
    lines.append(t["generated"].format(value=now))
    lines.append(t["skills_scanned"].format(value=report.total_skills_scanned))
    lines.append(t["total_findings"].format(value=report.total_findings))
    lines.append(
        t["headline"].format(
            critical=report.critical_count,
            high=report.high_count,
            safe=report.safe_count,
            total=report.total_skills_scanned,
        )
    )
    lines.append("")

    # Summary table
    lines.append(t["summary"])
    lines.append("")
    lines.append(
        f"| {t['table_skill']} | {t['table_severity']} | {t['table_findings']} | {t['table_safe']} | {t['table_duration']} |"
    )
    lines.append("|-------|----------|----------|------|----------|")

    sorted_results = sorted(
        report.scan_results,
        key=lambda r: ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", "SAFE"].index(
            r.max_severity.value if hasattr(r.max_severity, "value") else str(r.max_severity)
        ),
    )

    for result in sorted_results:
        sev = result.max_severity.value if hasattr(result.max_severity, "value") else str(result.max_severity)
        safe = "✅" if result.is_safe else "❌"
        duration = f"{result.scan_duration_seconds:.1f}s"
        lines.append(f"| {result.skill_name} | {severity_badge(sev)} | {len(result.findings)} | {safe} | {duration} |")

    lines.append("")

    # Per-skill details (only for skills with findings)
    flagged = [r for r in sorted_results if r.findings]
    if flagged:
        lines.append(t["detailed_findings"])
        lines.append("")

        for result in flagged:
            sev = result.max_severity.value if hasattr(result.max_severity, "value") else str(result.max_severity)
            lines.append(f"### {result.skill_name} — {severity_badge(sev)}")
            lines.append("")

            for finding in result.findings:
                fsev = finding.severity.value if hasattr(finding.severity, "value") else str(finding.severity)
                lines.append(f"- **{severity_badge(fsev)}** `{finding.rule_id}` — {finding.title}")
                if finding.description:
                    lines.append(f"  > {finding.description}")
                if finding.file_path:
                    loc = finding.file_path
                    if finding.line_number:
                        loc += f":{finding.line_number}"
                    lines.append(f"  > {t['file']}: `{loc}`")
                if finding.remediation:
                    lines.append(f"  > **{t['remediation']}：** {finding.remediation}")
                lines.append("")

    else:
        lines.append(t["detailed_findings"])
        lines.append("")
        lines.append(t["no_findings"])
        lines.append("")

    return "\n".join(lines)


def scan_with_progress(scanner: SkillScanner, skills_dir: str) -> Report:
    """Run scan_directory logic with per-skill progress output."""
    base = Path(skills_dir)
    if not base.exists():
        raise FileNotFoundError(f"Directory does not exist: {base}")

    skill_dirs = sorted(
        {p.parent for p in base.rglob("SKILL.md")},
        key=lambda p: p.name,
    )
    total = len(skill_dirs)
    if total == 0:
        print("  No skills found.")
        return Report()

    print(f"  Found {total} skills to scan\n")

    report = Report()
    loaded_skills = []
    scan_start = time.time()

    width = len(str(total))
    longest_name = 0

    for i, skill_dir in enumerate(skill_dirs, 1):
        name = skill_dir.name
        longest_name = max(longest_name, len(name))
        counter = f"[{i:>{width}}/{total}]"
        print(f"  {counter} {name} ...", end="", flush=True)

        t0 = time.time()
        try:
            skill = scanner.loader.load_skill(skill_dir)
            result = scanner._scan_single_skill(skill, skill_dir)
            report.add_scan_result(result)
            loaded_skills.append(skill)

            elapsed = time.time() - t0
            sev = result.max_severity.value if hasattr(result.max_severity, "value") else str(result.max_severity)
            tag = severity_badge(sev)
            n_findings = len(result.findings)
            detail = f"{n_findings} finding{'s' if n_findings != 1 else ''}" if n_findings else ""
            print(f"\r  {counter} {name:{longest_name}}  {tag:18} {detail:20} ({elapsed:.1f}s)")

        except SkillLoadError as e:
            elapsed = time.time() - t0
            print(f"\r  {counter} {name:{longest_name}}  ⚠️  SKIP ({e}) ({elapsed:.1f}s)")
            report.skills_skipped.append({"skill": str(skill_dir), "reason": str(e)})

        except Exception as e:
            elapsed = time.time() - t0
            print(f"\r  {counter} {name:{longest_name}}  ❌ ERROR ({e}) ({elapsed:.1f}s)")
            report.skills_skipped.append({"skill": str(skill_dir), "reason": str(e)})

    wall = time.time() - scan_start

    if len(loaded_skills) > 1:
        print("\n  Running cross-skill overlap analysis ...", end="", flush=True)
        t0 = time.time()
        try:
            overlap = scanner._check_description_overlap(loaded_skills)

            from skill_scanner.core.analyzers.cross_skill_scanner import CrossSkillScanner

            cross = CrossSkillScanner().analyze_skill_set(loaded_skills)
            all_cross = [*list(overlap or []), *list(cross or [])]
            if scanner.policy.disabled_rules:
                all_cross = [f for f in all_cross if f.rule_id not in scanner.policy.disabled_rules]
            if all_cross:
                scanner._apply_severity_overrides(all_cross)
                report.add_cross_skill_findings(all_cross)
            elapsed = time.time() - t0
            print(f" {len(all_cross)} finding{'s' if len(all_cross) != 1 else ''} ({elapsed:.1f}s)")
        except Exception as e:
            print(f" error: {e}")

    print(f"\n  Done in {wall:.1f}s")
    return report


def main():
    args = parse_args()
    print("Building scanner (behavioral + trigger + optional LLM + balanced policy)...")
    scanner = build_scanner()
    print(f"Analyzers: {scanner.list_analyzers()}\n")

    print(f"Scanning {args.skills_dir}/...")
    report = scan_with_progress(scanner, args.skills_dir)

    print(f"\nResults: {report.total_skills_scanned} skills, {report.total_findings} findings")
    print(f"  Critical: {report.critical_count}  High: {report.high_count}  Safe: {report.safe_count}")

    md = generate_report(report, lang=args.lang)
    with open(args.output_file, "w") as f:
        f.write(md)

    print(f"\nReport written to {args.output_file}")


if __name__ == "__main__":
    main()
