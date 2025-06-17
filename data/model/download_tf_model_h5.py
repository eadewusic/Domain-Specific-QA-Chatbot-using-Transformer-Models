# My Tensorflow model is 356.58 MB which exceeds GitHub's file
# size limit of 100.00 MB and I've used up LFS storage
# Hence using Google Drive approach

import gdown

file_id = ""
output = "data/model/tf_model.h5"

print("Downloading model...")
gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)
print("Download complete!")