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
mood: {mood}
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
    attrs = None
    if speaker == "boss":
        attrs = ["bold"]
    cprint(line, colors.get(speaker, "white"), "on_black", attrs)

def main(mood, speaker, recipient, prompt):
    instructions = get_instructions()
    payload = get_payload(instructions, speaker, recipient, prompt, mood)

    print(f"{speaker = }")
    print(f"{recipient = }")
    print(f"{prompt = }")
    print(f"{mood = }")
    response = requests.post(URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error: {response.status_code}: {response.text}")


if __name__ == "__main__":
    mood = sys.argv[1]
    speaker = sys.argv[2]
    recipient = sys.argv[3]
    line = " ".join(sys.argv[4:])
    reply = main(mood, speaker, recipient, line)
    say(sys.argv[2], reply)
