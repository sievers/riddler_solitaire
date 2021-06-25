import numpy as np
N=10  #how many cards we're going to have, not counting the joker

#we'll encode the state of currently drawn cards with a number between 0 and 2**N-1,
#where the ith digit in binary is if we have drawn that card already

#given a number, convert to binary and sum 1 for the first digit (if non-zero), 2 for the second
#3 for the third digit etc.   for convenience/speed, use bit-shift and bit-and operators
def get_current_score(n):  
    score=0
    i=0
    while n>0:
        i=i+1
        score=score+(n&1)*i
        n=n>>1
    return score


#convert an integer index to an array holding its binary representation
def N2arr(n):
    vec=np.empty(N,dtype='int')
    for i in range(N):
        vec[i]=(n>>i)&1
    return vec

#convert a binary representation back to an integer
def arr2N(vec):
    tot=0
    for i in range(N):
        #tmp=vec[i]<<i
        #print(tmp)
        tot=tot+(vec[i]<<i)
    return tot


#get the expected score under optimal play.

def get_score(ind,dict):
    if ind in dict.keys():
        #if we already know our current score, return it.  Otherwise
        return dict[ind]
    else:
        #otherwise, find our expected store if we were to draw a new card.
        #we get that by summing over the expected value of all the child states,
        #and dividing by n_child+1, where the +1 is because we have a chance of 
        #drawing the joker.
        tot=0
        arr=N2arr(ind)
        tmp=arr.copy()
        nchild=0
        #loop over possible children and get their scores
        for i in range(N):
            tmp[:]=arr
            if tmp[i]==0:
                tmp[i]=1
                nn=arr2N(tmp)
                tot=tot+get_score(nn,dict)
                nchild=nchild+1
        new_score=tot/(nchild+1)  #this is the score we expect if we draw
        cur_score=get_current_score(ind)    #this is the score we expect if we sit pat
        if new_score>cur_score:   #pick the higher of the two and save it.
            dict[ind]=new_score
        else:
            dict[ind]=cur_score
        return dict[ind]         #now that we know our score, return it


mydict={}

#we know that if we have drawn all the non-joker cards, 
#it would be silly to draw another one.  This lets us get
#our state started.
mydict[2**N-1]=get_current_score(2**N-1)  

score=get_score(0,mydict)
print('score is ',score)
