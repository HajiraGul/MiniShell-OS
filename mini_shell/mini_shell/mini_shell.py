import os
import platform
import shlex
import subprocess
import sys

try:
    import readline
except ImportError:
    readline = None

HISTORY_FILE = os.path.expanduser("~/.iiui_shell_history")
command_history = []

BUILTIN_COMMANDS = [
    "cd", "pwd", "clear", "history", "help", "touch", "exit", "cat", "rm"
]

if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        command_history = [line.strip() for line in f if line.strip()]

def save_to_history(command_line):
    if command_line.strip() and (not command_history or command_history[-1] != command_line):
        command_history.append(command_line)
        try:
            with open(HISTORY_FILE, "a") as f:
                f.write(command_line + "\n")
        except Exception as e:
            print(f"IIUI-Shell: Failed to save history: {e}")

def completer(text, state):
    options = [cmd for cmd in BUILTIN_COMMANDS if cmd.startswith(text)]
    if state < len(options):
        return options[state]
    return None

if readline:
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
else:
    if platform.system() == "Windows":
        print("Note: Tab completion not available on Windows without readline support.")

def execute_command(command_line):
    if not command_line.strip():
        return

    save_to_history(command_line)

    try:
        args = shlex.split(command_line)
    except ValueError as e:
        print(f"IIUI-Shell: Error parsing command: {e}")
        return

    if not args:
        return

    if "|" in args:
        handle_piping(command_line)
        return

    if ">" in args or "<" in args:
        handle_redirection(args)
        return

    cmd = args[0]

    if platform.system() == "Windows" and cmd == "ls":
        args[0] = "dir"
        cmd = "dir"

    if cmd == "exit":
        print("Exiting IIUI-Shell...")
        sys.exit(0)
    elif cmd == "cd":
        path = args[1] if len(args) > 1 else os.path.expanduser("~")
        try:
            os.chdir(path)
        except FileNotFoundError:
            print(f"IIUI-Shell: cd: No such file or directory: {path}")
        except Exception as e:
            print(f"IIUI-Shell: cd: {e}")
    elif cmd == "pwd":
        print(os.getcwd())
    elif cmd == "clear":
        os.system("cls" if platform.system() == "Windows" else "clear")
    elif cmd == "history":
        for i, cmd_hist in enumerate(command_history):
            print(f"{i + 1}: {cmd_hist}")
    elif cmd == "help":
        print("""
IIUI-Shell Help:
  cd <path>         - Change directory.
  pwd               - Print working directory.
  clear             - Clear the screen.
  history           - Show command history.
  touch <file>...   - Create new file(s).
  rm <file>...      - Remove file(s).
  exit              - Exit the shell.
  help              - Show this help message.

  Supports:
    - Built-in commands
    - System commands (ls, echo, mkdir, whoami, date)
    - I/O Redirection: >, <
    - Pipes: |
        """)
    elif cmd == "touch":
        if len(args) < 2:
            print("touch: missing file operand")
        else:
            for fname in args[1:]:
                try:
                    with open(fname, 'a'):
                        os.utime(fname, None)
                except Exception as e:
                    print(f"touch: cannot touch '{fname}': {e}")
    elif cmd == "rm":
        if len(args) < 2:
            print("rm: missing operand")
        else:
            for fname in args[1:]:
                try:
                    os.remove(fname)
                except FileNotFoundError:
                    print(f"rm: cannot remove '{fname}': No such file or directory")
                except IsADirectoryError:
                    print(f"rm: cannot remove '{fname}': Is a directory")
                except PermissionError:
                    print(f"rm: cannot remove '{fname}': Permission denied")
                except Exception as e:
                    print(f"rm: cannot remove '{fname}': {e}")
    elif cmd == "cat":
        if len(args) < 2:
            print("cat: missing file operand")
        else:
            if platform.system() == "Windows":
                for fname in args[1:]:
                    try:
                        with open(fname, "r") as f:
                            print(f.read(), end="")
                    except FileNotFoundError:
                        print(f"cat: {fname}: No such file or directory")
                    except Exception as e:
                        print(f"cat: {fname}: {e}")
            else:
                try:
                    subprocess.run(args, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"IIUI-Shell: command '{' '.join(args)}' failed with exit code {e.returncode}")
                except FileNotFoundError:
                    print(f"IIUI-Shell: {cmd}: command not found")
                except Exception as e:
                    print(f"IIUI-Shell: Error executing command '{cmd}': {e}")
    else:
        try:
            subprocess.run(" ".join(args), check=True, shell=True)
        except FileNotFoundError:
            print(f"IIUI-Shell: {cmd}: command not found")
        except subprocess.CalledProcessError as e:
            print(f"IIUI-Shell: command '{' '.join(args)}' failed with exit code {e.returncode}")
        except PermissionError:
            print(f"IIUI-Shell: {cmd}: permission denied")
        except Exception as e:
            print(f"IIUI-Shell: Error executing command '{cmd}': {e}")

