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

    def run(self) -> None:
        """Start the interactive shell loop."""
        print("Welcome to MiniOS!")
        print("Type 'help' to see available commands.")

        while self._running:
            prompt = f"{self.fs.get_current_path()} > "
            raw_input_line = input(prompt)
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

            if command == "help":
                self._cmd_help(args)
            elif command == "pwd":
                self._cmd_pwd(args)
            elif command == "list":
                self._cmd_list(args)
            elif command == "create":
                self._cmd_create(args)
            elif command == "mkdir":
                self._cmd_mkdir(args)
            elif command == "cd":
                self._cmd_cd(args)
            elif command == "read":
                self._cmd_read(args)
            elif command == "write":
                self._cmd_write(args)
            elif command == "rename":
                self._cmd_rename(args)
            elif command == "move":
                self._cmd_move(args)
            elif command == "delete":
                self._cmd_delete(args)
            elif command == "exit":
                self._cmd_exit(args)
            else:
                raise ValueError(f"Unknown command: {command}")
        except FileSystemError as error:
            print(f"Error: {error}")
        except ValueError as error:
            print(f"Error: {error}")
        except Exception as error:
            print(f"Error: unexpected failure: {error}")

    def _cmd_help(self, args: list[str]) -> None:
        if args:
            raise ValueError("Usage: help")
        print("Supported commands:")
        print("  help")
        print("  pwd")
        print("  list [path]")
        print("  create <path>")
        print("  mkdir <path>")
        print("  cd <path>")
        print("  read <path>")
        print("  write <path> <content>")
        print("  rename <path> <new_name>")
        print("  move <source_path> <destination_path>")
        print("  delete <path>")
        print("  exit")

    def _cmd_pwd(self, args: list[str]) -> None:
        if args:
            raise ValueError("Usage: pwd")
        print(self.fs.get_current_path())

    def _cmd_list(self, args: list[str]) -> None:
        if len(args) > 1:
            raise ValueError("Usage: list [path]")
        path = args[0] if args else ""
        items = self.fs.list_directory(path)
        for item in items:
            print(item)

    def _cmd_create(self, args: list[str]) -> None:
        if len(args) != 1:
            raise ValueError("Usage: create <path>")
        self.fs.create_file(args[0])
        print("OK")

    def _cmd_mkdir(self, args: list[str]) -> None:
        if len(args) != 1:
            raise ValueError("Usage: mkdir <path>")
        self.fs.make_directory(args[0])
        print("OK")

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
        print("OK")

    def _cmd_rename(self, args: list[str]) -> None:
        if len(args) != 2:
            raise ValueError("Usage: rename <path> <new_name>")
        self.fs.rename(args[0], args[1])
        print("OK")

    def _cmd_move(self, args: list[str]) -> None:
        if len(args) != 2:
            raise ValueError("Usage: move <source_path> <destination_path>")
        self.fs.move(args[0], args[1])
        print("OK")

    def _cmd_delete(self, args: list[str]) -> None:
        if len(args) != 1:
            raise ValueError("Usage: delete <path>")
        self.fs.delete(args[0])
        print("OK")

    def _cmd_exit(self, args: list[str]) -> None:
        if args:
            raise ValueError("Usage: exit")
        self._running = False
        print("Goodbye!")
