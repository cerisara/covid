import torch
import torch.nn as nn
import torch.nn.functional as F

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

