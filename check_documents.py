
from pathlib import Path

folder = Path("data/documents")
files = sorted(folder.glob("*.txt"))

print(f"Total text files found: {len(files)}\n")

for file in files:
    text = file.read_text(encoding="utf-8").strip()

    print(f"File: {file.name}")
    print(f"Characters: {len(text)}")
    print(f"Preview: {text[:200].replace(chr(10), ' ')}")
    print("-" * 50)

    if not text:
        print("WARNING: This file is empty!")
