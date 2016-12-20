#-*- coding: UTF-8 -*- 
import os
import sys
import glob
from ssf_api import *
from os import listdir
from os.path import isfile, join
from Word_order import *
from Clause_joining import *


ssf = SSF("sample_input.dat")
for tree in ssf.getTrees():
    draw=Join_clauses(tree)
    PS_tree=draw.ps_tree()
    print PS_tree+'\n\n'

            