def handle_redirection(args):
    try:
        if ">" in args:
            index = args.index(">")
            command_parts = args[:index]
            if not command_parts or index + 1 >= len(args):
                print("IIUI-Shell: Redirection error: missing command or file.")
                return
            output_file = args[index + 1]
            with open(output_file, "w") as f_out:
                subprocess.run(" ".join(command_parts), stdout=f_out, stderr=subprocess.STDOUT, check=True, shell=True)
        elif "<" in args:
            index = args.index("<")
            command_parts = args[:index]
            if not command_parts or index + 1 >= len(args):
                print("IIUI-Shell: Redirection error: missing command or file.")
                return
            input_file = args[index + 1]
            with open(input_file, "r") as f_in:
                subprocess.run(" ".join(command_parts), stdin=f_in, check=True, shell=True)
    except FileNotFoundError as e:
        print(f"IIUI-Shell: File or command not found: {e}")
    except subprocess.CalledProcessError as e:
        print(f"IIUI-Shell: command '{' '.join(command_parts)}' failed with exit code {e.returncode}")
    except IndexError:
        print("IIUI-Shell: Redirection error: Invalid syntax.")
    except Exception as e:
        print(f"IIUI-Shell: Redirection error: {e}")

def handle_piping(command_line):
    try:
        pipe_commands_str = command_line.split("|")
        commands_args_list = [shlex.split(cmd_str.strip()) for cmd_str in pipe_commands_str]

        if any(not cmd_args for cmd_args in commands_args_list):
            print("IIUI-Shell: Pipe error: empty command.")
            return

        num_cmds = len(commands_args_list)
        prev_proc = None
        procs = []

        for i, cmd_args in enumerate(commands_args_list):
            # Platform-specific command mapping
            if platform.system() == "Windows":
                if cmd_args[0] == "ls":
                    cmd_args[0] = "dir"
                if cmd_args[0] == "grep":
                    cmd_args[0] = "findstr"

            stdin_source = prev_proc.stdout if prev_proc else None
            stdout_dest = subprocess.PIPE if i < num_cmds - 1 else None

            proc = subprocess.Popen(" ".join(cmd_args), stdin=stdin_source, stdout=stdout_dest, shell=True)
            procs.append(proc)

            if prev_proc and prev_proc.stdout:
                prev_proc.stdout.close()
            prev_proc = proc

        for proc in procs:
            proc.communicate()
    except FileNotFoundError as e:
        print(f"IIUI-Shell: Pipe error: command not found: {e}")
    except ValueError:
        # Suppress the closed pipe error
        pass
    except Exception as e:
        print(f"IIUI-Shell: Pipe error: {e}")


def main():
    print("Welcome to IIUI-Shell. Type 'help' for assistance.")
    while True:
        try:
            # Set the prompt display string to a user-friendly name
            actual_prompt = "IIUI_MiniShell> "
            command_line = input(actual_prompt)
            execute_command(command_line)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except EOFError:
            print("\nExiting IIUI-Shell...")
            break


if __name__ == "__main__":
    main()
