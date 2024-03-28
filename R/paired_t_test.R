# Expected better score path
preprocessing_1_path = "./results/cross-validation/original_bg-sub_temp-filter.csv"

#Expected worse score path
preprocessing_2_path = "./results/cross-validation/rgbe3.csv"

#Paramer
params = c("metrics.precision.B.","metrics.recall.B.", "metrics.mAP50.B.", "metrics.mAP50.95.B.", "fitness")

data_1 = read.csv2(preprocessing_1_path,sep = ",")
data_2 = read.csv2(preprocessing_2_path,sep = ",")

fitness_1 = data_1$metrics.mAP50.B. |> as.numeric() * 0.1 + data_1$metrics.mAP50.95.B. |> as.numeric() * 0.9
fitness_2 = data_2$metrics.mAP50.B. |> as.numeric() * 0.1 + data_2$metrics.mAP50.95.B. |> as.numeric() * 0.9

t.test(fitness_1,fitness_2, paired = T, alternative = "greater") |> print()
