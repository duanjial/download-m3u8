#!./env/bin/python3

import argparse
from util import Util
import logging
import threading
from datetime import datetime
from video_downloader import VideoDownloader
from exceptions import OverLimitException, VideoTypeNotSupportException, UnableToClickException

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
    logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S %p',
                        level=logging.INFO)
    if link:
        video_downloader = VideoDownloader(video_type=video_type)
        try:
            video_downloader.download(link)
            logging.info("Finished downloading")
        except OverLimitException as e:
            logging.error(e.get_msg())
        except VideoTypeNotSupportException as e:
            logging.error(e.get_msg())
        except UnableToClickException as e:
            logging.error(e.get_msg())
    if fileName:
        Util.download_mp4(fileName)
    logging.info("Finished download, exit")
