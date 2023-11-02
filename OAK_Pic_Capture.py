#!/usr/bin/env python3

from pathlib import Path
import cv2
import depthai as dai
import time

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
monoLeft = pipeline.create(dai.node.MonoCamera)
xoutLeft = pipeline.create(dai.node.XLinkOut)

monoRight = pipeline.create(dai.node.MonoCamera)
xoutRight = pipeline.create(dai.node.XLinkOut)

xoutLeft.setStreamName("left")
xoutRight.setStreamName("right")

# Properties
monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)


# Linking
monoLeft.out.link(xoutLeft.input)
monoRight.out.link(xoutRight.input)


# Connect to device and start pipeline
with dai.Device(pipeline) as device:
    # Output queue will be used to get the grayscale frames from the output defined above
    qLeft = device.getOutputQueue(name="left", maxSize=4, blocking=False)
    qRight = device.getOutputQueue(name="right", maxSize=4, blocking=False)
    #

    leftdirname = "left_mono_data"
    rightdirname = "right_mono_data"

    Path(leftdirname).mkdir(parents=True, exist_ok=True)
    Path(rightdirname).mkdir(parents=True, exist_ok=True)

    i = 0
    while True:
        i = i + 1
        inLeft = qLeft.get()  # Blocking call, will wait until a new data has arrived
        inRight = qRight.get()  # Blocking call, will wait until a new data has arrived
        # Data is originally represented as a flat 1D array, it needs to be converted into HxW form
        # Frame is transformed and ready to be shown

        cv2.imshow("left", inLeft.getCvFrame())
        cv2.imshow("right", inRight.getCvFrame())

        # After showing the frame, it's being stored inside a target directory as a PNG image
        cv2.imwrite(f"{leftdirname}/{i}.png", inLeft.getFrame())
        cv2.imwrite(f"{rightdirname}/{i}.png", inRight.getFrame())

        if cv2.waitKey(1) == ord('q'):
            break
