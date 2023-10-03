# Tool for automatizing creation of github repository with API

## Prerequisites

- API key from Github with the permissions to create repository, e.g. `repo`\
  (can be created in `Settings -> Developer Settings -> Personal access tokens (classic) -> Tokens (clasic)`)
- `docker-compose || docker compose`

## Usage

1. Clone this repository to your path
2. Go to the repository and add the path to your `$PATH` env var with:
    ```bash
    echo 'PATH='$(pwd)':$PATH' >> ~/.bashrc
    ```

## Test

### Test with `docker-compose`

1. Add API key to `.secret` file in repository
2. Set up `creds.env` with env vars:
    ```bash
    USER="timmotej"
    TOKEN_FILE="/mnt/.secret"
    NAME="reponame"
    PRIVATE="true"
    ```
3. Execute:
    ```bash
    docker compose up
    ```

### Test with python

1. Add python libraries, e.g. with `pipenv`:
    ```bash
    pipenv install requests click
    ```
2. Go to `pipenv shell`
3. Execute script with:
    ```bash
    python3 main.py --user $user --name $reponame --private "true/false" --description "Some description about your repo" --token "$token"
    ```
