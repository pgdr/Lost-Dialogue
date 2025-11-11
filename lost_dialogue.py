import requests
import json
import os
import sys
from termcolor import colored, cprint

authinfo_path = os.path.expanduser("~/.authinfo")
OPENAI_API_KEY = ""

try:
    with open(authinfo_path, "r") as fh:
        OPENAI_API_KEY = fh.readline().strip().split(" ")[-1]
except FileNotFoundError:
    exit("The .authinfo file is not found.")

if not OPENAI_API_KEY:
    exit("OpenAI API key is not set in .authinfo.")

URL = "https://api.openai.com/v1/chat/completions"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}


def get_instructions():
    with open("instructions.md", "r") as fh:
        return "\n".join(l for l in fh)


def get_payload(instructions, speaker, recipient, line, mood, mode="statement"):
    return {
        "model": "gpt-4-1106-preview",
        "messages": [
            {
                "role": "system",
                "content": instructions,
            },
            {
                "role": "user",
                "content": f"""<content>
speaker: {speaker}
recipient: {recipient}
line: {line}
mood: {mode}
mode: {mode}
</content>""",
            },
        ],
    }


def say(speaker, line):
    colors = {
        "ninja": "light_blue",
        "princess": "light_magenta",
        "boss": "dark_grey",
    }
    cprint(line, colors.get(speaker, "white"), "on_black")


if __name__ == "__main__":
    speaker = sys.argv[2]
    recipient = sys.argv[3]
    line = " ".join(sys.argv[4:])
    mood = sys.argv[1]
    instructions = get_instructions()
    payload = get_payload(instructions, speaker, recipient, line, mood)

    print(f"{speaker = }")
    print(f"{recipient = }")
    print(f"{line = }")
    print(f"{mood = }")

    response = requests.post(URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        say(sys.argv[2], reply)
    else:
        exit(f"Error: {response.status_code}: {response.text}")
