import torch
import torch.nn as nn
import torch.nn.functional as F
import string
import corpus
from showdata import NB

embdim=50
winlen=20
ndigs =10

class Mod(nn.Module):
    def __init__(self,nchars):
        super(Mod,self).__init__()
        self.e = nn.Embedding(nchars,embdim)
        self.lay1 = nn.Linear(embdim*winlen,100)
        self.lay2 = nn.Linear(100,100)
        self.lastlay = nn.Linear(100, 8*ndigs)

    def forward(self,x):
        # x = (batch,winlen)
        z = self.e(x)
        # z = (batch,winlen,embdim)
        z = z.view(-1,winlen*embdim)
        z = self.lay1(z)
        z = F.relu(z)
        z = self.lay2(z)
        z = F.relu(z)
        z = self.lastlay(z)
        z = z.view(-1,8,ndigs)
        return z

def get8digs(s):
    if len(s)==0||len(s)>8: return []
    r = []
    for c in s:
        r.append(ord(c)-ord('0'))
    r = [0]*8-len(s) + r
    return r

def train():
    nbs = NB()
    chars = string.printable
    nchars = len(chars)
    voc = {}
    for c in chars: voc[c]=len(voc)
    m = Mod(nchars)
    for utts in corpus.loadData():
        for u in utts:
            n=nbs.findall(u)
            if n>0:
                for a,b in nbs.nbs:
                    s=[]
                    i=1
                    while a-i>=0 and len(s)<winlen:
                        c=u[a-i]
                        if c in voc: s.append(voc[c])
                        i+=1
                    if len(s)==winlen:
                        goldy = get8digs(u[a,b])
                        x = torch.tensor(s)
                        x = x.view(1,winlen)
                        y = m(x)
                        print(y)
                        exit()

train()

