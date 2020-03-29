
import os
import numpy as np
from pylatex import Document, Section, Subsection, Tabular, Math, TikZ, Axis, \
    Plot, Figure, Matrix, Alignat
from pylatex.utils import italic

# Custom
from browseTerminal import terminalBrowser
from LatexGenerator import generator

bt = terminalBrowser()

#path = "/home/filippo/Desktop/Uni/Materiali/appunti.txt"
path = bt.browse()

filename = path.split("/")[-1].split(".")[0]

file_ = open(path, "r")

lines = file_.readlines()

gen = generator(filename, lines)
gen.generate()
