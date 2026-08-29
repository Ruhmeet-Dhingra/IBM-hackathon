FILLER_WORDS = {
    "please",
    "could",
    "would",
    "can",
    "you",
    "me",
    "for",
    "the",
    "a",
    "an",
    "i",
    "want",
    "u"
}
ALIASES = {
    "launch": "open",
    "start": "open",
    "run": "open",

    "find": "search",
}


def clean_command(command):

    words = command.lower().split()

    cleaned = []

    for word in words:

        # Remove filler words
        if word in FILLER_WORDS:
            continue

        # Replace aliases
        word = ALIASES.get(word, word)

        cleaned.append(word)

    return " ".join(cleaned)