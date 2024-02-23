create_boxplot <- function(data, value_column, category_column1, category_column2, title = NULL, angle = 45, metric_labels = NULL) {
  
  default_title <- ifelse(is.null(title), paste("Box Plot for", substitute(data)), title)
  
  plot <- ggplot2::ggplot(data, ggplot2::aes(x = factor(get(category_column2)), y = get(value_column), fill = factor(get(category_column1)))) +
    ggplot2::geom_boxplot() +
    ggplot2::labs(x = category_column2, y = value_column, fill = category_column1, title = default_title) +
    ggplot2::theme_minimal() +
    ggplot2::theme(axis.text.x = element_text(angle = angle, hjust = 1))  # Rotate x-axis labels
  
  if (!is.null(metric_labels)) {
    plot <- plot + scale_fill_discrete(labels = metric_labels)
  }
  
  return(plot)  # Return the ggplot object
}



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

metric_labels <- c("mAP50.95", "mAP50","Precision", "Recall")
plt <- create_boxplot(df_long,"Value","metric","Filename",title = "Boxplots of the results for different preprocessing steps", metric_labels = metric_labels)

factor <- 2
# Example usage:
ggsave(
  filename = file.path("visualizations", "boxplots",  "overview.png"),
  plot = plt,
  width = 16 * factor,
  height = 16 * factor,
  units = "cm"
)
cat("Saved: ", parameter, "\n")

