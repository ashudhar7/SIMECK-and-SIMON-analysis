#!/usr/bin/env python
# coding: utf-8

# In[1]:


def highwaylist():
    alph,bet,gam,pro = [],[],[],[]
    with open('alph.txt') as ip1, open('bet.txt') as ip2, open('gam.txt') as ip3, open('pro.txt') as ip4:
        for i1,i2,i3,i4 in zip(ip1,ip2,ip3,ip4):
            hw.append(NMTS(int(i1.strip()),int(i2.strip()),int(i3.strip()),float(i4.strip()))) 


# In[2]:


def mask_1(a,b,wshift):
    s1=0
    var=0
    while(s1==0):
        a1=(a<<(wshift))&mask
        b1=(b<<(wshift))&mask
        s1=a1+b1
        if(s1==0):
            var=var+1
        wshift=wshift-1
        mask1=(mask<<var)&mask
    return mask1


# In[3]:


import math
def weightAND(alpha1,beta1,gamma1): 
    s=(gamma1&(~(alpha1^beta1)))&mask
    temp=bin((alpha1^beta1)&mask)
    wt=(temp[1:].count("1"))
    if(s!=0):        
        return -200,200
    else:
        return wt,math.pow(2,-wt)


# In[4]:


#weight1(0,2147483648,2147483648)


# In[5]:


#right circular shifts
def ROR(x,r):
    x = ((x << (SIMON_TYPE - r)) + (x >> r)) & mask
    return x

#left circular shifts
def ROL(x,r):
    x = ((x >> (SIMON_TYPE - r)) + (x << r)) & mask
    return x


# In[6]:


def find_diff_path_rev(st1,st0,SIMON_ROUNDS, n):
    lp=1             
    temp_wt=0
    tempdec_list=[]
    for i in range (0,SIMON_ROUNDS):
        #print(hex(st1),hex(st0))
        inp1=st1;inp0=st0
        tempst0=st0;st0=st1; st1=tempst0
        
        B=ROL(st1,beta)
        C=ROL(st1,gamma)
        #op=A^B
        wt=-200
        while(wt==-200):
            op=hw[random.randint(0,len(hw)-1)].dz
            #op=(random.randint(0,mask))
            wt,wt1=weightAND(st1,B,op)
        D=op^C; E=st0^D; st0=E
        #print(hex(st0))
        
        #tempdec_list.append(NMTS(st1,st0,op,wt)) 
        tempdec_list.append(NMTS(inp1,inp0,op,wt))
        temp_wt= temp_wt+tempdec_list[i].wt
    n=n+1
    return tempdec_list, temp_wt, n


# In[7]:


def find_diff_path(st1,st0,SIMON_ROUNDS,n):
    lp=1             
    temp_wt=0
    tempdec_list=[]
    for i in range (0,SIMON_ROUNDS):
        #print(hex(st1),hex(st0),hex(alpha),hex(beta))
        #A=ROL(st1,alpha)
        B=ROL(st1,beta)
        C=ROL(st1,gamma)
        #op=A^B
        wt=-200
        while(wt==-200):
            op=hw[random.randint(0,len(hw)-1)].dz
            #op=(random.randint(0,mask))
            wt,wt1=weightAND(st1,B,op)
        D=op^C; E=st0^D
        #print(wt)
        
        tempdec_list.append(NMTS(st1,st0,op,wt)) 
        temp_wt= temp_wt+tempdec_list[i].wt
        
        #update state with new valid output differential
        st0=st1; st1=E
    n=n+1
    return tempdec_list, temp_wt, n


# In[8]:


def find_best_path(st1,st0, SIMON_ROUNDS, wt_above, best_wt):
    #using n as index value for list
    n=0
    for r in range(SIMON_ROUNDS,0,-1):
        tempdec_list, temp_wt, n = find_diff_path(st1,st0,r, n)
        if((temp_wt+wt_above) < best_wt):
            best_wt= temp_wt+wt_above
            for i,j in zip(range(n-1,SIMON_ROUNDS), range(len(tempdec_list))):
                dec_list[i]=(NMTS(tempdec_list[j].dx,tempdec_list[j].dy,tempdec_list[j].dz,tempdec_list[j].wt))
        if(n<SIMON_ROUNDS):
            st1=dec_list[n].dx
            st0=dec_list[n].dy
        wt_above= wt_above+dec_list[n-1].wt    
    return best_wt


# In[9]:


def find_best_path_rev(st1,st0, SIMON_ROUNDS, wt_above, best_wt):
    #using n as index value for list
    n=0
    for r in range(SIMON_ROUNDS,0,-1):
        tempdec_list, temp_wt, n = find_diff_path_rev(st1,st0,r, n)
        if((temp_wt+wt_above) < best_wt):
            best_wt= temp_wt+wt_above
            for i,j in zip(range(n-1,SIMON_ROUNDS), range(len(tempdec_list))):
                dec_list_rev[i]=(NMTS(tempdec_list[j].dx,tempdec_list[j].dy,tempdec_list[j].dz,tempdec_list[j].wt))
        if(n<SIMON_ROUNDS):
            st1=dec_list_rev[n].dx
            st0=dec_list_rev[n].dy
        wt_above= wt_above+dec_list_rev[n-1].wt    
    return best_wt


# In[ ]:


import random
import math
#alpha beta are for left and right circular shift     
beta, gamma = 5,1
SIMON_ROUNDS=12
SIMON_TYPE=32
mask = 2 ** 32 - 1
wshift=31
#wt_above=0
#wt_above_rev=0
#best_wt=999
#best_wt_rev=999
bw=999
s=9999
hw=[]

class NMTS(object):
    """__init__() functions as the class constructor"""
    def __init__(self, dx=None, dy=None, dz=None, wt=None):
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.wt = wt
        
highwaylist()
for ch in range(1,len(hw)-1):
    dec_list=[0]*SIMON_ROUNDS
    dec_list_rev=[0]*SIMON_ROUNDS
    wt_above=0
    wt_above_rev=0
    best_wt=500
    best_wt_rev=500
    count=0  
    #print(ch,ch,ch)
    while(bw>21):
        #ch=random.randint(0,len(hw)-1)
        st1=hw[ch].dx
        st0=hw[ch].dy
        SIMONROUNDS=7
        best_wt=find_best_path(st1,st0,SIMONROUNDS,wt_above,best_wt)
        count=count+1
        if(count>20):
            break
        SIMONROUNDS_rev=5
        st1=hw[ch].dx
        st0=hw[ch].dy
        #ch=ch+1
        best_wt_rev=find_best_path_rev(st1,st0,SIMONROUNDS_rev,wt_above,best_wt_rev)
        bw=best_wt+best_wt_rev
        if(bw<s):
            s=bw
            print(s,ch)
            print("Dec list is in reverse:")   
            for i in range(SIMONROUNDS_rev-1,-1,-1):    
                print("Starting input of %i round and weight:" %i,hex(dec_list_rev[i].dx),hex(dec_list_rev[i].dy),hex(dec_list_rev[i].dz),(dec_list_rev[i].wt))

            print("Dec list is:")   
            for i in range(0,SIMONROUNDS):    
                print("Starting input of %i round and weight:" %i,hex(dec_list[i].dx), hex(dec_list[i].dy),hex(dec_list[i].dz),(dec_list[i].wt))
            print("Best weight is:",bw)
    


# In[ ]:




