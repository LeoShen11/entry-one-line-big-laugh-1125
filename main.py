"""One Line, Big Laugh — entry program.

Writes a single hilarious line to /output/entry.txt, then reads it back
and checks it byte for byte. The line is the whole entry: no title, no
setup, no explanation around it.
"""

import os

# The line. Drafted and picked in this session over two runners-up:
#   "I put my phone on Do Not Disturb and then spent the whole evening
#    missing it more than anyone I've ever dated."
#   "My sleep tracker congratulated me on eight hours of sleep, which is
#    impressive, since I spent six of them staring at the ceiling
#    negotiating with my brain."
# The winner below has the sharpest turn: you do the healthy thing
# (delete the ex), and your own phone betrays you with a helpful
# suggestion. The quoted fragment is the specific, absurd detail that
# makes it stick in the head after one reading.
LINE = (
    "I finally deleted my ex's number, and my phone immediately "
    "suggested texting them because I 'usually message them around "
    "this time.'"
)

MAX_CHARS = 200
MAX_WORDS = 25


def validate(line: str) -> None:
    """The gate's own rules, checked before anything is written."""
    if not line or not line.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if line != line.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in line):
        raise ValueError("entry must not contain control characters")
    if "  " in line:
        raise ValueError("entry must not contain double spaces")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    words = line.split()
    if len(words) > MAX_WORDS:
        raise ValueError(
            f"entry is {len(words)} words, over the {MAX_WORDS} limit"
        )
    # One sentence: a single terminal mark (. ! ?), allowing a closing quote.
    stripped = line.rstrip("'\"")
    if not stripped or stripped[-1] not in ".!?":
        raise ValueError("entry must end with a single sentence terminator")
    if sum(ch in ".!?" for ch in stripped[:-1]) > 0:
        raise ValueError("entry must be exactly one sentence")


def output_path() -> str:
    """The grader's path, with a local fallback for a dev run."""
    try:
        os.makedirs("/output", exist_ok=True)
        probe = "/output/.write-test"
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("ok")
        os.remove(probe)
        return "/output/entry.txt"
    except OSError:
        os.makedirs("output", exist_ok=True)
        return os.path.join("output", "entry.txt")


def main() -> None:
    validate(LINE)
    path = output_path()
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(LINE)
    # Read-back check: what landed on disk must be the line, byte for byte.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != LINE:
        raise ValueError("read-back mismatch: entry.txt is not the line")
    print(f"entry: {len(LINE)} characters, {len(LINE.split())} words")
    print(written)


if __name__ == "__main__":
    main()
