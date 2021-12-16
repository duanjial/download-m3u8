#!./env/bin/python3

from pytube import YouTube, Playlist
import os
import argparse


def combineVideo(filename, title, directory):
    if directory is None:
        os.system(
            f"ffmpeg -loglevel warning -i ./video/{filename} \
                -i ./audio/{filename} -c copy ./output/{filename}.mp4"
        )
        os.system(f'mv ./output/{filename}.mp4 ./output/"{title}".mp4')
    else:
        os.system(
            f"ffmpeg -loglevel warning -i ./video/{filename}.mp4 \
                -i ./audio/{filename}.mp4 \
                    -c copy ./output/{directory}/{filename}.mp4"
        )
        os.system(
            f'mv ./output/{directory}/{filename}.mp4 \
            ./output/{directory} /"{title}".mp4'
        )


def progressFunction(stream, chunk, bytes_remaining):
    iteration = stream.filesize - bytes_remaining
    printProgressBar(
        iteration, stream.filesize, prefix="Progress", suffix="Complete", length=50
    )


def deleteFile(filename):
    os.system(f"rm ./audio/{filename} ./video/{filename}")


def printProgressBar(
    iteration,
    total,
    prefix="",
    suffix="",
    decimals=2,
    length=100,
    fill="█",
    printEnd="\r",
):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent \
            complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + "-" * (length - filledLength)
    print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def downloadVideo(url, filename, directory=None):
    yt = YouTube(url, on_progress_callback=progressFunction)
    video = (
        yt.streams.filter(file_extension="mp4", type="video", adaptive=True)
        .order_by("resolution")
        .desc()
        .first()
    )
    audio = yt.streams.filter(file_extension="mp4", type="audio").first()
    title = yt.title
    if ".mp4" not in filename:
        filename = filename + ".mp4"
    print(f"Start downloading {title} Audio")
    audio.download(output_path="./audio", filename=filename)
    print(f"Finish downloading {title} Audio")
    print(f"Start downloading {title} Video")
    video.download(output_path="./video", filename=filename)
    print(f"Finish downloading {title} Video")

    print("Start combining:")
    combineVideo(filename, title, directory)
    print(f"Finish combining {title}.mp4")
    deleteFile(filename)


def run():
    parser = argparse.ArgumentParser(
        description="Download youtube video with a given url"
    )
    parser.add_argument("-u", "--url")
    parser.add_argument("-f", "--filename")
    parser.add_argument("-l", "--list")
    parser.add_argument("-d", "--directory")
    args = parser.parse_args()
    url = args.url
    filename = args.filename
    playlist = args.list
    directory = args.directory

    if playlist is not None:
        if directory is None:
            parser.error("-l requires -d directory name provided")
        p = Playlist(playlist)
        os.system(f"mkdir ./output/{directory}")
        print(f"Downloading {p.title}")
        for i, video_url in enumerate(p.video_urls):
            downloadVideo(video_url, str(i), directory)
        print(f"Finish downloading {p.title}")
    elif url is not None:
        if filename is None:
            parser.error("-u requires -f filename provided")
        downloadVideo(url, filename)
    else:
        parser.print_help()


if __name__ == "__main__":
    run()
