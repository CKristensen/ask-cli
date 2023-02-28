#!/usr/bin/env python
import openai
import os
import argparse
import requests

openai.api_key = os.getenv('OPENAI_API_KEY')
wolfram_app_id = os.getenv('WOLFRAM_APP_ID')

parser = argparse.ArgumentParser(prog='Ask AI from CLI. Ask GPT from the comfort of your CLI.',
                                 epilog='ask -m cd "make a python script that print hello world!"')
parser.add_argument('default')
parser.add_argument("-m,", "--model", help="""available models:
                    td: text-davinci-003    ||
                    tc: text-curie-001      ||
                    tb: text-babbage-001    ||
                    ta: text-ada-001        ||
                    cd: code-davinci-002    ||
                    cc: code-cushman-001    ||
                    w: wolfram-alpha-simple ||""")
parser.add_argument("-t", "--temperature", help="""What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.""")
parser.add_argument("-v", "--verbose", action='store_true')
parser.add_argument("-p", "--prompt", help="g: give git commands, w: improve writing, k: kubectl commands")

model_dict = {
    "td": "text-davinci-003",
    "tc": "text-curie-001",
    "tb": "text-babbage-001",
    "ta": "text-ada-001",
    "cd": "code-davinci-002",
    "cc": "code-cushman-001",
    "w": "wolfram-alpha",
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

def ask_chatgpt(prompt):
    try:
      max_tokens = 4000 if "davinci" in model else 2048
      requested_tokens = max_tokens - int(len(prompt)/2)
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
        response = str(e)
    except openai.error.RateLimitError as e:
        response = str(e)

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
if model != "wolfram-alpha":
    response = ask_chatgpt(args.default)
else:
    response = ask_wolfram(args.default)    
print(response)                             
