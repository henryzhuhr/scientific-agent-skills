````md
# Running MATLAB and GNU Octave Scripts from Bash

This document shows common ways to execute MATLAB-style `.m` scripts from a Bash environment using both MATLAB (MathWorks) and GNU Octave. It covers interactive use, non-interactive batch runs, passing arguments, capturing output, and practical patterns for automation and CI.

## Contents

- Requirements
- Quick comparisons
- Running MATLAB scripts from Bash
  - Interactive mode
  - Run a script non-interactively
  - Run a function with arguments
  - Run one-liners
  - Working directory and path handling
  - Capturing output and exit codes
  - Common MATLAB flags for scripting
- Running Octave scripts from Bash
  - Interactive mode
  - Run a script non-interactively
  - Run a function with arguments
  - Run one-liners
  - Making `.m` files executable (shebang)
  - Working directory and path handling
  - Capturing output and exit codes
  - Common Octave flags for scripting
- Cross-compatibility tips (MATLAB + Octave)
- Example: a portable runner script
- Troubleshooting

## Requirements

### MATLAB
- MATLAB must be installed.
- The `matlab` executable must be on your PATH, or you must reference it by full path.
- A valid license is required to run MATLAB.

Check:
```bash
matlab -帮助| head
````

### GNU Octave

* Octave must be installed.
* The `octave` executable must be on your PATH.

Check:

```bash
octave --version
```

## Quick comparison

| Task                          | MATLAB                            | Octave                   |
| ----------------------------- | --------------------------------- | ------------------------ |
| Interactive shell             | `matlab` (GUI by default)         | `octave`                 |
| Headless run (CI)             | `matlab -batch "cmd"` (preferred) | `octave --eval "cmd"`    |
| Run script file               | `matlab -batch "run('file.m')"`   | `octave --no-gui file.m` |
| Exit with code                | `exit(n)`                         | `exit(n)`                |
| Make `.m` directly executable | uncommon                          | common via shebang       |

## Running MATLAB scripts from Bash

### 1) Interactive mode

Starts MATLAB. Depending on your platform and install, this may launch a GUI.

```bash
matlab
```

For terminal-only use, prefer `-nodesktop` and optionally `-nosplash`:

```bash
matlab -nodesktop -nosplash
```

### 2) Run a script non-interactively

Recommended modern approach: `-batch`. It runs the command and exits when finished.

Run a script with `run()`:

```bash
matlab -batch“运行('myscript.m')”
```

If the script relies on being run from its directory, set the working directory first:

```bash
matlab -batch“cd('/path/to/project');运行('myscript.m')"
```

Alternative older pattern: `-r` (less robust for automation because you must ensure MATLAB exits):

```bash
matlab -nodisplay -nosplash -r"运行('myscript.m');退出"
```

### 3) Run a function with arguments

If your file defines a function, call it directly. Prefer `-batch`:

```bash
matlab -batch"myfunc(123, 'abc')"
```

To pass values from Bash variables:

```bash
matlab -batch "myfunc(${N}, '${NAME}')"
```

If arguments may contain quotes or spaces, consider writing a small MATLAB wrapper function that reads environment variables.

### 4) Run one-liners

```bash
matlab -batch “显示（2 + 2）”
```

Multiple statements:

```bash
matlab -batch“a = 1; b = 2; fprintf（'％d \ n'，a + b）”
```

### 5) Working directory and path handling

Common options:

* Change directory at startup:

```bash
matlab -batch“cd（'/路径/到/项目'）; myfunc()"
```

* Add code directories to MATLAB path:

```bash
matlab -batch "addpath('/path/to/lib'); myfunc()"
```

To include subfolders:

```bash
matlab -batch "addpath(genpath('/path/to/project')); myfunc()"
```

### 6) Capturing output and exit codes

Capture stdout/stderr:

```bash
matlab -batch "运行('myscript.m')" > matlab.out 2>&1
```

Check exit code:

```bash
matlab -batch “运行（'myscript.m'）”
echo $？
```

To explicitly fail a pipeline, use `exit(1)` on error. Example pattern:

```matlab
try
运行（'myscript.m'）;
catch ME
 disp（getReport（ME））;
