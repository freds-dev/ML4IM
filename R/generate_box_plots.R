# Debug: parameter <- "metrics.mAP50.B."
add_filename_column <- function(df) {
  # Extract file name from 'File' column
  df$Filename <- sub(".*/([^/]+)\\.csv", "\\1", df$File)
  
  # Remove file extension
  df$Filename <- sub("\\.csv", "", df$Filename)
  
  return(df)
}

for(parameter in c("epoch","metrics.precision.B.","metrics.recall.B.","metrics.mAP50.B.","metrics.mAP50.95.B.")){


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

library(ggplot2)


create_boxplot <- function(data, file_column, value_column) {
  # Create a boxplot using ggplot2 with rotated axis labels
  p <- ggplot(data, aes(x = get(file_column), y = get(value_column))) +
    geom_boxplot() +
    labs(title = "Boxplot for Each File", x = "File", y = "Value") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust = 1))
  
  # Print the boxplot
  return(p)
}

factor <- 2
# Example usage:
p <- create_boxplot(df, "Filename", "Value")
ggsave(
  filename = file.path("visualizations", "boxplots", paste0(parameter, ".png")),
  plot = p,
  width = 16 * factor,
  height = 16 * factor,
  units = "cm"
)
cat("Saved: ", parameter, "\n")

}
# 
