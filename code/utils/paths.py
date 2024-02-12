import os
from dotenv import load_dotenv

load_dotenv()

IS_LOCAL = os.getenv('IS_LOCAL') == "TRUE"
LOCAL_PATH_DATA = os.getenv('LOCAL_PATH_DATA')
PALMA_PATH_DATA = os.getenv('PALMA_PATH_DATA')

def get_base_dir()-> str:
    return LOCAL_PATH_DATA if IS_LOCAL else PALMA_PATH_DATA

def get_homography() -> str:
    return os.path.join(get_base_dir(), "homography_calib.yaml")

def get_calib_rgb() -> str:
    return os.path.join(get_base_dir(), "calib_dng.yaml")

def get_calib_event() -> str:
    return os.path.join(get_base_dir(), "calib_raw.yaml")

def get_config_path(config_name:str) -> str:
    return os.path.join(get_base_dir(),"configs",config_name)

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