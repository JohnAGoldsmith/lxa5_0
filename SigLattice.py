from operator import itemgetter

def sigListToString(sigList):
	sigList.sort()
	return "=".join(sigList)

class SigLattice:
    def __init__(self):
		self.m_siglist = list()
		self.m_sigcount = dict()
    def add(self,signature,count =1):
        if len(signature) < 1:
            return
        sig = sigListToString(signature)
        if signature not in self.m_siglist:
			self.m_siglist.append(signature)
			self.m_sigcount[sig] = count
        else:
            self.m_sigcount[sig] += count
    def count(sig):
            if sig in self.m_sigcount:
                return self.m_sigcount[sig]
            else:
                return 0
    def deposit(self,signature):
		#print ("sig lattice" , signature)
        MAXIMUM_COUNT = 10
        sig = sigListToString(signature)
        if sig not in self.m_sigcount:
            self.m_sigcount[sig] = 1
        if self.m_sigcount[sig] < MAXIMUM_COUNT:
            self.m_sigcount[sig] += 1
        else:
            return
        if len(signature) == 1:
			return
        self.add(signature)
        for i in range(len(signature)):
			newSig = list(signature)
			del newSig[i]
			self.deposit(newSig)
        self.lattice_sort()
		#print ("sig lattice height" , len(self.m_siglist))
    def lattice_sort(self):
		self.m_siglist.sort(key="".join )
		self.m_siglist.sort(key = len,reverse=True)
    def latticeCount(self):
		return len(self.m_siglist)
    def lattice_print(self):
		for i in range(len(self.m_siglist)):
			sig = sigListToString(self.m_siglist[i])
			print (i, self.m_siglist[i], self.m_sigcount[sig])
