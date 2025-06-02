# Hardcode Finder

A command-line tool to detect hardcoded literal values in Python (AST-based), JavaScript and Java (Regex-based) source code.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Features

* Analyzes **Python** (`.py`) files using Abstract Syntax Trees (AST) for accuracy.
* Analyzes **JavaScript** (`.js`) files using Regular Expressions (Regex) for common patterns.
* Analyzes **Java** (`.java`) files using Regular Expressions (Regex) to identify variables and constants.
* Recursively scans specified directories.
* Command-line interface with arguments for batch processing.
* Clear output: highlights file, line number, variable name, and detected value.
* No external Python libraries required.

---

## Supported Languages

* **Python (.py):** AST-based analysis provides high accuracy for direct literal assignments (strings, numbers, lists, dicts, etc.).

* **JavaScript (.js):** Regex-based analysis targets common single-line literal assignments (`var`, `let`, `const`). This method is effective for simpler cases but less precise than AST analysis.

* **Java (.java):** Regex-based analysis that detects variable declarations and constants (`static final`) with hardcoded literal values.

---

## Requirements

* Python 3.8+

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/IcaroGabrielS/HardcodeFinder.git
   ```

2. Navigate to the project directory:
   ```bash
   cd HardcodeFinder
   ```

---

## Usage

Run the script with the directory path to scan and specify which language(s) to analyze:

```bash
python mainFinder.py [directory] [options]
```

### Command-line Arguments

- `directory`: Path to the directory you want to scan
- `--all`: Analyze all supported languages
- `--python`: Analyze only Python files
- `--javascript`: Analyze only JavaScript files
- `--java`: Analyze only Java files

### Examples

Analyze all supported languages in the current directory:
```bash
python mainFinder.py . --all
```

Analyze only Python files in a specific directory:
```bash
python mainFinder.py /path/to/project --python
```

Analyze JavaScript files in a project:
```bash
python mainFinder.py /path/to/project --javascript
```

### Output Example

```
Scanning directory for Python files (.py): /path/to/project
Scanned 15 Python file(s). Hardcoded values found in 5 file(s).

--- Potentially Hardcoded Literal Values Found (Python) ---

  In File: /path/to/project/config.py
    L12   | Var: API_URL                  | Value: "https://api.example.com"
    L13   | Var: MAX_RETRIES              | Value: 3
    L14   | Var: DEFAULT_TIMEOUT          | Value: 30

  In File: /path/to/project/utils.py
    L45   | Var: log_levels               | Value: ["DEBUG", "INFO", "WARNING", "ERROR"]
-----------------------------------------------------------------