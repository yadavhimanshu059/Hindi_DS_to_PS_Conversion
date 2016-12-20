#!/usr/bin/python
#-*- coding: UTF-8 -*- 
import os
import sys
import glob
from ssf_api import *
from os import listdir
from os.path import isfile, join
from Phrases import *
from operator import itemgetter
import string


class Rule_selection(object):
    def __init__(self, tree, pred):
        self.tree=tree
        self.pred=pred
        
    def rule_selection(self):
        
        get=Fragments(self.tree, self.pred)
        predicate={get.predicate()[0] : get.predicate()[2]}
        Pred_P=get.predicate()[1]
        Pred_Pos=get.predicate()[3]
        
        dict_frag=get.fragments()

        all_dict_frag=dict(dict_frag.items()+predicate.items())
        all_dict_frag=dict(dict_frag)
        all_dict_frag.update(predicate)

        SYM=''
        for chunk in self.tree.getChildren(self.pred.getName()):
            if chunk.isChild('rsym', self.pred.getName()):
                sym_term=''
                for node in chunk:
                    if not node.getLemma()=='((':
                        sym_term=sym_term+' '+node.getName()
                SYM="[.SYM"+sym_term+" ]"
            
        S = ''
        Arg0=''
        all_frag=''
        ordered_fragments=sorted(all_dict_frag.items(), key=itemgetter(1))
        
        if Pred_Pos=='VGF' or Pred_Pos=='NULL__VGF':
            if not (ordered_fragments[0][0].split()[0]=='[.VGF' or ordered_fragments[0][0].split()[0]=='[.NULL__VGF'):
                for frag in ordered_fragments:
                    if frag[0]==ordered_fragments[0][0]:
                        Arg0=frag[0]
                    else:
                        all_frag=all_frag+frag[0]
                Arg0=string.replace(Arg0, ' Label ', '')
                all_frag=string.replace(all_frag, ' Label ', '')

                #if stype.isSimpleTransitive():
                if not SYM=='':
                    S=" [.S"+Arg0+" [.VP"+all_frag+" ]"+" "+SYM+" ]"
                else:
                    S=" [.S"+Arg0+" [.VP"+all_frag+" ]"+" ]"
                #S="This is Simple Transitive construnction:"+"\n"+S
            else:
                for frag in ordered_fragments:
                    all_frag=all_frag+frag[0]
                if not SYM=='':
                    S=" [.S"+" [.VP"+all_frag+" ]"+" "+SYM+" ]"
                else:
                    S=" [.S"+" [.VP"+all_frag+" ]"+" ]"
                    
        elif Pred_Pos=='VGNN' or Pred_Pos=='VGNF':
            if not (ordered_fragments[0][0].split()[0]=='[.VGNN' or ordered_fragments[0][0].split()[0]=='[.VGNF'):
                for frag in ordered_fragments:
                    if frag[0]==ordered_fragments[0][0]:
                        Arg0=frag[0]
                    else:
                        all_frag=all_frag+frag[0]
                Arg0=string.replace(Arg0, ' Label ', '')
                all_frag=string.replace(all_frag, ' Label ', '')
                
                if not SYM=='':
                    S=" [.S-"+Pred_Pos[2]+Pred_Pos[3]+Arg0+" [.VP"+all_frag+" ]"+" "+SYM+" ]"
                else:
                    S=" [.S-"+Pred_Pos[2]+Pred_Pos[3]+Arg0+" [.VP"+all_frag+" ]"+" ]"
            else:
                for frag in ordered_fragments:
                    all_frag=all_frag+frag[0]
                if not SYM=='':
                    S=" [.S-"+Pred_Pos[2]+Pred_Pos[3]+" [.VP"+all_frag+" ]"+" "+SYM+" ]"
                else:
                    S=" [.S-"+Pred_Pos[2]+Pred_Pos[3]+" [.VP"+all_frag+" ]"+" ]"
        elif Pred_Pos=='NULL__VGNF' or Pred_Pos=='NULL__VGNN':
            if not (ordered_fragments[0][0].split()[0]=='[.NULL__VGNN' or ordered_fragments[0][0].split()[0]=='[.NULL__VGNF'):
                for frag in ordered_fragments:
                    if frag[0]==ordered_fragments[0][0]:
                        Arg0=frag[0]
                    else:
                        all_frag=all_frag+frag[0]
                Arg0=string.replace(Arg0, ' Label ', '')
                all_frag=string.replace(all_frag, ' Label ', '')
                
                if not SYM=='':
                    S=" [.S-"+Pred_Pos[8]+Pred_Pos[9]+Arg0+" [.VP"+all_frag+" ]"+" "+SYM+" ]"
                else:
                    S=" [.S-"+Pred_Pos[8]+Pred_Pos[9]+Arg0+" [.VP"+all_frag+" ]"+" ]"
            else:
                for frag in ordered_fragments:
                    all_frag=all_frag+frag[0]
                if not SYM=='':
                    S=" [.S-"+Pred_Pos[8]+Pred_Pos[9]+" [.VP"+all_frag+" ]"+" "+SYM+" ]"
                else:
                    S=" [.S-"+Pred_Pos[8]+Pred_Pos[9]+" [.VP"+all_frag+" ]"+" ]"
                    
        else:
            pred_terminal_nv={get.predicate()[4] : get.predicate()[2]}
            all_dict_frag_nv=dict(dict_frag.items()+pred_terminal_nv.items())
            all_dict_frag_nv=dict(dict_frag)
            all_dict_frag_nv.update(pred_terminal_nv)
            ordered_frag_nv=sorted(all_dict_frag_nv.items(), key=itemgetter(1))
            
            for frag in ordered_frag_nv:
                all_frag=all_frag+frag[0]
            all_frag=string.replace(all_frag, ' Label ', '')
            if not SYM=='':
                S=" [."+Pred_Pos+all_frag+" "+SYM+" ]"
            else:
                S=" [."+Pred_Pos+all_frag+" ]"

        return S


        
