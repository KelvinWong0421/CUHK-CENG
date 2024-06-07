import os
import argparse
from PIL import Image

import numpy as np
import torch
import torchvision
import torchvision.transforms.functional as TF
import cv2

from model import SRCNN
from utils import *

parser = argparse.ArgumentParser(description="SRCNN super res toolkit")
parser.add_argument("filename", metavar="LR_video", type=str, help="the path to input LR video")
parser.add_argument("--checkpoint", metavar="path_to_checkpoint", type=str, required=True,
                    help="the path to checkpoint")
parser.add_argument("--cuda", action="store_true", help="use CUDA to speed up computation")
opt = parser.parse_args()

# check cuda
if opt.cuda and not torch.cuda.is_available():
    raise Exception("No GPU found, please run without --cuda")

# Load model
device = torch.device("cuda" if opt.cuda and torch.cuda.is_available() else "cpu")
map_location = "cuda:0" if opt.cuda else device
checkpoint = load_checkpoint(opt.checkpoint, map_location)
model = SRCNN()
model.load_state_dict(checkpoint["model_state_dict"])
model.to(device)
model.eval()

# Open video capture
cap = cv2.VideoCapture(opt.filename)
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
output_name = os.path.splitext(opt.filename)[0] + "_sr.mp4"

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_name, fourcc, fps, (frame_width*3, frame_height*3))

# Function to perform super-resolution on a single frame
def super_resolve_frame(frame, model, device):
    with torch.no_grad():
        image = TF.to_tensor(frame).unsqueeze(0).to(device)
        output = model(image)
        output = TF.to_pil_image(output[0].cpu())
    return output

# Process frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    sr_frame = super_resolve_frame(frame, model, device)
    sr_frame = cv2.cvtColor(np.array(sr_frame), cv2.COLOR_RGB2BGR)
    sr_frame = cv2.resize(sr_frame, (frame_width*3, frame_height*3))
    out.write(sr_frame)

# Release video capture and writer
cap.release()
out.release()
cv2.destroyAllWindows()

print("Output HR video saved to '{output}'".format(output=output_name))



#python super_resolve_video.py source.mp4 --checkpoint ./checkpoint.best --cuda