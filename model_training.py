# -*- coding: utf-8 -*-
"""notebook63f3923925

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/notebook63f3923925-32473b10-5224-451c-9f5f-7b9b6905d101.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240324/auto/storage/goog4_request%26X-Goog-Date%3D20240324T093211Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D80afad0b8c1d534629057212f754a7f1d24bf65582e8687c41f92e0a53efd3d873db554ac92b33da0a903fdd8abf2b564261f7bea0614ce5119a0fe5a381e1908d5c9ba49f12a1fc0b1b50f466d4b1a8bad957e8339cfe453b401da9ee658955588e53f2dbaa270642a5f5c0f1a377542fe1fb711d789ae154119f173612d5da17b82dc40d1e283bea500faf429190934b1f6b349dbe8fe3d567592811e8faf66f92600493128acd5ad44ed8b6cae6e3fc0c3f5a90ea80fefd67aa404dbe9c3f9373b17d36353adffffb69d8e3058793c980e27d87f883886aecb1170e61a4be3413ac514923f89326d56e16de7cdd0b18e9363e8db6d3027fcca1310423139f
"""



!pip3 install face_recognition

import seaborn as sn
import torch
from torch.autograd import Variable
import time
import os
import sys
from torch import nn
from torchvision import models
import random
import pandas as pd
from sklearn.model_selection import train_test_split
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
import numpy as np
import cv2
import matplotlib.pyplot as plt
import face_recognition
import json
import glob

# Code to crop only the faces in the videos for training

import os
import cv2
import glob
import face_recognition
from tqdm import tqdm

def create_face_videos(input_dir, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get the list of video files in the input directory
    video_files = glob.glob(os.path.join(input_dir, '*.mp4'))

    # Iterate through each video file
    for video_path in tqdm(video_files):
        # Construct the output video path
        output_path = os.path.join(output_dir, os.path.basename(video_path))

        # Check if the output video already exists, skip if it does
        if os.path.exists(output_path):
            print("File already exists:", output_path)
            continue

        # Open the video file
        video_capture = cv2.VideoCapture(video_path)

        # Initialize video writer for the output video
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (112, 112))

        # Loop through each frame in the video
        while True:
            # Read the next frame
            ret, frame = video_capture.read()

            # If no more frames, break the loop
            if not ret:
                break

            # Detect faces in the frame
            face_locations = face_recognition.face_locations(frame)

            # If faces are found, crop and resize them and write to output video
            for face_location in face_locations:
                top, right, bottom, left = face_location
                face = frame[top:bottom, left:right]
                face = cv2.resize(face, (112, 112))
                out.write(face)

        # Release the video capture and writer objects
        video_capture.release()
        out.release()

        print("Face video saved:", output_path)

input_dir = '/kaggle/input/train-dataset/'
output_dir = '/kaggle/working/face_cropped_videos/'

create_face_videos(input_dir, output_dir)

from torch.utils.data.dataset import Dataset

class create_dataset(Dataset):
    def __init__(self,input_videos_path, labels,sequence_length = None,transformations = None):
        self.input_videos_paths = input_videos_path
        self.labels = labels
        self.transformations = transformations
        self.sequence_length = sequence_length
    def __len__(self):
        return len(self.input_videos_path)
    def __getitem__(self,idx):
        video_path = self.input_videos_path[idx]
        frames = []
        current_video_name = video_path.split('/')[-1]
        label = self.labels.iloc[(labels.loc[labels["file"] == current_video_name].index.values[0]),1]
        if label == 'REAL':
            label = 1
        else:
            label = 0
        for i,frame in enumerate(self.extract_frames(video_path)):
          frames.append(self.transformations(frame))
          if(len(frames) == self.sequence_length):
            break
        frames = torch.stack(frames)
        return frames,label
    def extract_names(self,path):
      video_object = cv2.VideoCapture(path)
      while True:
          result, image = video_object.read()
          if result:
              yield image

# Input the data into data loader

import random
import pandas as pd
from sklearn.model_selection import train_test_split

headers_for_csv = ["file","label"]
labels = pd.read_csv('/kaggle/input/labels/labels.csv',names=headers_for_csv)

train_video_files = glob.glob('/kaggle/input/train_dataset/*.mp4')
test_video_files = glob.glob('/kaggle/input/test_dataset/*.mp4')


print("No of training videos: " + len(train_video_files))
print("No of testing videos: " + len(test_video_files))

im_size = 120
mean = [0.450, 0.450, 0.450]
std = [0.220, 0.220, 0.220]

transformations = transforms.Compose([
                                        transforms.ToPILImage(),
                                        transforms.Resize((im_size,im_size)),
                                        transforms.ToTensor(),
                                        transforms.Normalize(mean,std)])

train_data = create_dataset(train_video_files,labels,sequence_length = 20,transform = train_transforms)
val_data = video_dataset(test_video_files,labels,sequence_length = 20,transform = train_transforms)
train_loader = DataLoader(train_data,batch_size = 4,shuffle = True,num_workers = 4)
valid_loader = DataLoader(val_data,batch_size = 4,shuffle = True,num_workers = 4)

