#imports
from pytube import YouTube
import os
import pyperclip
import re
import json

#essential class
class Downloader:
    def __init__(self, video: str, path='./'):
        self.video = YouTube(video)
        self.streams = self.video.streams
        self.path = path
        self.title = self.video.title
        self.description = self.video.description
        self.thumb = self.video.thumbnail_url

    def get_max(self):
        yt = self.streams.get_highest_resolution()
        yt.download(output_path=self.path)
    
    def get_lowest(self):
        yt = self.streams.get_lowest_resolution()
        yt.download(output_path=self.path)

    def get_audio(self):
        yt = self.streams.filter(only_audio=True).first()
        vid = yt.download(output_path=self.path)
        base, ext = os.path.splitext(vid)
        new_file = base + '.mp3'
        os.rename(vid, new_file)

def CheckPaths(paths: list) -> list:
    ex = []
    for p in range(len(paths)):
        if os.path.exists(paths[p]) == True:
            ex.append(paths[p])
    return ex

def ShowOptions(options: list):
    for opt in range(len(options)):
        print(f'    {opt} | {options[opt]}')

def main():
    #getting video
    video = str(input("Link of the video (blank = get from clipboard): ")) or pyperclip.paste()
    print(f'Url: {video}')
    assert re.search(r'http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?', video), 'Invalid URL'

    #getting quality
    options = ['MP3 Audio', 'Lowest Quality', 'Max Quality']
    print('OPTIONS:')
    ShowOptions(options)
    option = dir(Downloader)[-3:][int(input('Choose the option: '))]

    #getting path
    try:
        with open('paths.json') as f: data = json.load(f)
        paths = CheckPaths(data['paths'])
        print('PATHS: ')
        ShowOptions(paths)
    except:
        print('Error while reading paths.json')
    path = input('Choose a custom or existing paths(blank = ./):') or './'
    if path.isnumeric() == True and int(path) <= len(paths): d = Downloader(video, paths[int(path)])
    else: d = Downloader(video, path)
    print(f'Downloading {d.title}...')
    getattr(d, option)()
    print('Video Downloaded!')


if __name__ == '__main__':
    main()