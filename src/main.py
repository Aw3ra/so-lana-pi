from modules.audio_content.audio import generate_and_stream_audio
from modules.ai_generations.responding import generate_response, generate_text
from ai_generations.transcribe import transcribe
from audio_content.audio_in import record_audio
from crypto.solana.create_wallet import create_wallet
from crypto.solana.check_balance import check_balance, get_transactions_for_pubkey
from user.user import update_wallet, get_user

import os
import time
import json


def process_audio(text):
    response = generate_response(text)
    print(response)
    # If the returned response is an object, then it is a function call
    if isinstance(response, dict):
        arguments = json.loads(response["arguments"])
        if response["name"]=="send_money":
            if not get_user()["wallet"]["private_key"]:
                new_response = generate_text(
                    "{INFORMATION} There is no wallet connected to you. You MUST ask them if they would like you to create and connect one"
                    )

                generate_and_stream_audio(new_response)
            else:
                print(arguments)
                new_response = generate_text(
                    "{INFORMATION} You have just sent "+arguments["name"] + str(arguments["amount"]) + " " + arguments["currency"] + " from the users wallet"
                    )
                generate_and_stream_audio(new_response)
        elif response["name"]=="create_wallet":
            if get_user()["wallet"]["private_key"]:
                new_response = generate_text(
                    "{INFORMATION} You already have a wallet connected to you. Tell them to stop being silly."
                    )
                generate_and_stream_audio(new_response)
            else:
                wallet = create_wallet()
                update_wallet(wallet)
                new_response = generate_text(
                    "{INFORMATION} You have just created and connected a wallet to yourself to allow you to interact with solana on the users behalf, the wallet address is: "+str(wallet.public_key)+" now continue with the request"
                    )
                generate_and_stream_audio(new_response)
        elif response["name"]=="check_balance":
            name = arguments["name"]
            if name not in get_user()['contacts']:
                new_response = generate_text(
                    "{INFORMATION} The user does not have a contact called "+name
                    )
                generate_and_stream_audio(new_response)
                return
            # Check the wallet address of the user
            address = get_user()['contacts'][arguments["name"]]['public_key']
            balance = check_balance(address)
            print(balance)
            # Wait 2 seconds
            # This is where we would fetch some transactions and make them readable
            new_response = generate_text(
                "{INFORMATION} You have just checked the balance for "+arguments["name"]+" and it is "+str(balance)+" SOL(solana token)."
                )
            generate_and_stream_audio(new_response)
        elif response["name"]=="check_transactions":
            name = arguments["name"]
            if name not in get_user()['contacts']:
                new_response = generate_text(
                    "{INFORMATION} The user does not have a contact called "+name
                    )
                generate_and_stream_audio(new_response)
                return
            # Check the wallet address of the user
            contacts = get_user()['contacts']
            address = contacts[arguments["name"]]['public_key'][0]
            transactions = get_transactions_for_pubkey(address, contacts=contacts, user=arguments["name"], interacted_with=arguments["interacted_with"])
            print(arguments)
            print(transactions)
            # Wait 2 seconds
            time.sleep(2)
            # This is where we would fetch some transactions and make them readable
            new_response = generate_text(
                "{INFORMATION} "+arguments["name"]+"'s most recent transactions are "+str(transactions)
                )
            generate_and_stream_audio(new_response)
    else:
        generate_and_stream_audio(response)


def start():
    print("Lana is on")
    while True:
        audio_file = record_audio()
        if audio_file:
            text = transcribe(audio_file).text
            if "lana" in text.lower():
                generate_and_stream_audio("Yes?")
                print("Activated 'Lana' mode!")
                while True:  # Enter the "Hey Lana" mode
                    audio_file = record_audio()
                    if audio_file:
                        text = transcribe(audio_file).text
                        os.remove(audio_file)
                        print(text)
                        if text == "You":
                            pass
                        if "thanks lana" in text.lower():
                            print("Exiting 'Hey Lana' mode!")
                            break  # Exit the "Hey Lana" mode
                        else:
                            process_audio(text)

                
    # Text to generate a response from


def test_commands():
    command= "How many times have I interacted with Qudo?"
    process_audio(command)

if __name__ == "__main__":
    test_commands()

