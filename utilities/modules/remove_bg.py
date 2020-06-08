import cv2
import os
import shutil
import numpy as np


ROOT_DIR = "../.."

SRC_FOLDER = f"{ROOT_DIR}/utilities/training_data/raw"
TRAIN_FOLDER_NO_BG = f"{ROOT_DIR}/utilities/training_data/training_no_bg"

src_folder = SRC_FOLDER
train_folder = TRAIN_FOLDER_NO_BG

def remove_background(image_rgb, start_x=0, start_y=0, width=150, height=150):
    # Convert to RGB
#     image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    # Rectange values: start x, start y, width, height
    rectangle = (start_x, start_y, width, height)
    # Create initial mask
    mask = np.zeros(image_rgb.shape[:2], np.uint8)
    # Create temporary arrays used by grabCut
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    # Run grabCut
    cv2.grabCut(image_rgb, # Our image
                mask, # The Mask
                rectangle, # Our rectangle
                bgdModel, # Temporary array for background
                fgdModel, # Temporary array for background
                5, # Number of iterations
                cv2.GC_INIT_WITH_RECT) # Initiative using our rectangle
    # Create mask where sure and likely backgrounds set to 0, otherwise 1
    mask_2 = np.where((mask==2) | (mask==0), 0, 1).astype('uint8')
    # Multiply image with new mask to subtract background
    image_rgb_nobg = image_rgb * mask_2[:, :, np.newaxis]
    return image_rgb_nobg
    
# Loop through each subfolder in the input folder
def img_process(src_folder=SRC_FOLDER, train_folder=TRAIN_FOLDER_NO_BG):
    for root, folders, files in os.walk(src_folder):
        for sub_folder in folders:
            print('processing folder ' + sub_folder)
            # Create a matching subfolder in the output dir
            save_folder = os.path.join(train_folder,sub_folder)
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            # Loop through the files in the subfolder
            file_names = os.listdir(os.path.join(root,sub_folder))
            for file_name in file_names:
                # Open the file
                file_path = os.path.join(root,sub_folder, file_name)
#               print("reading " + file_path)
                # Create a gray version and save it
                image_rgb = cv2.imread(file_path)
                image_rgb_nobg = remove_background(image_rgb, 23, 23, 110, 125)
                save_as = os.path.join(save_folder, file_name)
                cv2.imwrite(save_as, image_rgb_nobg)
#             print("writing " + save_as)
#             image_rgb_nobg.save(save_as)

def dump_process(src_folder, train_folder):
    list_img = os.listdir(src_folder)
    save_folder = train_folder
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    for file_name in list_img:
        # Open the file
        file_path = os.path.join(src_folder, file_name)
#       print("reading " + file_path)
        # Create a gray version and save it
        image_rgb = cv2.imread(file_path)
        image_rgb_nobg = remove_background(image_rgb, 23, 23, 110, 125)
        save_as = os.path.join(save_folder, file_name)
        cv2.imwrite(save_as, image_rgb_nobg)