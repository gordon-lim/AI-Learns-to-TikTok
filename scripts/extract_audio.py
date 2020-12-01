import moviepy.editor as mp
import argparse
import os

parser = argparse.ArgumentParser("Export audio from every video in directory")
# -- Create the descriptions for the commands
i_desc = "The location of the input video directory"
o_desc = "The location of the output audio directory"

parser.add_argument(
    "-i", help=i_desc, default="/Volumes/gordonssd/tiktok/train_set/video")
parser.add_argument(
    "-o", help=o_desc, default="/Volumes/gordonssd/tiktok/train_set/audio")


args = parser.parse_args()

for basename in os.listdir(args.i):
    videoname = os.path.splitext(basename)[0]
    input_video = mp.VideoFileClip(args.i + f"/{basename}")
    input_video.audio.write_audiofile(args.o + "/" + videoname + ".mp3")
