#!/Users/y1275963/anaconda/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:36:10 2015

@author: y1275963

Get Barron 800's list and meaning
"""

import getlist
import pickle 
import random

def geterate_pickel():
    baseurl = 'http://www.memrise.com/course/121215/barrons-800-essential-word-list-gre/'
    
    base = {}
    for i in range(1,81):
        print i
        url = baseurl + str(i)
        dic = getlist.getdic(url)
        real_dic = {v: k for k, v in dic.items()}
        base[i] = real_dic
        
    pickle.dump(base, open('b800.pickle','wb'))
    return base
    
def dump(passed,nonepassed):
    pickle.dump(passed,open('b800passed','wb'))
    pickle.dump(nonepassed,open('b800nonepassed','wb'))
    
def read():
    ped = pickle.load(open('b800passed','rb'))
    nonepede = pickle.load(open('b800nonepassed','rb'))
    return ped,nonepede
    
    
if __name__ == "__main__":
    dic = pickle.load(open('b800.pickle','rb'))
    passed,nonepassed = read()
    
    all_dic = {}
    for i in range(1,4):
        all_dic.update(dic[i])
    
    dicpool = all_dic
    
    for qitem in dicpool:
        
        if qitem in passed:
            pass
        else:
            
            print qitem
            # Get the choice:
            choices = [dicpool[qitem]]
            
            while len(choices) != 4:
                pick = random.choice(dicpool.values())
                if pick not in choices:
                    choices.append(pick)
            random.shuffle(choices)
            for index,item in enumerate(choices):
                print index+1,item
                
            # prompt input:
            sel = raw_input('You choices:\n')
            if str(sel) == 'n':
                break
            else: 
                if choices[int(sel)-1] == dicpool[qitem]:
                    print qitem ,"passed\n"
                    passed.append(qitem)
                else:
                    print qitem ,"*****wrong,the right answer is:\n",dicpool[qitem],'\n'
                    nonepassed.append(qitem)
                
                dump(passed,nonepassed)
            
        

        
    
    
        
     