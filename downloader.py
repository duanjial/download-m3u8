#!./env/bin/python3

import argparse
from util import Util
from video_downloader import VideoDownloader

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download video with the provided link"
    )
    parser.add_argument("--link", dest="link", help="Full video url")
    parser.add_argument(
        "--file-name", dest="fileName", help="[Optional]: file name from tmp folder"
    )
    parser.add_argument(
        "--type",
        dest="video_type",
        required=True,
        choices=["bomb", "youtube"],
        help="Video type: [bomb, youtube]",
    )
    args = parser.parse_args()
    fileName = args.fileName
    link = args.link
    video_type = args.video_type

    if link:
        video_downloader = VideoDownloader(video_type=video_type)
        video_downloader.download(link)
    if fileName:
        Util.download_mp4(fileName)
