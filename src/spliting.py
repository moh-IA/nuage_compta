import os
import shutil
import glob
import random




def img_split_train_test(source_dir, train_size):

    # Create empty data folder with train and test folder  if not exists 
    if not os.path.exists("../data"):
        os.makedirs("../data")
    else:
        if not os.path.exists("../data/train"):
            os.makedirs("../data/train")
        if not os.path.exists("../data/test"):
            os.makedirs("../data/test")
    
    # Get the subdirectories folder in source_dir image folder 
    for folder in os.listdir(source_dir):
        if os.path.isdir(os.path.join(source_dir, folder)):

            images =  glob.glob(pathname= str(source_dir + folder + '/*.png'))

            train_subdir = os.path.join("../data/train", folder)
            test_subdir = os.path.join("../data/test", folder)

            # Create subdirectories in train and test folders
            if not os.path.exists(train_subdir):
                os.makedirs(train_subdir)
            if not os.path.exists(test_subdir):
                os.makedirs(test_subdir)
            
            # Randomly copy image to train or test folder 
            train_img_count = 0
            test_img_count = 0
            for image in images:
                if random.uniform(0, 1) <= train_size:
                    shutil.copy(image, train_subdir)
                    train_img_count +=1
                else:
                    shutil.copy(image, test_subdir)
                    test_img_count += 1
    
        # Display copieds images

        print('Copied '+ str( train_img_count) +' images in '+train_subdir)
        print('Copied '+ str( test_img_count) +' images in '+test_subdir)






            





    












