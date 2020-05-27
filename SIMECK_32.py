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


#weightAND(0x80,0x1,0x80)


# In[5]:


#right circular shifts
def ROR(x,r):
    x = ((x << (SIMECK_TYPE - r)) + (x >> r)) & mask
    return x

#left circular shifts
def ROL(x,r):
    #print(hex(x),hex(x))
    x = ((x >> (SIMECK_TYPE - r)) + (x << r)) & mask
    #print(hex(x))
    return x


# In[6]:


#x=0x8000
#r=2
#ROL(x,r)


# In[7]:


#a=0x2
#b=0x82
#c=a^b
#print(hex(c))


# In[8]:


def find_diff_path(st1,st0,SIMECK_ROUNDS,n):
    lp=1             
    temp_wt=0
    tempdec_list=[]
    for i in range (0,SIMECK_ROUNDS):
        #print(hex(st1),hex(st0),hex(alpha),hex(beta))
        A=st1
        B=ROL(st1,beta)
        C=ROL(st1,gamma)
        #op=A^B
        wt=-200
        while(wt==-200):
            op=hw[random.randint(0,len(hw)-1)].dz
            #op=(random.randint(0,mask))
            wt,wt1=weightAND(A,B,op)
        D=op^C; E=st0^D
        #print(wt)
        
        tempdec_list.append(NMTS(st1,st0,op,wt)) 
        temp_wt= temp_wt+tempdec_list[i].wt
        
        #update state with new valid output differential
        st0=st1; st1=E
    n=n+1
    return tempdec_list, temp_wt, n

#if(len(ddt)!=0):
#            print(hex(st1),hex(st0))
#            index=(random.randint(0,len(ddt)-1))
#            temp_op=ddt[index].dz
#           temp_wt,temp_wt1=weightAND(A,B,temp_op)
#            if(temp_wt!=-200):
#                op=temp_op
#               wt,wt1=temp_wt,temp_wt1
#        else:


# In[9]:


def find_best_path(st1,st0, SIMECK_ROUNDS, wt_above, best_wt):
    #print(hex(st1),hex(st0))
    #print(hex(st1),hex(st0),'best_path')
    #using n as index value for list
    n=0
    for r in range(SIMECK_ROUNDS,0,-1):
        tempdec_list, temp_wt, n = find_diff_path(st1,st0,r, n)
        if((temp_wt+wt_above) < best_wt):
            best_wt= temp_wt+wt_above
            for i,j in zip(range(n-1,22), range(len(tempdec_list))):
                dec_list[i]=(NMTS(tempdec_list[j].dx,tempdec_list[j].dy,tempdec_list[j].dz,tempdec_list[j].wt))
        #print(n)
        if(n<SIMECK_ROUNDS):
            st1=dec_list[n].dx
            st0=dec_list[n].dy
        wt_above= wt_above+dec_list[n-1].wt
    return best_wt


# In[11]:


#alpha beta are for left and right circular shift  
import random
import math 
beta, gamma = 5,1
SIMECK_ROUNDS=11
SIMECK_TYPE=16
mask = 2 ** 16 - 1
wshift=15
dec_list=[0]*22
wt_above=0
best_wt=999
s=9999
class NMTS(object):
    """__init__() functions as the class constructor"""
    def __init__(self, dx=None, dy=None, dz=None, wt=None):
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.wt = wt
#highwaylist()
hw=[]
#nested loop to run number of time
highwaylist()
ch=0
while(best_wt>25):
    #print(hex(hw[ch].dx),hex(hw[ch].dy))
    best_wt=find_best_path(hw[ch].dx,hw[ch].dy,SIMECK_ROUNDS,wt_above,best_wt)
    ch=ch+1
    if(best_wt<s):
        s=best_wt
        print(s,ch)
        if(best_wt<33):
            print("Dec list is:")   
            for i in range(0,SIMECK_ROUNDS):    
                print(hex(dec_list[i].dx), hex(dec_list[i].dy),hex(dec_list[i].dz),(dec_list[i].wt))

print("Best weight is:",best_wt) 


# In[ ]:




