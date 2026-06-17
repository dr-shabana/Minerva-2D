cmake_minimum_required(VERSION 3.10)

# set the project name
project(minerva2d-apprun)

# add the executable
add_executable(AppRun main.c)
target_link_libraries(AppRun dl)
