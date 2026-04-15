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
            print(f"Error: invalid usage - {error}")
        except Exception as error:
            print(f"Error: unexpected failure: {error}")

    def _cmd_help(self, args: list[str]) -> None:
        if args:
            raise ValueError("Usage: help")
        print("Commands:")
        print("  help                              Show this help message")
        print("  pwd                               Show current path")
        print("  list [path]                       List directory contents")
        print("  create <path>                     Create an empty file")
        print("  mkdir <path>                      Create a directory")
        print("  cd <path>                         Change current directory")
        print("  read <path>                       Read file content")
        print("  write <path> <content>            Write content to file")
        print("  rename <path> <new_name>          Rename file or directory")
        print("  move <source> <destination>       Move/rename an entry")
        print("  delete <path>                     Delete file/empty directory")
        print("  exit                              Exit MiniOS")

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
            print("(empty)")
            return

        for item in items:
            marker = "[F]" if node.children[item].is_file else "[D]"
            print(f"{marker} {item}")

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
