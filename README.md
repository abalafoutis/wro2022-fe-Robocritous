Engineering materials
====

This repository contains engineering materials of a self-driven vehicle's model participating in the WRO Future Engineers competition in the season 2022.

## Content

* `t-photos` contains 2 photos of the team (an official one and one funny photo with all team members)
* `v-photos` contains 6 photos of the vehicle (from every side, from top and bottom)
* `video` contains the video.md file with the link to a video where driving demonstration exists
* `schemes` contains one or several schematic diagrams in form of JPEG, PNG or PDF of the electromechanical components illustrating all the elements (electronic components and motors) used in the vehicle and how they connect to each other.
* `src` contains code of control software for all components which were programmed to participate in the competition
* `models` contains files for the models used by our 3D printer.

## Introduction

Our robot uses the NVIDIA Jetson Nano as a main controller. It takes as input only the image from a web camera and a program written in Python decides for the rotation angle of a servo motor (for turning) and the rotation speed of a DC motor (for controlling the speed). We have also used an on-off switch for powering the main controller and a push button for executing our main program.

## Qualification Round

`main.py` is the main program on Jetson Nano for the first round of the competition. After it gets the image from camera, it cuts out 3 areas on it, 1 on the right side, 1 on the left, and at the bottom. The program converts them from the bgr color model to hsv, and findes the needed items on it. The ones on the left and right are used to detect the walls. After detection, it uses the proportional-derivative controller to help robot move in the center between 2 walls. Then if we see 1 wall, and don't see the other, the robot starts to turn. The part at the bottom is used to count lines, that we have passed. When the robot passes 12 lines, it stops. ![image](https://user-images.githubusercontent.com/461045/192097505-1eebad60-50d2-411b-be54-f4d596aa5f54.png)

## Final Round

`main2.py` is the main program on Jetson Nano for the final round of the competition. It's practically similar to main.py. It's 2 more area in it, 1 is used to detect signes, and, based on theres position, make robot go arond them. A proportional-derivative controller is also used here. The other is used to find out, in which direction robot goes.

## Connection with Jetson Nano


