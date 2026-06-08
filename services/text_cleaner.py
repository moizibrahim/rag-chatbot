from collections import Counter
import re


def remove_repeated_headers(pages):

    line_counter = Counter()

    for page in pages:

        unique_lines = set(
            line.strip()
            for line in page["text"].splitlines()
            if line.strip()
        )

        line_counter.update(unique_lines)

    repeated_lines = {
        line
        for line, count in line_counter.items()
        if count > len(pages) * 0.3
    }

    for page in pages:

        lines = page["text"].splitlines()

        cleaned = "\n".join(
            line
            for line in lines
            if line.strip() not in repeated_lines
        )

        # Generic cleanup
        cleaned = re.sub(
            r'\b(M Odd Header|M Even Header)\b',
            '',
            cleaned
        )

        cleaned = re.sub(
            r'webMethods Service Development Help\s+Version\s+\d+\.\d+',
            '',
            cleaned
        )

        cleaned = re.sub(
            r'\b\d{1,4}\b(?=\s+[A-Z])',
            '',
            cleaned
        )

        cleaned = re.sub(
            r'\s+',
            ' ',
            cleaned
        ).strip()

        page["text"] = cleaned

    return pages