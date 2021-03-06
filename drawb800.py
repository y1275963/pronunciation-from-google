#!/Users/y1275963/anaconda/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 13:36:10 2015

@author: y1275963

Get Barron 800's list and meaning
"""

import pickle 
import random
import sys
import os
import time
import subprocess
from datetime import date, timedelta
import datetime
import time
import numpy as np
import course_details

from matplotlib.pyplot import imshow
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import check
import time
import testfor
import v2a
        
class quer:
    def __init__(self,num):
        self.b800 = pickle.load(open('b800.pickle','rb'))
        self.p3000 = pickle.load(open('course_details.pickle','rb'))
        self.data = pickle.load(open('bigpool.pick','rb'))
        self.genq(num)
        print self.qpool,'\n'
        
#        self.joindata =  self.join()        

    def showimg(self,query):
        plt.ion()
        plt.show()
                    
        dirimage = [re for re in os.listdir('/Users/y1275963/Pictures/dicima') if re.startswith(query)]
        
        dirimage = dirimage[0:4]
        f1 = plt.figure()
        
        index = 0
        for index,item in enumerate(dirimage):
            try:
                f1.add_subplot(2,2,index)
                pil_im = Image.open('/Users/y1275963/Pictures/dicima/%s'%item, 'r')
                imshow(np.asarray(pil_im))
                time.sleep(0.05)
            except IOError,e:
                pass
                
    def study(self):
        self.spool = []
        for item in self.filelist:
            print self.spool
            self.spool.append(item)
            self.showimg(item)
            raw_input()
            print item
            subprocess.Popen(['afplay','/Users/y1275963/v2a/audio/'+item+'.mp3'])
            print item,' Dic, ', self.data[item]['exp']
            print item,' lon, ', check.checkwords(item)
            if len(self.spool)>=10:
                self.spool.reverse()
                self.test(self.spool)
    def test(self,qpool):
        
        while len(qpool) !=0 :
            start = time.time()
            
            qitem = qpool.pop()
            while self.data[qitem]['class'] == 'abandon':
                qitem = qpool.pop()
            
            self.showimg(qitem)


            print qitem
            subprocess.Popen(['afplay','/Users/y1275963/v2a/audio/'+qitem+'.mp3'])
            
            choices = self.genchoice(self.data[qitem]['exp'],[li for li in self.data],4)
            raw_input('think first')
            for index,item in enumerate(choices):
                print index+1,item
                
            sel = raw_input('You choices:\n')
            while str(sel) not in [str(x) for x in range(1,len(choices)+1)]+['a','q','d']:
                sel = raw_input('wrong input')
                
            end = time.time()
            timeuse = end - start
            
            
            
            if str(sel) == 'q':
                break
            elif str(sel) == 'a':
                self.data[qitem]['class'] ='abandon' 
                re = qitem
                
            elif str(sel) == 'd':
                print qitem ,"*****wrong,the right answer is:\n",self.data[qitem]['exp'],'\n'
                self.data[qitem]['wrong'].append([datetime.datetime.today(),timeuse,'No idea'])
                for i in range(random.randint(2,4)):
                    qpool.insert(random.randint(0,len(qpool)),qitem)
                re = raw_input('wait for review: ')
            else:
                if choices[int(sel)-1] == self.data[qitem]['exp']:
                    print qitem ,"passed\n"
                    self.data[qitem]['right'].append([datetime.datetime.today(),timeuse])
                    re = qitem
                else:
                    print qitem ,"*****wrong,the right answer is:\n",self.data[qitem]['exp'],'\n'
                    self.data[qitem]['wrong'].append([datetime.datetime.today(),timeuse,choices[int(sel)-1]])
                    for i in range(random.randint(2,4)):
                        qpool.insert(random.randint(0,len(qpool)),qitem)
                    re = raw_input('wait for review: ')
            while str(re).strip() != qitem:
                re = raw_input('wait for review: ')

            pickle.dump(self.data,open('bigpool.pick','wb'))
            pickle.dump(self.data,open(os.path.join('rec',time.strftime("%Y%m%d-%H%M%S")),'wb'))
         


        
    def join(self):
        #a4:
#    test = course_details.returndic('/Users/y1275963/v2a/check_a4','check_a4')
    
    #    return test
        pass
        
    def genq(self,num):
        b800 = [x for x in self.data if self.data[x]['class'] =='b800' ]
        # Untouthed 
        ut = [x for x in b800 if len(self.data[x]['right'])==0 and len(self.data[x]['wrong'])==0]
        
        yesterday = datetime.datetime.today() - timedelta(days = 1)
        today = datetime.datetime.today() -  timedelta(days = 0)
        
        right = [x for x in self.data if len(self.data[x]['right']) >0 ]
        wrong = [x for x in self.data if len(self.data[x]['wrong']) >0 ] # with wrong records
        
        notright = [x for x in b800 if len(self.data[x]['right'])==0]# Without right records
        # Yesterday wrong and today_wrong check the last recordes
        # [-1] : Check the last the recoddes, 0 : only concern the date wrong the time etc.
        yest_wrong = [x for x in wrong if sameday(self.data[x]['wrong'][-1][0],yesterday)]
        today_wrong = [x for x in wrong if sameday(self.data[x]['wrong'][-1][0],today)]
        
#        f_slow = lambda x: np.mean([x[-1] for x in tk.data[x]['right']])
#        # If the average response time is larger than %
#        av_slow = [x for x in right if f_slow(x) > self.getdraw(90) ]   
        
        last_slow = [x for x in right if self.data[x]['right'][-1][-1] > self.getdraw(70)]
        
        list_a4 = [x for x in self.data if self.data[x]['class'] == 'check_a4']
        
        #from list:
        if True:
            def fromlist(filename):
                with open(filename) as f:
                    lines = f.read().splitlines()
                    lines = [item.lower() for item in lines]
                    lines = [item for item in lines if not item.startswith('#')]
                return lines
                
            li = fromlist('/Users/y1275963/v2a/rev3_4')
            poollist = [x for x in self.data]
            
            filelist = list(set(li) & set(poollist))
            notinlist = list(set(li) - set(filelist))
            for item in notinlist:
                try:               
                    self.data[item] = {'class':'added','exp':check.checkwords(item),'right' : [],'wrong':[]}
                    print item
                except TypeError:
                    pass   
            pickle.dump(self.data,open('bigpool.pick','wb'))
            pickle.dump(self.data,open(os.path.join('rec',time.strftime("%Y%m%d-%H%M%S")),'wb'))                         
                
        p3000 = [x for x in self.data if self.data[x]['class'] =='p3000' ]  
        qpool = filelist
        self.filelist = li

        random.shuffle(qpool)
        
        
  #      for item in self.data :
#          if self.data[item]['class'] == 'p3000' and len(self.data[item]['wrong']) == 0 and len(self.data[item]['right']) == 0 and item in [x for x in self.p3000[34]]:
#          if self.data[item]['class'] =='b800' and len(self.data[item]['wrong']) == 0 and  len(self.data[item]['right']) == 0:
         #   if self.data[item]['class'] =='b800' and  len(self.data[item]['right'])==0 and len(self.data[item]['wrong'])== 0:
#                qpool.append(item)  
        
        self.poll = qpool
        
        if len(qpool) >num:
            self.qpool = list(random.sample(set(qpool),num))
        else:
            self.qpool = qpool
            
        # To avoid len(qpool) == 0:
        try:
            print "sample data: ",self.data[self.qpool[0]]
        except:
            pass

                    
        
    def genchoice(self,right,choicepool,num):
        choices = [right]
        while len(choices) != num:
            pick = random.choice(choicepool)
            pick = self.data[pick]['exp']
            if pick not in choices:
                choices.append(pick)
        random.shuffle(choices) 
        return choices
    
    def getdraw(self,perc):
        tk = self.data
        
        right_p = [tk[x]['right'] for x in tk if tk[x]['class']=='b800']
        wrong_p = [tk[x]['wrong'] for x in tk if tk[x]['class']=='b800']
        
    
        right = reduce(lambda x,y: x+y, right_p)
        wrong = reduce(lambda x,y:x+y, wrong_p)
    
        from matplotlib import pyplot
        #pyplot.scatter(range(len(right)),[x[-1] for x in right])
       # pyplot.scatter(range(len(wrong)),[x[1] for x in wrong])
        
        right_res = np.array([x[-1] for x in right])
        wrong_res = np.array([x[1] for x in wrong])
        return np.percentile(right_res, perc)
        
            
    
def quifind(data,query):
    tk = []
    for item in data:
        if len(data[item][query])>0:
            tk.append([item,data[item]])
    return tk
def quifind2(data,query):
    tk = []
    for item in data:
        if len(data[item]['right'])==0 and len(data[item]['wrong'])==0  and data[item]['class'] =='b800':
            tk.append([item,data[item]])
    return tk   
def getf(listl):
    tk = []
    for item in listl:
        tk.append(item[0])
    return tk
    
def chf(listl):
    for item in listl:
        if len(listl[item]['right']) != 0:
            for item2 in listl[item]['right']:
                item2[0] = parse(item2[0])
                print item2
                
def timetest(dic):
    yesterday = datetime.datetime.today() - timedelta(seconds = 7200)
    for item in dic:
        if dic[item]['wrong'] != []:
            if dic[item]['wrong'][-1][0] > yesterday:
                print item
                
def sameday(d1,d2):
    if d1.month == d2.month and d1.day == d2.day:
        return True
    else:
        return False
        

    


    
if __name__ == "__main__":
    tk = quer(25)
    print "a: abandon,q: quit, d:don't know"
#    tk.test()  
#    

    pool = tk.poll
    print len(pool)
    #tk.test(tk.qpool)
        