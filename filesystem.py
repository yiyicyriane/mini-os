"""Core filesystem structure and path resolution for MiniOS."""

from __future__ import annotations

from exceptions import InvalidOperationError, NotADirectoryError, PathNotFoundError
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
