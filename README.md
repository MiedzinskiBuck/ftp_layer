# FTP BruteForce with IP rotation through TOR

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

Script to perform Brute Force attacks in a host that has an IP based lockout rule such as fail2ban.
The IP rotation feature is done through a TOR proxy, so a few configuration is needed.

## Install and Configuration

First, we need to install the dependencies:

    $ sudo pip3 install -r requirements.txt

The tool was written in Python3, so I'm not sure if it will run on previous versions...

To be able to proxy the requests, you'll need the TOR service running and also a few configurations on it.

    $ sudo apt-get install tor

After install TOR, we need to alter its configs to authenticate to the Controller method. Those configuration can be made in the "torrc" config file.

    $ sudo vim /etc/tor/torrc

First of all, we need to uncomment the **ControlPort 9051** and, since we have enabled our ControlPort, we need to set an authentication to it. 
To do so, we need to generate a **TOR-HASH**.

    $ tor --hash-password [YOURPASSWORD]

Then, we need to uncomment the line with **HashedControlPassword 16:5D24B24133137E1660FABCFB6F4662FAABACA785A56CD02E91AA0BADB2** and change the hash with the newly generated one.

Thats pretty much it! Now you should be able to use the tool.

## Usage

Usage: socks_brute_ftp.py -t [TARGET] -p [PORT] -L [USERNAMELIST] -P [PASSWORDLIST]

- Target = The target's IP address.
- Port = The target's FTP running PORT. If none is provided, the tool will consider the default port as 21.
- UsernameList = The wordlist that you will use for the usernames.
- PasswordList = The wordlist that you will use for the passwords.
