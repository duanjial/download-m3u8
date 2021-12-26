from fake_browser import FakeBrowser
from util import Util
import logging
import threading
import re
from exceptions import OverLimitException, VideoTypeNotSupportException


class VideoDownloader:
    def __init__(self, video_type=None) -> None:
        self._logger = logging.getLogger()
        self.video_type = video_type

    def download(self, link) -> None:
        if self.video_type == "bomb":
            url = self._get_request_url(link)
            if not url:
                raise OverLimitException("You are over the limit, please try again tomorrow!!")
            idx = url.index("?")
            self._logger.info("Start downloading")
            self._download_bomb_with_url(url[:idx])
        elif self.video_type == "youtube":
            self._download_youtube()
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
        logging.info("Another thread finished")

    def _download_youtube(self):
        pass
