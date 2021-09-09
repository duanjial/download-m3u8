#!./env/bin/python3

import argparse
from util import Util
from video_downloader import VideoDownloader

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download video with the provided link"
    )
    parser.add_argument("--link", dest="link")
    parser.add_argument("--file-name", dest="fileName")
    parser.add_argument(
        "--type", dest="type", required=True, choices=["bomb", "youtube"]
    )
    args = parser.parse_args()
    fileName = args.fileName
    link = args.link
    type = args.type

    if link:
        video_downloader = VideoDownloader(type=type)
        video_downloader.download(link)
    if fileName:
        Util.download_mp4(fileName)
