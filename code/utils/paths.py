import os
from dotenv import load_dotenv

load_dotenv()

IS_LOCAL = os.getenv('IS_LOCAL') == "TRUE"
LOCAL_PATH_DATA = os.getenv('LOCAL_PATH_DATA')
PALMA_PATH_DATA = os.getenv('PALMA_PATH_DATA')

def get_base_dir()-> str:
    return LOCAL_PATH_DATA if IS_LOCAL else PALMA_PATH_DATA

def get_annotations_path()->str:
    return os.path.join(get_base_dir(), "annotations.ndjson")

def get_dataset_dir(dataset_name:str)-> str:
    return os.path.join(get_base_dir(),"datasets",dataset_name)

def get_video_dir(video_dir_name: str) -> str:
    return os.path.join(get_base_dir(),"videos",video_dir_name)

def get_data_yaml(dataset_name: str) -> str:
    return os.path.join(get_base_dir(),"datasets",dataset_name,"data.yaml")
    
def get_result_dir(dataset_name: str) -> str:
    dir = os.path.join(get_base_dir(),"results",dataset_name)
    os.makedirs(dir,exist_ok=True)
    return dir