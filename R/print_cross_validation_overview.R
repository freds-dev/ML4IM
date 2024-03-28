library(stringr)
dir = "./results/cross-validation/"

files <- list.files(dir)

experiment_ids <- c(
  "o-bs-tf_hsv.csv"                     = "01",
  "o-bs-tf.csv"                         = "02",
  "o-tf-o_hsv.csv"                      = "03",
  "o-tf-o.csv"                          = "04",
  "original_bg-sub_temp_filter_rgb.csv" = "05",
  "original_bg-sub_temp-filter_hsv.csv" = "06",
  "original_bg-sub_temp-filter.csv"     = "07",
  "original_hsv.csv"                    = "08",
  "original.csv"                        = "09",
  "rgbe3.csv"                           = "10"
)


df <- NULL

fitness <- function(data) {
  return(
    data$`metrics.mAP50.95.B.` |> as.numeric() * 0.9 + data$`metrics.mAP50.B.` |> as.numeric() * 0.1
  )
}


c("epoch","metrics.precision.B.","metrics.recall.B.","metrics.mAP50.B.","metrics.mAP50.95.B.") -> parameters

parameter = parameters[5]


for (file in files) {
  csv <- read.csv2(file.path(dir, file), sep = ",")
  if (nrow(csv) != 10) {
    unique_names <- unique(csv$name |> substring(1, 38))
    for (un in unique_names) {
      entries <- grep(un, csv$name, value = T)
      if (length(entries) > 1) {
        csv <- csv[csv$name != entries[1], ]
      }
    }
  }
  fit <- fitness(csv)
  tmp <- data.frame(file = csv[[parameter]])
  names(tmp) <- file
  df <- dplyr::bind_cols(df, tmp)
}

names(df) <- c("(DVS_DVS-BS_DVS-TF)-HSV", "DVS_DVS-BS_DVS-TF", "(DVS_DVS-BS_DVS)-HSV", "DVS_DVS-BS_DVS", "DVS_DVS-BS_DVS-BS-TF_RGB-BS", "(DVS_DVS-BS_DVS-BS-TF)-HSV","DVS_DVS-BS_DVS-BS-TF", "(DVS_DVS_DVS)-HSV", "DVS_DVS_DVS", "RGB-R_RGB-G_RGB-B_DVS")


cat(parameter,"\n")
for(experiment in names(df)){
cat("\t",experiment,":\n")
  cat("\t\tMean:",mean(df[[experiment]] |> as.numeric()),"\n")
  cat("\t\tMax:",max(df[[experiment]] |> as.numeric()),"\n")
  cat("\t\tMin:",min(df[[experiment]] |> as.numeric()),"\n")
  cat("\t\tMedian:",median(df[[experiment]] |> as.numeric()),"\n")
  
}