退出（1）;
end
exit（0）;
```

Run it:

```bash
matlab -batch“尝试，运行（'myscript.m'）;抓住我，disp（getReport（ME））;退出（1）;结束;退出（0）;“
```

### 7) Common MATLAB flags for scripting

Commonly useful options:

* `-batch "cmd"`: run command, return a process exit code, then exit
* `-nodisplay`: no display (useful on headless systems)
* `-nodesktop`: no desktop GUI
* `-nosplash`: no startup splash
* `-r "cmd"`: run command; must include `exit` if you want it to terminate

Exact availability varies by MATLAB release, so use `matlab -help` for your version.

## Running GNU Octave scripts from Bash

### 1) Interactive mode

```bash
octave
```

Quieter:

```bash
octave --quiet
```

### 2) Run a script non-interactively

Run a file and exit:

```bash
octave --no-gui myscript.m
```

Quieter:

```bash
octave --quiet --no-gui myscript.m
```

Some environments use:

```bash
octave --无窗口系统myscript.m
```

### 3) Run a function with arguments

If `myfunc.m` defines a function `myfunc`, call it via `--eval`:

```bash
octave --quiet --eval "myfunc(123, 'abc')"
```

If your function is not on the Octave path, add paths first:

```bash
octave --quiet --eval "addpath('/path/to/project'); myfunc()"
```

### 4) Run one-liners

```bash
octave --quiet --eval "disp(2+2)"
```

Multiple statements:

```bash
octave --quiet --eval "a=1; b=2; printf('%d\n', a+b);"
```

### 5) Making `.m` files executable (shebang)

This is a common "standalone script" pattern in Octave.

Create `myscript.m`:

```matlab
# !/usr/bin/env Octave
disp("来自 Octave 的你好");
```

Make executable:

```bash
chmod +x myscript.m
```

Run:

```bash
./myscript.m
```

If you need flags (quiet, no GUI), use a wrapper script instead, because the shebang line typically supports limited arguments across platforms.

### 6) Working directory and path handling

Change directory from the shell before running:

```bash
cd /path/to/project
octave --quiet --no-gui myscript.m
```

Or change directory within Octave:

```bash
octave --quiet --eval "cd('/path/to/project'); run('myscript.m');"
```

Add paths:

```bash
octave --quiet --eval "addpath('/path/to/lib');运行（'myscript.m'）;“
```

### 7) Capturing output and exit codes

Capture stdout/stderr:

```bash
octave --quiet --no-gui myscript.m > Octave.out 2>&1
```

Exit code:

```bash
octave --quiet --no-gui myscript.m
echo $?
```

To force non-zero exit on error, wrap execution:

```matlab
try
 run('myscript.m');
catch err
 disp(err.message);
退出（1）;
end
exit（0）;
```

Run it:

```bash
octave --quiet --eval“尝试，运行（'myscript.m'）;捕获错误，disp（err.message）;退出（1）;结束;退出（0）;“
```

### 8) Common Octave flags for scripting

Useful options:

* `--eval "cmd"`: run a command string
* `--quiet`: suppress startup messages
* `--no-gui`: disable GUI
* `--no-window-system`: similar headless mode on some installs
* `--persist`: keep Octave open after running commands (opposite of batch behavior)

Check:

```bash
octave --帮助|头 -n 50
```

## Cross-compatibility tips (MATLAB and Octave)

1. Prefer functions over scripts for automation
   Functions give cleaner parameter passing and namespace handling.

2. Avoid toolbox-specific calls if you need portability
   Many MATLAB toolboxes have no Octave equivalent.

3. Be careful with strings and quoting
   MATLAB and Octave both support `'single quotes'`, and newer MATLAB supports `"double quotes"` strings. For maximum compatibility, prefer single quotes unless you know your Octave version supports double quotes the way you need.

4. Use `fprintf` or `disp` for output
   For CI logs, keep output simple and deterministic.

5. Ensure exit codes reflect success or failure
   In both environments, `exit(0)` indicates success, `exit(1)` indicates failure.

## Example: a portable Bash runner

This script tries MATLAB first if available, otherwise Octave.

Create `run_mfile.sh`:

```bash
# !/usr/bin/env bash
set -euo pipelinefail

FILE="${1:?用法：run_mfile.sh path/to/script_or_function.m}"
CMD="${2:-}" # 可选命令覆盖

if命令 -v matlab >/dev/null 2>&1;那么
 if [[ -n "$CMD" ]];然后
 matlab -batch "$CMD"
 else
 matlab -batch "run('${FILE}')"
 fi
elif command -v Octave >/dev/null 2>&1;那么
 if [[ -n "$CMD" ]]; then
 Octave --quiet --no-gui --eval "$CMD"
 else
 Octave --quiet --no-gui "$FILE"
 fi
else
 echo "在路径上既没有找到 matlab 也没有找到 Octave" >&2
 退出 127
fi
```

Make executable:

```bash
chmod +x run_mfile.sh
```

Run:

```bash
./run_mfile.sh myscript.m
```

Or run a function call:

```bash
./run_mfile.sh myfunc.m "myfunc(1, 'abc')"
```

## Troubleshooting

### MATLAB: command not found

* Add MATLAB to PATH, or invoke it by full path, for example:

```bash
/Applications/MATLAB_R202x?.app/bin/matlab -batch "disp('ok')"
```

### Octave：服务器上的 GUI 问题

* 使用 `--no-gui` 或 `--no-window-system`.

### 脚本依赖于相对路径

* `cd` 在启动之前进入脚本目录，或者执行在调用 `run()`.

### 传递字符串时引用问题`cd()` 在 MATLAB/Octave 中 `cd()`* 避免在 `--eval` 或 `-batch`.
中进行复杂引用* 使用环境变量，并在输入时在 MATLAB/Octave 内部读取它们复杂。

### MATLAB 和 Octave

之间的不同行为* 检查不支持的函数或工具箱调用。
* 使用 `--eval` 或 `-batch` 运行最少的重现步骤以隔离不兼容性。
