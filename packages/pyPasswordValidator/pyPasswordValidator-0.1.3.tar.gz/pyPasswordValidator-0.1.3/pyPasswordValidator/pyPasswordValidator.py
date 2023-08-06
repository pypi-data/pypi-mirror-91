#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module summary

Attempts to detect if a password(s) passed meets requirements according to the The National Institute of Standards and Technology
"""
#import
import re #used to replace non ascii
import sys #used to read from stdin
import argparse #create a help automagically
import time

start = time.time()

def is_ascii(pwd_string):
    '''Takes in a string. Checks if ASCII or not. Returns true or false. '''
    return all(ord(char) < 128 for char in pwd_string)

def remove_non_ascii(pwd_string):
    '''Takes a string and attempts to replace all non-ASCII with asterisk.'''
    return re.sub(r'[^\x00-\x7F]','*', pwd_string)

def main():
    for input in sys.stdin:
        input = input.strip()
        input_len = len(input)

        MIN_INPUT = 8
        MAX_INPUT = 64

        # 1. Have an 8 character minimum and
        if (input_len < MIN_INPUT):
            print("{} -> Error: Too Short".format(input))
        # 2. AT LEAST 64 character maximum
        elif (input_len > MAX_INPUT):
            print("{} -> Error: Too Long".format(input))
        else:
            # 3. Allow all ASCII characters and spaces (unicode optional)
            is_ascii_result = is_ascii(input)
            if is_ascii_result == False:
                removed=remove_non_ascii(input)
                print("{} -> Error: Invalid Charaters".format(removed))
            else:
                #4. Not be a common password
                try:
                    common_pass_set = set(line.strip() for line in open(args.Path))
                    if (input in common_pass_set):
                        print("{} -> Error: Too Common".format(input))
                except IOError:
                    print("Passed File is not accessible")
    end = time.time()
    print(end - start)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Detect if a password meets requirements')
    parser.add_argument('Path',metavar='Filepath', help='File path to list')

    args = parser.parse_args()

    main()

