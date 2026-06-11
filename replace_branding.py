#!/usr/bin/env python3
"""Branding unification: replace Oideya Guest House, ゲストハウス, guesthouse in all HTML files."""
import glob

def process_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    change_count = 0
    for old, new in replacements:
        occurrences = content.count(old)
        if occurrences > 0:
            content = content.replace(old, new)
            change_count += occurrences

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return change_count


# Replacements are ordered: most specific / longest first to avoid partial matches.
# Protected strings (never changed):
#   - "GUEST HOUSE · OSAKA" (header subcopy)
#   - "oideya_osaka" (Instagram account)
REPLACEMENTS = [
    # =========================================================
    # 【A】 Brand name: Oideya Guest House → Oideya
    #   Applied first so the "Guest House" substring is gone
    #   before any English "guest house" fallback runs.
    # =========================================================
    ("Oideya Guest House", "Oideya"),

    # =========================================================
    # 【B】 Japanese ゲストハウス replacements
    #   Ordered from most specific compound → generic fallback.
    # =========================================================
    # Special compound (must precede B1 to avoid redundant 古民家 prefix)
    ("古民家一棟貸しゲストハウス", "一棟貸切古民家宿"),
    # Overlap of B2 + B5 — handle before either fires
    ("一棟貸しのゲストハウスや民家", "一棟貸しの宿や民家"),
    # B1
    ("一棟貸しゲストハウス", "一棟貸切古民家宿"),
    # B2
    ("一棟貸しのゲストハウス", "一棟貸しの古民家宿"),
    # B3 (no ゲストハウス in this one)
    ("一棟貸し施設", "一棟貸切宿"),
    # B4 — spaced keyword variant first, then compound
    ("町家 ゲストハウス", "町家 一棟貸切宿"),
    ("町家ゲストハウス", "町家一棟貸切宿"),
    # B5
    ("ゲストハウスや民家", "一棟貸し宿や民家"),
    # Specific review text referring to Oideya
    ("ゲストハウスはとても清潔でした", "一棟貸切古民家宿はとても清潔でした"),
    # Generic fallback — all remaining ゲストハウス refer to Oideya in these blog posts
    ("ゲストハウス", "一棟貸切古民家宿"),

    # =========================================================
    # 【C】 English guesthouse / guest house replacements
    #   Context-specific rules first, generic fallbacks last.
    # =========================================================
    # "used as / renovated as guesthouses" → private rentals
    ("for use as guesthouses", "for use as private rentals"),
    ("renovated for use as guesthouses", "renovated for use as private rentals"),
    ("renovated as guesthouses", "renovated as private rentals"),
    # Category comparison sentence
    ("A kominka guesthouse or rental", "A kominka rental"),
    # Property-as-subject references (→ Oideya or "the property")
    ("from the guesthouse.", "from Oideya."),
    ("The guesthouse was very clean!", "The property was very clean!"),
    ("near the guest house", "near Oideya"),
    ("The guest house provides", "Oideya provides"),
    # Compound descriptors
    ("whole-house guesthouse", "whole-house rental"),
    ("machiya guesthouse", "machiya whole-house rental"),
    # Generic fallback — any remaining single-word or two-word form
    ("guesthouse", "whole-house rental"),
    ("guest house", "whole-house rental"),
]


def main():
    html_files = sorted(glob.glob('./**/*.html', recursive=True))

    total_changes = 0
    changed_files = []

    for filepath in html_files:
        count = process_file(filepath, REPLACEMENTS)
        if count > 0:
            changed_files.append((filepath, count))
            total_changes += count

    print("=== Replacement Summary ===")
    print(f"Total replacements : {total_changes}")
    print(f"Files changed      : {len(changed_files)}")
    print()
    for filepath, count in changed_files:
        print(f"  {count:3d}  {filepath}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
