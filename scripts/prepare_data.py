import argparse
from sys import platform
import os
import cv2
import numpy as np
import sys
import pandas as pd

if True:
    sys.path.append('/Volumes/gordonssd/tiktok/openpose/python')
    from openpose import pyopenpose as op

# Flags
parser = argparse.ArgumentParser()
parser.add_argument("--video_folder", default="train_set/video",
                    help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
args = parser.parse_known_args()

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "/Volumes/gordonssd/tiktok/openpose/models/"

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

train_df = pd.DataFrame(columns=np.arange(start=0, stop=450, step=2))

video_folder = os.listdir(args[0].video_folder)
for video_name in video_folder:
    cap = cv2.VideoCapture(args[0].video_folder + "/" + video_name)
    count = 0
    while cap.isOpened():
        ret, image = cap.read()
        if ret:
            # Process Image
            datum = op.Datum()
            datum.cvInputData = image
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))
            train_df.at[video_name, count] = str(datum.poseKeypoints)
            train_df.to_csv(
                "/Volumes/gordonssd/tiktok/train_set/train.csv")
            count += 2
            cap.set(1, count)
        else:
            cap.release()
            break

imageToProcess = cv2.imread("/Volumes/gordonssd/tiktok/images/just_dance.jpg")
cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", imageToProcess)
cv2.waitKey(0)
