from fake_browser import FakeBrowser
from util import Util
import re


class VideoDownloader:
    def __init__(self, type=None) -> None:
        self.type = type

    def download(self, link) -> None:
        if self.type == "bomb":
            self._download_bomb(link)
        elif self.type == "youtube":
            self._download_youtube()
        else:
            raise Exception("Video type not supported yet")

    def _download_bomb(self, link) -> None:
        url = self._get_request_url(link)
        idx = url.index("?")
        self._download_bomb_with_url(url[:idx])

    def _get_request_url(self, link) -> str:
        fakeBrowser = FakeBrowser(headless=True)
        netData = fakeBrowser.get_net_data(link)
        filtered = filter(
            lambda entry: entry["initiatorType"] == "xmlhttprequest"
            and entry["nextHopProtocol"] == "http/1.1",
            netData,
        )
        urls = list(
            filter(
                lambda url: ".ts" not in url,
                list(map(lambda entry: entry["name"], filtered)),
            )
        )
        fakeBrowser.close()
        return urls[0]

    def _download_bomb_with_url(self, url):
        fileName = re.findall(r"\d+.m3u8", url)[0]
        homeUrl = Util.get_home_url(url, fileName)
        Util.download_m3u8_file(url, fileName)
        Util.add_home_url_to_m3u8_file(homeUrl, fileName)
        Util.download_mp4(fileName)

    def _download_youtube(self):
        pass
