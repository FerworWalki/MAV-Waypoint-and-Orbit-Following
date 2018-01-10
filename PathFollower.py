from math import atan2
import numpy as np

from PathFollowerTypes import *
##TODO:
####add constrain for course_angle_of_line !!!!!!!!!!!!!!!!!

class PathFollowing(object):

    k_path = 0  #positive constant describing how fast transition from plane position to desired path will take
    return_angle = 0 #angle in RADIANS between north axis and line in which we will get back to desired path

    def __init__(self,k_path,return_angle): #class constructor, get path following params
        self.k_path = k_path                #set k_path value commanded while creating instance
        self.return_angle = return_angle    #set return angle value commanded while creating instance

    """
    StraightLineFollowing method, returns:
        -commanded angle in radians
        -commanded height
    As arguments it takes
        -r vector from coords system zero point to line path begining, typeof MAV_coords_sys
        -p vectir describing actual plane position in 3d space, typeof MAV_coords_sys
        -q unit length vector describing line direction (line which we want to follow) Pline(r,q)
        -actual_course_angle , actual course angle in RADIANS between north axis and actual plane moving direction,
        used in output angle constrain calculation
    """
    def StraigthLineFollowing(self,r,p,q,actual_course_angle):  
        """
        Calculating commanded course angle of plane
        """
        def CalculateAngle():
            print("\n----------Calcilating commanded angle----------")
            ####add constrain for course angle !!!!!!!!!!!!!!!!!
            course_angle_of_line = np.arctan2(q.e,q.n) #calculate course angle of line, formula (10.1)
            e_p = MAV_coords_sys(p.GetArray() - r.GetArray()) #calculate plane position error vector
            err_vec = GetStandingVector(e_p) #get standing vector from e_p (transpose)
            e_pi = Get_Ri(course_angle_of_line) * err_vec #transfrom e_p vector from internal frame to path frame
            print("path_error in path frame",e_pi)
            e_pi = MAV_coords_sys(e_pi) #convert np vector to MAV_coords_sys type
            print("course angle of line [deg]=", np.degrees(course_angle_of_line))
            #calculate commanded course angle in radians, using forumla 10.8
            commanded_course_angle = course_angle_of_line - (self.return_angle * 2* np.arctan(self.k_path * e_pi.e)/np.pi)
            print ("calculated commanded course angle [deg]",np.degrees(commanded_course_angle))
            print("----------Finished calcilating commanded angle----------\n")
            return commanded_course_angle #return method result in radians
        """
        Calculating commanded height of plane
        """
        def CalculateAltitude():
            print("\n----------Calcilating altitutde----------")
            e_p = p.GetArray() - r.GetArray() #calculate plane position vector
            print("e_p =",e_p)
            n = np.cross(q.GetArray(), np.array([0,0,1])) #calculate vector orthogonal to plane q-k
            n = n / np.linalg.norm(n)   #normalize vector vec/len(vec)
            print("n=", n)
            s = e_p - np.dot(e_p,n)*n   #calculating error vector projection to plane vertical containg vector q
            n = MAV_coords_sys(n)   #convert from np to MAV_coords_sys datatype
            s = MAV_coords_sys(s)   #convert from np to MAV_coords_sys datatype
            print("s=",s.GetArray())
            #calculate commanded height using formula (10.5)
            height = -r.d - (np.linalg.norm([s.n,s.e])*(q.d/np.linalg.norm([q.n,q.e]))) 
            print ("height",height)
            print("----------Finished calculating altitude----------\n")
            return height #return method result
        return CalculateAngle(), CalculateAltitude() #returns straight line following result


'''Create variables with path following parameters k_path and reaturn angle'''
KPath = 0.1
ReturnAngle = np.radians(50)

'''Instatniate path following objects with parameters in constructor'''
path_following = PathFollowing(KPath,ReturnAngle)
'''Create varables of type MAV_coords_sys storing n,e,d coords of vectors '''
r = MAV_coords_sys([1,1,1])     #vector from coords system zero point to start of straight line path
q = MAV_coords_sys( [2,2,2])    #unit vector describing straight line path direction according to north axis
p = MAV_coords_sys([3,3,3])     #actual plane position 
plane_course_angle = np.radians(6) #actual plane course angle
'''Call method calculating straight line following
variables of commanded course angle and desired height'''
course_angle, commanded_height = path_following.StraigthLineFollowing(r,p,q,plane_course_angle)





