#!/usr/bin/env python
import openai
import os
import argparse

openai.api_key = os.getenv('OPENAI_API_KEY')

parser = argparse.ArgumentParser(prog='Ask GPT from CLI!',
                                 epilog='ask -m cd "make a python script that print hello world!"')
parser.add_argument('default')
parser.add_argument("-m,", "--model", help="""
available models: td: text-davinci-003 || tc: text-curie-001 || tb: text-babbage-001 || ta: text-ada-001 || cd: code-davinci-002 || cc: code-cushman-001
""")
parser.add_argument("-v,", "--verbose", action='store_true')

model_dict = {
    "td": "text-davinci-003",
    "tc": "text-curie-001",
    "tb": "text-babbage-001",
    "ta": "text-ada-001",
    "cd": "code-davinci-002",
    "cc": "code-cushman-001",
    "text-davinci-003": "text-davinci-003",
    "text-curie-001": "text-curie-001",
    "text-babbage-001": "text-babbage-001",
    "text-ada-001": "text-ada-001",
    "code-davinci-002": "code-davinci-002",
    "code-cushman-001": "code-cushman-001",
}
args = parser.parse_args()
model = model_dict.get(args.model or "text-davinci-003") 

def ask_chatgpt(prompt):
  max_tokens = 4000 if "davinci" in model else 2048
  requested_tokens = max_tokens - int(len(prompt)/2)
  completions = openai.Completion.create(
  engine=model,
  prompt=prompt,
  max_tokens=requested_tokens,
  n=1,
  stop=None,
  temperature=0.5,
  )

  message = completions.choices[0].text
  return message
if args.verbose:
    print(f"asking {model}")
    print(f"asking {args.default}")
try:
    response = ask_chatgpt(args.default)
except openai.error.APIError as e:
    response = str(e)
except openai.error.RateLimitError as e:
    response = str(e)
print(response)
