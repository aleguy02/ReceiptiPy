# What is SpotiPy?

Logging into SpotiPy lets you see my top ten tracks in the past month! Inspired by Receiptify, I made SpotiPy to jump into deploying a Flask app to a VPS from a Docker container. This project was made for practice ahead of my Production Engineering Fellowship and is no longer maintained.

## Tech Stack

[![My Skills](https://skillicons.dev/icons?i=html,tailwind,flask,python,docker)](https://skillicons.dev)

## Features

This project is WIP! Features coming soon include:

- [x] Getting my top tracks from the past month
- [ ] Getting YOUR top tracks from the past month

## Prerequisites

- [Python 3.12.x](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Optional)

## Running Locally

Fork this project. After forking, run the following commands in your terminal to set it up locally.

```bash
git clone FORKED_REPO_URL
cd cloned_repo
```

Create a new file called `.env` and paste in the contents from `.env_example`. Then, follow the steps to create an app from the [Spotify Web API docs](https://developer.spotify.com/documentation/web-api). For Redirect URIs, put "http://127.0.0.1:5000/callback". Get your Client ID and Client Secret from the Spotify API Dashboard. For your FLASK_SECRET_KEY, generate a secure random key with the following command.

```bash
$ python -c 'import secrets; print(secrets.token_hex())'
'192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
```

After these steps, you're ready to run the app in one of two ways.

### 1) Docker

To run ReceiptiPy in a Docker container, first build an image then run the image in a container.

```bash
docker build -t receiptipy .
docker run -p 5000:5000 receiptipy
```

Press `ctrl + c` do stop the container. Read `Dockerfile` for more information

### 2) Local (Linux)

You can also just run the app on your machine, it just requires a littlemore setup. First, create a Python virtual machine and activate it (for dependency management).

```bash
python -m venv myenv
source myenv/bin/activate
```

**Note**: You'll know it worked if you now see (myenv) on the left of your username in the terminal. If you are on Windows, you may have to do `myenv\Scripts\Activate.ps1` instead. Read more about virtual environments in the [documentation](https://docs.python.org/3/library/venv.html). You can always deactivate (exit) your virtual environment with `deactivate`.

Next, install the dependencies from the `requirements.txt` file.

```bash
pip install --upgrade pip && pip install -r requirements.txt
```

Finally, run the application with EITHER of the following command.

```bash
python app.py
flask run
```

## Acknowledgements

Shout out to [Michelle Liu](https://github.com/michellexliu), the creator of the original ReceiptiPy
