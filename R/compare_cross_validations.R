# Assuming your data frame is named 'your_data'
preprocessing_1 <- read.csv2("results/cross-validation/original.csv",sep=",", header = TRUE)
preprocessing_2 <- read.csv2("results/cross-validation/original_hsv.csv",sep=",", header = TRUE)
preprocessing_3 <- read.csv2("results/cross-validation/o-bs-tf_hsv.csv",sep=",", header = TRUE)

# Remove rows where 'name' ends with '2'
preprocessing_1 <- your_data[!grepl("2$", your_data$name), ]

combined_data <- rbind(data.frame(Preprocessing = "Preprocessing1", id = 1:10,preprocessing_1),
                       #data.frame(Preprocessing = "Preprocessing2", id = 1:10,preprocessing_2),
                       data.frame(Preprocessing = "Preprocessing3", id = 1:10,preprocessing_3))

library(car)
combined_data$metrics.precision.B. |> as.numeric() -> combined_data$metrics.precision.B.
leveneTest(metrics.precision.B. ~ Preprocessing, data = combined_data)

precision_matrix <- matrix(combined_data$metrics.precision.B., ncol = 1)

# Add the grouping variable to the matrix
precision_matrix <- cbind(precision_matrix, combined_data$preprocessing_group)

# Perform Friedman test
friedman_precision <- friedman.test(metrics.precision.B. ~ Preprocessing | id,data= combined_data)

# Print Friedman test results
print(friedman_precision)
