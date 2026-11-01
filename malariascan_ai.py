import os
import sys
import random
import numpy as np
import tensorflow as tf

SEED = 42
CELL_SIZE = 96
BATCH = 64
EPOCHS = 25
LEARNING_RATE = 0.001
DECISION_LINE = 0.5
UNSURE_LOW, UNSURE_HIGH = 0.30, 0.70
CELL_CLASSES = ["Uninfected", "Parasitized"]

random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

script_folder = os.path.dirname(os.path.abspath(__file__))
model_file = os.path.join(script_folder, "malariascan_model.keras")
log_file = os.path.join(script_folder, "malariascan_training_log.csv")
Code What it does and why we use it

downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
dataset_folder = None
for folder, sub_folders, files in os.walk(downloads_folder):
 if "Parasitized" in sub_folders and "Uninfected" in sub_folders:
 dataset_folder = folder
 break
if dataset_folder is None:
 print("Could not find the cell images. ...")
 sys.exit()

all_paths, all_labels = [], []
for label_number, class_name in enumerate(CELL_CLASSES):
 class_folder = os.path.join(dataset_folder, class_name)
 png_files = sorted(f for f in os.listdir(class_folder) if f.lower().endswith(".png"))
 all_paths += [os.path.join(class_folder, f) for f in png_files]
 all_labels += [label_number] * len(png_files)
all_paths = np.array(all_paths)
all_labels = np.array(all_labels)

