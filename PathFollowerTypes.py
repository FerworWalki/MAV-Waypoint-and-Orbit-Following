import numpy as np
###################--DATA_TYPES--################
""" Describing MAV coordinate system
    .n - north coordinate (x)
    .e - east coordinate (y)
    .d - down coordinate (-z)
"""
class MAV_coords_sys(object): #vector r
    n = None
    e = None
    d = None

    def __init__(self, l=[]):
        self.n = l[0]
        self.e = l[1]
        self.d = l[2]
    def GetList(self):
        return [self.n, self.e, self.d]
    def GetArray(self):
        return np.array([self.n, self.e, self.d])
    
###################--METHODS--################
        
'''Returns rotation matrix, input argument - angle in radians
    Create right handed coordinate system'''
def Get_Ri(input_radians):
    rot_angle = input_radians
    c = np.cos(rot_angle)
    s = np.sin(rot_angle)
    rot_matrix = np.matrix('{} {} {}; \
			    {} {} {}; \
			    {} {} {}'.format( c , s , 0 ,
                                             -s , c , 0 ,
                                              0 , 0 , 1 ))
    return rot_matrix

'''Return standing vector, from object
    type MAV_coords_sys'''
def GetStandingVector(vector):
    return np.matrix('  {}; \
                        {} ; \
                        {} '.format( vector.n, vector.e,vector.d ))

'''Calculates angle contrain in/out in radians'''
def CalculateAngleConstrain(output_angle,actual_angle):
    while output_angle - actual_angle < -np.pi:
        output_angle = output_angle + 2 * np.pi
    while output_angle - actual_angle > np.pi:
        output_angle = output_angle - 2 * np.pi
    return output_angle
