
dir = "./results/cross-validation/"

list_files = list.files(dir)

k = 9

csv_data <- read.csv2(file.path(dir,list_files[k]), sep = ",")



print(list_files[k])

c("epoch","metrics.precision.B.","metrics.recall.B.","metrics.mAP50.B.","metrics.mAP50.95.B.") -> parameters

for(i in 1:length(parameters)){
  parameters[i] -> parameter 
  print(paste0("   ",parameter))
  print(paste0("      Max: ",csv_data[[parameter]] |> as.numeric() |> max()))
  print(paste0("      Min: ",csv_data[[parameter]] |> as.numeric() |> min()))
  print(paste0("      Mean: ",csv_data[[parameter]] |> as.numeric() |> mean()))
  print(paste0("      Median: ",csv_data[[parameter]] |> as.numeric() |> median()))
  print(paste0("      Var: ",csv_data[[parameter]] |> as.numeric() |> var()))
}
