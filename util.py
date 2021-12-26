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
                    if duration_list:
                        duration = Util.get_duration(duration_list[0])
            threading.Timer(1, Util.progress_bar_fn, [progress_thread, log_file]).start()

    @staticmethod
    def get_duration(duration):
        time_list = [ele.strip() for ele in duration.split(":")][-3]
        duration_in_sec = int(time_list[2])
        if time_list[1]:
            duration_in_sec += int(time_list[1]) * 60
        if time_list[0]:
            duration_in_sec += int(time_list[0]) * 60 * 60
        print(duration_in_sec)
        return duration_in_sec
