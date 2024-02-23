project <- "rgbe3"

files <- list.files(file.path("..", "results", project))

example <- files[1]

# Install and load the required packages
library(readr)
library(stringr)

read_yolov7 <- function(path) {
  lines <- read_lines(path)
  if (length(lines) == 1) {
    return(NULL)
  }
  headers <- unlist(str_split(lines[1], "\\s+"))
  lines <- lines[-1]
  data_split <- str_split(lines, "\\s+")
  result <- as.data.frame(do.call(rbind, data_split))
  colnames(result) <- headers
  return(result)
}

result_list <- list()

for (file in files) {
  print(file)
  txt_path <- file.path("..", "results", project, file, "results.txt")
  data <- read_yolov7(txt_path)
  if (!is.null(data)) {
    nms <- data |> names()
    nms[length(nms)] <- nms[length(nms)] |> paste0("_iou")
    names(data) <- nms
    data$name <- file
  }
  result_list[[file]] <- data
}

transform_epoch <- function(data){
  data$epoch <- sapply(strsplit(data$epoch, "/"), function(x) as.numeric(x[1]))
  return(data)
}
df <- NULL
for (result in result_list) {
  epoch_value <-
    0.1 * (result$map50 |> as.numeric()) + 0.9 * (result$map95 |> as.numeric())
  index_max <- which.max(epoch_value)
  print(index_max)
  df <- dplyr::bind_rows(df, result[index_max, ])
}

df <- transform_epoch(df)

rename_column <- function(df, old_col_name, new_col_name) {
  if (old_col_name %in% names(df)) {
    names(df)[names(df) == old_col_name] <- new_col_name
    return(df)
  } else {
    cat("Column '", old_col_name, "' not found in the data frame.\n")
    return(NULL)
  }
}

df <- rename_column(df,"box","train.box_loss") 
df <- rename_column(df,"cla","train.cls_loss")
df <- rename_column(df,"obj","train.cls_loss")
df <- rename_column(df,"p","metrics.precision.B.")
df <- rename_column(df,"r","metrics.recall.B.")
df <- rename_column(df,"map50","metrics.mAP50.B.")
df <- rename_column(df,"map95","metrics.mAP50.95.B.")
df <- rename_column(df,"vbox","val.box_loss") 
df <- rename_column(df,"vcla","val.cls_loss")
df <- rename_column(df,"vobj","val.dfl_loss")
df$lr.pg0 = NA
df$lr.pg1 = NA
df$lr.pg2 = NA

write.csv(df,file = file.path("results","cross-validation",paste0(project,".csv")))

