import ffmpeg
import shutil
from pathlib import Path
from threading import Thread

import youtube_dl


class DownloadThread(Thread):
    def __init__(self, opts, url):
        super().__init__()
        self.opts = opts
        self.url = url

    def run(self):
        with youtube_dl.YoutubeDL(self.opts) as ydl:
            download_info = ydl.extract_info(self.url, download=False)
            filename = Path(ydl.prepare_filename(download_info))
            ydl.download([self.url])
        self.result = filename


class MP4:
    def __init__(self, config, url):
        self.config = config
        self.url = url
        self.audio_opts = dict(self.config.opts, **{
            "format": "bestaudio[ext=m4a]/bestaudio",
            "outtmpl": f"{self.config.outdir}/audio/%(title)s.%(ext)s",
        })
        self.video_opts = dict(self.config.opts, **{
            "format": "bestvideo[ext=mp4]/bestvideo",
            "outtmpl": f"{self.config.outdir}/video/%(title)s.%(ext)s"
        })

    def merge(self, audio_file, video_file):
        result = Path(self.config.outdir) / f"{Path(audio_file).stem}.mp4"
        input_video = ffmpeg.input(video_file)
        input_audio = ffmpeg.input(audio_file)
        out = ffmpeg.output(input_video, input_audio, filename=result,
                            vcodec='copy', acodec='aac', strict='experimental')
        out.run(quiet=True)
        return result

    def cleanup(self, video_file, audio_file):
        shutil.rmtree(Path(video_file).parent)
        shutil.rmtree(Path(audio_file).parent)

    def create(self):
        audio_thread = DownloadThread(opts=self.audio_opts, url=self.url)
        video_thread = DownloadThread(opts=self.video_opts, url=self.url)
        audio_thread.start()
        video_thread.start()
        audio_thread.join()
        video_thread.join()
        self.config.info_log.set_description_str(f"Start merging video and audio...")
        audio_file, video_file = audio_thread.result, video_thread.result
        res = self.merge(audio_file=audio_file, video_file=video_file)
        self.cleanup(audio_file=audio_file, video_file=video_file)
        self.config.info_log.set_description_str(f"{res}:finished")
        return res
