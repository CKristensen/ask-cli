#!/bin/bash

#Create a python environment with openai installed
#Check if python is installed
if ! [ -x "$(command -v python)" ]; then
  echo 'Error: python is not installed.' >&2
  exit 1
fi

#Check if virtualenv is installed
if ! [ -x "$(command -v virtualenv)" ]; then
  echo 'Error: virtualenv is not installed.' >&2
  exit 1
fi

#Create the environment
virtualenv -p python3 gptenv

#Activate the environment
source gptenv/bin/activate

#Install openai
pip install openai

# check if source line has been appended to bashrc
if grep -Fxq "source $(pwd)/.askgptrc" ~/.zshrc
then
    echo ".askgptrc has already been appended to ~/.zshrc"
else
    cp ./askgpt.py ~/.askgpt.py
    echo 'alias gptenv789=''"source '"$(pwd)"'/gptenv/bin/activate"' >> ~/.zshrc
    echo "source $(pwd)/.askgptrc &&" >> ~/.zshrc
    echo ".askgptrc appended to ~/.zshrc"
    echo "added .askgpt.py to ~"
fi
deactivate
source ~/.zshrc

