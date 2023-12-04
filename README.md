# ML4IM
Study project - machine learning for insect monitoring


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


#### Build a dataset
```
> python3 build_dataset.py -h
usage: build_dataset.py [-h] -video_dir_name VIDEO_DIR_NAME -dataset_name
                        DATASET_NAME -amount_videos AMOUNT_VIDEOS
                        -frames_per_video FRAMES_PER_VIDEO

Process videos.

options:
  -h, --help            show this help message and exit
  -video_dir_name VIDEO_DIR_NAME
                        Path to the source videos folder
  -dataset_name DATASET_NAME
                        Name of the created dataset
  -amount_videos AMOUNT_VIDEOS
                        Amount of random choosen videos for the dataset
  -frames_per_video FRAMES_PER_VIDEO
                        Amount of frames per video
```

#### Preprocessing individual bands
```
> python3 preprocess_bands.py -h
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

#### Preprocessing complete videos
```
> python3 preprocess_videos.py -h 
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
#### Training a model
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
| Function name            | Possible input channels       | Output channels             | Note                                                                             | Implementing process_bands functionality |
| ------------------------ | ----------------------------- | --------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------- |
| `bg_subtraction`         | 1-3                           | 1 actual, three implemented |                                                                                  |               Yes                           |
| `contrast_enhancement`   | 1 actual, implemented 3 bands | 1 actual, three implemented |                                                                                  |                  No                        |
| `morph`                  | 1 actual, implemented 3 bands | 1 actual, three implemented |                                                                                  |                  No                      |
| `moving_average`         | 3 bands                       | 3 bands                     | Using as output, band 1 for original, band 2 and 3 for different scoped averages |                  No                        |
| `optical_flow_farneback` | 3 bands                       | 3 bands                     | One original, one result, one black                                              |                  No                        |
| `temporal_filtering`     | 1 actual, 3 implemnted        | 1 actual, 3 implemented     |                                                                                  |                  Yes                        |
