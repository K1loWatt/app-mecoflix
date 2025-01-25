from dataclasses import dataclass
from pathlib import Path
from multiprocessing import Pool
import shutil
import subprocess
import json
from typing import cast
from dataclasses import field

def run_subprocess(command: list[str]) -> str:

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {result.stderr}")

    return result.stdout


@dataclass
class AudioCodec:
    id_: str

@dataclass
class AudioTrack:
    codec: AudioCodec
    format: str

@dataclass
class VideoFile():

    path: Path
    name: str | None = None

    @classmethod
    def copy_from(self, from_: Path, to_: Path) -> "VideoFile":
        raise NotImplementedError

    @property
    def audio_tracks(self) -> list[AudioTrack] | None:
        raise NotImplementedError

@dataclass
class VideoFileOS(VideoFile):

    _audio_tracks: list[AudioTrack] = field(default_factory=list)

    @classmethod
    def copy_from(cls, from_: Path, to_:Path) -> "VideoFileOS":

        shutil.copy(from_, to_)
        video = cls(path=to_)
        return video

    @property
    def audio_tracks(self) -> list[AudioTrack] | None:

        result = run_subprocess(["mediainfo", "--Output=JSON", str(self.path)])
        media_info = json.loads(result)

        for track in media_info["media"]["track"]:
            if track["@type"] == "Audio":
                codec = AudioCodec(id_=track["CodecID"])
                audio_track = AudioTrack(format=track["format"], codec=codec)
                self._audio_tracks.append(audio_track)

        return self._audio_tracks

def get_videos() -> list[VideoFile]:
    video_files = []
    for video_path in Path(".").rglob("*.mkv"):
        video = VideoFileOS(path=video_path)
        video_files.append(video)

    return cast(list[VideoFile], video_files)


def transform_audio(video: VideoFile, to_:Path) -> VideoFile:

    run_subprocess(
        [
            "ffmpeg",
            "-y",
            "-i",
            video.path.as_posix(),
            "-c:v",
            "copy",
            "-c:a",
            "libmp3lame",
            to_.as_posix()
            ]
        )
    return video

if __name__ == "__main__":

    videos = get_videos()
    new_videos = []
    for video in videos:
        new_video = video.copy_from(video.path, to_=Path(f"./video_copy_{video.path.name}"))
        new_videos.append(new_video)

    with Pool(processes=4) as pool:
        to_:Path = Path("./movie_transformed.mkv")
        videos_transformed = pool.starmap(transform_audio, [(new_videos[0],to_)])

    print("Videos transformed")


