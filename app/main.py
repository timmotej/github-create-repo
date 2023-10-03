#!/usr/bin/env python3

import create_repo
import click
import sys
import os

@click.command()
@click.option("--name", default="", help="Name of the new repo.")
@click.option("--user", default="", help="Name of the user")
@click.option("--token", default="", help="Token to repo")
@click.option("--token_file", default="", help="Token file path")
@click.option("--private", default="", help="Repository private or no?")
@click.option("--description", default="", help="Repository private or no?")

def main(name, user, token, token_file, private, description):
    name = name or os.getenv("NAME", False)
    user = user or os.getenv("USER", "timmotej")
    token = token or os.getenv("TOKEN", False)
    token_file = token_file or os.getenv("TOKEN_FILE", False)
    if private == "":
        private = os.getenv("PRIVATE", True)
    description = description or os.getenv("DESCRIPTION", "")
    if not description:
        description = name.replace("-"," ").replace("_"," ").title()
    github_client = create_repo.Git(secret_file=token_file, secret=token)
    ret = github_client.create_repository(name=name, user=user, description=description, private=private)
    print(ret)

if __name__ == "__main__":
     main()
