from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip
from data_tools.utils import diarize_speakers
import json
from sys import argv

# get first parameter from single.py {ID}
ID = argv[1] if len(argv) > 1 else 'QvkbctEwb5Y'

ydl_opts = {
   "outtmpl": f"{ID}.%(ext)s",
}

with YoutubeDL(ydl_opts) as ydl:
    ydl.download(ID)


video = VideoFileClip(f'./{ID}.mp4')
video.audio.write_audiofile(f'./{ID}.mp3')

transcription = diarize_speakers(f'./{ID}.mp3')

with open(f'./{ID}.json', 'w') as f:
    json.dump(transcription, f, indent=4)

# Initialize a list to hold the text output
txt_output = []

# Loop through each segment and append the text to the list
for segment in transcription['segments']:
    txt_output.append(segment['text'])

# `txt_output` now contains only the texts from each segment as a list of strings
# save as .txt file
with open(f'./{ID}.txt', 'w') as f:
    f.write('\n'.join(txt_output))

# save as .srt file
with open(f'./{ID}.srt', 'w') as f:
    for i, segment in enumerate(transcription['segments']):
        start = str(segment['start'])
        end = str(segment['end'])
        text = segment['text']
        f.write(f'{i}\n')
        f.write(f'{start} --> {end}\n')
