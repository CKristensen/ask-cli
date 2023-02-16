#!/bin/bash

# check if source line has been appended to bashrc
if grep -Fxq "source $(pwd)/.askgptrc" ~/.bashrc
then
    echo ".askgptrc has already been appended to ~/.bashrc"
else
    echo "source $(pwd)/.askgptrc" >> ~/.bashrc
    echo ".askgptrc appended to ~/.bashrc"
fi
