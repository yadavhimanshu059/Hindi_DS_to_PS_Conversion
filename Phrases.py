
#-*- coding: UTF-8 -*-
# filename   : Phrases.py
# author     : Himanshu Yadav
# last update: 7/13/2016
import os
import sys
import glob
from ssf_api import *
from os import listdir
from os.path import isfile, join
from Word_order import *
from operator import itemgetter
import string


############################## Begin: class Phrases ##############################

class Non_projective(object):
    def __init__(self, tree):
        self.tree=tree
        self.check=Word_order(self.tree)

    def non_proj(self, ChunkName, child_P, child_child):
        flag=''
        value=False
        child_child_f=''
        mod_flag_child=''
        flag_child_posn=0
        
        ls_order=[]
        for node in child_child:
            ls_order.append(node[1])
        child_posn={}
        child_posn[ChunkName]=self.check.order()[ChunkName]
        for chunk in self.tree.getChildren(ChunkName):
            child_posn[chunk.getName()]=self.check.order()[chunk.getName()]

        parent_posn=self.check.order()[child_P]
        ordered_child=sorted(child_posn.items(), key=itemgetter(1))
        for child in ordered_child:
            if child[1]<parent_posn:
                if min(ls_order)<child[1]:
                    flag='min'        
            elif child[1]>parent_posn:
                if max(ls_order)>child[1]:
                    flag='max'

        if flag=='min':
            for nodes in child_child:
                if nodes[1]==min(ls_order):
                    flag_child=nodes[0]
                    flag_child_posn=nodes[1]
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==min(ls_order):
                    flag_empty=nodename+'**'
                    flag_empty=string.replace(flag_empty, 'VGF', 'S')
                    flag_empty=string.replace(flag_empty, 'VGNF', 'S-NF')
                    flag_empty=string.replace(flag_empty, 'VGNN', 'S-NF')
                    flag_chunk=self.tree.getChunk(nodename)
                    if flag_chunk.isChild(None, child_P):
                        signal_copy=True
                    else:
                        signal_copy=False
            if flag_child[1]=='[':        
                mod_flag_child=string.replace(flag_child, flag_child.split()[0], ' [.'+flag_empty, 1)
            else:
                mod_flag_child=flag_child

            if signal_copy==True:
                dict_child_child=dict(child_child)
                dict_child_child[' '+flag_empty] = dict_child_child.pop(flag_child)
            else:
                dict_child_child=dict(child_child)
                del dict_child_child[flag_child]
                
            ordered_child_child=sorted(dict_child_child.items(), key=itemgetter(1))  
            for childname in ordered_child_child:
                child_child_f=child_child_f+childname[0]

        elif flag=='max':            
            for nodes in child_child:
                if nodes[1]==max(ls_order):
                    flag_child=nodes[0]
                    flag_child_posn=nodes[1]
            for nodename in self.check.order().keys():
                if self.check.order()[nodename]==max(ls_order):
                    flag_empty=nodename+'**'
                    flag_empty=string.replace(flag_empty, 'VGF', 'S')
                    flag_empty=string.replace(flag_empty, 'VGNF', 'S-NF')
                    flag_empty=string.replace(flag_empty, 'VGNN', 'S-NF')
                    flag_chunk=self.tree.getChunk(nodename)
                    if flag_chunk.isChild(None, child_P):
                        signal_copy=True
                    else:
                        signal_copy=False

            if flag_child[1]=='[':        
                mod_flag_child=string.replace(flag_child, flag_child.split()[0], ' [.'+flag_empty, 1)
            else:
                mod_flag_child=flag_child

            if signal_copy==True:
                dict_child_child=dict(child_child)
                dict_child_child[' '+flag_empty] = dict_child_child.pop(flag_child)
            else:
                dict_child_child=dict(child_child)
                del dict_child_child[flag_child]
                
            ordered_child_child=sorted(dict_child_child.items(), key=itemgetter(1))  
            for childname in ordered_child_child:
                child_child_f=child_child_f+childname[0]
        
        if flag=='min' or flag=='max':
            value=True
        
        return [value, child_child_f, mod_flag_child, flag_child_posn]
 
