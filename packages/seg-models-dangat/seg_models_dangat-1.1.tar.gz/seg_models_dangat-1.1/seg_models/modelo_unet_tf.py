from data_preparation import DataPreparation
import tifffile as tiff
import os
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm_notebook as tqdmn
from skimage.transform import resize
from skimage.morphology import label
from sklearn.model_selection import KFold

import tensorflow as tf
from keras.models import Model, load_model
from keras.layers import Input, BatchNormalization, Activation, Dense, Dropout
from keras.layers.core import Lambda, RepeatVector, Reshape
from keras.layers.convolutional import Conv2D, Conv2DTranspose
from keras.layers.pooling import MaxPooling2D, GlobalMaxPool2D
from keras.layers.merge import concatenate, add
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

###

if tf.config.list_physical_devices('GPU'):
    phys_dev = tf.config.list_physical_devices('GPU')
    tf.config.experimental.set_memory_growth(phys_dev[0], enable=True)
    tf.config.experimental.set_virtual_device_configuration(phys_dev[0], 
                                    [ tf.config.experimental.VirtualDeviceConfiguration(memory_limit=4000) ] )

class ModeloUNET(DataPreparation):
    """ Esta clase es un molde del modelo UNET desde tf.keras"""
    
    def __init__(self, im_height=128, im_width=128, Trained=False):
        DataPreparation.__init__(self, Trained=False)
        self.im_height = im_height
        self.im_width = im_width
    
    def conv2d_block(self, input_tensor, n_filters, kernel_size=3, batchnorm=True):

        """ Add 2 convolutional layers with parameters passed to it """

        # First Layer
        x = Conv2D(filters=n_filters, kernel_size=(kernel_size, kernel_size), \
                kernel_initializer='he_normal', padding='same')(input_tensor)
        if batchnorm:
            x = BatchNormalization()(x)
        x = Activation('relu')(x)

        # Second Layer
        x = Conv2D(filters=n_filters, kernel_size=(kernel_size, kernel_size), \
                kernel_initializer='he_normal', padding='same')(x)
        if batchnorm:
            x = BatchNormalization()(x)
        x = Activation('relu')(x)

        return x
    
    def get_unet(self, input_img, n_filters=16, dropout=0.1, batchnorm=True):

        """ It defines UNET Architecture """

        # Encoder
        c1 = self.conv2d_block(input_img, n_filters = n_filters * 1, kernel_size = 3, batchnorm = batchnorm)
        p1 = MaxPooling2D((2, 2))(c1)
        p1 = Dropout(dropout)(p1)

        c2 = self.conv2d_block(p1, n_filters = n_filters * 2, kernel_size = 3, batchnorm = batchnorm)
        p2 = MaxPooling2D((2, 2))(c2)
        p2 = Dropout(dropout)(p2)

        c3 = self.conv2d_block(p2, n_filters = n_filters * 4, kernel_size = 3, batchnorm = batchnorm)
        p3 = MaxPooling2D((2, 2))(c3)
        p3 = Dropout(dropout)(p3)

        c4 = self.conv2d_block(p3, n_filters = n_filters * 8, kernel_size = 3, batchnorm = batchnorm)
        p4 = MaxPooling2D((2, 2))(c4)
        p4 = Dropout(dropout)(p4)

        c5 = self.conv2d_block(p4, n_filters = n_filters * 16, kernel_size = 3, batchnorm = batchnorm)

        # Decoder
        u6 = Conv2DTranspose(n_filters * 8, (3, 3), strides = (2, 2), padding = 'same')(c5)
        u6 = concatenate([u6, c4])
        u6 = Dropout(dropout)(u6)
        c6 = self.conv2d_block(u6, n_filters * 8, kernel_size = 3, batchnorm = batchnorm)

        u7 = Conv2DTranspose(n_filters * 4, (3, 3), strides = (2, 2), padding = 'same')(c6)
        u7 = concatenate([u7, c3])
        u7 = Dropout(dropout)(u7)
        c7 = self.conv2d_block(u7, n_filters * 4, kernel_size = 3, batchnorm = batchnorm)

        u8 = Conv2DTranspose(n_filters * 2, (3, 3), strides = (2, 2), padding = 'same')(c7)
        u8 = concatenate([u8, c2])
        u8 = Dropout(dropout)(u8)
        c8 = self.conv2d_block(u8, n_filters * 2, kernel_size = 3, batchnorm = batchnorm)

        u9 = Conv2DTranspose(n_filters * 1, kernel_size = (3, 3), strides = (2, 2), padding = 'same')(c8)
        u9 = concatenate([u9, c1])
        u9 = Dropout(dropout)(u9)
        c9 = self.conv2d_block(u9, n_filters * 1, kernel_size = 3, batchnorm = batchnorm)
        
        outputs = Conv2D(1, (1, 1), activation = 'sigmoid')(c9)
        
        return Model(inputs = [input_img], outputs = [outputs])

        
    def model_compiler(self, verbose=False):
        """ This method compile the model with the arcitecture 
            builded in method get_unet
        
        Args: 
            None

        Returns:
            model (tf.keras Model Object)

        """
        input_img = Input((self.im_height, self.im_width, 1), name = 'img')
        model = self.get_unet(input_img, n_filters = 16, dropout = 0.05, batchnorm=True)
        model.compile(optimizer=Adam(), loss = 'binary_crossentropy', metrics = ['accuracy'])

        if verbose:
            model.summary()
        
        return model
    
    def callbacks_params(self, output_path, k):
        return [ EarlyStopping(patience=10, verbose=1),
                 ReduceLROnPlateau(factor=0.1, patience=5, min_lr=0.00001, verbose=1),
                 ModelCheckpoint(os.path.join(output_path, f'model-unet-train_kf_{k}.h5'), verbose=1, save_best_only=True, save_weights_only=True)
                ]

