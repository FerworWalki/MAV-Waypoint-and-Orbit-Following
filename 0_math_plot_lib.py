from mpl_toolkits.mplot3d import axes3d
from math import atan2
import matplotlib.pyplot as plt
import numpy as np


##TYPES####################################
""" path_origin- origin of path
    path_origin.n - north coordinate
    path_origin.e - east coordinate
    path_origin.d - down coordinate
"""
class path_origin(object):
    n = 0.0
    e = 0.0
    d = 0.0

    def __init__(self, l=[]):
        self.n = l[0]
        self.e = l[1]
        self.d = l[2]
    def GetList(self):
        return [self.n, self.e, self.d]
        
""" dir_vec - vector describing direction of travel (must be unit vector)
    q.n - north coordinate
    q.e - east coordinate
    q.d - down coordinate
"""
class dir_vec(object):
    n = 0.0
    e = 0.0
    d = 0.0

    def __init__(self, l=[]):
        self.n = l[0]
        self.e = l[1]
        self.d = l[2]

    def GetList(self):
        return [self.n, self.e, self.d]
        
###########################################
        
##METHODS##################################
        
def CalculateCourseAngle(qe,qn): #return atan2 in radians
    return atan2(qe,qn)

def NormalizeVector(x,y,z): #returns list [x,y,z] of normalized vector
    vec = np.array([x,y,z])
    vec_length = np.linalg.norm(vec)

    x_out = vec[0]/vec_length
    y_out = vec[1]/vec_length
    z_out = vec[2]/vec_length

    return [x_out, y_out, z_out]


###########################################
q  = dir_vec(NormalizeVector(2,3,1)) 
print (q.GetList())
print (q.n)
print (q.e)
print (q.d)


fig = plt.figure()
ax= fig.add_subplot(111,projection='3d')
x,y,z = axes3d.get_test_data(0.05)
ax.plot_wireframe(x,y,z, rstride =10, cstride=10)
plt.show()

"""print (CalculateCourseAngle(1,2))
q  = dir_vec(NormalizeVector(2,3,1))
print (q.d)
normalized = NormalizeVector(2,3,1)
print ("normalized", normalized)
"""




