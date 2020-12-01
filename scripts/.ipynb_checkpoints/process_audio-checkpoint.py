import os
import matplotlib.pyplot as plt
from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tempfile import mktemp

audio_fpath = "/Volumes/gordonssd/tiktok/train_set/audio/"
audio_clips = os.listdir(audio_fpath)

for audio_name in audio_clips:
    mp3_audio = AudioSegment.from_file(
        audio_fpath + audio_name, format="mp3")  # read mp3
    wname = mktemp('.wav')  # use temporary file
    mp3_audio.export(wname, format="wav")  # convert to wav
    FS, data = wavfile.read(wname)  # read wav file

    # save only spectrogram (minus axes or anything else)
    fig, ax = plt.subplots(1)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.axis('tight')
    ax.axis('off')

    # Note [:, 0] I'm only using left audio
    # The JustDance feedback sounds are left in the tracks
    ax.specgram(data[:, 0], Fs=FS, NFFT=128, noverlap=0)
    # Remove .mp3
    audio_basename = os.path.splitext(audio_name)[0]
    fig.savefig('/Volumes/gordonssd/tiktok/train_set/spectrogram/' +
                audio_basename, dpi=300)
