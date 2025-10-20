''' 
This file works between the "mini_projects.py" and "say_yes.bat".
The goal is to automate the "deeplabcut.extract_frames" that demands yes typing from the user.
The function gets "path_config_file" for each mini project (contains one video),
(the configuration contains the video's path and number of frames to extract)
and calls "deeplabcut.extract_frames". 
'''

import sys
import deeplabcut

def main(path_config_file):
    deeplabcut.extract_frames(path_config_file, 'automatic', 'kmeans')

if __name__ == "__main__":
    # check if the script is being run from the command line
    if len(sys.argv) > 1:
        # get the path_config_file argument from the command line
        path_config_file = sys.argv[1]
        # call the main function with the provided argument
        main(path_config_file)
    else:
        print("Usage: python script.py path_to_config_file.yaml")