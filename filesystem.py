"""Core filesystem structure and path resolution for MiniOS."""

from __future__ import annotations

from exceptions import (
    AlreadyExistsError,
    InvalidOperationError,
    NotADirectoryError,
    NotAFileError,
    PathNotFoundError,
)
from models import Node


class FileSystem:
    """In-memory filesystem with path resolution utilities."""

    def __init__(self) -> None:
        """Initialize filesystem root and current working directory."""
        self.root = Node(name="/", is_file=False, parent=None)
        self.current = self.root

    def get_current_path(self) -> str:
        """Return current working directory as an absolute path."""
        if self.current.is_root():
            return "/"

        parts: list[str] = []
        node = self.current
        while node.parent is not None:
            parts.append(node.name)
            node = node.parent
        return "/" + "/".join(reversed(parts))

    def resolve_path(self, path: str) -> Node:
        """Resolve an absolute/relative path and return its node."""
        if path is None:
            raise InvalidOperationError("Path cannot be None.")

        path = path.strip()
        if path == "":
            return self.current

        if path.startswith("/"):
            node = self.root
            components = path.split("/")[1:]
        else:
            node = self.current
            components = path.split("/")

        for component in components:
            if component == "" or component == ".":
                continue
            if component == "..":
                if node.parent is not None:
                    node = node.parent
                continue

            if node.is_file:
                raise NotADirectoryError(f"'{node.name}' is not a directory.")
            if component not in node.children:
                raise PathNotFoundError(f"Path not found: {path}")
            node = node.children[component]

        return node

    def resolve_parent_and_name(self, path: str) -> tuple[Node, str]:
        """
        Resolve a path into (parent_directory_node, target_name).

        This is useful for operations like create/rename/move where the target
        entry may not exist yet, but its parent directory must exist.
        """
        if path is None:
            raise InvalidOperationError("Path cannot be None.")

        raw_path = path.strip()
        if raw_path == "":
            raise InvalidOperationError("Path cannot be empty.")

        is_absolute = raw_path.startswith("/")
        components = raw_path.split("/")
        filtered: list[str] = [part for part in components if part not in ("", ".")]

        if not filtered:
            raise InvalidOperationError("Path must include a target name.")

        target_name = filtered[-1]
        if target_name == "..":
            raise InvalidOperationError("Target name cannot be '..'.")

        parent_components = filtered[:-1]
        parent_node = self.root if is_absolute else self.current

        for component in parent_components:
            if component == "..":
                if parent_node.parent is not None:
                    parent_node = parent_node.parent
                continue

            if parent_node.is_file:
                raise NotADirectoryError(f"'{parent_node.name}' is not a directory.")
            if component not in parent_node.children:
                raise PathNotFoundError(f"Parent path not found: {path}")
            parent_node = parent_node.children[component]

        if parent_node.is_file:
            raise NotADirectoryError(f"'{parent_node.name}' is not a directory.")

        return parent_node, target_name

    def list_directory(self, path: str = "") -> list[str]:
        """List a directory with folders first, then files, both sorted."""
        node = self.resolve_path(path) if path.strip() else self.current
        if node.is_file:
            raise NotADirectoryError(f"'{node.name}' is not a directory.")

        directories = sorted(
            [name for name, child in node.children.items() if not child.is_file]
        )
        files = sorted([name for name, child in node.children.items() if child.is_file])
        return directories + files

    def create_file(self, path: str) -> None:
        """Create an empty file at the given path."""
        parent, name = self.resolve_parent_and_name(path)
        if name in parent.children:
            raise AlreadyExistsError(f"'{name}' already exists")
        parent.add_child(Node(name=name, is_file=True, parent=parent))

    def make_directory(self, path: str) -> None:
        """Create a directory at the given path."""
        parent, name = self.resolve_parent_and_name(path)
        if name in parent.children:
            raise AlreadyExistsError(f"'{name}' already exists")
        parent.add_child(Node(name=name, is_file=False, parent=parent))

    def change_directory(self, path: str) -> None:
        """Change current working directory."""
        target = self.resolve_path(path)
        if target.is_file:
            raise NotADirectoryError(f"'{target.name}' is not a directory.")
        self.current = target

    def read_file(self, path: str) -> str:
        """Read file content."""
        node = self.resolve_path(path)
        if not node.is_file:
            raise NotAFileError(f"'{node.name}' is not a file.")
        return node.content

    def write_file(self, path: str, content: str) -> None:
        """Write text content to an existing file."""
        node = self.resolve_path(path)
        if not node.is_file:
            raise NotAFileError(f"'{node.name}' is not a file.")
        node.content = content

    def rename(self, path: str, new_name: str) -> None:
        """Rename a file or directory."""
        if new_name is None:
            raise InvalidOperationError("New name cannot be None.")
        new_name = new_name.strip()
        if not new_name:
            raise InvalidOperationError("New name cannot be empty.")
        if "/" in new_name or new_name in (".", ".."):
            raise InvalidOperationError("Invalid new name.")

        parent, old_name = self.resolve_parent_and_name(path)
        if old_name not in parent.children:
            raise PathNotFoundError(f"Path not found: {path}")
        if new_name in parent.children:
            raise AlreadyExistsError(f"'{new_name}' already exists")

        node = parent.children.pop(old_name)
        node.name = new_name
        parent.children[new_name] = node

    def move(self, source_path: str, destination_path: str) -> None:
        """Move an entry to a directory or a new target path."""
        src_parent, src_name = self.resolve_parent_and_name(source_path)
        if src_name not in src_parent.children:
            raise PathNotFoundError(f"Path not found: {source_path}")

        source_node = src_parent.children[src_name]
        if source_node.is_root():
            raise InvalidOperationError("Cannot move root directory.")

        try:
            destination_node = self.resolve_path(destination_path)
            if destination_node.is_file:
                raise InvalidOperationError(
                    "Destination file exists; provide a directory or new path."
                )
            target_parent = destination_node
            target_name = source_node.name
        except PathNotFoundError:
            target_parent, target_name = self.resolve_parent_and_name(destination_path)

        if target_parent.is_file:
            raise NotADirectoryError(f"'{target_parent.name}' is not a directory.")
        if target_name in target_parent.children:
            raise AlreadyExistsError(f"'{target_name}' already exists")
        if source_node is target_parent:
            raise InvalidOperationError("Cannot move a directory into itself.")
        if not source_node.is_file and self._is_descendant(
            ancestor=source_node, node=target_parent
        ):
            raise InvalidOperationError(
                "Cannot move a directory into its own subdirectory."
            )

        src_parent.children.pop(src_name)
        source_node.name = target_name
        source_node.parent = target_parent
        target_parent.children[target_name] = source_node

    def delete(self, path: str) -> None:
        """Delete a file or an empty directory."""
        parent, name = self.resolve_parent_and_name(path)
        if name not in parent.children:
            raise PathNotFoundError(f"Path not found: {path}")

        node = parent.children[name]
        if not node.is_file and node.children:
            raise InvalidOperationError("directory is not empty")

        parent.remove_child(name)

    def _is_descendant(self, ancestor: Node, node: Node) -> bool:
        """Return True when node is in ancestor's subtree."""
        current: Node | None = node
        while current is not None:
            if current is ancestor:
                return True
            current = current.parent
        return False
