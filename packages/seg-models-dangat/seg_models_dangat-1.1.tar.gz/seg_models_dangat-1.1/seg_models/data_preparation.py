import os
import tifffile as tiff
import pandas as pd
import numpy
import re
import numpy
import random
import pickle as pkl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from datetime import datetime
from matplotlib import gridspec
from sklearn.model_selection import train_test_split
from tqdm import tqdm_notebook as tqdmn
from skimage.transform import resize
from keras.preprocessing.image import img_to_array, load_img

class DataPreparation():

    """ This class is created to read, organize
    and load images in order to models could be trained and compared 
    each one to rest.
    """

    def __init__(self, Trained=False):
        
        self.trained = Trained
        self.df = pd.DataFrame({})


    def read_data(self, inpath):
        """ Split data into two sets: TRAIN and TEST sets

        Args:
            self.inpath (string): Indicate the path where train images is allocated.
                This path must point out two folders: 
                    1. images (folder) where images for training are allocated.
                    2. masks_extent (folder) where masks of images in 1. are allocated.

        Returns:
            df (DataFrame) : A dataframe with all images corresponding to train set
                                   including their corresponding masks_extents.
        """

        if os.path.exists(inpath):
            self.inpath = inpath
            train_mask_list = [ mask for mask in os.listdir(os.path.join(self.inpath, "masks_extent")) ]
            train_image_list = [ img for img in os.listdir( os.path.join( self.inpath, "images" ) ) ]
            df = pd.DataFrame( {  "image": train_image_list,
                                  "mask": train_mask_list
                               } )
            df["Via"] = df["mask"].apply(lambda via: "1" if via.endswith("1.tif") else "0" )
            print(f"No. of images (with road/ no road) for tranining step:\n{df['Via'].value_counts(dropna=False)}")
            
            self.df =  df

            return self.df

        else:
            return "Training path was not expected, please check your path for training images"
               


    def __repr__(self):
        """
        This method prints the main description about 
        DataPreparation instance object
        
        """
        return "DataPreparation Instance Object created"



    def split_alldata(self, semilla=123, test_size=0.2, sample_no=421):
        """ This method split the data in TRAIN and TEST sets. 
        
        Args:
            
            semilla (int): Is an OPTIONAL argument in order to execute the function 
            more than once to produce the same splitting tasks with same data. 
            
            test_size (int): Is an OPTIONAL Value of data proportion during splitting tasks for test set.
            sample_no (int): Is an OPTIONAL Value to show consistency between image and mask names.
            
        Returns:
           x_train (Serie): Is a Serie of all images names for train set.
           x_test  (Serie): Is a Serie of all images names for test set.
           y_train (Serie): Is a Serie of all masks names for train set.
           y_test  (Serie): Is a Serie of all masks names for test set.
        
        """

        if len(self.df) != 0:
            x_train, x_test, y_train, y_test = train_test_split(self.df["image"],
                                                                self.df["mask"], 
                                                                test_size=test_size,
                                                                stratify=self.df["Via"],
                                                                random_state=semilla
                                                                )
            print("Size of x_train: {}".format(x_train.shape))
            print("Size of x_test: {}".format(x_test.shape))
            print("Size of y_train: {}".format(y_train.shape))
            print("Size of y_test: {}".format(y_test.shape))

            print("----"*20)
            
            print("Example of a sample from train dataset with:\nimage: {}\nmask: {}\n"\
                          .format(x_train.iloc[sample_no], y_train.iloc[sample_no]))
            self.x_train = x_train
            self.x_test = x_test
            self.y_train = y_train
            self.y_test = y_test

            return self.x_train, self.x_test, self.y_train, self.y_test

            

        else:
            return "There is no data to split"

    
    def plot_samples(self, num_of_samples=3):
        """ 
        This illustrates some samples from the original image
        , its overlapping and corresponding masks.
        
        Args:
            num_of_samples (int):  Number of samples to show on figure.

        Returns:
            None

        """
        if num_of_samples > 0 and num_of_samples:
            
            fig = plt.figure(figsize=(5*num_of_samples, 5*num_of_samples))
            gs = gridspec.GridSpec( nrows=num_of_samples, 
                                    ncols=2,
                                    height_ratios=[.5 for i in range(num_of_samples)]
                                  )
            ax = [np.nan for i in range(num_of_samples*2)]
            
            for i in range(0, num_of_samples):
                
                num_r = random.randint(0, self.df.shape[0])
                #img = mpimg.imread(os.path.join(self.inpath, 'images', self.df["image"].iloc[num_r]))
                img = tiff.imread(os.path.join(self.inpath, 'images', self.df["image"].iloc[num_r]))
                img = img / 65535.0
                img = 255.0 * img
                img = img.astype(np.int)
                ax[i] = fig.add_subplot(gs[i, 0])
                ax[i].imshow(img[:,:,1]) # Shows only second channel
                ax[i].set_title("BRN sample")
                #plt.colorbar(ticks=[0.1, 0.3, 0.5, 0.7], orientation='horizontal')

                mask = mpimg.imread(os.path.join(self.inpath, 'masks_extent', self.df["mask"].iloc[num_r]))
                ax[i+1] = fig.add_subplot(gs[i, 1])
                maskplot = plt.imshow(mask)
                ax[i+1].set_title("MASK sample")
                #plt.colorbar(ticks=[0.1, 0.3, 0.5, 0.7], orientation='horizontal')
            plt.axis("off")
            plt.show()
        else:
            return "you must insert at least an integer value > 0 in order to plot it"
        
    def read_images(self, inpath, xt, yt, set_type):
        """ This method Read and Store all .tiff train images into Tensors 
    
        Args:
            inpath (string): A string indicating the basepath where train images are located.
            xt (Serie): A serie containing all images names for training.
            yt (Serie): A serie containing all masks names for training.

        Returns:
            self.X (tensor): Tensor of dimension [ len(self.x_train), im_height, im_width, 1) ]
            self.Y (tensor): Tensor of dimension [ len(self.y_train), im_height, im_width, 1) ]
    
        """
        self.inpath = inpath
        
        print(xt.iloc[0])

        height_im = 128
        width_im = 128
        
        if not os.path.exists('source_data'):
            os.mkdir('source_data')
        
        train_data_pkl = os.path.join('source_data', "X_Y_train_data.pkl" )
        train_list_pkl = os.path.join('source_data', 'x_and_y_train_lists.pkl')
        test_data_pkl = os.path.join('source_data', "X_Y_test_data.pkl" )
        test_list_pkl = os.path.join('source_data', "x_and_y_test_lists.pkl")

        if set_type == "train" and os.path.exists(train_list_pkl):

            with open(train_list_pkl, 'rb') as xt_list:
                [xt_saved, yt_saved] = pkl.load(xt_list)

            # Check if xt is a new one list of images names for training 
            #   and checking whether pkl file for train data exists.
            if set(xt.tolist()[0]) == set(xt_saved.tolist()[0]) and os.path.exists(train_data_pkl):
                with open(train_data_pkl, 'rb') as rf:
                    [ self.X, self.Y ] = pkl.load( rf )
                print("data for train set is ready to use")

        elif set_type == "test" and os.path.exists(test_list_pkl):

            with open(test_list_pkl, 'rb') as xtest_list:
                [xtest_saved, xtest_saved] = pkl.load(xtest_list)
            
            # Check if xt is a new one list of images names for test set
            #   and checking whether okl file for test set data exists.
            if set(xt.tolist()[0]) == set(xtest_saved.tolist()[0]) and os.path.join.exists(test_data_pkl):
                with open(test_list_pkl, 'rb') as rf:
                    [ self.X, self.Y ] = pkl.load(rf)
        else:
            self.X = np.zeros( ( len(xt), height_im, width_im, 1 ), dtype=np.float16 ) 
            self.Y = np.zeros( ( len(yt), height_im, width_im, 1 ), dtype=np.float16 )

            print("Shape of self.X: {}".format(self.X.shape))
            print("Shape of self.Y: {}".format(self.Y.shape))

            for n, _ in enumerate( tqdmn(xt, total=len(xt))):
            
                # Loading image n-th from xt serie
                img = tiff.imread(os.path.join(self.inpath, 'images', xt.iloc[n]))
                img = resize( img, ( 128, 128, 1 ), mode='constant', preserve_range=True)
                self.X[n] = img / 65535.0
            
                # Loading mask n-th from yt serie
                mask = load_img( os.path.join(self.inpath, 'masks_extent', yt.iloc[n]) )
                mask = img_to_array(mask)
                mask = resize( mask, (128, 128, 1 ), mode='constant', preserve_range=True)
                self.Y[n] = mask / 255.0
            
            if set_type == "train":

                # Saving train data inside a .pkl file
                with open(train_data_pkl, 'wb') as wf:
                    pkl.dump([self.X, self.Y], wf)

                with open(os.path.join('source_data', 'x_and_y_train_lists.pkl'), 'wb') as xt_list:
                    pkl.dump([xt, yt], xt_list)
            
            if set_type == "test":

                # Saving train data inside a .pkl file
                with open(test_data_pkl, 'wb') as wf:
                    pkl.dump([self.X, self.Y], wf)

                with open(os.path.join('source_data', 'x_and_y_test_lists.pkl'), 'wb') as xt_list:
                    pkl.dump([xt, yt], xt_list)

        return self.X, self.Y
