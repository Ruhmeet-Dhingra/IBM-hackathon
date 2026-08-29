def parse_command(command):

    command = command.lower().strip()

    words = command.split()

    if not words:
        return None

    return {
        "action": words[0],
        "words": words,
        "text": command
    }