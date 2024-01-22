# Automated-SSH-Login-through-Brute-Forcing

This is a simple Python script designed to perform automated SSH brute force attacks by trying common passwords against a specified host and username. It utilizes the paramiko library for SSH connections and the pwn library for convenient input handling.

Usage
Clone the Repository:

bash

git clone https://github.com/AkshatM1707/SSH-BruteForcing.py

cd ssh-brute-forcer

Install Dependencies:

pip install -r requirements.txt

Run the Script:



python ssh_brute_forcer.py

Follow the prompts to enter the target IP address and username.

Disclaimer
Use this tool responsibly and only on systems that you have explicit permission to test. Unauthorized access to computer systems is illegal and unethical.

Password List
The script uses a list of common passwords stored in the file ssh-common-passwords.txt. You may want to replace or supplement this list with your own password dictionary for more comprehensive testing.

Contributing
Contributions are welcome! If you have improvements or additional features to suggest, feel free to open an issue or submit a pull request.
