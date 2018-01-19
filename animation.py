import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


plt.ion() #interactive mode
fig = plt.figure() #create new figure
fig_MAV = fig.add_subplot(111, projection='3d') #create new plot on which we will draw data

#show fullscreen#######################
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
plt.show()
#######################################

#describe 3d range of view [min,max]
view_limit_x = [-2,2]
view_limit_y = [-2,2]
view_limit_z = [0,6]

#define time of sleep between loops
sampling_time_s = 0.00001;
loop_iteriations = 60 #condition to exit while loop

"""
Drawing circle figure input parameters:
    -figure, figure to draw on (matplotlib.pyplot)
    -radius of circle
    -vector describing center of vector, type of list
"""
def DrawCircle(figure,radius,center):
    theta = np.linspace(-np.pi, np.pi, 200)
    circle_x = np.sin(theta) * radius + center[0]
    circle_y = np.cos(theta) * radius + center[1]
    circle_z = np.repeat(np.array([center[2]]), 200)
    figure.plot(circle_x,circle_y,circle_z) #plotting circle


"""
Drawing 3d line, input arguments:
    -figure, figure to draw on (matplotlib.pyplot)
    -begining , 3d vec typeof list, begining of line
    -unit_vector, 3d vec typeof list, description of line direction
    -length of line
"""
def DrawLine(figure,begining,unit_vector, length = 100):
    point = np.linspace(0, 0.1, 1000)


    xx = np.repeat(np.array([begining[0]]), 1000)
    x = xx + point * unit_vector[0] * length

    yy = np.repeat(np.array([begining[1]]), 1000)
    y = yy + point * unit_vector[1] * length

    zz = np.repeat(np.array([begining[2]]), 1000)
    z = zz + point * unit_vector[2] * length
    figure.plot(x,y,z) #plotting line

def CreateFigure(figure,lim_x,lim_y,lim_z,name_x,name_y,name_z):
    figure.set_xlim(lim_x)
    figure.set_ylim(lim_y)
    figure.set_zlim(lim_z)
    figure.set_xlabel(name_x)
    figure.set_ylabel(name_y)
    figure.set_zlabel(name_z)


"""
Drawing one quiver arrow:
    -figure, figure to draw on (matplotlib.pyplot)
    -plane_position - 3d position vec typeof array
    -commanded_course - is commanded course angle in radians
    -commanded_height
"""
def DrawMAV(figure,plane_position,commanded_course,commanded_height):
    north = np.tan(commanded_course);
    east = np.cos(commanded_course) * np.sqrt(2)
    figure.quiver(plane_position[0], plane_position[1], plane_position[2], east, north, commanded_height, length=1, normalize=True)

def DrawMAV2(figure,plane_position,plane_position_old):
    east = plane_position[0] - plane_position_old[0]
    north = plane_position[1] - plane_position_old[1]
    down = plane_position[2] - plane_position_old[2]
    figure.quiver(plane_position[0], plane_position[1], plane_position[2], east, north, down, length=0.5, normalize=True,color='r')
    

    
"""
Create status string input arguments:
    -plane_pos - actual plane position list xyz
    -course_angle- actual course angle of plane in radians
    -star_of_line- point of line begining , list xyz coords
    -dir_of_lie - unit vector (list xyz) describing commanded line direction
    -orbit_center- center of commanded orbit (list xyz coords)
    -orbit_radius - commanded radius of followed circle (scalar variable)
    -commanded_course - commanded course angle in radias
    -commended_height - commanded height of plane
    -rp = floating point variables rounding parameter 
"""
def ComposeStatusString(plane_pos= [7,7,7],course_angle = 0.3,start_of_line = [1,2,3],dir_of_line = [6,6,6],orbit_center = [1,2,3],orbit_radius = 0.55, commanded_course = 0.3,commanded_height = 1,rp = 3):
    output_string = 'Act MAV pos: ' + str([  round(plane_pos[0],rp), round(plane_pos[1],rp), round(plane_pos[2],rp)  ]) + \
                    '\nAct course [deg]: ' + str(round(   np.degrees(course_angle), rp)) + \
                    '\nStart of line: ' + str([  round(start_of_line[0],rp), round(start_of_line[1],rp), round(start_of_line[2],rp)  ]) + \
                    '\nDir of line: ' + str([  round(dir_of_line[0],rp), round(dir_of_line[1],rp), round(dir_of_line[2],rp)  ]) + \
                    '\nOrbit center: ' + str([  round(orbit_center[0],rp), round(orbit_center[1],rp), round(orbit_center[2],rp)  ]) + \
                    '\nOrbit radius: ' + str(round(orbit_radius, rp)) + \
                    '\nCommanded course [deg] : ' + str(round(   np.degrees(commanded_course), rp)) + \
                    '\nCommanded height: ' + str(round(commanded_height, rp))
    return output_string

