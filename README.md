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
This script is intended to combine multiple CSV files located in the "./results" directory. It calculates a weighted average of two specific columns ("metrics.mAP50.B." and "metrics.mAP50.95.B.") in each CSV file, finds the row with the maximum value, and combines this row from each file into a single dataframe called "res." The script then writes this combined dataframe to a CSV file named "combined-results.csv" in the same directory. Additionally, it prints out each row as it is processed and the total number of rows in the combined dataframe.

#### `generate_split_results.R`
This script performs the following tasks:

1. It retrieves a list of directories in the "../results" directory, excluding certain directories specified in the `exclude_list`.
2. For each dataset in the `datasets` list, it performs the following steps:
   - Sets the dataset name as `DATASET_NAME`.
   - Constructs the path to the results directory for the current dataset.
   - Reads CSV files from the results directory, calculates the weighted average of specific columns, finds the row with the maximum value, and combines these rows into a dataframe called `res`.
   - Writes the `res` dataframe to a CSV file in the "results/cross-validation" directory with the dataset name as the filename.
   - Generates bar plots for each column (excluding the "name" column) in the `res` dataframe and saves them as PNG files in the "visualizations/DATASET_NAME" directory.

Additionally, the script defines a function `generate_bar_plot` to create bar plots using ggplot2, and it includes example usage of this function for generating bar plots.

#### `compare_cross_validations.R` (depracted/not in use)
This script performs the following operations:

1. Reads three CSV files named "original.csv", "original_hsv.csv", and "o-bs-tf_hsv.csv" into separate data frames: `preprocessing_1`, `preprocessing_2`, and `preprocessing_3`, respectively.
2. Removes rows from `preprocessing_1` where the 'name' column ends with '2'.
3. Combines the data from `preprocessing_1` and `preprocessing_3` into a single data frame named `combined_data`, adding a column indicating the preprocessing method.
4. Converts the 'metrics.precision.B.' column of `combined_data` to numeric values.
5. Conducts a Levene's test to assess the equality of variances of the 'metrics.precision.B.' variable across the different preprocessing methods.
6. Constructs a matrix (`precision_matrix`) containing the 'metrics.precision.B.' values and the corresponding preprocessing groups.
7. Performs a Friedman test to analyze whether there are differences in the 'metrics.precision.B.' values among the preprocessing methods, accounting for the repeated measures (indicated by the 'id' variable).
8. Prints the results of the Friedman test.

Please note that there is a commented-out section related to `preprocessing_2`, which is not used in subsequent analysis. Additionally, some variable names (e.g., 'preprocessing_group') used in the script are assumed to be defined elsewhere in the code.

#### `create_cross_validation_results_y7.R`
This script appears to perform the following tasks:

1. It defines a function `read_yolov7` to read data from a YOLOv7 results file.
2. It reads YOLOv7 results files located in a specified directory (`project`) and stores the data in a list of data frames (`result_list`), where each element corresponds to a file.
3. For each data frame in `result_list`, it calculates a weighted average of two metrics (`map50` and `map95`) and selects the row with the maximum value.
4. It defines a function `transform_epoch` to process the 'epoch' column of the selected data frame to extract numerical values.
5. It renames columns in the selected data frame to match specific naming conventions.
6. It adds columns for learning rates (`lr.pg0`, `lr.pg1`, `lr.pg2`) and writes the resulting data frame to a CSV file in the "results/cross-validation" directory with the project name as the filename.

This script seems to be part of a data processing pipeline for YOLOv7 results, where it reads, selects, transforms, and organizes data for further analysis or visualization.

#### `generate_box_plots.R`
This script performs the following tasks:

1. It defines a function `add_filename_column` to extract the filename from the 'File' column and add it as a new column 'Filename' in the dataframe.
2. It initializes lists for experiment names (`experiment_names`) and experiment IDs (`experiment_ids`) based on predefined mappings.
3. It sets up parameters, colors, and y-labels for creating boxplots.
4. It reads CSV files from the "results/cross-validation" directory and stores the data in a list of data frames.
5. It combines all data frames into a single data frame (`df`) and adds a 'Filename' column.
6. It creates boxplots for each parameter using ggplot2, with data grouped by experiment ID.
7. It saves the boxplot visualizations as PNG files in the "visualizations/boxplots" directory.

