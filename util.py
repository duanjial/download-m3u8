import urllib.request
import shutil
import threading
import os
import re


class Util:
    @staticmethod
    def download_m3u8_file(url, file_name):
        if not os.path.exists("./tmp"):
            os.makedirs("./tmp")
        file = os.path.join("./tmp", file_name)
        with urllib.request.urlopen(url) as response, open(file, "wb") as outFile:
            shutil.copyfileobj(response, outFile)

    @staticmethod
    def download_mp4(file_name):
        if not os.path.exists("./videos"):
            os.makedirs("./videos")
        if not os.path.exists("./logs"):
            os.makedirs("./logs")
        # os.system(
        #     f"ffmpeg -hide_banner -loglevel error -stats -protocol_whitelist file,http,https,tcp,tls,crypto \
        #         -progress block.txt -i ./tmp/{file_name} -c copy ./videos/{file_name[:-5]}.mp4"
        # )
        # While downloading, output to log for progress value as well
        os.system(
            f"ffmpeg -hide_banner -protocol_whitelist file,http,https,tcp,tls,crypto"
            f" -i ./tmp/{file_name} -c copy ./videos/{file_name[:-5]}.mp4 1> ./logs/{file_name[:-5]}_log 2>&1"
        )

    @staticmethod
    def add_home_url_to_m3u8_file(home_url, file_name):
        with open(os.path.join("./tmp", file_name), "r") as file:
            lines = file.readlines()

        def add_prefix(line):
            if not line.startswith("#"):
                return home_url + line
            else:
                return line

        data = list(map(add_prefix, lines))
        with open(os.path.join("./tmp", file_name), "w") as file:
            file.writelines(data)

    @staticmethod
    def get_home_url(url, file_name):
        return url.replace(file_name, "")

    @staticmethod
    def progress_bar_fn(progress_thread, log_file):
        if not progress_thread.is_set():
            if os.path.exists(log_file):
                with open(log_file, "r") as file:
                    duration_list = re.findall(r'Duration: \d{2}:\d{2}:\d{2}', file.read())
                    duration = 0
                    if duration_list:
                        duration = Util.get_duration(duration_list[0])
                raw_time_in_sec = 0
                with open(log_file, "r") as file:
                    raw_time = re.findall(r'time=\d{2}:\d{2}:\d{2}', file.read())
                    if raw_time:
                        raw_time_in_sec = Util.get_duration(raw_time[-1].split("=")[1])
                if duration and raw_time_in_sec:
                    percentage = round((raw_time_in_sec / duration) * 100)
                    # print(f"{percentage}%")
                    Util.print_progress_bar(
                        raw_time_in_sec, duration, prefix="Progress", suffix="Complete", length=50
                    )
            threading.Timer(1, Util.progress_bar_fn, [progress_thread, log_file]).start()
        else:
            if os.path.exists(log_file):
                with open(log_file, "r") as file:
                    duration_list = re.findall(r'Duration: \d{2}:\d{2}:\d{2}', file.read())
                    duration = 0
                    if duration_list:
                        duration = Util.get_duration(duration_list[0])
                Util.print_progress_bar(
                    duration, duration, prefix="Progress", suffix="Complete", length=50
                )

    @staticmethod
    def get_duration(duration):
        time_list = [ele.strip() for ele in duration.split(":")][-3:]
        duration_in_sec = int(time_list[2])
        if time_list[1]:
            duration_in_sec += int(time_list[1]) * 60
        if time_list[0]:
            duration_in_sec += int(time_list[0]) * 60 * 60
        return duration_in_sec

    @staticmethod
    def print_progress_bar(
            iteration,
            total,
            prefix="",
            suffix="",
            decimals=2,
            length=100,
            fill="█",
            print_end="\r",
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
        print(f"\r{prefix} |{bar}| {percent}% {suffix}", end=print_end)
        # Print New Line on Complete
        if iteration == total:
            print()
