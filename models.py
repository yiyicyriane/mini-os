"""Data models for the MiniOS in-memory file tree."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Node:
    """Represents a file or directory in the in-memory tree."""

    name: str
    is_file: bool
    parent: Node | None = None
    children: dict[str, Node] = field(default_factory=dict)
    content: str = ""

    def __post_init__(self) -> None:
        """Validate node state after construction."""
        if not self.name:
            raise ValueError("Node name cannot be empty.")

        if self.is_file:
            # Files cannot have child nodes.
            self.children = {}
        elif self.content:
            # Directories should not carry file-like content.
            raise ValueError("Directory nodes cannot contain text content.")

    def add_child(self, child: Node) -> None:
        """Attach a child node to a directory node."""
        if self.is_file:
            raise ValueError("Cannot add children to a file node.")
        if child.name in self.children:
            raise ValueError(f"Child '{child.name}' already exists.")
        child.parent = self
        self.children[child.name] = child

    def remove_child(self, name: str) -> Node:
        """Detach and return a child by name."""
        if self.is_file:
            raise ValueError("File nodes do not have children.")
        if name not in self.children:
            raise ValueError(f"Child '{name}' does not exist.")
        child = self.children.pop(name)
        child.parent = None
        return child

    def get_child(self, name: str) -> Node:
        """Return a named child node."""
        if self.is_file:
            raise ValueError("File nodes do not have children.")
        if name not in self.children:
            raise ValueError(f"Child '{name}' does not exist.")
        return self.children[name]

    def is_root(self) -> bool:
        """Return True when this node is the root node."""
        return self.parent is None
