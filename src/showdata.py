import corpus 

class NB:
    def findall(self,utt):
        self.u=utt
        self.nbs=[]
        i=0
        while i<len(utt):
            if utt[i].isdigit():
                for j in range(i+1,len(utt)):
                    if not utt[j].isdigit(): break
                self.nbs.append((i,j))
                i=j
            i+=1
            # TODO: handle negative numbers
        return len(self.nbs)

    def tostr(self):
        s=' '.join([self.u[a:b] for a,b in self.nbs])
        return s

    def onlydigits(self,cs,a,b):
        for c in self.u[a:b]:
            if c.isdigit(): continue
            if c in cs: continue
            return False
        return True

    def classif(self):
        self.typs=[]
        s=self.u
        i=0
        while i<len(self.nbs):
            a,b=self.nbs[i]

            # test for REF
            if s[a-1]=='[' or s[a-1]=='(':
                cl = ']' if s[a-1]=='[' else ')'
                # may be a reference
                if s[b]==cl: 
                    self.nbs[i]=(a-1,b+1)
                    self.typs.append(0)
                    i+=1
                    continue
                else:
                    k=s.find(cl,b+1)
                    if k>=0 and self.onlydigits(" ,",b+1,k):
                        self.typs.append(0)
                        todel=[]
                        for j in range(i+1,len(self.nbs)):
                            if self.nbs[j][1]>=k: break
                            todel.append(j)
                        todel=todel[::-1]
                        for j in todel: del self.nbs[j]
                        self.nbs[i]=(a-1,k+1)
                        i+=1
                        continue

            # test for URL
            j=s.rfind(' ',a)
            if j<0: j=0
            else: j+=1
            if s[j:j+4]=="http":
                print("OK")
                exit()
                self.typs.append(1)
                self.nbs[i]=(j,b)
                # TODO: merge URLs a posteriori
                i+=1
                continue

            self.typs.append(666)
            i+=1

    def showClass(self):
        typos={
                0:'ref',
                1:'url',
                666: 'UNK'
            }
        for i in range(len(self.nbs)):
            t = typos[self.typs[i]]
            a,b=self.nbs[i]
            print(t+"\t"+self.u[a:b])

nbs = NB()
for utts in corpus.loadData():
    # print(corpus.curfile+" "+str(len(utts)))
    for u in utts:
        n=nbs.findall(u)
        print(nbs.tostr())

