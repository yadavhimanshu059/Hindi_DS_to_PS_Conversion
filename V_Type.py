# -*- coding: utf-8 -*-
import sys
import glob
from ssf_api import *
from os import listdir
from os.path import isfile, join
from Phrases import *
#from V_Type import *
from operator import itemgetter
from Rule_Selection import *
import string


class V_type(object):
    def __init__(self, tree):
        self.tree=tree
        
    def isPassive(self, pred):
        flag=0
        flag_1=0
        n=0
        for node in pred:
            if not node.getLemma()=='((':
                n=n+0
                if n==0:
                    if node.getAF()[6]=='या':
                        n=n+1
                if n==1:
                    if node.getAF()[0]=='जा':
                        flag=flag+1
                    else:
                        flag=flag+0

        if not flag==0:
            return True

    def isNegationafterVaux(self, pred):
        posn=0
        node_posn={}
        for node in pred:
            posn=posn+1
            node_posn[node.getPos()]=posn

        for catg in node_posn.keys():
            if catg=='NEG':
                neg_posn=node_posn[catg]
                VAUX_posn=[]
                for catgr in node_posn.keys():
                    if catgr=='VAUX':
                        VAUX_posn.append(node_posn[catgr])
                for posns in VAUX_posn:
                    if neg_posn>posns:
                        return True
                        
            


#SSF_DIR ="F:/__New_Jee1/Evolution/Fold_4_RWL/Project-6_(DSD_to_PSD)/HDTB_pre_release_version-0.05/HDTB_pre_release_version-0.05/InterChunk/SSF/utf/news_articles_and_heritage/Training/"
#n_odd=0
#for filename in listdir(SSF_DIR):
#    ssf = SSF(SSF_DIR+filename)
#    for tree in ssf.getTrees():       
#        PS_tree=''
#        for chunk in tree:
#            if chunk.isFiniteVerb():
#                pred=chunk
#        get=V_type(tree, pred)
#        odd_tree=get.isNegationafterVaux()
#        if odd_tree:
#            n_odd=n_odd+1
#            print tree.__str__()
#            print "\n\n\n\n"
        
#print "Total number of such trees (out of around 7000 trees)="+str(n_odd)
