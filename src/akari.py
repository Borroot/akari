from z3 import *
import time

from printer import display
from loader import *
from constants import *
from drawer import draw
from generator import generate, XAXIS, YAXIS, XYAXIS
from z3solver import z3solve, z3solves, z3unique
from tracksolver import *
from verifier import verify_all


def main():
    verify_all()


if __name__ == '__main__':
    main()
