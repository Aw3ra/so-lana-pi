import modules.crypto.solana.wallet as interact
import modules.user.user as User
import json


def crypto_handler(command):
    try:
        arguments = json.loads(command["arguments"])
        if command['name']=="create_wallet":
            user.update_wallet(interact.create_wallet())
            return "{INFORMATION} Wallet created successfully"

        elif command['name']=="crypto_check_balance":
            pub_key = get_public_key(arguments.get('name', None).lower())
            balance = interact.check_balance(pub_key)
            return "{INFORMATION} "+arguments.get("name")+"'s balance is "+str(balance)

        elif command['name']=="crypto_check_transactions":
            if arguments.get('name'):
                pub_key = get_public_key(arguments.get('name').lower())
            else:
                user_name = User.get_user().get('name')
                if user_name:
                    pub_key = get_public_key(user_name.lower())
                else:
                    pub_key = None
            interacted_with = arguments.get('interacted_with', '').lower() if arguments.get('interacted_with') else "none"
            user = arguments.get('name', '').lower() if arguments.get('name') else User.get_user().get('name').lower()
            amount = arguments.get('amount', 100)
            # Conver the amount to an int
            if amount:
                amount = int(amount)
            transactions = interact.get_transactions_for_pubkey(
                pub_key,
                user=user,
                interacted_with=interacted_with,
                amount=amount,
                contacts=User.get_contacts()
                )
            return "{INFORMATION} "+user+"'s most recent transactions are "+str(transactions)+". Reply with a brief overview"
        elif command["name"]=="crypto_check_price":
            token = arguments.get('token', None)
            price = "$20"
            return "{INFORMATION} "+token+"'s price is "+str(price)
    except Exception as e:
        print(e)
        
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