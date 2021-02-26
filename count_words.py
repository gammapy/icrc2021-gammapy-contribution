from pathlib import Path

filename = Path("abstract.md")

text = filename.read_text()

print(f"Number of words: {len(text.split())}")

