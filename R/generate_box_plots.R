# Debug: parameter <- "metrics.mAP50.B."
add_filename_column <- function(df) {
  # Extract file name from 'File' column
  df$Filename <- sub(".*/([^/]+)\\.csv", "\\1", df$File)
  
  # Remove file extension
  df$Filename <- sub("\\.csv", "", df$Filename)
  
  return(df)
}

# Initialize experiment names based on unique values of df$Filename
experiment_names <- c(
  "o-bs-tf_hsv"                     = "(DVS_DVS-BS_DVS-TF)-HSV",
  "o-bs-tf"                         = "DVS_DVS-BS_DVS-TF",
  "o-tf-o_hsv"                      = "(DVS_DVS-BS_DVS)-HSV",
  "o-tf-o"                          = "DVS_DVS-BS_DVS",
  "original_bg-sub_temp_filter_rgb" = "DVS_DVS-BS_DVS-BS-TF_RGB-BS",
  "original_bg-sub_temp-filter_hsv" = "(DVS_DVS-BS_DVS-BS-TF)-HSV",
  "original_bg-sub_temp-filter"     = "DVS_DVS-BS_DVS-BS-TF",
  "original_hsv"                    = "(DVS_DVS_DVS)-HSV",
  "original"                        = "DVS_DVS_DVS",
  "rgbe3"                           = "RGB-R_RGB-G_RGB-B_DVS"
)

experiment_ids <- c(
  "o-bs-tf_hsv"                     = "01",
  "o-bs-tf"                         = "02",
  "o-tf-o_hsv"                      = "03",
  "o-tf-o"                          = "04",
  "original_bg-sub_temp_filter_rgb" = "05",
  "original_bg-sub_temp-filter_hsv" = "06",
  "original_bg-sub_temp-filter"     = "07",
  "original_hsv"                    = "08",
  "original"                        = "09",
  "rgbe3"                           = "10"
)



colors = c("#FFFFFF" ,"#00BFC4" ,"#C77CFF", "#7CAE00" ,"#F8766D")
ylabels = c("Epoch", "Precision", "Recall", "mAP@0.5", "mAP@0.5-0.95")
c("epoch","metrics.precision.B.","metrics.recall.B.","metrics.mAP50.B.","metrics.mAP50.95.B.") -> parameters
for(i in 1:length(parameters)){
parameter <- parameters[i]
color <- colors[i]
ylabel <- ylabels[i]

# Check file paths
files <- list.files("results/cross-validation", full.names = TRUE)

# Initialize an empty list to store individual data frames
df_list <- list()

# Loop through each file
for (file in files) {
  # Read the CSV file
  print(file)
  data <- read.csv(file)
  name <- strsplit(file,"/") |> unlist() 
  # Create a data frame with the specified column
  df_file <- data.frame(File = file, Value = data[[parameter]])
  
  # Append the data frame to the list
  df_list <- c(df_list, list(df_file))
}

# Combine all data frames into a single data frame
df <- do.call(rbind, df_list)
df <- add_filename_column(df)
df$ExperimentName <- experiment_names[df$Filename]
df$ExperimentID <- experiment_ids[df$Filename]

library(ggplot2)

create_boxplot <- function(data, file_column, value_column, color, xlabel = "Experiment", ylabel = "Bla") {
  # Calculate median for each group
  median_values <- aggregate(data[[value_column]], by = list(data[[file_column]]), FUN = median)
  
  # Reorder levels based on median values
  ordered_levels <- median_values[order(-median_values$x), "Group.1"]
  data[[file_column]] <- factor(data[[file_column]], levels = ordered_levels)
  
  # Create a boxplot using ggplot2 with rotated axis labels
  p <- ggplot(data, aes(x = get(file_column), y = get(value_column))) +
    geom_boxplot(fill = color) +
    ggplot2::stat_summary(fun.data = function(x) { data.frame(y = median(x)) }, 
                          geom = "text", 
                          aes(label = ifelse(floor(..y..) == 0, sprintf("%.3f", ..y..), sprintf("%.3f", ..y..))), 
                          vjust = -0.5, 
                          position = position_dodge(width = 0.75)) +
    ggplot2::stat_summary(fun.data = function(x) { data.frame(y = max(x)) }, 
                          geom = "text", 
                          aes(label = ifelse(floor(..y..) == 0, sprintf("%.3f", ..y..), sprintf("%.3f", ..y..))), 
                          vjust = 1.5, 
                          position = position_dodge(width = 0.75), 
                          show.legend = FALSE) +
    ggplot2::stat_summary(fun.data = function(x) { data.frame(y = min(x)) }, 
                          geom = "text", 
                          aes(label = ifelse(floor(..y..) == 0, sprintf("%.3f", ..y..), sprintf("%.3f", ..y..))), 
                          vjust = -0.5, 
                          position = position_dodge(width = 0.75), 
                          show.legend = FALSE) +
    labs(title = paste0("Distribution of ",ylabel," scores"), x = xlabel, y = ylabel) +
    theme_minimal() +
    theme(plot.title = element_text(size=10))
  
  # Print the boxplot
  return(p)
}



height_factor <- 1
width_size <- 8.50714756389
p <- create_boxplot(df, "ExperimentID", "Value",color, ylabel = ylabel)
ggsave(
  filename = file.path("visualizations", "boxplots", paste0(parameter, ".png")),
  plot = p,
  width = width_size,
  height = width_size * height_factor,
  units = "cm",
)
cat("Saved: ", parameter, "\n")

}
# 
