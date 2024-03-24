# -*- coding: utf-8 -*-
"""prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/prediction-3b3ec685-029b-452e-9aa9-c58ad5e9bdd5.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240324/auto/storage/goog4_request%26X-Goog-Date%3D20240324T102836Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D1ac0b13ffbb5f27738a13f237f98839892b78ee4efa42b42470e717ab4efbfcc8f9f8941752ad0766556a805f76eb0d78dd734b5ab6d5d0ac55d6988590fbb0b6c05c467e13da961edc293b37096f6b000dc68bf825f61a6dad5f7db6497ea4711f0d7a1bc792a960c29ac78b20712906699d6192744fd65e1d012f845d212223dc73b9d7c883c09af5d19c2ff9382241fd21af21fcfe01b585bbb137455c7d755c5e6992f8ff6cf8404724e4e60f00ed5ea690fac859ec3688ef5ff396d20cfbd4bf9e2b0b4e8e2d7eb572ca48e45bb32ccbed458ea3f8d58cecaec0cf860be3822606810854aaf128a87d8f650e46031f0c44a069898209c4affcd3c9d22ce
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'validate-dataset:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F4659986%2F7928667%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240324%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240324T102836Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D9ad1e4603e3fb539179ae34e88154cc42cdcd8cc717395b9f3b67868eb3f7f9f024a6e636e516073881d075f369be22c150757bde4f76e98ee946375a1f2ded94923c966d232cea52ab028fc7acdfb5d65af2da2b41dfbbfc9bdeb124c20c14b38e0bed809be4fb04ca9baa7707f0fb4a0a44d905e8581019a667fc9cd43ed7b232ab27306dac75f67b39f8bc338f41546455e939470a522ed142c93ac63d9bbd9a011948f9935ea771868564ed3465029ac055d11d0cc2c92200d2f00e1105b3bafb0f616bf57e465d603181811bd58c9d486c2836b2127305ecfa14afbc8fd75a3c23f0f3f5bc43270d02a7b46df8f2edc7050034c6526669a150d9e40ad8e,models:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F4660005%2F7928691%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240324%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240324T102836Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D663284c4d561e68035b5645ebc1b97e9ebdafd14c06518790fd619b248ea627ae8afb5a57632aa42bdf7e993ec184432672f6448ecde5b5cbfcd69cbd56e0d94c638b7c11dfd9cb6f543083c7a2ccb966ff11371e10d333ece3bab4c697ee7fbc229c166284b14172b93ff28492aa5fd04a5b61ee6184314ab2069926349a73a6f7a8501c37fa18219b337f253312383cda8480308b95a374ae6376e9b3bd727a83b08cba1d14c88ed39dd00014202a7dd17827efea6515ddc67d21819e5f0cb70c910016f8ad621c479465d36b72652435c5de7d04d978e4d8c2efaa27d81c8dd62d321777d8be3320651f902cf216b8ca9f1fbeb66698122c35ea82c219c4f,labels-data-used:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F4660123%2F7928848%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240324%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240324T102836Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3Da8a952248d2b0d2a63f87e27c8915cc0771e2ce7767d5d5bf13e35292c3ecac4301f1759ee1d68ef348118449244eca9a0a26720a717fd46c2cd0ae38ac141dba756d116aa200dd965cea6afd609a642f5ce3af8ee8dd9d463c11005ce24d22f641a78fff15786d6066ec24eef56fb581a5f719c4984a45e8c31994a7c9e4b33a91a9bc14adf288b229475c97f93fd750bd5416882ab7768f80b09859ee601d99c784d2fef5ebf892353a405eb0729efcf03ed832ea55a2ad2f50557bca7110a2f45c284e142687dfdf92ec8639ace6489bcad066826b189d80406cc15632c233491407a8b5f4dc9a9f229ea006c3180da3c809bfe3a48b9b7072175f922d955'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

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
import os
import cv2
import glob
import face_recognition
from tqdm import tqdm
import random
import torch
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import face_recognition
import torch
from torch.autograd import Variable
import time
import os
import sys
import os
from torch import nn
from torchvision import models
import torch
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import face_recognition

videos_to_predict = ['/kaggle/input/validate-dataset/ehthgupumf.mp4']
trained_model = '/kaggle/input/models/model.pt'

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

# Load the pre trained model

model.load_state_dict(torch.load(trained_model))
model.eval()

sm = nn.Softmax()
frame_size = 120
mean = [0.450, 0.450, 0.450]
std = [0.220, 0.220, 0.220]

transformations = transforms.Compose([
                                        transforms.ToPILImage(),
                                        transforms.Resize((frame_size,frame_size)),
                                        transforms.ToTensor(),
                                        transforms.Normalize(mean,std)])

class create_dataset(Dataset):
    def __init__(self,input_videos_path, labels,sequence_length = None,transformations = None):
        self.input_videos_path = input_videos_path
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
            face_array = face_recognition.face_locations(frame)
            try:
                top,right,bottom,left = face_array[0]
                frame = frame[top:bottom,left:right,:]
            except:
              pass
            frames.append(self.transformations(frame))
            if(len(frames) == self.sequence_length):
              break
        frames = torch.stack(frames)
        return frames.unsqueeze(0)
    def extract_frames(self,path):
        video_object = cv2.VideoCapture(path)
        while True:
            result, image = video_object.read()
            if result:
              yield image

headers_for_csv = ["file","label"]
labels = pd.read_csv('/kaggle/input/labels-data-used/labels.csv',names=headers_for_csv)
loaded_video_data = create_dataset(videos_to_predict, labels, sequence_length = 20,transformations = transformations)

def predict(model, tensor, output_path='./'):
    logits = model(tensor.to('cuda'))[1]
    logits = sm(logits)
    _, prediction = torch.max(logits, 1)
    confidence = logits[:, int(prediction.item())].item() * 100
    print('Confidence of prediction:', confidence)
    return [int(prediction.item()), confidence]

for i in range(0,len(videos_to_predict)):
  print("Current video: " + videos_to_predict[i])
  result = predict(model, loaded_video_data[i],'./')
  if result[0] == 1:
    print("REAL")
  else:
    print("FAKE")