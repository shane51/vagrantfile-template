import argparse

parser = argparse.ArgumentParser(description='Run test in docker')

parser.add_argument(dest='filenames', metavar='filename', nargs='*')
parser.add_argument('-D', '--dir', metavar='Directory', required=True,
                    dest='directory', action='append',
                    help='root directory of test file')

args = parser.parse_args()
print(args.directory[0])
print(args.filenames[0])