# Creation of model

from torch import nn
from torchvision import models

class Model(nn.Module):
    def __init__(self, num_classes,latent_dim= 2048, lstm_layers=1 , hidden_dim = 2048, bidirectional = False):
        super(Model, self).__init__()
        model = models.resnext50_32x4d(pretrained = True) #Residual Network CNN
        self.model = nn.Sequential(*list(model.children())[:-2])
        self.lstm = nn.LSTM(latent_dim,hidden_dim, lstm_layers,  bidirectional)
        self.relu = nn.LeakyReLU()
        self.dp = nn.Dropout(0.4)
        self.linear1 = nn.Linear(2048,num_classes)
        self.avgpool = nn.AdaptiveAvgPool2d(1)
    def forward(self, x):
        batch_size,seq_length, c, h, w = x.shape
        x = x.view(batch_size * seq_length, c, h, w)
        fmap = self.model(x)
        x = self.avgpool(fmap)
        x = x.view(batch_size,seq_length,2048)
        x_lstm,_ = self.lstm(x,None)
        return fmap,self.dp(self.linear1(torch.mean(x_lstm,dim = 1)))

# Create an instance of the model class with 2 output classes

model = Model(2).cuda()

# Commented out IPython magic to ensure Python compatibility.
# Define train and validation epochs

def train_epoch(epoch, num_epochs, data_loader, model, criterion, optimizer):
    model.train()
    losses = AverageMeter()
    accuracies = AverageMeter()
    t = []
    for i, (inputs, targets) in enumerate(data_loader):
        if torch.cuda.is_available():
            targets = targets.type(torch.cuda.LongTensor)
            inputs = inputs.cuda()
        _,outputs = model(inputs)
        loss  = criterion(outputs,targets.type(torch.cuda.LongTensor))
        acc = calculate_accuracy(outputs, targets.type(torch.cuda.LongTensor))
        losses.update(loss.item(), inputs.size(0))
        accuracies.update(acc, inputs.size(0))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        sys.stdout.write(
                "\r[Epoch %d/%d] [Batch %d / %d] [Loss: %f, Acc: %.2f%%]"
#                 % (
                    epoch,
                    num_epochs,
                    i,
                    len(data_loader),
                    losses.avg,
                    accuracies.avg))
    torch.save(model.state_dict(),'/content/checkpoint.pt')
    return losses.avg,accuracies.avg
def test(epoch,model, data_loader ,criterion):
    print('Testing')
    model.eval()
    losses = AverageMeter()
    accuracies = AverageMeter()
    pred = []
    true = []
    count = 0
    with torch.no_grad():
        for i, (inputs, targets) in enumerate(data_loader):
            if torch.cuda.is_available():
                targets = targets.cuda().type(torch.cuda.FloatTensor)
                inputs = inputs.cuda()
            _,outputs = model(inputs)
            loss = torch.mean(criterion(outputs, targets.type(torch.cuda.LongTensor)))
            acc = calculate_accuracy(outputs,targets.type(torch.cuda.LongTensor))
            _,p = torch.max(outputs,1)
            true += (targets.type(torch.cuda.LongTensor)).detach().cpu().numpy().reshape(len(targets)).tolist()
            pred += p.detach().cpu().numpy().reshape(len(p)).tolist()
            losses.update(loss.item(), inputs.size(0))
            accuracies.update(acc, inputs.size(0))
            sys.stdout.write(
                    "\r[Batch %d / %d]  [Loss: %f, Acc: %.2f%%]"
#                     % (
                        i,
                        len(data_loader),
                        losses.avg,
                        accuracies.avg
                        )
                    )
        print('\nAccuracy {}'.format(accuracies.avg))
    return true,pred,losses.avg,accuracies.avg
class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()
    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
def calculate_accuracy(outputs, targets):
    batch_size = targets.size(0)

    _, pred = outputs.topk(1, 1, True)
    pred = pred.t()
    correct = pred.eq(targets.view(1, -1))
    n_correct_elems = correct.float().sum().item()
    return 100* n_correct_elems / batch_size

# Perform training

from sklearn.metrics import confusion_matrix

lr = 1e-5

num_epochs = 20

optimizer = torch.optim.Adam(model.parameters(), lr= lr,weight_decay = 1e-5)

criterion = nn.CrossEntropyLoss().cuda()
train_loss_avg =[]
train_accuracy = []
test_loss_avg = []
test_accuracy = []
for epoch in range(1,num_epochs+1):
    l, acc = train_epoch(epoch,num_epochs,train_loader,model,criterion,optimizer)
    train_loss_avg.append(l)
    train_accuracy.append(acc)
    true,pred,tl,t_acc = test(epoch,model,valid_loader,criterion)
    test_loss_avg.append(tl)
    test_accuracy.append(t_acc)

