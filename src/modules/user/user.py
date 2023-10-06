import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, 'user.json')


# Load in the conversation json file
with open(file_path) as json_file:
    user = json.load(json_file)

def clear_conversation():
    # Clear everything except the first message in the conversation
    user["conversation"] = user["conversation"][:1]
    with open(file_path, 'w') as outfile:
        json.dump(user, outfile, indent=4)

def get_user():
    return user

def get_contacts():
    return user["contacts"]

def update_wallet(wallet):
    user["wallet"]["private_key"] = str(wallet.private_key)
    user["wallet"]["public_key"] = str(wallet.public_key)
    with open(file_path, 'w') as outfile:
        json.dump(user, outfile, indent=4)

def user_handler(command):
    arguments = json.loads(command["arguments"])
    if command["name"]=="user_add_contact":
        name = arguments.get("name", None).lower()
        public_key = arguments.get("public_key", None)
        # If the public key is none, then request a public key from the user
        if public_key == None:
            return "{INFORMATION REQUEST} The user has not provided a public key for: "+name+". Ask them if they'd like to provide a QR or for them to spell it out."
        # If the contact already exists, append the public key to the list
        if name in user["contacts"]:
            # If the public key already exists, don't add it
            if public_key not in user["contacts"][name]["public_key"]:
                user["contacts"][name]["public_key"].append(public_key)
                with open(file_path, 'w') as outfile:
                    json.dump(user, outfile, indent=4)
                return "{INFORMATION} Added a new public key for: "+name
            else:
                return "{INFORMATION} Public key has already been added for: "+name
        else:
            user["contacts"][name] = {"public_key": [public_key]}
            with open(file_path, 'w') as outfile:
                json.dump(user, outfile, indent=4)
            return "{INFORMATION} Added "+name+" to your contacts list"



if __name__ == "__main__":
    user_handler({"name": "user_add_contact", "arguments": '{"name": "Hunter", "public_key": "none"}'})