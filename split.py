#REMPLACER COLUMNWANTED PAR LE LABEL DES IMAGES
import os
import shutil
import glob
import random

def img_split_tt(train_size): #source_dir, train_size

    osget = os.getcwd()
    #print (osget)
    sep = os.sep
    source_dir = os.path.join(osget, 'alphabet-dataset' + sep) #osget + sep + 'alphabet-dataset' + sep
    #print(source_dir)
    # Create empty data folder with train and test folder if not exists
    os.makedirs(osget + sep + "data" + sep + "test" + sep, exist_ok=True)
    os.makedirs(osget + sep + "data" + sep + "train" + sep, exist_ok=True)
    
    train = osget + sep + "data" + sep + "train" + sep
    test = osget + sep + "data" + sep + "test" + sep
    
    #print(train)
    #print(test)


    # Get the subdirectoris folder in source_dir image folder
    for folder in os.listdir(source_dir):
        if os.path.isdir(os.path.join(source_dir, folder)):

            images = glob.glob(pathname= str(source_dir + folder + '/*.png'))
            train_subdir = osget + sep + "data" + sep + "test" + sep + folder + sep
            test_subdir = osget + sep + "data" + sep + "train" + sep + folder + sep

            #Create subdirectories in train and test folders
            os.makedirs(train_subdir, exist_ok=True)
            os.makedirs(test_subdir, exist_ok=True)
            
            # Randomly copy image to train or test folder
            train_img_count = 0
            test_img_count = 0
            for image in images:
                if random.uniform(0, 1) <= train_size:
                    shutil.copy(image, train_subdir)
                    train_img_count +=1
                else:
                    shutil.copy(image, test_subdir)
                    test_img_count +=1
        
        #Display copied images
        print(os.path)
        print('Copied '+ str( train_img_count) +' images in '+train_subdir)
        print('Copied '+ str( test_img_count) +' images in '+test_subdir)


img_split_tt(0.66)