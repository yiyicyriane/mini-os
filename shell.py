"""Interactive shell for MiniOS."""

from __future__ import annotations

import shlex

from exceptions import FileSystemError
from filesystem import FileSystem


class Shell:
    """Command interpreter for MiniOS."""

    def __init__(self) -> None:
        """Initialize shell state."""
        self.fs = FileSystem()
        self._running = True
        self.commands = {
            "help": self._cmd_help,
            "pwd": self._cmd_pwd,
            "list": self._cmd_list,
            "create": self._cmd_create,
            "mkdir": self._cmd_mkdir,
            "cd": self._cmd_cd,
            "read": self._cmd_read,
            "write": self._cmd_write,
            "rename": self._cmd_rename,
            "move": self._cmd_move,
            "delete": self._cmd_delete,
            "exit": self._cmd_exit,
        }

    def run(self) -> None:
        """Start the interactive shell loop."""
        print("=== Welcome to MiniOS ===")
        print("Type 'help' for commands, 'exit' to quit.")

        while self._running:
            prompt = f"MiniOS:{self.fs.get_current_path()}$ "
            try:
                raw_input_line = input(prompt)
            except EOFError:
                print("\nGoodbye!")
                break
            except KeyboardInterrupt:
                print("\nError: interrupted")
                continue
            self.handle_command(raw_input_line)

    def handle_command(self, raw_input_line: str) -> None:
        """Parse and execute one shell command safely."""
        try:
            raw_input_line = raw_input_line.strip()
            if not raw_input_line:
                return

            parts = shlex.split(raw_input_line)
            command = parts[0]
            args = parts[1:]

            handler = self.commands.get(command)
            if handler is None:
                print(f"Error: unknown command '{command}'")
                return
            handler(args)
        except FileSystemError as error:
            print(f"Error: {error}")
        except ValueError as error:
            print(f"Error: invalid usage - {error}")
        except Exception:
            print("Error: unexpected internal error")

    def _cmd_help(self, args: list[str]) -> None:
        if args:
            raise ValueError("Usage: help")
        help_rows = [
            ("help", "Show this help message"),
            ("pwd", "Show current path"),
            ("list [path]", "List directory contents"),
            ("create <file>", "Create an empty file"),
            ("mkdir <dir>", "Create a directory"),
            ("cd <path>", "Change directory"),
            ("read <file>", "Display file content"),
            ("write <file> <content>", "Write content to a file"),
            ("rename <old> <new>", "Rename file or directory"),
            ("move <src> <dest>", "Move file/directory"),
            ("delete <path>", "Delete file or empty directory"),
            ("exit", "Exit MiniOS"),
        ]
        print("Commands:")
        for usage, description in help_rows:
            print(f"  {usage:<30}{description}")

    def _cmd_pwd(self, args: list[str]) -> None:
        if args:
            raise ValueError("Usage: pwd")
        print(self.fs.get_current_path())

    def _cmd_list(self, args: list[str]) -> None:
        if len(args) > 1:
            raise ValueError("Usage: list [path]")
        path = args[0] if args else ""
        node = self.fs.resolve_path(path) if path else self.fs.current
        items = self.fs.list_directory(path)
        if not items:
            print("Directory is empty")
            return

        for item in items:
            marker = "[FILE]" if node.children[item].is_file else "[DIR]"
            print(f"{marker} {item}")

    def _cmd_create(self, args: list[str]) -> None:
        if len(args) != 1:
            raise ValueError("Usage: create <path>")
        path = args[0]
        self.fs.create_file(path)
        print(f"File '{self._entry_name(path)}' created successfully")

    def _cmd_mkdir(self, args: list[str]) -> None:
        if len(args) != 1:
            raise ValueError("Usage: mkdir <path>")
        path = args[0]
        self.fs.make_directory(path)
        print(f"Directory '{self._entry_name(path)}' created successfully")

    def _cmd_cd(self, args: list[str]) -> None:
        if len(args) != 1:
            raise ValueError("Usage: cd <path>")
        self.fs.change_directory(args[0])

    def _cmd_read(self, args: list[str]) -> None:
        if len(args) != 1:
            raise ValueError("Usage: read <path>")
        print(self.fs.read_file(args[0]))

    def _cmd_write(self, args: list[str]) -> None:
        if len(args) < 2:
            raise ValueError("Usage: write <path> <content>")
        path = args[0]
        content = " ".join(args[1:])
        self.fs.write_file(path, content)
        print(f"Content written to '{self._entry_name(path)}'")

    def _cmd_rename(self, args: list[str]) -> None:
        if len(args) != 2:
            raise ValueError("Usage: rename <path> <new_name>")
        self.fs.rename(args[0], args[1])
        print("Renamed successfully")

    def _cmd_move(self, args: list[str]) -> None:
        if len(args) != 2:
            raise ValueError("Usage: move <source_path> <destination_path>")
        self.fs.move(args[0], args[1])
        print("Moved successfully")

    def _cmd_delete(self, args: list[str]) -> None:
        if len(args) != 1:
            raise ValueError("Usage: delete <path>")
        self.fs.delete(args[0])
        print("Deleted successfully")

    def _cmd_exit(self, args: list[str]) -> None:
        if args:
            raise ValueError("Usage: exit")
        self._running = False
        print("Goodbye!")

    def _entry_name(self, path: str) -> str:
        """Extract display name from a path string."""
        normalized = path.rstrip("/")
        if not normalized:
            return path
        return normalized.split("/")[-1]
