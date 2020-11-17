import zipfile
from tqdm import tqdm
import os
import argparse
import shutil
parser = argparse.ArgumentParser()

import urllib.request, subprocess

parser.add_argument("--tag")
args = parser.parse_args()
args.tag = args.tag.split("/")[-1]
def extract_file(output_path):
    with zipfile.ZipFile(output_path) as zip_ref:
        zip_ref.extractall("")


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, total_size=None):
        if total_size is not None:
            self.total = total_size
        self.update(b * bsize - self.n)

def download_file_with_bar(url, output_path, size=None):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1], ascii=True) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=lambda b, bsize, tsize: t.update_to(b, bsize,
                                                                                                             size) if size is not None else t.update_to(
            b, bsize, tsize))



def download_file_and_extract(url, output_path, size=None):
    download_file_with_bar(url, output_path, size)
    extract_file(output_path)
    os.remove(output_path)

def set_java_home(path):
    os.environ["JAVA_HOME"] = os.path.join(os.getcwd(), path)

def extend_path():
    set_java_home("jdk-14.0.2")
    os.environ["PATH"] = os.environ["PATH"] + ";" + os.path.join(os.environ["JAVA_HOME"], "bin")

jdk_link = "https://download.java.net/java/GA/jdk14.0.2/205943a0976c4ed48cb16f1043c5c647/12/GPL/openjdk-14.0.2_windows-x64_bin.zip"
jdk_zip_name = "JDK.zip"

download_file_and_extract(jdk_link, jdk_zip_name)
extend_path()
subprocess.check_call(["gradlew.bat", "RatPoison"])
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, _, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def kill_jdk():
    # kill all processes returned by `jps.exe -q`
    try:
        str_path = "jps.exe"
        processes = [int(x) for x in subprocess.getoutput(f"\"{str_path}\" -q").split("\n")]
        for process in processes:
            try:
                os.kill(process, 0)
            except Exception:
                pass
    except Exception:
        # Nah
        pass
kill_jdk()

def yeahdefinately():
    for file in os.listdir("build/"):
        if "RatPoison" in file:
            rp_dir = os.path.join(f"build/{file}")
            shutil.move("jdk-14.0.2", rp_dir)
            for bruh in os.listdir(rp_dir):
                if "RatPoison" in bruh and ".bat" in bruh:
                    with open(f"{rp_dir}/{bruh}") as f:
                        lines = f.readlines()
                        new_lines = [lines[0], '\tcd /d "%~dp0"\n', '\tset "JAVA_HOME=%~dp0/jdk-14.0.2"\n', '\tset "PATH="%JAVA_HOME%/bin"\n', "".join(lines[3:])]
                    with open(f"{rp_dir}/{bruh}", "w") as f:
                        f.writelines("".join(new_lines))
                    zip_name = f'RatPoison-{args.tag}.zip'
                    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
                    zipdir(rp_dir, zipf)
                    zipf.close()
                    print(f"::set-output name=zip::{zip_name}")
                    return
yeahdefinately()