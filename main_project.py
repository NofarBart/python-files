'''
This file configures and trains a DeepLabCut network on a given video,
then analyzes the video and creates a labeled video output.
It uses napari for labeling frames, defines body parts and skeleton structure for tracking,
and sets various training parameters.
In the end, it calls the file "complete_network_code.py" to continue processing (using the new neuaral network created).
'''

import napari
import deeplabcut
import sys

ZERO = 0
ONE = 1
TWO = 2
DIS_ITERS = 10
SAVE_ITERS = 100
MAX_ITERS = 75000

shuffle = ONE # edit if needed; 1 is the default.
tracktype= 'ellipse' # box, skeleton, ellipse
VideoType = 'mp4' # mp4, MOV, or avi, whatever you uploaded!

# retrieve command-line arguments
path_config_file = sys.argv[ONE]
videofile_path  = sys.argv[TWO]

# modify the configuration
cfg = deeplabcut.auxiliaryfunctions.read_config(path_config_file)

# Define hierarchical structure for body parts
cfg["bodyparts"] = ["right_front",
    "right_front",
    "right_back",
    "right_back",
    "left_front",
    "left_front",
    "left_back",
    "left_back",
    "tail_base",
    "tail_upper",
    "tongue"]

cfg["skeleton"] = []

cfg['pcutoff']=0.4

cfg['batch_size']=4

# write the modified configuration back to the config file (cfg)
deeplabcut.auxiliaryfunctions.write_config(path_config_file, cfg)

with napari.gui_qt():
    deeplabcut.label_frames(path_config_file)

deeplabcut.check_labels(path_config_file)

deeplabcut.create_training_dataset(path_config_file, augmenter_type='imgaug')

# parameters for training
deeplabcut.train_network(path_config_file, shuffle=shuffle, displayiters=DIS_ITERS,saveiters=SAVE_ITERS, maxiters=MAX_ITERS)

# let's evaluate first
deeplabcut.evaluate_network(path_config_file, plotting=False)

# analyze the video
deeplabcut.analyze_videos(path_config_file,[videofile_path], videotype=VideoType)

# create labeled video (visualization of the tracked points according to requested parameters- cfg)
deeplabcut.create_labeled_video(path_config_file,[videofile_path])

print("finished main project file!")