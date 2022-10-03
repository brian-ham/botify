SETUP

Because this project was created locally on my computer, rather than using CS50's Codespaces, there are a few steps needed for setup. First, the user must download a code editor application, a popular one being VSCode. Then, the user must download all the packages needed, including:

1) Install Python from python.org, and verify the installation using python3 --version in the terminal
2) Install Flask using pip3 install Flask-Session, and run python3 -m venv .venv
3) Download the CS50 library with pip3 install CS50 from https://github.com/cs50/libcs50
4) Download SQLite from https://www.sqlite.org/download.html

The project also uses Python libaries that must be installed. Follow the instructions at https://spacy.io/usage based on your operating system to download the Spacy library, which takes care of the natural language processing necessary.

RUNNING

Once the setup is complete, download the entire ZIP file included and open in VSCode; be careful not to mess with the structure, as that may affect the final result. This means that all the files should be included in the same folder. Once the environment is opened, get to the right folder by changing directories, and then run "flask run." Follow the link that the terminal provides (http://127.0.0.1:5000/). The page should open in your default browser.

SPACY: 
pip install -U pip setuptools wheel
pip install -U spacy

Walkthrough Link: https://youtu.be/UuthorXTz-U