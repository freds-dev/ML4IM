# ML4IM
Study project - machine learning for insect monitoring

## Experiments

| Channels | Channel-Encoding | ID | Name                               | Model |
|------------|-----|----|------------------------------------|-----------------------|
|  3          | RGB    | 01 | DVS\_DVS\_DVS                     | [Best performing model](https://github.com/freds-dev/ML4IM/releases/01) |
|  3          | RGB    | 02 | DVS\_DVS-TF\_DVS                 | [Best performing model](https://github.com/freds-dev/ML4IM/releases/02) |
|  3          | RGB    | 03 | DVS\_DVS-BS\_DVS-TF              | [Best performing model](https://github.com/freds-dev/ML4IM/releases/03) |
|  3          | RGB    | 04 | DVS\_DVS-BS\_DVS-BS-TF         | [Best performing model](https://github.com/freds-dev/ML4IM/releases/04) |
|  3          | HSV | 05 | (DVS\_DVS\_DVS)-HSV              | [Best performing model](https://github.com/freds-dev/ML4IM/releases/05) |
|  3          | HSV    | 06 | (DVS\_DVS-TF\_DVS)-HSV          | [Best performing model](https://github.com/freds-dev/ML4IM/releases/06) |
|  3          | HSV    | 07 | (DVS\_DVS-BS\_DVS-TF)-HSV      | [Best performing model](https://github.com/freds-dev/ML4IM/releases/07) |
|  3          | HSV    | 08 | (DVS\_DVS-BS\_DVS-BS-TF)-HSV  | [Best performing model](https://github.com/freds-dev/ML4IM/releases/08) |
| 4         | RGB    | 09 | RGB-R\_RGB-G\_RGB-B\_DVS          | [Best performing model](https://github.com/freds-dev/ML4IM/releases/09) |
|  4          |  RGB   | 10 | DVS\_DVS-BS\_DVS-BS-TF\_RGB-BS | [Best performing model](https://github.com/freds-dev/ML4IM/releases/10) |


## Structure

- **archive**: Contains archived or deprecated files.
- **code**: This directory holds all the code-related files.
  - **frames**: Possibly contains code related to handling or processing frames from videos.
  - **preprocessing**: Code related to preprocessing data, possibly for model training.
    - **__pycache__**: Cached Python files for faster execution.
  - **utils**: Utility functions or modules.
    - **__pycache__**: Cached Python files for faster execution.
  - **yolov7_custom**: The "yolov7_custom" directory contains a customized implementation of YOLOv7 and is cloned from the repository at https://github.com/PaulaScharf/yolov7-custom.
  - **data**: Data files.
  - **videos**: Video data.
    - **tm_1**: Data related to "tm_1".
      - **2023-09-30-perennial_garden_extssd**: Data related to perennial garden with a specific date.
- **R**: R language related files: Scripts that evaluate and visualize yolo results.
- **report**: Files related to reports.
  - **data**: Data files related to the report.
    - **cross-validation**: Data related to cross-validation.
  - **figures**: Figures or visualizations for the report.
    - **preprocessings**: Preprocessing-related figures.
      - **extracted_frames**: Figures related to extracted frames.
    - **results**: Result-related figures.
      - **boxplots**: Boxplot figures.
- **results**: Result files.
  - **cross-validation**: Cross-validation results.
- **scripts**: Scripts.
- **visualizations**: Visualizations or figures.
  - **boxplots**: Boxplot visualizations.
  - **combined-results-wo-cross**: Combined results without cross-validation visualizations.
  

## Setup
The hole setup is optimized for using this repo both locally and on PALMA, if you setup the system in both environments following these instructions, it is easy to quickly change between both environments 

1. Clone the repository to your environment: `git clone https://github.com/freds-dev/ML4IM`
2. Setup your environment:
    1. Create a directory for your data
    2. Move the annotations `ndjson` file into this  directory and rename it to `annotations.ndjson`
    3. Move the video data from sciebo into a subdirectory called `videos`. Inside this directory rename the video dir after your needs
3. Setup `.env` file (Use `.env.example` file as basis)
    1. `IS_LOCAL`, to `TRUE` if you running local, `FALSE` if you are running on PALMA
    2. `LOCAL_PATH_DATA`, to the root of the data directory created in 2 on your local machine
    3. `PALMA_PATH_DATA`, to the  root of the data directory created in 2 on PALMA commonly somethink like `/scratch/tmp/<username>/path/to/project/data`
4. Run `pip install -r requirements.txt`
5. `cd` into `code`
6. Run different scripts based on usage

## Usage
The documentation of each script inside `./code` is retrievable by `python <scriptname> -h`


### Dependency managment

You can generate the `requirements.txt` running `pipreqs .` from the root of this project (`pipreqs` is installable via `pip`)

## Examples

### Create a dataset
```sh
python3 build_dataset.py -video_dir "original" -dataset_name "original-smaller" -amount_videos 5 -frames_per_video 100
```
Building a dataset with name `original-smaller` from the video directory `original`. Using the first 100 frames from 5 random sampled videos.

## Sources

- [PALMA Documentation](https://confluence.uni-muenster.de/display/HPC)

## Documentation

### Scripts for direct usage (inside `/code`)
Each script, that should be directly called is inside the `/code` directory. The scripts are
designed as `CLI` tools, which are documented in this section.


#### `build_dataset_multithread.py`
```
usage: build_dataset_multithread.py [-h] -video_dir_name VIDEO_DIR_NAME
                                    -dataset_name DATASET_NAME
                                    [-amount_videos AMOUNT_VIDEOS]
                                    [-frames_per_video FRAMES_PER_VIDEO]
                                    [-core_factor CORE_FACTOR]

Process videos.

options:
  -h, --help            show this help message and exit
  -video_dir_name VIDEO_DIR_NAME
                        Path to the source videos folder
  -dataset_name DATASET_NAME
                        Name of the created dataset
  -amount_videos AMOUNT_VIDEOS
                        Amount of random choosen videos for the dataset. If
                        the value is below 1, all videos are taken (default =
                        0)
  -frames_per_video FRAMES_PER_VIDEO
                        Amount of frames per video. If the value is below 1,
                        all videos are taken (default = 0)
  -core_factor CORE_FACTOR
                        Capacity of system and cores. The function will
                        evaluate the number of available cpu cores and
                        multiplies them with this factor, to determine the
                        number of used threads. Needs to be in range [0,1]
                        (default = 0.25)
```

#### `build_dataset.py`
```
usage: build_dataset.py [-h] -video_dir_name VIDEO_DIR_NAME -dataset_name
                        DATASET_NAME [-amount_videos AMOUNT_VIDEOS]
                        [-frames_per_video FRAMES_PER_VIDEO]

Process videos.

options:
  -h, --help            show this help message and exit
  -video_dir_name VIDEO_DIR_NAME
                        Path to the source videos folder
  -dataset_name DATASET_NAME
                        Name of the created dataset
  -amount_videos AMOUNT_VIDEOS
                        Amount of random choosen videos for the dataset. If
                        the value is below 1, all videos are taken (default =
                        0)
  -frames_per_video FRAMES_PER_VIDEO
                        Amount of frames per video. If the value is below 1,
                        all videos are taken (default = 0)
```

#### `preprocess_bands_multithread.py`
```
usage: preprocess_bands_multithread.py [-h] -source SOURCE [-txt TXT] -save
                                       SAVE -func FUNC [-inband INBAND]
                                       [-outband OUTBAND OUTBAND OUTBAND]
                                       [-core_factor CORE_FACTOR]

Process videos on band level.

options:
  -h, --help            show this help message and exit
  -source SOURCE        Path to the source videos folder
  -txt TXT              Path to the input text file (default: mp4_files.txt)
  -save SAVE            Path to the output directory for preprocessed videos
  -func FUNC            Module and function name for the preprocessing
                        function (e.g., module_name.function_name)
  -inband INBAND        Input band for the preprocessing. If inband=-1, use
                        all bands; otherwise, use the band with index inband
                        (default: -1)
  -outband OUTBAND OUTBAND OUTBAND
                        Used bands for preprocessing. Provide three boolean
                        values. For True use 1, for False 0 (default: 1 1 1,
                        meaning True True True)
  -core_factor CORE_FACTOR
                        Capacity of system and cores. The function will
                        evaluate the number of available cpu cores and
                        multiplies them with this factor, to determine the
                        number of used threads. Needs to be in range [0,1]
                        (default = 0.25)
```

#### `preprocess_bands.py`
```
usage: preprocess_bands.py [-h] -source SOURCE [-txt TXT] -save SAVE -func
                           FUNC [-inband INBAND]
                           [-outband OUTBAND OUTBAND OUTBAND]

Process videos on band level.

options:
  -h, --help            show this help message and exit
  -source SOURCE        Path to the source videos folder
  -txt TXT              Path to the input text file (default: mp4_files.txt)
  -save SAVE            Path to the output directory for preprocessed videos
  -func FUNC            Module and function name for the preprocessing
                        function (e.g., module_name.function_name)
  -inband INBAND        Input band for the preprocessing. If inband=-1, use
                        all bands; otherwise, use the band with index inband
                        (default: -1)
  -outband OUTBAND OUTBAND OUTBAND
                        Used bands for preprocessing. Provide three boolean
                        values. For True use 1, for False 0 (default: 1 1 1,
                        meaning True True True)
```

#### `preprocess_videos_multithread.py`
```
usage: preprocess_videos_multithread.py [-h] -source SOURCE -txt TXT -save
                                        SAVE -func FUNC
                                        [-core_factor CORE_FACTOR]

Process videos.

options:
  -h, --help            show this help message and exit
  -source SOURCE        Path to the source videos folder
  -txt TXT              Path to the input text file
  -save SAVE            Path to the output directory for preprocessed videos
  -func FUNC            Module and function name for the preprocessing
                        function (e.g., module_name.function_name)
  -core_factor CORE_FACTOR
                        Capacity of system and cores. The function will
                        evaluate the number of available cpu cores and
                        multiplies them with this factor, to determine the
                        number of used threads. Needs to be in range [0,1]
                        (default = 0.25)
```

#### `preprocess_videos.py`
```
usage: preprocess_videos.py [-h] -source SOURCE -txt TXT -save SAVE -func FUNC

Process videos.

options:
  -h, --help      show this help message and exit
  -source SOURCE  Path to the source videos folder
  -txt TXT        Path to the input text file
  -save SAVE      Path to the output directory for preprocessed videos
  -func FUNC      Module and function name for the preprocessing function
                  (e.g., module_name.function_name)
```

#### `split_dataset.py`
```
usage: split_dataset.py [-h] -video_dir_name_event VIDEO_DIR_NAME_EVENT
                        -video_dir_name_rgb VIDEO_DIR_NAME_RGB -config_name
                        CONFIG_NAME -dataset_name DATASET_NAME
                        [-amount_videos AMOUNT_VIDEOS]
                        [-frames_per_video FRAMES_PER_VIDEO] [-scene SCENE]
                        [-core_factor CORE_FACTOR]

Process videos.

options:
  -h, --help            show this help message and exit
  -video_dir_name_event VIDEO_DIR_NAME_EVENT
                        Path to the source videos folder
  -video_dir_name_rgb VIDEO_DIR_NAME_RGB
                        Path to the source videos folder
  -config_name CONFIG_NAME
                        Name of the channel configuration file.
  -dataset_name DATASET_NAME
                        Name of the created dataset
  -amount_videos AMOUNT_VIDEOS
                        Amount of random choosen videos for the dataset. If
                        the value is below 1, all videos are taken (default =
                        0)
  -frames_per_video FRAMES_PER_VIDEO
                        Amount of frames per video. If the value is below 1,
                        all videos are taken (default = 0)
  -scene SCENE          name of scene for validation
  -core_factor CORE_FACTOR
                        Capacity of system and cores. The function will
                        evaluate the number of available cpu cores and
                        multiplies them with this factor, to determine the
                        number of used threads. Needs to be in range [0,1]
                        (default = 1)
```

#### `start_scene_cross_validation.py`
```
usage: start_scene_cross_validation.py [-h] -dataset DATASET -video_event_name
                                       VIDEO_EVENT_NAME -video_rgb_name
                                       VIDEO_RGB_NAME -config_name CONFIG_NAME
                                       [-exception_scenes EXCEPTION_SCENES [EXCEPTION_SCENES ...]]

Start scenic cross validation.

options:
  -h, --help            show this help message and exit
  -dataset DATASET      Name of the dataset which is used for training
  -video_event_name VIDEO_EVENT_NAME
                        Directory where the event videos are located
  -video_rgb_name VIDEO_RGB_NAME
                        Directory where the rgb videos are located
  -config_name CONFIG_NAME
                        Name of the configuration file
  -exception_scenes EXCEPTION_SCENES [EXCEPTION_SCENES ...]
                        Array of scnees that will not be validated
```

#### `train.py`
```
> python3 train.py -h
usage: train.py [-h] -dataset DATASET [-epochs EPOCHS] [-batch BATCH]
                [-save_period SAVE_PERIOD] [-name NAME]
                [-model_path MODEL_PATH] [-device DEVICE] [-exist_ok] [-plots]

Train YOLO model.

options:
  -h, --help            show this help message and exit
  -dataset DATASET      Name of the dataset can be found as it is directory in
                        your "data/datasets" directory.
  -epochs EPOCHS        Number of training epochs (default: 100).
  -batch BATCH          Batch size for training, -1 uses an automatic approach
                        to define a well defined batch size(default: -1).
  -save_period SAVE_PERIOD
                        Save model checkpoints every N epochs (default: 10).
  -name NAME            The name of the run. It will use the dataset as
                        project and this name as name of the actual running
                        experiment
  -model_path MODEL_PATH
                        Path to the YOLO model configuration file (default:
                        yolov8n.yaml).
  -device DEVICE        Device index for training (default: 0). Use arrays
                        (e.g. [0,1] for multiple gpu usage and "cpu" for using
                        cpu)
  -exist_ok             Allow overwriting the project directory if it already
                        exists.
  -plots                Generate plots for each epoch(default: True).

```

### Scripts for evaluating and visualizing results of trainings (`./R`)
Hery you find a short text describing what each file inside the `./R` directory is doing

#### `generate_combined_results.R`
#### `generate_split_results.R`
#### `compare_cross_validations.R`
#### `create_cross_validation_results_y7.R`
#### `generate_box_plots.R`
#### `plot_overview_results.R`
#### `paired_t_test.R`
#### `paired_t_test_overview.R`
#### `pairwise_t_tests.R`
#### `print_cross_validation_overview.R`
#### `plot_fitness.R`


| ------------------------ | ----------------------------- | --------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------- |
| ------------------------ | ----------------------------- | --------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------- |
| `bg_subtraction`         | 1-3                           | 1 actual, three implemented |                                                                                  | Yes                                      |
| `contrast_enhancement`   | 1 actual, implemented 3 bands | 1 actual, three implemented |                                                                                  | No                                       |
| `morph`                  | 1 actual, implemented 3 bands | 1 actual, three implemented |                                                                                  | No                                       |
| `moving_average`         | 3 bands                       | 3 bands                     | Using as output, band 1 for original, band 2 and 3 for different scoped averages | No                                       |
| `optical_flow_farneback` | 3 bands                       | 3 bands                     | One original, one result, one black                                              | No                                       |
| `temporal_filtering`     | 1 actual, 3 implemnted        | 1 actual, 3 implemented     |                                                                                  | Yes                                      |
| `rgb_to_hsv`             | 3 needed                      | 3 needed                    | No implementation for `preprocess_bands`                                                                                 | No                                         |
