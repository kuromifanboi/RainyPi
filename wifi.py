from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from base64 import b64encode, b64decode

ENCRYPTION_KEY = b'YOUR_ENCRYPTION_KEY'
WIFI_CIPHER = AES.new(ENCRYPTION_KEY, AES.MODE_EAX)

def encrypt_data(data):
    cipher_text, _ = WIFI_CIPHER.encrypt_and_digest(data.encode('utf-8'))
    return b64encode(cipher_text).decode('utf-8')

def decrypt_data(encrypted_data):
    cipher_text = b64decode(encrypted_data.encode('utf-8'))
    data = WIFI_CIPHER.decrypt(cipher_text).decode('utf-8')
    return data

def save_wifi_credentials(encrypted_ssid, encrypted_password):
    with open("wifi_credentials.txt", "w") as file:
        file.write(encrypted_ssid + "\n")
        file.write(encrypted_password)

def load_wifi_credentials():
    try:
        with open("wifi_credentials.txt", "r") as file:
            encrypted_ssid = file.readline().rstrip()
            encrypted_password = file.readline().rstrip()

            ssid = decrypt_data(encrypted_ssid)
            password = decrypt_data(encrypted_password)

            return ssid, password

    except FileNotFoundError:
        return None, None

def handle_wifi_config():
    print("WiFi Configuration:")
    ssid = input("Enter WiFi SSID: ")
    password = input("Enter WiFi Password: ")

    # Encrypt and store the WiFi data
    encrypted_ssid = encrypt_data(ssid)
    encrypted_password = encrypt_data(password)
    save_wifi_credentials(encrypted_ssid, encrypted_password)

    print("WiFi configuration saved.")
