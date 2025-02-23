Hi,

Just a fun Little project i decided to spend a few hours on during the weekend. 

This will only work if you have a Tele2 wifi hub C2.

Showcase: https://www.youtube.com/watch?v=6XQjibwpra0&ab_channel=AlbinNyholm 

1. Install dependencies in a virtual python environment .venv inside of this folder.

2. Move chromedriver.exe over to .venv/scripts/

3a. To run the python script from powershell as administrator: go to Project folder in powershell and .venv\Scripts\Activate.ps1, then run script with python reservip.py <MAC_ADDRESS> <IP_ADDRESS>

3b. To run the script via the bat file as a cmd command: Specify the folder path, where the bat file is located, in your windows system envionment Path variable. After you've done this you should be able to do reservip <Mac Address> <IP Address>


