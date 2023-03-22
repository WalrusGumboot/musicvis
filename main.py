import os
import moviepy.video.io.ImageSequenceClip
import moviepy.editor as mpe
import wave
import audioop
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import tqdm

fps = 60
audio_file_name = "audio.wav"

reader = wave.open(audio_file_name, 'rb')
print(reader.getparams())

# We want an list of audio frames
samplewidth = reader.getsampwidth()
frames_per_vid_frame = reader.getframerate() // fps
total_frames = reader.getnframes() // frames_per_vid_frame
audio_frames = [audioop.rms(reader.readframes(frames_per_vid_frame), samplewidth) for i in range(total_frames)]
audio_frames_norm = list(map(lambda x: x * (1 / max(audio_frames)), audio_frames))

# plt.plot(list(range(total_frames)), audio_frames_norm)
# plt.title("RMS")
# plt.xlabel("Frame")
# plt.ylabel("RMS value")
# plt.show()

# now that we have the normalised frame values, all that's left to do is to
# generate frames according to those values and stitch them together


base_img = Image.open("img.png")
black_img = Image.new("RGBA", base_img.size, (0, 0, 0, 255))

try:
    os.mkdir('rawFrames')
except FileExistsError:
    # os.system("rm -rf rawFrames")
    # os.mkdir('rawFrames')
    pass
os.chdir('rawFrames')

max_len = len(str(len(audio_frames_norm)))

# progress_bar = tqdm(enumerate(audio_frames_norm))
# for idx, val in progress_bar:
#     progress_bar.set_description(f"{idx}: {val}")
#     this_frame = Image.blend(black_img, base_img, val)
#     this_frame.save(str(idx).zfill(max_len)+".png")


# We have now got all frames, all that is left to do is to splice
# them together and add the audio. It should all match up by default.

os.chdir("..")

audio_background = mpe.AudioFileClip(audio_file_name)
clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip("./rawFrames", fps=fps)
final_clip = clip.set_audio(audio_background)

final_clip.write_videofile('output.mp4')