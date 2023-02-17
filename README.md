# ASK-GPT-CLI

GPT-CLI is a command line interface (CLI) tool that allows you to ask GPT (Generative Pre-trained Transformer) questions directly from your API.  
Option to ask questions to OpenAI and Wolfram Alpha Models.  
You can use this tool by using the 'ask' command and the -m option to select your model.  
By default it will ask OpenAis text-davinci-003 the most powerfull model.  

## Getting Started

In order to use GPT-CLI, you will need to get your own OpenAI API key and Wolfram Alpha AppID.
To do so, you will need to create an account on the OpenAI/WolframAlpha platform and then generate an API key from the settings page.
Once you have your API key, you can add it to the GPT-CLI configuration file (.askgtprc).  
!!!MAKE SURE TO KEEP IT PRIVATE!!!
## Installation
your can run `zsh installzsh.sh` to install it.
you need zsh. To run on other systems .... ask chat gpt.  
to uninstall simply remove the lines added in .zshrc.  
The installaton will add some line to your .zshrc,   
create a python venv with openai installed on it  
and add a python script to your ~ folder.

## Usage

Once you have your API key, you can use GPT-CLI to ask GPT questions.
To do so, use the 'ask' command followed by the -m option to select your model. 
This will query the GPT-CLI API with your question and return the answer.
For example:
```
ask -m tc "What is the meaning of life?"

The meaning of life is what each person makes of it.
```
use the `ask --help` for more information.
```
usage: Ask AI from CLI. Ask GPT from the comfort of your CLI. [-h] [-m, MODEL] [-t TEMPERATURE] [-v] default

positional arguments:
  default

options:
  -h, --help            show this help message and exit
  -m, MODEL, --model MODEL
                        available models: td: text-davinci-003 || tc: text-curie-001 || tb: text-babbage-001 || ta: text-ada-001 || cd: code-davinci-002 || cc: code-cushman-001 || w:
                        wolfram-alpha-simple ||
  -t TEMPERATURE, --temperature TEMPERATURE
                        What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused
                        and deterministic.
  -v, --verbose

ask -m cd "make a python script that print hello world!"

```

## Conclusion

GPT-CLI is a great tool for quickly asking GPT questions from your API. 
To get started, you will need to generate an OpenAI API key and add it to the GPT-CLI configuration file. 
Once you have your API key, you can use the 'ask' command followed by the -m option to select your model.

## Author 
This tool was made by GPT3 with the help of Carl Kristensen.
If any questions please ask the main author ChatGPT.  

