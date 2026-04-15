"""MiniOS entry point."""

from shell import Shell


def main() -> None:
    """Launch the MiniOS shell."""
    shell = Shell()
    shell.run()


if __name__ == "__main__":
    main()
