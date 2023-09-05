import os
from argparse import ArgumentParser
from pathlib import Path

from podslicer import cli

parser = ArgumentParser(prog="podslicer")
parser.add_argument("track")
args = parser.parse_args()

cli.run(Path(os.path.join(os.getcwd(), args.track)))
