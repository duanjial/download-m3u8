import os.path

from fake_browser import FakeBrowser
from util import Util
import logging
import threading
import re
from pytube import YouTube, Playlist
from exceptions import OverLimitException, VideoTypeNotSupportException


class VideoDownloader:
    def __init__(self, video_type=None, youtube_file_name=None, directory=None) -> None:
        self._logger = logging.getLogger()
        self.video_type = video_type
        self._youtube_file_name = youtube_file_name
        self._directory = directory

    def download(self, link) -> None:
        success = False
        count = 0
        url = None
        if self.video_type == "bomb":
            while not success and count < 5:
                url = self._get_request_url(link)
                count += 1
                if url:
                    success = True
            if not success and count == 5:
                raise OverLimitException("You are over the limit, please try again tomorrow!!")
            self._logger.info(f"Download from url: {url}")
            try:
                if url:
                    idx = url.index("?")
                    self._download_bomb_with_url(url[:idx])
            except Exception as e:
                self._logger.info("No ? mark found, use url directly")
                self._download_bomb_with_url(url)
        elif self.video_type == "youtube":
            self._download_youtube(link, self._directory)
        else:
            raise VideoTypeNotSupportException("Video type not supported yet")

    def _get_request_url(self, link) -> str:
        fake_browser = FakeBrowser(headless=True)
        net_data = fake_browser.get_net_data(link)
        filtered = filter(
            lambda entry: entry["initiatorType"] == "xmlhttprequest"
                          and entry["nextHopProtocol"] == "http/1.1",
            net_data,
        )
        urls = list(
            filter(
                lambda url: ".ts" not in url,
                list(map(lambda entry: entry["name"], filtered)),
            )
        )
        fake_browser.close()
        return urls[0] if urls else None

    def _download_bomb_with_url(self, url):
        file_name = re.findall(r"\d+.m3u8", url)[0]
        home_url = Util.get_home_url(url, file_name)
        Util.download_m3u8_file(url, file_name)
        Util.add_home_url_to_m3u8_file(home_url, file_name)
        progress_bar_thread = threading.Event()
        Util.progress_bar_fn(progress_bar_thread, f"./logs/{file_name[:-5]}_log")
        Util.download_mp4(file_name)
        progress_bar_thread.set()

    def _download_youtube(self, url, directory=None):
        yt = YouTube(url, on_progress_callback=Util.progress_function)
        video = (
            yt.streams.filter(file_extension="mp4", type="video", adaptive=True).order_by("resolution").desc().first()
        )
        audio = yt.streams.filter(file_extension="mp4", type="audio").first()
        title = yt.title
        if ".mp4" not in self._youtube_file_name:
            self._youtube_file_name = self._youtube_file_name + ".mp4"
        self._logger.info(f"Start downloading {title} Audio")
        if not os.path.exists("./audio"):
            os.makedirs("./audio")
        audio.download(output_path="./audio", filename=self._youtube_file_name)
        self._logger.info(f"Finish downloading {title} Audio")
        self._logger.info(f"Start downloading {title} Video")
        if not os.path.exists("./video"):
            os.makedirs("./video")
        video.download(output_path="./video", filename=self._youtube_file_name)
        self._logger.info(f"Finish downloading {title} Video")

        self._logger.info("Start combining:")
        Util.combine_video(self._youtube_file_name, title, directory)
        self._logger.info(f"Finish combining {title}.mp4")
        Util.delete_file(self._youtube_file_name)
