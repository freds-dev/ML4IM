# Expected better score path
preprocessing_1_path = "./results/cross-validation/original_bg-sub_temp-filter.csv"

#Expected worse score path
preprocessing_2_path = "./results/cross-validation/rgbe3.csv"

#Paramer
params = c("metrics.precision.B.","metrics.recall.B.", "metrics.mAP50.B.", "metrics.mAP50.95.B.", "fitness")

data_1 = read.csv2(preprocessing_1_path,sep = ",")
data_2 = read.csv2(preprocessing_2_path,sep = ",")

data_1$fitness = data_1$metrics.mAP50.B. |> as.numeric() * 0.1 + data_1$metrics.mAP50.95.B. |> as.numeric() * 0.9
data_2$fitness = data_2$metrics.mAP50.B. |> as.numeric() * 0.1 + data_2$metrics.mAP50.95.B. |> as.numeric() * 0.9

for(param in params){
  print(param)
  t.test(data_1[[param]] |> as.numeric(), data_2[[param]] |> as.numeric(), paired = T, alternative = "greater") |> print()
}
