"""
Text normalization.
"""

import re

from brain_v2.vocabulary import ACTION_SYNONYMS


FILLER_WORDS = {
    "please",
    "can",
    "could",
    "would",
    "you",
    "for",
    "me",
    "the",
    "a",
    "an",
}
def normalize(text: str) -> str:
    """
    Normalize user input.
    """

    text = text.lower()

    text = re.sub(r"[^\w\s]", "", text)

    words = []

    for word in text.split():

        if word in FILLER_WORDS:
            continue

        word = ACTION_SYNONYMS.get(word, word)

        words.append(word)

    return " ".join(words)
if __name__ == "__main__":

    tests = [
        "Launch Chrome",
        "Could you please launch Chrome for me?",
        "Start Chrome",
        "Run Chrome",
        "Please open Chrome",
        "Find Quantum Computing",
    ]

    for text in tests:

        print(text)

        print(" -> ", normalize(text))

        print()