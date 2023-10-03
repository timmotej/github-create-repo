#!/usr/bin/env python3

import requests

class Git:
    def __init__(self, secret_file=None, secret=None):
        if secret_file:
            with open(secret_file, "r") as f:
                self._secret = f.read().strip()
        elif secret:
            self._secret = secret
        else:
            self._secret = None

    def create_repository(self, name, user, description="", private=True, is_template=False):
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self._secret}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        data = {
            "name": name,
            "description": description,
            "private": private,
            "is_template": is_template,
        }
        url = f"https://api.github.com/user/repos"
        ret = requests.post(url, json=data, headers=headers)
        if ret.status_code < 300:
            return ret
        else:
            print(ret.text)
            print(ret.status_code)
            print(ret.__dict__)
            return False

