#!/usr/bin/env python3

import cartographer

import argparse

def main():
    args = parse_arguments()

    with open(args.config_filepath) as file_stream:
        config_data = file_stream.read()

    cartographer_instance = cartographer.Cartographer(config_data)

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