import json
import torch
import os
from torch import nn
import torch.nn.functional as F
import numpy as np
import pandas as pd
import boto3

s3 = boto3.client("s3")


# Autoencoder model definition
class AutoEncoder(nn.Module):
    def __init__(self, in_fea, h1, latent_size, d_output, drop_rate):
        super(AutoEncoder, self).__init__()
        self.l1 = nn.Linear(in_fea, h1)
        self.l2 = nn.Linear(h1, latent_size)
        self.l3 = nn.Linear(latent_size, h1)
        self.l4 = nn.Linear(h1, in_fea)
        self.lpredict = nn.Linear(latent_size, d_output)
        self.drop = nn.Dropout(drop_rate)
        self.act1 = nn.Tanh()
        self.act2 = nn.Sigmoid()

    def forward(self, x):
        x1 = self.drop(F.relu(self.l1(x)))
        embedding = F.relu(self.l2(x1))
        x2 = F.relu(self.l3(embedding))
        x3 = self.l4(x2)
        xpredict = self.lpredict(embedding)
        return x3, embedding, xpredict


# Load the trained model
def load_model():
    in_fea = 691
    h1 = 512
    latent_size = 128
    d_output = 1
    drop_rate = 0.5
    model = AutoEncoder(in_fea, h1, latent_size, d_output, drop_rate)
    model.load_state_dict(torch.load("best_model.pt", map_location=torch.device("cpu")))
    model = model.double()
    model.eval()
    return model


# Read and process the CSV file from the API Gateway event
def process_csv(file_content):
    descriptors_data = pd.read_csv(file_content)
    descriptors_data_processed = descriptors_data.dropna(axis=1)
    CAS_values = descriptors_data_processed.iloc[:, 0]
    HC50 = descriptors_data_processed.iloc[:, 1].to_numpy()
    descriptors = descriptors_data_processed.iloc[:, 2:].to_numpy()

    # Normalize the test data based on the training set statistics
    mean = np.mean(descriptors, axis=0)
    std = np.std(descriptors, axis=0)
    descriptors = (descriptors - mean) / std
    descriptors[np.isnan(descriptors)] = 0
    descriptors[np.isinf(descriptors)] = 0

    return descriptors, CAS_values, HC50


# Lambda handler function
def handler(event, context):
    # Decode the base64 encoded file content
    body = event["body"]
    fileName = json.loads(body)["fileName"]
    path = f"/tmp/${fileName}"
    bucket_name = os.environ["BUCKET_NAME"]
    s3.download_file(Bucket=bucket_name, Key=fileName, Filename=path)

    model = load_model()

    # Process CSV
    descriptors, _, _ = process_csv(path)

    # Predictions
    predictions = []
    for sample in descriptors:
        sample_tensor = torch.tensor(sample, dtype=torch.double)
        _, _, predicted_hc50 = model(sample_tensor)
        predictions.append(predicted_hc50.item())

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "X-Requested-With": "*",
        },
        "body": json.dumps(predictions),
    }