class Phrase(object):
    # initializes 'Phrase' from 'tree' and 'ChunkName'
    # tree: one of the tree line from SSF treelist
    # Chunkname: Name of the chunk from chunklist in the tree
    def __init__(self, tree):
        self.tree=tree
        self.check=Word_order(self.tree)        # calls 'Word_order' class which allocates unique id to each chunk according to linear word order
        self.handle=Non_projective(self.tree)

    # draws terminal nodes for any chunk (e.g. splits phrasal NP node into NNP and PSP terminal nodes)
    # chunk: any chunk from chunk-list in a tree
    def terminal_nodes(self, chunk):
        feature_1=''
        for node in chunk:
            feature=''
            if node.getLemma()=='((':
                feature_1=feature_1
            else:
                node_name=node.getName()
                node_name=string.replace(node_name, 'ठ', 'प')
                #node_name=string.replace(node_name, '2', '')
                #node_name=string.replace(node_name, '3', '')
                #node_name=string.replace(node_name, '4', '')
                feature=' [.'+node.getPos()+' '+node_name+' ]'
                feature_1=feature_1+feature
        t_node=feature_1
        return t_node        
    
    # draws internal phrase structure for a given phrase.
    # uses modifier-modified relation given in DS treebank to identify head child of a phrase.
    # takes takes head_child as a chunk to draw phrase structure of non-head children
    def phrase(self, chunk):
        ChunkName=chunk.getName()
        Chunk_PC=chunk.getPos()
        head_Posn=self.check.order()[ChunkName]
        head_child=self.terminal_nodes(chunk)
        all_dict_child={}
        for chunk in self.tree.getChildren(ChunkName):
            if chunk.getPos()=='VGF' or chunk.getPos()=='NULL__VGF' or chunk.getPos()=='VGNN' or chunk.getPos()=='VGNF' or chunk.getPos()=='NULL__VGNN' or chunk.getPos()=='NULL__VGNF':
                child=' flag '+str(self.check.order()[chunk.getName()])
                all_dict_child[child]=self.check.order()[chunk.getName()]
            else:
                child_P=chunk.getName()
                child_PC=chunk.getPos()
                child_Posn=self.check.order()[child_P]
                if not self.tree.getChildren(child_P):
                    child=' [.'+child_PC+self.terminal_nodes(chunk)+' ]'
                    all_dict_child[child]=child_Posn
                else:
                    child_child_f=''
                    child_child=self.phrase(chunk)
                    if self.handle.non_proj(ChunkName, child_P, child_child)[0]:                    
                        child_child_f=self.handle.non_proj(ChunkName, child_P, child_child)[1]
                        
                        flag_child=self.handle.non_proj(ChunkName, child_P, child_child)[2]
                        flag_child_posn=self.handle.non_proj(ChunkName, child_P, child_child)[3]
                        all_dict_child[flag_child]=flag_child_posn
                    else:
                        for node in child_child:
                            child_child_f=child_child_f+node[0]    
                    child=' [.'+child_PC+child_child_f+' ]'
                    all_dict_child[child]=child_Posn
        all_dict_child[head_child]=head_Posn
        ordered_child=sorted(all_dict_child.items(), key=itemgetter(1))    

        return ordered_child
        
############################## End  : class Phrase   ###############################
    
############################## Begin: class Fragments ##############################
# It applies the fragmention process on a given clause and fragments it into predicate, arguments and adjuncts for distinction.

