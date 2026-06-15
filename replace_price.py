#!/usr/bin/env python3
"""Replace Oideya's room rate ¥15,000 → ¥10,000 in all HTML files.

Skips ¥15,000–25,000/room (hotel comparison price in post-12-en.html)
by using a negative-lookahead for dash characters.
"""
import re
import glob

# Match ¥15,000 NOT followed by – (en dash) or - (hyphen), i.e. not a price range.
PRICE_RE = re.compile(r'¥15,000(?![–\-])')

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = PRICE_RE.sub('¥10,000', content)
    # Japanese form without ¥ sign: 15,000円 → 10,000円
    new_content = new_content.replace('15,000円', '10,000円')

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count = len(PRICE_RE.findall(content)) + content.count('15,000円')
        return count
    return 0


def main():
    html_files = sorted(glob.glob('./**/*.html', recursive=True))
    total = 0
    changed = []

    for filepath in html_files:
        count = process_file(filepath)
        if count:
            changed.append((filepath, count))
            total += count

    print("=== Price Replacement Summary ===")
    print(f"Total replacements : {total}")
    print(f"Files changed      : {len(changed)}")
    print()
    for filepath, count in changed:
        print(f"  {count:3d}  {filepath}")
    print("\nDone.")


if __name__ == "__main__":
    main()
