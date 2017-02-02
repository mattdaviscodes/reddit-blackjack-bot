import argparse

meta_parser = argparse.ArgumentParser()
meta_parser.add_argument('--test', action="store_true")
meta_args = meta_parser.parse_args()