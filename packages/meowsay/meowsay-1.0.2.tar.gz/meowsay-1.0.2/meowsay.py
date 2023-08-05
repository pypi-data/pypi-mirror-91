"""
Cowsay, but better.

To use meowsay, simply run the following in your terminal:

    meowsay <text>

you can also pipe the data from stdin:

    echo "Hello" | meowsay

or

    cat file.txt | meowsay
"""
import sys
from collections import deque
from typing import List


def meowsay() -> None:
    """Meowsay CLI interface."""
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = sys.stdin.read()

    paragraphs = text.split('\n\n')

    print_bubble(paragraphs)
    print_cat()


def format_paragraph(paragraph: str) -> List[str]:
    """Formats paragraph of text into lines with max width of 40 characters"""
    words = deque(paragraph.split())

    formatted_lines: List[str] = []
    line = ''
    while words:
        word = words[0]
        if line == '':
            line = word
            words.popleft()
            continue

        if len(line) + 1 + len(word) <= 40:
            line = line + ' ' + word
            words.popleft()

        else:
            formatted_lines.append(line)
            line = ''

    if line:
        formatted_lines.append(line)

    return formatted_lines


def print_bubble(paragraphs: List[str]) -> None:
    """Prints the text in a chat bubble"""
    if len(paragraphs) == 1:
        words = paragraphs[0].split()
        text = ' '.join(words)

        # Special case: single line output
        if len(text) <= 40:
            print('', '_' * (len(text)+2))
            print('<', text, '>')
            print('', '-' * (len(text)+2))
            return

    formatted_lines: List[str] = []
    for paragraph in paragraphs:
        lines = format_paragraph(paragraph)
        formatted_lines.extend(lines)
        formatted_lines.append('')

    formatted_lines.pop()  # remove extra newline at the end

    bordered_lines: List[str] = []

    size = max(len(line) for line in formatted_lines)
    bordered_lines.append(f" {'_' * (size+2)}")

    first_line = formatted_lines[0]
    bordered_lines.append(f'/ {first_line:{size}} \\')

    for line in formatted_lines[1:-1]:
        bordered_lines.append(f'| {line:{size}} |')

    last_line = formatted_lines[-1]
    bordered_lines.append(f'\\ {last_line:{size}} /')

    bordered_lines.append(f" {'-' * (size+2)}")

    for bordered_line in bordered_lines:
        print(bordered_line)


def print_cat() -> None:
    """Prints cat"""
    print('\n'.join(
        [
            r"        \      |\---/|",
            r"         \     | ,_, |",
            r"                \_`_/-..----.",
            r"             ___/ `   ' ,\"\"+ \  sk",
            r"            (__...'   __\    |`.___.';",
            r"              (_,...'(_,.`__)/'.....+",
        ]
    ))
