#!/usr/bin/env python
import openai
import os
import argparse
import requests
import sqlite3
from typing import List, Dict

openai.api_key = os.getenv('OPENAI_API_KEY')
wolfram_app_id = os.getenv('WOLFRAM_APP_ID')

parser = argparse.ArgumentParser(prog='Ask AI from CLI. Ask GPT from the comfort of your CLI.',
                                 epilog='ask -m cd "make a python script that print hello world!"')
parser.add_argument('default')
parser.add_argument("-m,", "--model", help="""available models:
                    tt: gpt-4(CHAT GPT) ||
                    td: text-davinci-003        ||
                    tc: text-curie-001          ||
                    tb: text-babbage-001        ||
                    ta: text-ada-001            ||
                    cd: code-davinci-002        ||
                    cc: code-cushman-001        ||
                    w: wolfram-alpha-simple     ||""")
parser.add_argument("-t", "--temperature",
                    help="""What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.""")
parser.add_argument("-v", "--verbose", action='store_true')
parser.add_argument("-p", "--prompt", help="g: give git commands, w: improve writing, k: kubectl commands")
parser.add_argument("-c", "--clear", help="clears the chat history", action='store_true')

model_dict = {
    "tt": "gpt-4",
    "td": "text-davinci-003",
    "tc": "text-curie-001",
    "tb": "text-babbage-001",
    "ta": "text-ada-001",
    "cd": "code-davinci-002",
    "cc": "code-cushman-001",
    "w": "wolfram-alpha",
    "gpt-3.5-turbo": "gpt-3.5-turbo",
    "text-davinci-003": "text-davinci-003",
    "text-curie-001": "text-curie-001",
    "text-babbage-001": "text-babbage-001",
    "text-ada-001": "text-ada-001",
    "code-davinci-002": "code-davinci-002",
    "code-cushman-001": "code-cushman-001",
}
args = parser.parse_args()
model = model_dict.get(args.model or "text-davinci-003")
temperature = args.temperature or 1

db_path = 'chat.db'


class dbHandler:

    @staticmethod
    def __init__():
        conn = sqlite3.connect(db_path)
        conn.execute(
            "CREATE TABLE IF NOT EXISTS chathistory (id INTEGER PRIMARY KEY AUTOINCREMENT, chatid INTEGER, role TEXT, content TEXT)")
        conn.commit()
        conn.close()

    @staticmethod
    def add_or_replace_chat(conversation: List[Dict[str, str]]):
        conn = sqlite3.connect(db_path)
        for message in conversation:
            conn.execute("DELETE FROM chathistory")
            conn.execute("INSERT OR REPLACE INTO chathistory (id, role, content) VALUES (?, ?, ?)",
                         (message['id'], message['role'], message['content']))
        conn.commit()
        conn.close()

    @staticmethod
    def get_chat() -> list:
        conn = sqlite3.connect(db_path)
        cursor = conn.execute("SELECT id, role, content from chathistory")
        chat_history = sorted([{'id': row[0], 'role': row[1], 'content': row[2]} for row in cursor],
                              key=lambda x: x['id'])
        conn.commit()
        conn.close()
        return chat_history

    @staticmethod
    def delete_chat():
        conn = sqlite3.connect(db_path)
        conn.execute("DELETE FROM chathistory")
        conn.execute("INSERT OR REPLACE INTO chathistory (id, role, content) VALUES (?, ?, ?)",
                     (1, "system", "you are a helpful assuistant"))

        conn.commit()
        conn.close()


def ask_gpt(prompt):
    try:
        max_tokens = 8000 if "4" in model else 2048
        requested_tokens = max_tokens - int(len(prompt) / 2)
        completions = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=requested_tokens,
            n=1,
            stop=None,
            temperature=temperature,
        )
        message = completions.choices[0].text
        return message
    except openai.error.APIError as e:
        return str(e)
    except openai.error.RateLimitError as e:
        return str(e)


def ask_chatgpt(prompt):
    chat_history = dbHandler()
    messages = chat_history.get_chat()

    # get biggst id
    if messages:
        last_id = messages[-1]['id']
    user_msg = {"id": last_id+1, "role": "user", "content": prompt}
    messages.append(user_msg)
    # drop the keys with name 'id'
    request = [{k: v for k, v in d.items() if k != 'id'} for d in messages]

    completions = openai.ChatCompletion.create(
        model="gpt-4",
        messages=request
    )
    response_content = completions.choices[0]["message"]["content"]
    messages.append({"id": last_id+2, "role": "assistant", "content": response_content})
    chat_history.add_or_replace_chat(messages)
    return response_content


def ask_wolfram(question):
    # Make a request to the Wolfram Alpha API
    r = requests.get('http://api.wolframalpha.com/v1/spoken',
                     params={'output': 'json', 'input': question, 'appid': wolfram_app_id,
                             'format': 'plaintext'})
    if r.status_code == 200:
        print(str(r.text))
    else:
        # Return an error message
        return f'I could not get answer from Wolfram Alpha. {r.status_code}'


prompts = {
    "g": "give only git commands for the following:",
    "k": "give only kubectl commands for the following:",
    "w": "please correct and make this message more readable:"
}

if args.prompt:
    args.default = (prompts.get(args.prompt) or "") + args.default
if args.verbose:
    print(f"asking {model}")
    print(f"asking {args.default}")
if args.clear:
    history = dbHandler()
    history.delete_chat()
if model == "wolfram-alpha":
    response = ask_wolfram(args.default)
if model == "gpt-3.5-turbo":
    response = ask_chatgpt(args.default)
else:
    response = ask_gpt(args.default)
print(response)
