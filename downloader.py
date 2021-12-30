#!./env/bin/python3

import argparse
import time

from util import Util
import logging
import threading
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
        "--youtube-file-name", dest="youtube_file_name", help="Youtube temp file name"
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
    youtube_file_name = args.youtube_file_name
    link = args.link
    video_type = args.video_type
    logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %I:%M:%S %p',
                        level=logging.INFO)
    logging.info("Start downloading")
    if link:
        video_downloader = VideoDownloader(video_type=video_type, youtube_file_name=youtube_file_name)
        try:
            video_downloader.download(link)
        except OverLimitException as e:
            logging.error(e.get_msg())
        except VideoTypeNotSupportException as e:
            logging.error(e.get_msg())
        except UnableToClickException as e:
            logging.error(e.get_msg())
    if fileName:
        progress_bar_thread = threading.Event()
        Util.progress_bar_fn(progress_bar_thread, f"./logs/{fileName[:-5]}_log")
        Util.download_mp4(fileName)
        progress_bar_thread.set()
    time.sleep(1)
    logging.info("Finished downloading")
