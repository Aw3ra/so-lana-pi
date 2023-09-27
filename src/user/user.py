import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'user.json')


# Load in the conversation json file
with open(file_path) as json_file:
    user = json.load(json_file)


def get_user():
    return user

def update_wallet(wallet):
    user["wallet"]["private_key"] = str(wallet.private_key)
    user["wallet"]["public_key"] = str(wallet.public_key)
    with open(file_path, 'w') as outfile:
        json.dump(user, outfile, indent=4)