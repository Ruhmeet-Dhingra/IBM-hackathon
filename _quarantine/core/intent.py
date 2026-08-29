INTENTS = {

    "browser": [
        "browser",
        "internet",
        "chrome",
        "web"
    ],

    "youtube": [
        "youtube",
        "video",
        "videos"
    ],

    "github": [
        "github",
        "repository",
        "repo"
    ],

    "search": [
        "search",
        "find",
        "look"
    ]

}
def detect_intent(command):

    command = command.lower()

    for intent, keywords in INTENTS.items():

        for keyword in keywords:

            if keyword in command:

                return intent

    return None