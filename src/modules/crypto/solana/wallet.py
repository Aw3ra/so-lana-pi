import requests
import json
import os

API_KEY=os.environ["RPC_URL"]
HELIUS_KEY=os.environ["HELIUS_KEY"]

def check_balance(public_key):
    url = f"https://api.helius.xyz/v0/{public_key}/balances?api-key={HELIUS_KEY}"
    response = requests.get(url).json()
    return response


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
    for transaction in response[:amount]:
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
    print(json.dumps(check_balance("9DtsixQAmaHZ1UPRqoGFNocezYYWBXFjU9pHtSCrRYzc"), indent=4))