#!/usr/bin/env python3
from pathlib import Path

from nvda_desk.architecture.validation import validate_architecture

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    for result in validate_architecture(root):
        print(result)
    print("PASS: structural architecture validation")
