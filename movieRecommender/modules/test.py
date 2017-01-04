import numpy as np

a = np.random.rand(10,3)
i = np.array(range(10))
i = i.reshape(10,1)
a = np.concatenate((i,a),axis=1)
b = np.array([[1,4,5],[1,-1,1]]).T

#np.logical_or([a[:,0] == x for x in b[:,0]])
np.logical_or.reduce([a[:,0] == x for x in b[:,0]])
a[np.logical_or.reduce([a[:,0] == x for x in b[:,0]])]


#another method
@np.vectorize
def selected(elmt): return elmt in b[:,0]
r = a[selected(a[:, 0])]
#print r

m = np.concatenate((np.arange(10).reshape(10,1), np.random.rand(10).reshape(10,1)),axis=1)
print m
@np.vectorize
def myFunc(ele) :
    if ele >= 0.8 :
        return 1
    else :
        return 0 

#print myFunc(m[:,1])
print m[np.array([ x < 0.4 for x in m[:,1]])]