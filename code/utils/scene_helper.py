import re
import os
from utils.helper import read_ndjson
from utils.paths import get_annotations_path
from utils.labelbox_to_coco import get_video_location, video_is_labeled
from utils.paths import get_video_dir

def remove_pattern_from_string(input_string):
    pattern = r"_\d{3}-\d{3}_\d+\.mp4|_\d+_\d+\.mp4"
    result_string = re.sub(pattern, "", input_string)
    return result_string


def get_all_scenes():
    data = read_ndjson(get_annotations_path())
    data = [d for d in data if video_is_labeled(d)]
    scenes = []
    for entry in data:
        scene_name = remove_pattern_from_string(entry["data_row"]["external_id"])
        if not scene_name in scenes:
            scenes.append(scene_name)
    return scenes 

def get_scene_to_video_combination():
    data = read_ndjson(get_annotations_path())
    data = [d for d in data if video_is_labeled(d)]
    comb = dict()
    for i in range(len(data)):
        str = remove_pattern_from_string(data[i]["data_row"]["external_id"])
        if str in comb.keys():
            comb[str].append(i)
        else:
            comb[str] = [i]

    return comb 