This script is designed to visualize the distribution of certain metrics (e.g., precision, recall, mAP@0.5, etc.) across different experiments, helping to analyze and compare the performance of different configurations or setups.

#### `plot_overview_results.R`
This script defines a function `create_boxplot` to generate box plots using ggplot2. It then proceeds to create box plots to visualize the distribution of different metrics across various experiments.

Here's a summary of what the script does:

1. Defines a function `create_boxplot` to create box plots.
2. Defines experiment names mapping.
3. Defines a function `add_filename_column` to extract filename information from the 'File' column and add it as a new column 'Filename' in the dataframe.
4. Reads data from CSV files located in the "results/cross-validation" directory and stores it in a list of data frames.
5. Combines all data frames into a single data frame (`df`) and converts it from wide to long format using the `pivot_longer` function from the tidyr package.
6. Orders the 'Filename' factor levels according to a desired order.
7. Maps experiment names to the 'Filename' factor levels.
8. Creates a box plot using the `create_boxplot` function, specifying the value column, category columns, title, and metric labels.
9. Saves the generated box plot as a PNG file in the "visualizations/boxplots" directory.

This script is designed to provide an overview of experiment results by visualizing the distribution of various metrics across different experiments.

#### `paired_t_test.R`
This script seems to compare the fitness scores of two different preprocessing methods using a one-sided paired t-test. Here's a summary of the script:

1. It defines paths to two CSV files containing the cross-validation results for two different preprocessing methods: `preprocessing_1_path` and `preprocessing_2_path`.
2. It specifies a list of parameters to compare, including precision, recall, mAP@0.5, mAP@0.5-0.95, and fitness.
3. It reads the data from the CSV files into separate data frames: `data_1` for preprocessing method 1 and `data_2` for preprocessing method 2.
4. It calculates fitness scores for each method based on the formula `0.1 * metrics.mAP50.B. + 0.9 * metrics.mAP50.95.B.`.
5. It conducts a one-sided paired t-test, testing the hypothesis that the fitness score for preprocessing method 1 is greater than that for preprocessing method 2 (`alternative = "greater"`).
6. It prints the results of the t-test.

Overall, this script is designed to statistically compare the fitness scores of two different preprocessing methods to determine if one method performs significantly better than the other.

#### `paired_t_test_overview.R`
This script is designed to compare multiple CSV files containing cross-validation results by performing a pairwise t-test on a weighted combination metric derived from each file. Here's a summary of what the script does:

1. **Load Necessary Libraries**: It loads the tidyverse and broom libraries for data manipulation and statistical analysis.

2. **Define Functions**:
   - `calculate_metric`: This function calculates a weighted combination metric from the cross-validation results, where the metric is computed as 0.1 * `metrics.mAP50.B.` + 0.9 * `metrics.mAP50.95.B.`.
   - `perform_t_test`: This function performs a one-sided t-test with the alternative hypothesis that the first dataset's metric is greater than the second dataset's metric.
   - `compare_csv_files`: This function reads CSV files from a specified directory, performs pairwise t-tests on the calculated metrics, and visualizes the results using a heatmap. It iterates over all pairs of CSV files, calculates p-values using the `perform_t_test` function, and populates a matrix with the results.

3. **Example Usage**:
   - It specifies the directory containing the CSV files (`dir_location`) and calls the `compare_csv_files` function to compare the CSV files within that directory.
   - The heatmap generated by the `compare_csv_files` function visualizes the p-values resulting from the pairwise t-tests. Lower p-values indicate a more significant difference between the compared datasets.

Overall, this script provides a systematic way to compare multiple sets of cross-validation results, allowing users to assess the statistical significance of differences between the performance metrics derived from different experiments or configurations.

#### `pairwise_t_tests.R`
The provided R script is aimed at conducting pairwise t-tests on a set of CSV files containing cross-validation results, followed by the generation of LaTeX code to create a table displaying the results.

Here's a summary of what the script does:

1. **Load Libraries**: The script starts by loading the necessary libraries, including `stringr`, `dplyr`, `kableExtra`, and `tibble`.

