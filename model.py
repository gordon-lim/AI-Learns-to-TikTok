import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F
import numpy as np

class EncoderCNN(nn.Module):
    def __init__(self, input_size): # input_size to RNN
        super(EncoderCNN, self).__init__()
        resnet = models.resnet50(pretrained=True)
        for param in resnet.parameters():
            param.requires_grad_(False) # because I'm only training the linear layer
        
        modules = list(resnet.children())[:-1] # replace last linear layer in resnet with my own
        self.resnet = nn.Sequential(*modules)
        self.embed = nn.Linear(resnet.fc.in_features, input_size)

    def forward(self, images):
        features = self.resnet(images)
        features = features.view(features.size(0), -1)
        features = self.embed(features)
        '''
        features.shape[0]==batch_size & features.shape[1]==embed_size
        '''
        return features
    

class DecoderRNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=1):
        super(DecoderRNN, self).__init__()
        #self.embedding = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers=num_layers, batch_first=True)
        self.fc1 = nn.Linear(hidden_size, hidden_size*2)
        self.fc2 = nn.Linear(hidden_size*2, input_size)
        self.num_layers = num_layers
    
    def forward(self, features, pose_coordinates): 
        # features refer to the encoded spectrograms
        print("Features.shape: {}".format(features.shape))
        print("Poses.shape: {}".format(pose_coordinates.shape))
        # Gordon: I think I should combine features and captions into a single input vector
        inputs = torch.cat((features.unsqueeze(1), pose_coordinates[:,:-1]), 1) # KIV
        print("Concat Inputs.shape: {}".format(inputs.shape))
        out, hidden = self.lstm(inputs) # Use default hidden initialisation
        print("Output from LSTM.shape: {}".format(out.shape))
        x = self.fc1(out)
        x = self.fc2(x)
        print("Output from Linear.shape: {}".format(x.shape))
        return x

    def sample(self, inputs, states=None, max_len=225):
        " accepts pre-processed image tensor (inputs) and returns predicted poses (225*50) "
        
        # Govind S commented in Knowledge that this will help reduce repetitive predictions
        states = (torch.randn(self.num_layers, 1, 500), 
                  torch.randn(self.num_layers, 1, 500)) # TODO: Move to CUDA if avail
        
        predicted_poses = []
        h_c = states
        x = inputs
        for i in range(max_len):
        # Step through the sequence one element at a time.
        # after each step, hidden contains the hidden state.
            out, h_c = self.lstm(x, h_c)
            x = self.fc1(out)
            x = self.fc2(x) # 1*1*50
            # remove first and second dimension
            pose = x.squeeze(0)
            pose = pose.squeeze(0)
            # reshape to 25*2
            pose = pose.view(25,2)
            # allow numpy operations by turning off grad
            pose = pose.detach()
            
            predicted_poses.append(pose)
            
        return predicted_poses
        
        