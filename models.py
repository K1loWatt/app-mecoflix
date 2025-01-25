from dataclasses import dataclass
from pathlib import Path
from abc import ABC, abstractmethod
from multiprocessing import Pool
import shutil
import subprocess
import json

@dataclass
class AudioCodec:
    id_: str
    pass

@dataclass
class AudioTrack:
    codec: AudioCodec
    format: str

@dataclass
class VideoTrack:
    pass

@dataclass
class VideoFile(ABC):
    
    path: Path
    name: str | None = None
    
    @classmethod
    @abstractmethod
    def copy_from(self, from_: Path, to_: Path) -> "VideoFile":
        raise NotImplementedError
    
    @property
    @abstractmethod
    def audio_tracks(self) -> list[AudioTrack] | None:
        raise NotImplementedError
    

@dataclass
class VideoFileOS(VideoFile):
    
    _audio_tracks: list[AudioTrack] | None = None

    @classmethod
    def copy_from(cls, from_: Path, to_:Path) -> "VideoFileOS":
        
        shutil.copy(from_, to_)
        video = cls(path=to_)
        return video
        
    @property
    def audio_tracks(self) -> list[AudioTrack] | None:
        
        result = subprocess.run(
            ["mediainfo", "--Output=JSON", str(self.path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"mediainfo failed: {result.stderr}")
        
        media_info = json.loads(result.stdout)
        
        self.audio_tracks = []
        for track in media_info["media"]["track"]:
            if track["@type"] == "Audio":
                codec = AudioCodec(id_=track["CodecID"])  # TODO populate 
                audio_track = AudioTrack(format_=track["format"], codec=codec)
                self._audio_tracks.append(audio_track)
        
        return self._audio_tracks
    
def get_videos() -> list[VideoFile]:
    video_files = []
    for video_path in Path(".").rglob("*.mkv"):
        video = VideoFileOS(path=video_path)
        #video = VideoFileOS(path=video_path)
        video_files.append(video)
    return video_files

def transform_audio(video: VideoFile, to_:Path) -> VideoFile:
    command = [
        "ffmpeg",
        "-y",  # Overwrite output files without asking
        "-i", str(video.path),
        "-c:v", "copy",
        "-c:a", "libmp3lame",
        str(to_)
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result.stderr}")
    
    return video
    
if __name__ == "__main__":
    
    videos = get_videos()
    new_videos = []
    for video in videos:
        new_video = video.copy_from(video.path, to_=f"video_copy_{video.path.name}")
        new_videos.append(new_video)
        
    with Pool(processes=4) as pool:
    #for video in videos:
    #    to_:Path = Path("./movie_transformed.mkv")
    #    video = transform_audio(video, to_)
        
        to_:Path = Path("./movie_transformed.mkv")
        videos_transformed = pool.starmap(transform_audio, [(new_videos[0],to_)])  

    print("Videos transformed")


    
"""
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
   
   
  repository = VideoRepository(mediainfo_binary=Path("mediainfo"))
    handler = MIMFHandler(ffmpeg_binary=Path("ffmpeg"))
    new_videos = transform_audio_files_multiprocess(filter, repository, handler)
    
    print("Videos transformed")
    print(new_videos)
    
    
         
"""