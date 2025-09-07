# MiniShell-OS
A cross-platform command-line shell implementation in Python. This shell provides a comprehensive set of features, including built-in commands, I/O redirection, piping, command history, and tab completion, mimicking the behavior of traditional UNIX/Linux shells.

---
## Project Overview

This "IIUI Mini Shell" project is a Python-based command-line interface designed to provide a hands-on understanding of fundamental Operating Systems concepts. It interprets user commands, executes them either internally or via the system shell, and integrates advanced features like process management, I/O stream handling, and command history, making it a robust learning tool for shell design and implementation.

---

### 🚀 Core Functionality
-   **Built-in Commands**: `cd`, `pwd`, `clear`, `history`, `help`, `touch`, `rm`, `cat`, `exit`. These commands are handled directly by the shell for efficiency and platform consistency.
-   **System Command Support**: Execute any external system command (e.g., `ls`, `echo`, `mkdir`, `whoami`, `date`, `grep`, `findstr`, etc.) by leveraging subprocesses.
-   **Cross-platform Compatibility**: Designed to work seamlessly on Windows, Linux, and macOS environments.
-   **Command History**: Persistent command history is maintained across sessions, stored in a dedicated file.
-   **Tab Completion**: Auto-completion feature for built-in commands, enhancing user experience and command entry speed.

---

### 🔧 Advanced Features
-   **I/O Redirection**: Comprehensive support for redirecting input (`<`) and output (`>`) streams for commands.
-   **Piping**: Allows chaining multiple commands together using the `|` operator, where the output of one command becomes the input of the next.
-   **Error Handling**: Robust and user-friendly error handling mechanisms to provide clear feedback for various command execution issues.
-   **Smart Prompt**: A dynamic and informative command prompt that intelligently displays the current working directory, abbreviating the home directory with `~`.

---
### 🎯 Key Capabilities
-   **Platform Adaptation**: Automatically maps common UNIX commands like `ls` to `dir` and `grep` to `findstr` on Windows for a consistent user experience.
-   **Persistent History**: Command history is saved to `~/.iiui_shell_history` (or an appropriate path on Windows) and automatically loaded at startup.
-   **Graceful Exit**: Ensures proper cleanup and safe termination of the shell session upon `exit` command or EOF.
-   **Signal Handling**: Gracefully handles interrupt signals (e.g., Ctrl+C) and End-Of-File (EOF) conditions.

---
## Quick Start

### Prerequisites
* Python 3.6 or higher installed on your system
* No additional dependencies required (uses only Python standard library)

### Installation & Running

#### Method 1: Direct Python Execution
1. Clone or download this repository
2. Navigate to the project directory
3. Run the shell:
   ```bash
   python mini_shell.py
   ```

#### Method 2: Using Executable (Windows)
1. Download `mini_shell.exe` from the releases page
2. Double-click to run or execute from command prompt:
   ```cmd
   mini_shell.exe
   ```

#### Method 3: Using Executable (Linux/macOS)
1. Download the executable from the releases page
2. Make it executable and run:
   ```bash
   chmod +x mini_shell
   ./mini_shell
   ```

### First Run
When you start the shell, you'll see:
```bash
Welcome to IIUI-Shell. Type 'help' for assistance.
IIUI_MiniShell>
```
### Type `help` to see all available commands, or start using the shell immediately!
---

### Built-in Commands

| Command | Description |
|---------|-------------|
| `cd <path>` | Change directory |
| `pwd` | Print working directory |
| `clear` | Clear the screen |
| `history` | Show command history |
| `touch <file>...` | Create new file(s) |
| `rm <file>...` | Remove file(s) |
| `cat <file>...` | Display file contents |
| `help` | Show help message |
| `exit` | Exit the shell |

### Examples

```bash
# Basic commands
IIUI_MiniShell> pwd
/home/user/projects

IIUI_MiniShell> ls
file1.txt  file2.txt  directory/

# File operations
IIUI_MiniShell> touch newfile.txt
IIUI_MiniShell> cat newfile.txt
IIUI_MiniShell> rm oldfile.txt

# I/O redirection
IIUI_MiniShell> echo "Hello World" > output.txt
IIUI_MiniShell> cat < input.txt

# Piping
IIUI_MiniShell> ls | grep .txt
IIUI_MiniShell> cat file.txt | wc -l

# System commands
IIUI_MiniShell> whoami
IIUI_MiniShell> date
IIUI_MiniShell> mkdir newdir
```

---
## File Structure
```bash
mini-shell/
├── mini_shell.py # Main shell implementation
├── mini_shell.spec # PyInstaller configuration
├── build/ # Build artifacts
├── dist/ # Distribution files
└── README.md # This file
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Hajira Gul**  
