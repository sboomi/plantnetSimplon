"""
Add local directories in the file
"""
import os

ROOT_DIR = os.getcwd()

SRC_FOLDER = f"{ROOT_DIR}/utilities/training_data/raw"
TRAIN_FOLDER = f"{ROOT_DIR}/utilities/training_data/training"
TRAIN_FOLDER_NO_BG = f"{ROOT_DIR}/utilities/training_data/training_no_bg"

UPLOADS_FOLDER = f"{ROOT_DIR}/uploads"
TEST_FOLDER = f"{ROOT_DIR}/uploads/training"