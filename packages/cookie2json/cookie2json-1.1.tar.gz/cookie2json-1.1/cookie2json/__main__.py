import cookie2json, argparse

parser = argparse.ArgumentParser()
parser.add_argument('cookie', help='plz put cookie plaintext here')
args = parser.parse_args()

print(cookie2json.format(args.cookie))
