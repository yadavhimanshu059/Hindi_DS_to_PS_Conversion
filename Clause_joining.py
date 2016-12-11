#-*- coding: UTF-8 -*- 
import os
import sys
import glob
from ssf_api import *
from os import listdir
from os.path import isfile, join
from Word_order import *
from Rule_Selection import *
import string


class Join_clauses(object):
    def __init__(self, tree):
        self.tree=tree
        self.check=Word_order(self.tree)

    def join_clauses(self, i_ChunkName, i_clause):
        clause=i_clause
        ChunkName=i_ChunkName
                
        for chunk in self.tree.getChildren(ChunkName):
            ChunkName=chunk.getName()
            if chunk.getPos()=='VGF' or chunk.getPos()=='NULL__VGF' or chunk.getPos()=='VGNN' or chunk.getPos()=='VGNF' or chunk.getPos()=='NULL__VGNN' or chunk.getPos()=='NULL__VGNF':
                draw_PS=Rule_selection(self.tree, chunk)
                emb_clause=draw_PS.rule_selection()
                n_flag=0
                for word in emb_clause.split():
                    if word=='flag':
                        n_flag=n_flag+1
                if not n_flag==0:
                    emb_clause=self.join_clauses(ChunkName, emb_clause)
                    clause=string.replace(clause, ' flag '+str(self.check.order()[ChunkName]), emb_clause)
                else:
                    clause=string.replace(clause, ' flag '+str(self.check.order()[ChunkName]), emb_clause)
            else:
                clause=self.join_clauses(ChunkName, clause)
                
        return clause
            
    def ps_tree(self):
        PS_tree=''
        for chunk in self.tree:
            if not chunk.getDrel():
                if not chunk.getDMrel():
                    ChunkName=chunk.getName()
                    PS_clause=Rule_selection(self.tree, chunk)
                    clause=PS_clause.rule_selection()
                    PS_tree=self.join_clauses(ChunkName, clause)

        return PS_tree
        