class Fragments(object):
    # initializes the Fragments from 'tree' and 'pred'
    # pred: head-chunk of the clause for which fragments are to be separated 
    def __init__(self, tree, pred):
        self.tree=tree
        self.pred=pred
        self.Pred_P=self.pred.getName()
        self.check=Word_order(self.tree)
        self.create=Phrase(self.tree)
        self.handle=Non_projective(self.tree)

    # returns predicate and its word order position
    def predicate(self):
        pred_Pos=self.pred.getPos()
        Pred_terminal=self.create.terminal_nodes(self.pred)
        Pred=' [.'+pred_Pos+Pred_terminal+' ]'
        Pred_Posn=self.check.order()[self.Pred_P]
        return [Pred, self.Pred_P, Pred_Posn, pred_Pos, Pred_terminal]

    # returns a dictionary of arguments with their word-order positions
    # we have at this level defined some basic labels like NP-SUBJ, NP-OBJ-1, NP-SUBJ-Dative etc. to ditinguish between arguments
    def fragments(self):
        all_dict_frag={}
        for chunk in self.tree.getChildren(self.Pred_P):
            ChunkName=chunk.getName()
            Chunk_Posn=self.check.order()[ChunkName]
            Chunk_PC=chunk.getPos()
            if (Chunk_PC=='VGF' or Chunk_PC=='NULL__VGF' or Chunk_PC=='VGNN' or Chunk_PC=='VGNF' or Chunk_PC=='NULL__VGNN' or Chunk_PC=='NULL__VGNF'):
                Frag=' flag '+str(Chunk_Posn)
                all_dict_frag[Frag]=Chunk_Posn
            else:
                child_f=''
                child=self.create.phrase(chunk)
                if self.handle.non_proj(self.Pred_P, ChunkName, child)[0]:                    
                    child_f=self.handle.non_proj(self.Pred_P, ChunkName, child)[1]
                    flag_child=self.handle.non_proj(self.Pred_P, ChunkName, child)[2]
                    flag_child_posn=self.handle.non_proj(self.Pred_P, ChunkName, child)[3]
                    all_dict_frag[flag_child]=flag_child_posn
                else:
                    for node in child:
                        child_f=child_f+node[0]

                if chunk.isChild('k1', self.Pred_P):
                    if self.tree.existChild('k1s', self.Pred_P):
                        Frag=" [."+Chunk_PC+child_f+" ]"
                        all_dict_frag[Frag]=Chunk_Posn
                    else:
                        Frag=" [."+Chunk_PC+'-SUBJ'+child_f+" ]"
                        all_dict_frag[Frag]=Chunk_Posn
                        
                elif chunk.isChild('k4', self.Pred_P):
                    Frag=" [."+Chunk_PC+'-OBJ-2'+child_f+" ]"
                    all_dict_frag[Frag]=Chunk_Posn
                
                elif chunk.isChild('k4a', self.Pred_P):
                    Frag=" [."+Chunk_PC+'-SUBJ-Dat'+child_f+" ]"
                    all_dict_frag[Frag]=Chunk_Posn

                elif chunk.isChild('pk1', self.Pred_P):
                    Frag=" [."+Chunk_PC+'-SUBJ'+child_f+" ]"
                    all_dict_frag[Frag]=Chunk_Posn

                elif chunk.isChild('jk1', self.Pred_P):
                    Frag=" [."+Chunk_PC+'-J-SUBJ'+child_f+" ]"
                    all_dict_frag[Frag]=Chunk_Posn
                    
                elif (chunk.isChild('k2', self.Pred_P) or chunk.isChild('k2p', self.Pred_P)):
                    Frag=" [."+Chunk_PC+'-OBJ-1'+child_f+" ]"
                    all_dict_frag[Frag]=Chunk_Posn

                elif chunk.isChild('k2g', self.Pred_P):
                    Frag=" [."+Chunk_PC+'-OBJ-2'+child_f+" ]"
                    all_dict_frag[Frag]=Chunk_Posn

                elif chunk.isChild('k2s', self.Pred_P):
                    Frag=" [."+Chunk_PC+'-OBJ-Comp'+child_f+" ]"
                    all_dict_frag[Frag]=Chunk_Posn
                    
                elif chunk.isChild('rsym', self.Pred_P):
                    SYM='|'

                else:
                    Frag=" [."+Chunk_PC+' Label '+child_f+" ]"
                    all_dict_frag[Frag]=Chunk_Posn

        return all_dict_frag




