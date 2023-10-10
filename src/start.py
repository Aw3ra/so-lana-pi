from Lana.lana import Lana
from modules.user.user import clear_conversation 

if __name__ == "__main__":
    lana = Lana()
    # lana.listen_and_respond()
    lana.process_command("Can you check my USDC balance?")