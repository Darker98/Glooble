import kagglehub

# Download latest version
path = kagglehub.dataset_download("fabiochiusano/medium-articles")

print("Path to dataset files:", path)