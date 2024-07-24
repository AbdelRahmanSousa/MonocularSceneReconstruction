from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("-p", "--port", dest='port', default="5000", type=int)
parser.add_argument("--host", dest='host', default="127.0.0.1")
parser.add_argument("--instant_ngp", dest='instant_ngp', required=True)
GLOBAL = parser.parse_args()