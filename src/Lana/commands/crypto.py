import modules.crypto.solana.wallet as interact
import modules.user.user as User
import json


def crypto_handler(command):
    try:
        arguments = json.loads(command["arguments"])
        if command['name']=="create_wallet":
            user.update_wallet(interact.create_wallet())
            return "{INFORMATION} Wallet created successfully"

        elif command['name']=="check_balance":
            pub_key = get_public_key(arguments.get('name', None).lower())
            balance = interact.check_balance(pub_key)
            return "{INFORMATION} "+arguments.get("name")+"'s balance is "+str(balance)

        elif command['name']=="check_transactions":
            pub_key = get_public_key(arguments.get('name', None).lower())
            interacted_with = arguments.get('interacted_with', None).lower()
            user = arguments.get('name', None).lower()
            amount = arguments.get('amount', None)
            transactions = interact.get_transactions_for_pubkey(
                pub_key,
                user=user,
                interacted_with=interacted_with,
                amount=amount,
                contacts=User.get_contacts()
                )
            return "{INFORMATION} "+arguments.get("name")+"'s most recent transactions are "+str(transactions)
    except:
        return "{ERROR} An error occurred while processing the command, let the user know to try again"
    
def get_public_key(name=None):
    try:
        user_contacts = User.get_contacts()
        user_info = user_contacts.get(name, {})
        public_key = user_info.get('public_key', [None])
    except Exception as e:
        # Log or handle the exception as appropriate
        print(f"An error occurred: {str(e)}")
        public_key = None
    
    return public_key[0]