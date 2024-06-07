#
# CSCI3290 Computational Imaging and Vision *
# --- Declaration --- *
# I declare that the assignment here submitted is original except for source
# material explicitly acknowledged. I also acknowledge that I am aware of
# University policy and regulations on honesty in academic work, and of the
# disciplinary guidelines and procedures applicable to breaches of such policy
# and regulations, as contained in the website
# http://www.cuhk.edu.hk/policy/academichonesty/ *
# Assignment 3
# Name : Wong Wai Chun 
# Student ID : 1155173231
# Email Addr : 1155173231@link.cuhk.edu.hk
#

import torch
import torch.nn as nn
import torch.nn.functional as F


class SRCNN(nn.Module):
    def __init__(self):
        super(SRCNN, self).__init__()
        ######################
        # write your code here

        # Conv. Layer 1: Patch extraction
        self.conv1 = nn.Conv2d(3, 64, kernel_size=(9, 9), padding=4)
        self.relu1 = nn.ReLU()
        
        # Conv. Layer 2: Non-linear mapping
        self.conv2 = nn.Conv2d(64, 32, kernel_size=(1, 1))
        self.relu2 = nn.ReLU()
        
        # Conv. Layer 3: Reconstruction
        self.conv3 = nn.Conv2d(32, 3, kernel_size=(5, 5), padding=2)




    def forward(self, x):
        ######################
        # write your code here
        x = F.interpolate(x, scale_factor=3, mode='bicubic', align_corners=True )
        x = self.relu1(self.conv1(x))
        
        # Conv. Layer 2
        x = self.relu2(self.conv2(x))
        
        # Conv. Layer 3
        x = self.conv3(x)
        
        return x  