"""
Drawing last positions of plane (condensation streak)
    -figure where to draw
    -plane_pos acutal plane pos
    -frames_memory how many frames remember
"""
def DrawMAVPath(figure,plane_pos,frames_memory):
        if len(x_path) < frames_memory:
            x_path.append(plane_pos[0])
            #print("\nx_path_drawmav",x_path)
            y_path.append(plane_pos[1])
            z_path.append(plane_pos[2])
        else:
            
            del x_path[0]
            del y_path[0]
            del z_path[0]
            x_path.append(plane_pos[0])
            y_path.append(plane_pos[1])
            z_path.append(plane_pos[2])
            #print("\nx_path_drawmav",x_path)
        figure.plot(x_path,y_path,z_path)

#create temporary data lists for xyz axes
x_path = []
y_path = []
z_path = []

i = 0
j = 0 # loop iterations counter 

#infinite loop

while(j <= loop_iteriations):
	try:
		j = j + 1.0
		i = i +0.1
		xx = np.cos(np.degrees(j))
		yy = np.sin(np.degrees(j))
		zz = i

		xx_old = np.cos(np.degrees(j -1))
		yy_old = np.sin(np.degrees(j -1))
		zz_old = i - 0.1

		
		CreateFigure(fig_MAV,view_limit_x,view_limit_y,view_limit_z,'East (x)','North (y)','Down (z)')

		DrawMAV2(fig_MAV,[xx,yy,zz],[xx_old,yy_old,zz_old])
		DrawMAVPath(fig_MAV,[xx,yy,zz],25)

		
		DrawLine(fig_MAV,[2,-2,4],[0.2,0.3,0.5],50)
		DrawCircle(fig_MAV,1,[0,0,0])

		fig_MAV.text(view_limit_x[0],view_limit_y[0],view_limit_z[0],ComposeStatusString([xx,yy,zz],0,[0,0,0],[0.2,0.3,0.5],[0,0,0],1,0,0))

		plt.show()
		plt.pause(sampling_time_s)
		fig_MAV.cla()



	except:
		print("interrupted")
		exit(1)

CreateFigure(fig_MAV,view_limit_x,view_limit_y,view_limit_z,'East (x)','North (y)','Down (z)')

#DrawMAV(fig_MAV,[xx,yy,zz],np.degrees(90),i)
DrawMAV2(fig_MAV,[xx,yy,zz],[xx_old,yy_old,zz_old])
DrawMAVPath(fig_MAV,[xx,yy,zz],25)


DrawLine(fig_MAV,[2,-2,4],[0.2,0.3,0.5],50)
DrawCircle(fig_MAV,1,[0,0,0])

fig_MAV.text(view_limit_x[0],view_limit_y[0],view_limit_z[0],ComposeStatusString([xx,yy,zz],0,[0,0,0],[0.2,0.3,0.5],[0,0,0],1,0,0))






"""
CreateFigure(fig_MAV,view_limit_x,view_limit_y,view_limit_z,'East (x)','North (y)','Down (z)')
DrawMAV(fig_MAV,[i,i,i],np.radians(90*i),i)
DrawLine(fig_MAV,[0,0,0],[0,0,1],50)
DrawCircle(fig_MAV,1,[1,1,1])
DrawMAVPath(fig_MAV,[i,i,i],50)
fig_MAV.text(view_limit_x[0],view_limit_y[0],view_limit_z[0],ComposeStatusString([i,i,i]))
plt.draw()










while(i <= loop_iteriations):
	try:
		j = j + 1.0
		i = i +0.1
		xx = np.cos(np.degrees(j))
		yy = np.sin(np.degrees(j))
		zz = i

		xx_old = np.cos(np.degrees(j -1))
		yy_old = np.sin(np.degrees(j -1))
		zz_old = i - 0.1
		CreateFigure(fig_MAV,view_limit_x,view_limit_y,view_limit_z,'East (x)','North (y)','Down (z)')

		#DrawMAV(fig_MAV,[xx,yy,zz],np.degrees(90),i)
		DrawMAV2(fig_MAV,[xx,yy,zz],[xx_old,yy_old,zz_old])
		DrawMAVPath(fig_MAV,[xx,yy,zz],50)

		
		DrawLine(fig_MAV,[0,0,0],[0,0,1],50)
		DrawCircle(fig_MAV,1,[1,1,1])

		fig_MAV.text(view_limit_x[0],view_limit_y[0],view_limit_z[0],ComposeStatusString([i,i,i]))

		plt.show()
		plt.pause(sampling_time_s)
		fig_MAV.cla()



	except:
		print("interrupted")
		exit(1)
"""
