# run on new video
'''
This file calculates (time) beginning and end of average movement in a given video,
of selected bodypart, in x or y.
It uses the fps parameter and dlc2kinematics library to extract velocities (speed with directions)
and determain wheter there was movement.
Positive velocities meaning the mouse run (in x) and negative that it stopped (the wheel is moving but mouse isn't
or at least that the leg if chosen is finishing movement- is moving back).
It visualizes the movement path of the mouse in the video,
plotting segments of movement between start and end points in different colors.
(Moving leg up in one color, dragging the leg on the surface of the wheel in another color).
'''
import deeplabcut
import dlc2kinematics
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import os
import numpy as np
import time_in_each_roi

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# constants
ZERO = 0
ONE = 1
TWO = 2
THREE = 3
END = 100 # end of frames in x (in graph) 
THRESHOLD = 50
shuffle = ONE
VideoType = 'mp4'


# path to the video file
video_path = "D:\\testing_videos_new\\vid2.mp4"
config = 'C:\Experiment16-Tester16-2024-02-21\config.yaml'
h5 = 'C:\\current\\Test_Blue_2024-03-27-124054-0000DLC_resnet50_Experiment11Mar25shuffle1_72600.h5'

df, bodyparts, scorer = dlc2kinematics.load_data(h5)


bpt='right_front_Z'

df_vel = dlc2kinematics.compute_velocity(df,bodyparts=['all'], filter_window=THREE, order=ONE)
df_speed = dlc2kinematics.compute_speed(df,bodyparts=[bpt], filter_window=THREE, order=ONE)


df_vel_bodypart = dlc2kinematics.compute_velocity(df,bodyparts=[bpt], filter_window=THREE, order=ONE)
df_vel_bodypart

# compute the average of 'x' values
average_x = df[scorer][bpt]['x'].median()
# compute the average of 'x' values
average_y = df[scorer][bpt]['y'].median()

# print the average
print("Average of 'x' values:", average_x)
# print the average
print("Average of 'y' values:", average_y)

for index, value in df_vel_bodypart[(scorer, bpt, 'x')].items():
# apply the condition to set the values in df[scorer][bpt] to zero based on velocity criteria
    if (df_vel_bodypart.loc[index, (scorer, bpt, 'x')] > 30) or (df_vel_bodypart.loc[index, (scorer, bpt, 'x')] < -30):
        df_vel_bodypart.loc[index, (scorer, bpt, 'x')] = 0
        df_vel_bodypart.loc[index, (scorer, bpt, 'y')] = 0
    if (df_vel_bodypart.loc[index, (scorer, bpt, 'y')] > 50) or (df_vel_bodypart.loc[index, (scorer, bpt, 'y')] < -50):
        df_vel_bodypart.loc[index, (scorer, bpt, 'x')] = 0
        df_vel_bodypart.loc[index, (scorer, bpt, 'y')] = 0
        # df.loc[index, (scorer, bpt, 'x')] = 200
for index, value in df[scorer][bpt]['x'].items():
# apply the condition to set the values in df[scorer][bpt] to zero based on velocity criteria
    if ((df.loc[index, (scorer, bpt, 'x')] > 330)):
        if (index > 2):
            df.loc[index, (scorer, bpt, 'x')] = df.loc[index - 2, (scorer, bpt, 'x')]
            df.loc[index, (scorer, bpt, 'y')] = df.loc[index - 2, (scorer, bpt, 'y')]

print(df[scorer][bpt])

dlc2kinematics.plot_velocity(df[scorer][bpt], df_vel_bodypart)

# let's calculate velocity of the snout

vel = time_in_each_roi.calc_distance_between_points_in_a_vector_2d(np.vstack([df[scorer][bpt]['x'].values.flatten(), df[scorer][bpt]['y'].values.flatten()]).T)

fps=120 # frame rate of camera in those experiments
time=np.arange(len(vel))*1./fps
vel=vel #notice the units of vel are relative pixel distance [per time step]

# store in other variables:
xleg=df[scorer][bpt]['x'].values
yleg=df[scorer][bpt]['y'].values
vleg=vel
plt.plot(time,vel*1./fps)
plt.title('Speed in pixels over time')
plt.xlabel('Time in seconds')
plt.ylabel('Speed in pixels per second')
plt.show()


velocity_values = df_vel_bodypart[(scorer, bpt, 'x')]
prev_value = velocity_values[ZERO]
frame_start = ZERO
frame_end = ZERO
flag = ZERO
color_forwards = iter(cm.BuGn(np.linspace(0,1,len(velocity_values))))
color_backwards = iter(cm.OrRd(np.linspace(0,1,len(velocity_values))))

# go over the velocities, check if reaches zero:
for index, value in velocity_values.items():
    c_f = next(color_forwards)
    c_b = next(color_backwards)
    # check if the value is higher than zero and is the first nan-negative value (starting movement)
    if (value > prev_value and value >= ZERO and prev_value < ZERO):
        frame_start = index


        # if movement ended, plot the end of the prev. movement as the start of the new
        # when flag is one or (frame_start - frame_end) is smaller than 5 it is a noise (false movement) 
        if (frame_end != ZERO and (frame_start - frame_end) > 5 and flag == ZERO):
            # Plot the end of the movement
            plt.plot(df[scorer][bpt]['x'][frame_end:frame_start - 3], -df[scorer][bpt]['y'][frame_end:frame_start - 3], color = c_b)
    # define as false movement 
    if ((index - frame_start) <= 5):
        flag = ONE


    # check if the value is smaller than zero and is the first nan-positive value (ending movement)
    elif (value < prev_value and value <= ZERO and prev_value > ZERO):
        flag = ZERO
        frame_end = index


    if (frame_start < frame_end):
       
        ## plt.plot(x, y, c=c)
        # Plot the start of the movement
        # c=next(color) #Change colour for each line in plot
        plt.plot(df[scorer][bpt]['x'][frame_start:frame_end], -df[scorer][bpt]['y'][frame_start:frame_end], color=c_f)
    prev_value = value
plt.title("Walking pattern of the mouse")
plt.xlabel("x location [AU]")
plt.ylabel("y location [AU]")
plt.show()