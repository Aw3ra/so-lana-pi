from solathon import Client, PublicKey, utils
import requests
import json
import os
from solathon import Keypair

def create_wallet():
    keypair = Keypair()
    # Return an object with the public and private key
    return keypair

API_KEY=os.environ["RPC_URL"]
HELIUS_KEY=os.environ["HELIUS_KEY"]

def check_balance(public_key):
    client = Client(API_KEY)
    balance = utils.lamport_to_sol(client.get_balance(PublicKey(public_key))['result']['value'])
    # Round up to 3 decimal places
    balance = round(balance, 3)
    return balance




def get_transactions_for_pubkey(public_key, user="uknown", contacts={}, amount=2000, interacted_with="none"):
    def shorten_sentences(sentence):
        parts = sentence.split()
        if len(parts) >= 5:
            if parts[1] == "transferred" and parts[4] == "to":
                return f"{parts[0]} sent {parts[5].split('.')[0]}: {parts[2]} {parts[3]}."
            elif parts[3] == "compressed":
                if parts[1] in {"minted", "transferred"}:
                    return f"{parts[0]} {parts[1]} cNFT to "+user
        return sentence

    url = f"https://api.helius.xyz/v0/addresses/{public_key}/transactions?api-key={HELIUS_KEY}"
    response = requests.get(url).json()
    returned_lst=[]
    for transaction in response[:2000]:
        desc = transaction["description"]
        if desc:
            # If an interacted_with is specified, then only return transactions that have interacted with that address
            if interacted_with != "none":
                # If interacted_with name's public key is not in the description, then skip this transaction
                if contacts[interacted_with]["public_key"][0] not in desc:
                    continue
            for contact_name, contact_data in contacts.items():
                for public_key in contact_data["public_key"]:
                    if public_key in desc:
                        desc = desc.replace(public_key, contact_name)
                if public_key in desc:  # To avoid checking other contacts once a match is found
                    break
            # Find any solana addresses in the string
            words = desc.split()
            for word in words:
                # If the word is 44 characters long
                if len(word) == 44 or len(word) == 43:
                    # Mark it as a solana address and replace it in the string with the first 4 digits and ...
                    desc = desc.replace(word, word[:4]+"..")
            returned_lst.append(shorten_sentences(desc))

    return returned_lst
            
if __name__ == "__main__":
    known_accounts = {
        "Awera": {
            "public_key": ["9DtsixQAmaHZ1UPRqoGFNocezYYWBXFjU9pHtSCrRYzc", "HNdVkA1GC1JGL2REpiTCugibnM6RjSWkSUcMM7PJ6QCg"],
            "domains": ["awera.sol"]
        },
        "Hunter": {
            "public_key": ["3rK1ufxPtNH22umXQzBvyRhigwJSnxz9VoDnqe5ANaDS"],
            "domains": ["hosty.sol"]
        },
        "Qudo": {
            "public_key": ["3rK1ufxPtNH22umXQzBvyRhigwJSnxz9VoDnqe5ANaDS"],
            "domains": ["qudo.sol"]
        },
        "Drip":{
            "public_key": ["DRiPPP2LytGjNZ5fVpdZS7Xi1oANSY3Df1gSxvUKpzny"],
            "domains": []
        },
        "Bangerz":{
            "public_key": ["BNGZxSZmbvHaPUb8xda2ikHypTuaa6MhMw98YWNfvpwL"],
            "domains": []
        }   
    }
    print(json.dumps(get_transactions_for_pubkey("9DtsixQAmaHZ1UPRqoGFNocezYYWBXFjU9pHtSCrRYzc", user = "Awera", interacted_with="Drip", contacts=known_accounts), indent=4))