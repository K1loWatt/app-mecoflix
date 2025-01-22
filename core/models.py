from dataclasses import dataclass
from pathlib import Path
from abc import ABC, abstractmethod
from multiprocessing import Pool

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
            

def trasnform_audio(video: VideoFile, handler: VideoHandler):
    
    new_video = video.copy()
    handler.transform_audio(new_video)
    
    return new_video

def transform_audio_files_multiprocess(filter, repo, handler: VideoHandler):

    videos = repository.get_videos(filter_)
    
    process_item_with_constant = trasnform_audio(trasnform_audio, constant=handler)

    with Pool(processes=4) as pool:  # Adjust 'processes' based on your CPU cores
        new_videos = pool.map(process_item_with_constant, videos)  # Map each item to the process_item function

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
    new_videos = transform_audio_files_multiprocess(filter, repository, handler)
    
    print("Videos transformed")
    print(new_videos)