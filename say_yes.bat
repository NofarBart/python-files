@REM say yes for extracting frames for a single video (mini project)
@echo off

set arg1=%1
echo |set /p="yes" | python frames_from_mini_projects.py %arg1%