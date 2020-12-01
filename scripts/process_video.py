import moviepy.editor as mp
import argparse
import os

parser = argparse.ArgumentParser("Process video into train data")
# -- Create the descriptions for the commands
v_desc = "The location of the input video"

# -- Create the arguments
parser.add_argument(
    "-v", help=v_desc, default="/Volumes/gordonssd/tiktok/videos/letskillthislove.mp4")

args = parser.parse_args()
basename = os.path.basename(args.v)
videoname = os.path.splitext(basename)[0]

clip = mp.VideoFileClip(args.v)

for i, j in enumerate(range(0, int(clip.duration), 15)):
    if j+15 < clip.duration:
        snippet = clip.subclip(j, j+15)
        snippet.write_videofile(
            f"/Volumes/gordonssd/tiktok/train_set/video/{videoname}{i}.mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, audio_codec="aac")
