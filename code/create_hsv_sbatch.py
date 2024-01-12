from os import listdir
from os.path import isfile, join
from utils.build_sbatch import *
from utils.file_system import write_file
from utils.helper import whoami


if __name__ == "__main__":
    user = whoami()
    path = f"/scratch/tmp/{user}/data/videos"
    videos = [f for f in listdir(path)]
    for video in videos:
        write_file(f"cpu_{video}_hsv.sh",build_cpu_script(video,f"{video}_hsv","preprocessing.rgb_to_hsv"))
        write_file(f"gpu_{video}_hsv.sh", build_gpu_script(f"{video}_hsv"))        
