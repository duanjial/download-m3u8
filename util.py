import urllib.request
import shutil
import os


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
        os.system(
            f"ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto \
                -i ./tmp/{file_name} -c copy ./videos/{file_name[:-5]}.mp4"
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
