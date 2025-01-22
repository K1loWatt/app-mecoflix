from dataclasses import dataclass
from pathlib import Path
from abc import ABC, abstractmethod

@dataclass
class AudioCodec:
    pass

@dataclass
class AudioTrack:
    codec: AudioCodec

@dataclass
class VideoTrack:
    pass

@dataclass
class VideoFile:
    
    name: str
    path: Path
    duration: int
    size: int
    resolution: str
    audio_tracks:list[AudioTrack] 
    video_tracks:list[VideoTrack]
    
@dataclass
class VideoHandler(ABC):

    @abstractmethod
    def transform_audio(self, audio_codec: AudioCodec, video_file: VideoFile) -> dict:
        pass
    

@dataclass
class MIMFHandler(VideoHandler):
    
    ffmpeg_binary: Path
    
    def transform_audio(self, audio_codec: AudioCodec, video_file: VideoFile) -> VideoFile:
        
        #check if video has the actual audio codec
        #if not
        #launch a ffmpeg command to transform the audio codec
        #this will produce a new video file with the new audio codec
        #ffmpeg -i input.mp4 -c:v copy -c:a aac output.mp4 -y #this will overrite the copied file
        #set new audio codec to the video file
            

def transform_audio(filter, video: VideoFile, handler: VideoHandler):

    videos = repository.get_videos(filter_)
    new_videos = []
    for video in videos:
        new_video = video.copy()
        handler.transform_audio(new_video)
        new_videos.append(new_video)
        
    return new_videos

class Repository(ABC):
    
    @abstractmethod
    def get_videos(self, filter_: dict) -> list[VideoFile]:
        pass
    
class VideoRepository(Repository):
    
    mediainfo_binary: Path
    
    def get_videos(self, filter_: dict, path: Path) -> list[VideoFile]:
        
        #find all video files
        #launch a mediainfo command to get the video metadata recursively
        #parse the output to get the video metadata
        #return a list of VideoFile objects
        
        return videos
    
if __name__ == "__main__":
    
    repository = VideoRepository(mediainfo_binary=Path("mediainfo"))
    handler = MIMFHandler(ffmpeg_binary=Path("ffmpeg"))
    new_videos = transform_audio(filter, repository, handler)
    
    print("Videos transformed")
    print(new_videos)