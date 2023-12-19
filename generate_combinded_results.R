results_dir <- "./results"

results_names <-
  list.files(results_dir) |> tools::file_path_sans_ext()
results_location <- list.files(results_dir, full.names = T)

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

write.csv(res,"combined-results.csv",sep = ",",row.names = FALSE)
