#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module summary

Attempts to detect if a password(s) passed meets requirements according to the The National Institute of Standards and Technology
"""
#import
import re #used to replace non ascii
import sys #used to read from stdin
import argparse #create a help automagically

def is_ascii(pwd_string):
    '''Takes in a string. Checks if ASCII or not. Returns true or false. '''
    return all(ord(char) < 128 for char in pwd_string)

def remove_non_ascii(pwd_string):
    '''Takes a string and attempts to replace all non-ASCII with asterisk.'''
    return re.sub(r'[^\x00-\x7F]','*', pwd_string)

def password_len(password_len):
    '''Takes a int for the string length and test if it is in with range'''
    if ( password_len >= 8) and (password_len <= 64):
        return True
    else:
        return False

def main():
    for input in sys.stdin:
        input = input.strip()
        input_len = len(input)

        try:
            # 1. Have an 8 character minimum and
            # 2. AT LEAST 64 character maximum

            if (password_len(input_len) == True):

                is_ascii_result = is_ascii(input)

                # 3. Allow all ASCII characters and spaces (unicode optional)
                try:
                    if is_ascii_result == True:
                        #4. Not be a common password
                        try:
                            with open(args.Path) as f:
                                for line in f:
                                    line = line.strip()
                                    if (input == line):
                                        print("{} -> Error: Too Common".format(input))
                        except IOError:
                            print("Passed File is not accessible")
                    else:
                        raise Exception
                except:
                    removed=remove_non_ascii(input)
                    print("{} -> Error: Invalid Charaters".format(removed))

            else:
                raise Exception
        except Exception:
            if(input_len <= 8):
                print("{} -> Error: Too Short".format(input))
            elif(input_len > 64):
                print("{} -> Error: Too Long".format(input))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Detect if a password meets requirements')
    parser.add_argument('Path',metavar='Filepath', help='File path to list')

    args = parser.parse_args()

    main()
