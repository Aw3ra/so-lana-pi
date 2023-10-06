# In lana/lana_class.py
from modules.ai_generations.responding import generate_response, generate_text
from modules.audio_content.audio_io import AudioRecorder, AudioPlayer
from modules.user.user import get_user, user_handler
from Lana.commands.crypto import crypto_handler
import time

class Lana:
    def __init__(self):
        self.audio_recorder = AudioRecorder()
        self.audio_player = AudioPlayer()
        self.user = get_user()

    def listen_and_respond(self):
        """Lana's primary function to listen to the user and respond accordingly."""
        print("Lana is on")
        while True:
            audio_file = self.audio_recorder.record()
            if audio_file:
                text = self.audio_recorder.transcribe(audio_file)
                if "lana" in text.lower():
                    self.audio_player.generate_and_stream("Yes?")
                    print("Activated 'Lana' mode!")
                    self.activated_mode()

    def activated_mode(self):
        """The mode where Lana actively listens to commands until exited."""
        while True:
            audio_file = self.audio_recorder.record()
            if audio_file:
                text = self.audio_recorder.transcribe(audio_file)
                if text == "thanks lana":
                    print("Exiting 'Hey Lana' mode!")
                    break
                else:
                    self.process_command(text)

    def process_command(self, text):
        """Processes user's spoken commands."""
        response = generate_response(text)
        # If the returned response is an object, then it is a function call
        if isinstance(response, dict):
            if response["name"].startswith("crypto"):
                result = crypto_handler(response)
            elif response["name"].startswith("user"):
                result = user_handler(response)
            elif response["name"].startswith("qr_scan"):
                code = self.scan_qr()
                command = generate_response(code)
                print(command)
                if isinstance(command, dict):
                    result = user_handler(command)
                    print(result)
                else:
                    result = command
            if result:
                audio_response = generate_text(result)
                self.audio_player.generate_and_stream(audio_response)
        else:
            self.audio_player.generate_and_stream(response)

    def scan_qr(self):
        """Scans a QR code and returns the data as a string"""
        print("Scanning QR code...")
        time.sleep(1)
        data = "1wbhvevbev"
        if data:
            return "{INFORMATION} Scanned QR code successfully, here is the data: "+data
        else:
            return "{ERROR} Could not scan QR code."