2. **Define Functions**:
   - `fitness`: This function calculates a fitness metric based on the weighted sum of `metrics.mAP50.95.B.` and `metrics.mAP50.B.` from the input data.
   - `calculate_t_tests`: This function conducts paired t-tests between all combinations of columns in the input data frame and returns a matrix of p-values.
   - `generate_latex_table`: This function generates LaTeX code for a table from the results of the t-tests. It includes conditional formatting to highlight statistically significant results.

3. **Data Processing**:
   - The script reads CSV files from a specified directory and creates a data frame (`df`) containing fitness metrics calculated using the `fitness` function.

4. **T-Test Calculation**:
   - The `calculate_t_tests` function is then applied to the `df` data frame to compute pairwise t-tests between different experiments based on their fitness metrics.

5. **Generate LaTeX Code**:
   - Finally, the `generate_latex_table` function converts the t-test results into LaTeX code for creating a formatted table. It includes conditional formatting to highlight statistically significant results.

6. **Print LaTeX Code**:
   - The generated LaTeX code is printed to the console.

The resulting LaTeX code can be used to create a table in a LaTeX document, providing a concise summary of the pairwise t-test results between different experiments based on their fitness metrics.

#### `print_cross_validation_overview.R`
The script you provided reads CSV files containing cross-validation results from a specified directory, calculates a fitness metric based on the weighted sum of `metrics.mAP50.95.B.` and `metrics.mAP50.B.`, and then summarizes statistics for a specific metric across different experiments. Here's a breakdown of what the script does:

1. **Load Necessary Libraries**: The script loads the `stringr` library.

2. **Define File Paths and Experiment IDs**: It specifies the directory containing the CSV files and assigns experiment IDs to each file based on their names.

3. **Define Fitness Function**: The `fitness` function calculates the fitness metric based on the specified weights for `metrics.mAP50.95.B.` and `metrics.mAP50.B.`.

4. **Define Parameters**: The script defines a vector `parameters` containing the names of metrics to analyze. It selects the fifth parameter (`metrics.mAP50.95.B.`) for analysis.

5. **Loop Through Files**: It iterates over each CSV file in the specified directory.

6. **Data Processing**:
   - For each file, it reads the CSV data.
   - It checks if the number of rows in the CSV data is not equal to 10. If not, it removes duplicate entries based on the first 38 characters of the `name` column.
   - It calculates the fitness metric for each file and stores the specified parameter (`metrics.mAP50.95.B.`) in a temporary data frame.

7. **Generate Summary Statistics**: For each experiment, the script calculates and prints the mean, maximum, minimum, and median values of the selected metric (`metrics.mAP50.95.B.`).

This script allows for an analysis of the performance of different experiments based on the `metrics.mAP50.95.B.` metric, providing summary statistics for each experiment.

#### `plot_fitness.R`
The script you provided performs the following tasks:

1. **Set Directory and List Files**: It sets the directory containing the CSV files and lists all files in that directory.

2. **Exclude Certain Files**: It excludes specific files (`exclude_files`) from the list of files.

3. **Define Fitness Function**: The `fitness` function calculates the fitness metric based on the weighted sum of `metrics.mAP50.95.B.` and `metrics.mAP50.B.`.

4. **Read CSV Files and Compute Fitness**: It reads each CSV file, calculates the fitness metric for each file, and creates a data frame (`df`) to store the fitness values.

5. **Prepare Data for Plotting**:
   - It extracts the first 19 characters of the file names (`nms`) to use as column names in the data frame.
   - It assigns the column names to the data frame.
   - It adds an index column to the data frame.
   - It converts the data frame from wide to long format using `pivot_longer` from the `tidyr` package.

6. **Write Data to CSV**: It writes the data frame (`df`) to a CSV file named "fitness.csv".

7. **Plotting**:
   - It plots the evolution of fitness values over epochs for each file using `ggplot2`.
   - The plot includes lines for each variable (file) colored differently.
   - It sets the title, subtitle, labels, and theme for the plot.
   - It saves the plot as an image file named "fitness.png".

Overall, the script reads the fitness values from CSV files, processes the data, and generates a plot illustrating the evolution of fitness values over epochs for different files.
