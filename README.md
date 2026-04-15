# Operating System Simulator (MiniOS)

MiniOS is a command-line based operating system simulator implemented in Python. It provides a simplified environment to demonstrate core operating system concepts such as file system management, command parsing, and directory navigation.

---

## Features

MiniOS supports the following commands:

- `help` – Show available commands
- `pwd` – Display current directory path
- `list [path]` – List files and directories
- `create <file>` – Create an empty file
- `mkdir <dir>` – Create a directory
- `cd <path>` – Change directory
- `read <file>` – Display file content
- `write <file> <content>` – Write content to a file
- `rename <old> <new>` – Rename a file or directory
- `move <src> <dest>` – Move or rename files/directories
- `delete <path>` – Delete a file or empty directory
- `exit` – Exit MiniOS

---

## System Design

The system follows a modular architecture:

```

User → Shell → FileSystem → In-Memory Tree

```

- **Shell Layer**
  - Handles user input and command parsing
  - Routes commands to the file system

- **FileSystem Layer**
  - Implements file and directory operations
  - Handles path resolution and validation

- **Storage Layer**
  - Uses a tree structure (`Node`) to represent files and directories in memory

---

## Project Structure

```

operating-system/
├── main.py          # Entry point
├── shell.py         # Command-line interface
├── filesystem.py    # Core logic
├── models.py        # Data structures
├── exceptions.py    # Custom exceptions

````

---

## Requirements

Before running MiniOS, make sure you have:

- **Git** installed
- **Python 3** installed
- A terminal environment (macOS Terminal, Linux shell, or Windows PowerShell)

Verify installation:

```bash
git --version
python3 --version
````

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/operating-system.git
cd operating-system
```

### 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Run the program

```bash
python3 main.py
```

---

## Example Usage (Full Demo Flow)

```bash
# Start MiniOS
python3 main.py

# Show available commands
help

# Create and write to a file
create note.txt
write note.txt "Hello MiniOS"
read note.txt

# Create and navigate directories
mkdir docs
cd docs
pwd

# Go back and list contents
cd ..
list

# Rename and move file
rename note.txt notes.txt
move notes.txt docs
list docs

# Error handling examples
delete not_exist.txt
cd unknown
```

---

## Error Handling

MiniOS includes robust error handling to ensure stability:

* Prevents crashes on invalid input
* Provides clear and consistent error messages
* Handles edge cases such as:

  * Non-existent paths
  * Duplicate names
  * Invalid operations
  * Non-empty directory deletion

---

## Notes

This project is a **simulation of an operating system**, focusing on high-level concepts such as:

* Shell behavior
* File system structure
* Command processing

It does not implement low-level OS components such as kernel or memory management.

---

## Author

Yiyi Wang