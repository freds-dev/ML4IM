library(ggplot2)
create_boxplot <- function(data, value_column, category_column1, category_column2, title = NULL, angle = 45, metric_labels = NULL) {
  
  default_title <- ifelse(is.null(title), paste("Box Plot for", substitute(data)), title)
  
  plot <- ggplot2::ggplot(data, ggplot2::aes(x = factor(get(category_column2)), y = get(value_column), fill = factor(get(category_column1)))) +
    ggplot2::geom_boxplot() +
    #ggplot2::stat_summary(fun.data = function(x) { data.frame(y = median(x)) }, 
    #                      geom = "text", 
    #                      aes(label = ifelse(floor(..y..) == 0, sprintf("%.3f", ..y..), sprintf("%.3f", ..y..))), 
    #                      vjust = -0.5, 
    #                      position = position_dodge(width = 0.75)) +
    #ggplot2::stat_summary(fun.data = function(x) { data.frame(y = max(x)) }, 
    #                      geom = "text", 
    #                      aes(label = ifelse(floor(..y..) == 0, sprintf("%.3f", ..y..), sprintf("%.3f", ..y..))), 
    #                      vjust = 1.5, 
    #                      position = position_dodge(width = 0.75), 
    #                     show.legend = FALSE) +
    #ggplot2::stat_summary(fun.data = function(x) { data.frame(y = min(x)) }, 
    #                      geom = "text", 
    #                      aes(label = ifelse(floor(..y..) == 0, sprintf("%.3f", ..y..), sprintf("%.3f", ..y..))), 
    #                      vjust = -0.5, 
    #                      position = position_dodge(width = 0.75), 
    #                      show.legend = FALSE) +
    ggplot2::labs(x = "Metric", y = "Value", fill = category_column1, title = default_title, subtitle = "Distribution of metrics across different experiments") +
    ggplot2::theme_minimal() +
    ggplot2::theme(plot.title = element_text(size = 10, face = "bold"), plot.subtitle = element_text(size = 8), text = element_text(family = "Times New Roman")) +
    ggplot2::scale_fill_discrete("ID",labels =  c(paste0("0",1:9),"10"))
  if (!is.null(metric_labels)) {
    plot <- plot + scale_x_discrete(labels = metric_labels)
  }
  return(plot)  # Return the ggplot object
}



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




add_filename_column <- function(df) {
  # Extract file name from 'File' column
  df$Filename <- sub(".*/([^/]+)\\.csv", "\\1", df$File)
  
  # Remove file extension
  df$Filename <- sub("\\.csv", "", df$Filename)
  
  return(df)
}
# List of metrics
metrics <- c("metrics.precision.B.", "metrics.recall.B.", "metrics.mAP50.B.", "metrics.mAP50.95.B.")

# Check file paths
files <- list.files("results/cross-validation", full.names = TRUE)

# Initialize an empty list to store individual data frames
df_list <- list()

# Loop through each file
for (file in files) {
  # Read the CSV file
  data <- read.csv(file)

  # Create a data frame with the specified columns
  df_file <- data.frame(File = file, Value = data[metrics])
  
  # Append the data frame to the list
  df_list <- c(df_list, list(df_file))
}

# Combine all data frames into a single data frame
df <- do.call(rbind, df_list)

library(tidyr)

df_long <- pivot_longer(df, 
                        cols = starts_with("Value.metrics"), 
                        names_to = "metric", 
                        values_to = "Value")

df_long <- df_long |> as.data.frame() |> add_filename_column()

desired_order <- c("original","o-tf-o","o-bs-tf","original_bg-sub_temp-filter","original_hsv","o-tf-o_hsv","o-bs-tf_hsv","original_bg-sub_temp-filter_hsv", "rgbe3","original_bg-sub_temp_filter_rgb")
df_long$Filename <- factor(df_long$Filename, levels = desired_order)
metric_labels <- c("mAP@0.5-0.95", "mAP@0.5","Precision", "Recall")
df_long$ExperimentName <- experiment_names[df_long$Filename]


plt <- create_boxplot(df_long,"Value","ExperimentName","metric",title = "Overview: Experiment results", metric_labels = metric_labels)

height_factor <- 1/2
width_size <- 17.8609625
# Example usage:
ggsave(
  filename = file.path("visualizations", "boxplots",  "overview.png"),
  plot = plt,  
  width = width_size,
  height = width_size * height_factor,
  units = "cm",
  dpi = 300
)

