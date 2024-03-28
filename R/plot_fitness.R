dir = "../results/original_bg-sub_temp-filter/"

files <- list.files(dir)

exclude_files <- c("first_run","first_run2")

files <- setdiff(files,exclude_files)


fitness <- function(data) {
  return(
    data$`metrics.mAP50.95.B.` |> as.numeric() * 0.9 + data$`metrics.mAP50.B.` |> as.numeric() * 0.1
  )
}

df <- NULL
for(file in files){
  csv <- read.csv2(file.path(dir,file,"results.csv"), sep = ",")
  fit <- fitness(csv)
  fit <- c(fit, rep(NA, 100 - length(fit)))
  tmp = data.frame(fi = fit)
  names(tmp) = c(file)
  dplyr::bind_cols(df,tmp) -> df
}

nms <- names(df) |> substring(1, 19)
names(df) <- nms
library(ggplot2)
library(tidyr)
df$index <- 1:nrow(df)
df_long <- pivot_longer(df, cols = -index, names_to = "variable", values_to = "value")

write.table(df,"fitness.csv", sep = ",")


# Plotting
plot <- ggplot(df_long, aes(x = index, y = value, color = variable)) +
  geom_line() +
  labs(x = "Epoch", y = "mAP@0.5-0.95 * 0.9 + mAP@0.5 * 0.1", title = "Evolution of fitness values in training", subtitle = "Development of fitness in different elements of cross-validation of experiment 04") +
  xlim(c(1,25)) + 
  theme_minimal() +
  ggplot2::theme(plot.title = element_text(size = 10, face = "bold"), plot.subtitle = element_text(size = 8), text = element_text(family = "Times New Roman"))
  
height_factor <- 1
width_size <- 8.50714756389 * 1.5
ggsave(
  filename ="fitness.png",
  plot = plot,
  width = width_size,
  height = width_size * height_factor,
  units = "cm"
)
