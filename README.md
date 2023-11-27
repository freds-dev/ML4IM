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
4. `cd` into `code`
5. Run different scripts based on usage

## Usage
The documentation of each script inside `./code` is retrievable by `python <scriptname> -h`

## Examples

### Create a dataset
```sh
python3 build_dataset.py -video_dir "original" -dataset_name "original-smaller" -amount_videos 5 -frames_per_video 100
```
Building a dataset with name `original-smaller` from the video directory `original`. Using the first 100 frames from 5 random sampled videos.

## Sources

- [PALMA Documentation](https://confluence.uni-muenster.de/display/HPC)

## Documentation