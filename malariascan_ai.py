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

train_paths, rest_paths, train_labels, rest_labels = train_test_split(
 all_paths, all_labels, test_size=0.30, stratify=all_labels, random_state=SEED)
val_paths, test_paths, val_labels, test_labels = train_test_split(
 rest_paths, rest_labels, test_size=0.50, stratify=rest_labels, random_state=SEED)

AUTO = tf.data.AUTOTUNE
train_stream = tf.data.Dataset.from_tensor_slices(
 (train_paths, train_labels.astype("float32")))
train_stream = train_stream.shuffle(len(train_paths), seed=SEED)

train_stream = train_stream.map(lambda path, label: (
 tf.image.resize(tf.io.decode_image(tf.io.read_file(path), channels=3,
 expand_animations=False), (CELL_SIZE, CELL_SIZE)) / 255.0,
 label), num_parallel_calls=AUTO)
train_stream = train_stream.cache()

random_flip_left_right random_flip_up_down rot90 (0, 90, 180 or 270 degrees)
random_brightness(0.08) random_saturation(0.85 - 1.15) clip_by_value(0, 1)

train_stream = train_stream.batch(BATCH).prefetch(AUTO)
val_stream = ... read -> resize -> /255 -> cache -> batch -> prefetch
test_stream = ... read -> resize -> /255 -> cache -> batch -> prefetch
