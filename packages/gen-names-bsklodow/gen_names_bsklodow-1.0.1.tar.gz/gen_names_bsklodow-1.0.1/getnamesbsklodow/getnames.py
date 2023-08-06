import names
import argparse

def get_names_len():
    name = names.get_full_name()
    print(f"{name} - {len(name)}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gender', help='set gender')
    args = parser.parse_args()
    print(args.gender)
    get_names_len()