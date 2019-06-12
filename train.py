# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 16:17:39 2019

@author: ryan4
"""

from IAINet import IAINet
from sklearn.model_selection import KFold
from keras.optimizers import SGD
from keras.utils import plot_model
import pickle

def train_model(train_imgs, train_labels, n_dim):
    """
    Train IAINet
    """    
    
    print("Setting up model...")
    model = IAINet((n_dim,n_dim,3))
    plot_model(model, to_file='model.png')
    print(model.summary())
    
    #Set up K-Fold cross-validation due to lack of data
    folds = 5
    kf = KFold(folds, shuffle = True)
    fold = 1
    
    print("Training...")
    
    for train_index, val_index in kf.split(train_imgs):
        #K-1 used for training, last K fold used for testing/validation
        data_train, data_val = train_imgs[train_index], train_imgs[val_index]
        labels_train, labels_val = train_labels[train_index], train_labels[val_index]
    
        model.compile(loss='binary_crossentropy',optimizer=SGD(lr=0.01,momentum=0.9,decay=1e-6), metrics=["accuracy"])    
        history = model.fit(data_train,labels_train,epochs=50,verbose=1,validation_data=(data_val,labels_val))
        model.save("Fold%s.h5" % fold)
        fold += 1
        
    with open('trainHistoryDict', 'wb') as file_pi:
        pickle.dump(history.history, file_pi)