#!/usr/bin/env python3

import cartographer
from lazee.json_handler import from_json_file

import argparse

def main():
    args = parse_arguments()

    cartographer_instance = cartographer.Cartographer(args.config_filepath)

    print(str(cartographer_instance))

    print("it didn't crash")

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Test that Cartographer instantiates")
    parser.add_argument("config_filepath", help="filepath to the Cartographer config")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()