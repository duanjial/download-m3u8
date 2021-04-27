#!./env/bin/python3

import urllib.request
import shutil
import os
import re
import argparse


def download_m3u8_file(url, file_name):
    if not os.path.exists("./downloadM3U8/tmp"):
        os.makedirs("./downloadM3U8/tmp")
    file = os.path.join("./downloadM3U8/tmp", file_name)
    with urllib.request.urlopen(url) as response, open(file, "wb") as outFile:
        shutil.copyfileobj(response, outFile)


def download_mp4(file_name):
    if not os.path.exists("./downloadM3U8/videos"):
        os.makedirs("./downloadM3U8/videos")
    os.system(
        f"ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto \
             -i ./downloadM3U8/tmp/{file_name} -c copy ./downloadM3U8/videos/{file_name[:-5]}.mp4"
    )


def add_home_url_to_m3u8_file(home_url, file_name):
    with open(os.path.join("./downloadM3U8/tmp", file_name), "r") as file:
        lines = file.readlines()

    def add_prefix(line):
        if not line.startswith("#"):
            return home_url + line
        else:
            return line

    data = list(map(add_prefix, lines))
    with open(os.path.join("./downloadM3U8/tmp", file_name), "w") as file:
        file.writelines(data)


def get_home_url(url, file_name):
    return url.replace(file_name, "")


class Downloader:
    @staticmethod
    def download(url):
        fileName = re.findall(r"\d+.m3u8", url)[0]
        homeUrl = get_home_url(url, fileName)
        download_m3u8_file(url, fileName)
        add_home_url_to_m3u8_file(homeUrl, fileName)
        download_mp4(fileName)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download m3u8 file from given url")
    parser.add_argument("url")
    args = parser.parse_args()
    url = args.url
    Downloader.download(url)
