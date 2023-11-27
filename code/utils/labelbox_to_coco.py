import os
from utils.helper import adjust_string_length
from utils.file_system import save_frames_from_video


def video_is_labeled(labelbox_data: dict) -> bool:
    return labelbox_data["projects"]["clor41l0i03gi07znfo8051e3"]["project_details"]["workflow_status"] == "IN_REVIEW"


def get_video_location(base_dir: str, json_row:dict) -> str:
    dir_name = json_row["data_row"]["details"]["dataset_name"]
    file_name = json_row["data_row"]["external_id"]
    return f"{base_dir}/{dir_name}/{file_name}"

class BoundingBox:
    
    x: float
    y: float
    w: float
    h: float
    
    def __init__(self,x,y,w,h) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self) -> str:
        return f"{self.x} {self.y} {self.w} {self.h}"
    

class Annotation:
    name: str
    bounding_box: BoundingBox

    def __init__(self, name, bounding_box) -> None:
        self.name = name
        self.bounding_box = bounding_box

    def __str__(self) -> str:
        return "0 "+self.bounding_box.__str__()
class AnnotationsVideo:

    frame:str
    frame_as_int: int
    annotations: [Annotation]

    def __init__(self,frame) -> None:
        self.frame = frame
        self.frame_as_int = int(frame)
        self.annotations = []

    def add_annotation(self, annotation):
        self.annotations.append(annotation)
    
    def save_to_file(self, dir: str,video_id: str) -> str:
        file_path = dir + f"img_{video_id}_{self.frame}.txt"
        with open(file_path, 'w') as f:
            f.write(self.__str__())    
        return file_path    
    def __str__(self) -> str:
        res = ""
        for bb in self.annotations:
            res += bb.__str__() +"\n"
        return res
    
def labelbox_bb_to_yolo(dict, width, height):
    center_x = dict["left"] + (dict["width"] /2)
    center_y = dict["top"] + (dict["height"] /2)
    
    center_x /= width
    center_y /= height
    
    width_bb = dict["width"] / width
    height_bb = dict["height"]/ height
    
    return BoundingBox(center_x,center_y,width_bb,height_bb)


def convert_to_coco_format(json_data) -> [AnnotationsVideo]:
    width, height = json_data["media_attributes"]["width"],json_data["media_attributes"]["height"]
    frames = json_data["projects"]['clor41l0i03gi07znfo8051e3']["labels"][0]["annotations"]["frames"]
    annotations = []
    for frame in frames:
        annotations_frame = AnnotationsVideo(adjust_string_length(frame, 6, "0"))
        objects = frames[frame]["objects"]
        for objectKey in objects:
            a = Annotation(objects[objectKey]["name"],labelbox_bb_to_yolo(objects[objectKey]["bounding_box"],width,height))        
            annotations_frame.add_annotation(a)
            
        annotations.append(annotations_frame)
    return annotations

def write_data_row(data_row:dict,video_id:int,dataset_dir:str, video_base_dir:str, frames_per_video, type: str = "train"):
    video_id = adjust_string_length(str(video_id),3,"0")
    frames : [AnnotationsVideo] = convert_to_coco_format(data_row)        
    for frame in frames:
        if frame.frame_as_int <= frames_per_video:
            frame.save_to_file(f"{dataset_dir}/{type}/labels/",video_id)
    
    video_location = get_video_location(video_base_dir, data_row)
    save_frames_from_video(video_location,os.path.join(dataset_dir,type,"images"),frames_per_video,video_id)
