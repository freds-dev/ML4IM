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
  tmp <- data.frame(file = fit)
  names(tmp) <- file
  df <- dplyr::bind_cols(df, tmp)
}

names(df) <- c("07", "03", "06", "02", "10", "08", "04", "05", "01", "09")

calculate_t_tests <- function(data) {
  num_columns <- sapply(data, is.numeric)
  numeric_data <- data[, num_columns]
  # Reorder columns based on mean
  means <- colMeans(numeric_data)
  sorted_cols <- names(numeric_data)[order(-means)]
  numeric_data <- numeric_data[, sorted_cols]
  
  
  num_vars <- ncol(numeric_data)
  
  results <- matrix(NA, nrow = num_vars, ncol = num_vars)
  
  for (i in 1:(num_vars - 1)) {
    for (j in (i + 1):num_vars) {
      if (is.na(results[i, j])) {
        # Check if pair has already been tested
        t_result <-
          t.test(numeric_data[, i],
                 numeric_data[, j],
                 paired = T,
                 alternative = "greater")
        results[i, j] <- t_result$p.value
      }
    }
  }
  
  colnames(results) <- names(numeric_data)
  rownames(results) <- names(numeric_data)
  
  return(results)
}

results <- calculate_t_tests(df)

# Load required libraries
library(kableExtra)
library(dplyr)
# Function to generate LaTeX code for a table from t-test results using kable and kableExtra
# Function to generate LaTeX code for a table from t-test results using kable and kableExtra
generate_latex_table <- function(results) {
  # Convert results to data frame
  result_df <- as.data.frame(results)
  
  # Initialize LaTeX code with table header
  latex_code <- "\\begin{table}[htbp]\n\\centering\n\\begin{tabular}{"
  for (i in 1:ncol(result_df)) {
    latex_code <- paste0(latex_code, "c")
    if (i < ncol(result_df)) {
      latex_code <- paste0(latex_code, "|")  # Add vertical lines between columns
    }
  }
  latex_code <- paste0(latex_code, "}\n\\hline\n")
  
  # Add column names
  col_names <- colnames(result_df)
  for (col in col_names) {
    latex_code <- paste0(latex_code, col, " & ")
  }
  latex_code <- sub(" & $", " \\\\\n\\hline\n", latex_code)  # Replace the last & with \\
  
  # Add data rows with conditional formatting
  for (i in 1:nrow(result_df)) {
    for (j in 1:ncol(result_df)) {
      if (!is.na(result_df[i, j])) {
        if (result_df[i, j] < 0.05) {
          latex_code <- paste0(latex_code, "\\cellcolor{green!25}{", sprintf("%.4f", result_df[i, j]), "} & ")
        } else {
          latex_code <- paste0(latex_code, "\\cellcolor{red!25}{", sprintf("%.4f", result_df[i, j]), "} & ")
        }
      } else {
        latex_code <- paste0(latex_code, "NA & ")  # Handle NA values
      }
    }
    latex_code <- sub(" & $", " \\\\\n\\hline\n", latex_code)  # Replace the last & with \\
  }
  
  # End LaTeX table
  latex_code <- paste0(latex_code, "\\end{tabular}\n")
  latex_code <- paste0(latex_code, "\\caption{Your caption here.}\n")
  latex_code <- paste0(latex_code, "\\label{tab:yourlabel}\n")
  latex_code <- paste0(latex_code, "\\end{table}")
  
  return(latex_code)
}
latex_code <- generate_latex_table(results)


cat(latex_code)  # Print the LaTeX code to console
