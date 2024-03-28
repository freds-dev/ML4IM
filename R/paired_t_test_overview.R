# Load necessary libraries
library(tidyverse)
library(broom)

# Function to calculate the weighted combination metric
calculate_metric <- function(data) {
  weighted_metric <- ((data$`metrics.mAP50.B.` |> as.numeric())*0.1) + ((data$`metrics.mAP50.95.B.` |> as.numeric())*0.9)
  return(weighted_metric)
}

# Function to perform t-test
perform_t_test <- function(data1, data2) {
  # Calculate metric for both datasets
  metric1 <- calculate_metric(data1)
  metric2 <- calculate_metric(data2)
  
  # Perform t-test
  t_test_result <- t.test(metric1, metric2, alternative = "greater")
  
  return(t_test_result$p.value)
}

# Function to read csv files, perform t-test and visualize results
compare_csv_files <- function(dir_location) {
  # List all csv files in the directory
  csv_files <- list.files(path = dir_location, pattern = "\\.csv$", full.names = TRUE)
  
  # Read csv files and store dataframes in a list
  data_list <- lapply(csv_files, read_csv)
  
  # Initialize a matrix to store p-values
  p_values <- matrix(NA, nrow = length(data_list), ncol = length(data_list))
  
  # Loop through all pairs of csv files
  for (i in 1:(length(data_list) - 1)) {
    for (j in (i+1):length(data_list)) {
      # Perform t-test for the pair
      p_value <- perform_t_test(data_list[[i]], data_list[[j]])
      p_values[i, j] <- p_value
    }
  }
  
  # Create a data frame with p-values
  p_values_df <- as.data.frame(p_values)
  rownames(p_values_df) <- csv_files
  p_values_df[is.na(p_values_df)] <- 1
  heatmap(as.matrix(p_values_df), col = c(heat.colors(10), "white"), symm = TRUE,
          main = "P-Values Comparison",
          xlab = "CSV Files", ylab = "CSV Files", na.rm = TRUE)
}

# Example usage
dir_location <- "results/cross-validation/"
compare_csv_files(dir_location)
