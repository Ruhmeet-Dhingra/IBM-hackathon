from core.commands import execute_command
from ai.chat import chat_response
from core.parser import parse_command
from core.nlp import clean_command
from core.logger import log

def process_input(user_input):

    log(f"Input: {user_input}")

    user_input = clean_command(user_input)

    log(f"Cleaned: {user_input}")

    parsed = parse_command(user_input)

    if parsed:

        log("Parser successful")

        execute_command(parsed)

    else:

        log("Parser failed")

        response = chat_response(user_input)

        print(response)