# Hardcode Finder

A command-line tool to detect hardcoded literal values in Python (AST-based) and JavaScript (Regex-based) source code.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Features

* Analyzes **Python** (`.py`) files using Abstract Syntax Trees (AST) for accuracy.
* Analyzes **JavaScript** (`.js`) files using Regular Expressions (Regex) for common patterns.
* Recursively scans specified directories.
* Interactive Command-Line Interface (CLI) menu.
* Clear output: highlights file, line number, variable name, and detected value.
* No external Python libraries required.

---

## Supported Languages

* **Python (.py):** AST-based analysis provides high accuracy for direct literal assignments (strings, numbers, lists, dicts, etc.).

* **JavaScript (.js):** Regex-based analysis targets common single-line literal assignments (`var`, `let`, `const`). This method is effective for simpler cases but less precise than AST analysis.

---

## Requirements

* Python 3.8+

---

## Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/IcaroGabrielS/HardcodeFinder.git](https://github.com/IcaroGabrielS/HardcodeFinder.git)
    ```


2.  Navigate to the project directory:
    ```bash
    cd HardcodeFinder
    ```

---

## Usage

1.  From the `HardcodeFinder` directory, run the main script:
    ```bash
    python mainFinder.py
    ```
    *(Adjust script name if yours is different, e.g., `hardcode_finder_main.py`)*

2.  Use the interactive menu to select the language and provide the full path to the directory you wish to scan.

