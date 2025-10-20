# DeepBrain python files (creating a new neural network)

## Description
This repository contains code files for creating a new analyzing mouse movement using machine learning `DeepLabCut` and the `dlc2kinematics` libraries.  
You may find more python files for using an existing neural network inside the repository `deepbrainproject`[https://github.com/NofarBart/deepbrainproject].

---

## Repository Structure

```
deeplabcut_python/
│
├── videos/ # contains example video(s) for analysis
│ └── vid11.mp4 # the original video- mouse running on a wheel
│ └── vid11DLC_resnet50_ExampleMay21shuffle1_19800_labeled.mp4 # demonstration of the NN output
├── docs/ # documentation
│ └── Deepbrain hebrew manual.pdf -> # files explained in pages 10-14, system is also explained in other pages
├── analyze.py
├── complete_network_code.py
├── frames_from_mini_projects.py
├── main_project.py
├── mini_projects.py
├── say_yes.bat
├── time_in_each_roi.py
└── README.md # This file

```