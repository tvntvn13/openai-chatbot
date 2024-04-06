#!/usr/bin/env python3

from os import getenv
from shutil import get_terminal_size
from time import sleep

from constants import Colors as c
from constants import Messages as m
from constants import Modes as mode
from openai import OpenAI

API_KEY = getenv("OPENAI_API_KEY", "")

if API_KEY == "":
    print(
        "\033[1;33mAPI key not found, please set the OPENAI_API_KEY environment variable.\033[0m"
    )  # noqa: E501
    exit(1)

client = OpenAI()

MODE = mode.RUDE_MODE

GREETING = MODE[0]
INSTRUCTIONS = MODE[1]


def center_text(text: str) -> str:
    terminal_width = get_terminal_size(fallback=(100, 24)).columns
    return text.center(terminal_width)


def sanitize_input(user_input: str) -> str:
    sanitized = user_input.strip()
    sanitized = "".join(filter(str.isprintable, sanitized))
    sanitized = sanitized[:500]
    return sanitized


print(f"{c.BLACK}{center_text(f"----------{c.YELLOW} {m.HEADER} {c.BLACK}----------")}")

print(f"\n{c.RED} {c.PURPLE}{GREETING}{c.RESET}")

while True:
    try:
        message = input(f"{c.GREEN}󰜴 {c.PINK}")

        if message.lower() in m.CLOSE_COMMANDS:
            print(f"{c.YELLOW}{m.GOODBYE_MESSAGE}{c.RESET}")
            sleep(1)
            break

        sanitized_message = sanitize_input(message)

    except EOFError:
        print(f"{c.YELLOW}{m.GOODBYE_MESSAGE}")
        break
    except KeyboardInterrupt:
        print(f"{c.YELLOW}{m.GOODBYE_MESSAGE}")
        break

    try:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": INSTRUCTIONS},
                {"role": "user", "content": message},
            ],
            stream=True,
        )
        print(f"{c.RED} ", end="", flush=True)
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(f"{c.PURPLE}{chunk.choices[0].delta.content}", end="", flush=True)
        print("")

    except Exception as e:
        print(f"{c.RED}An error occurred: {e}")
        break
