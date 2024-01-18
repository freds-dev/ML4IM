DATASET_NAME <- "original"

results_dir <- file.path("..","results",DATASET_NAME)

results_names <-
  list.files(results_dir) |> tools::file_path_sans_ext()

results_names <- results_names[!results_names == "first_run"]
results_names <- results_names[!results_names == "first_run1"]
results_names <- results_names[!results_names == "first_run2"]
results_names <- results_names[!results_names == "first_run3"]
results_names <- results_names[!results_names == "first_run4"]




results_location <- file.path(results_dir,results_names,"results.csv")

res = NULL
for (i in 1:length(results_location)) {
  file <- results_location[i]
  data <- read.csv(file)
  epoch_value <-
    0.1 * data$metrics.mAP50.B. + 0.9 * data$metrics.mAP50.95.B.
  index_max <- which.max(epoch_value)
  if (is.null(res)) {
    res = data[index_max, ]
    res[1,"name"] <- results_names[i]
    print(res)
  } else{
    res[nrow(res) + 1, ] = data[index_max, ]
    res[nrow(res), "name"] <- results_names[[i]]
  }
  print(nrow(res))
}

# Install ggplot2 package if not already installed
# install.packages("ggplot2")

# Load ggplot2 package
library(ggplot2)
generate_bar_plot <- function(data, data_column,title, label_column = "name") {

  # Check if the required columns exist in the data frame
  if (!(label_column %in% names(data) && data_column %in% names(data))) {
    stop("Specified columns not found in the data frame.")
  }

  # Determine the color scale limits based on the data_column
  scale_limits <- range(data[[data_column]])

  # Create the bar plot using ggplot2 with x and y axes switched
  plot <- ggplot(data, aes_string(x = data_column, y = label_column, fill = data[[data_column]])) +
    geom_bar(stat = "identity", color = "black") +
    scale_fill_viridis_c(
      limits = scale_limits
    ) +
    geom_text(aes(label = sprintf("%.2f", data[[data_column]])),
              #position = position_stack(vjust = 1.05),  # Adjust the vjust parameter
              nudge_x = 1,
              color = "black",
              size = 3) +
    labs(title = title,
         x = data_column,
         y = label_column) +
    theme_minimal()

  # Print the plot
  return(plot)
}


# Example usage:
# generate_bar_plot(res, "metrics.mAP50.B.", "your_label_column")
factor <- 2
names <- names(res)
for(name in names){
  if(name != "name"){
  plot <- generate_bar_plot(res,name,title =DATASET_NAME)
  ggsave(
    filename = file.path("visualizations",DATASET_NAME,paste0(name,".png")),
    plot = plot,
    width = 16 * factor,
    height = 9 * factor,
    units = "cm"
  )
  cat("Saved: ",name,"\n")
  }
}

# Example usage:
# Replace 'your_data_frame', 'label_column_name', and 'data_column_name' with actual values
# generate_bar_plot(your_data_frame, "label_column_name", "data_column_name")
