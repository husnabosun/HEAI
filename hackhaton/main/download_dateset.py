from datasets import load_dataset

# upload dataset from hugging-face
dataset = load_dataset("QuyenAnhDE/Diseases_Symptoms")

dataset["train"].to_csv("symptoms_dataset.csv", index=False)
