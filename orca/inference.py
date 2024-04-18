import torch
import numpy as np
import zuko

from typing import Tuple

"""
Tools for inference of data using normalizing flows networks.
"""
def prepare_data(theta, psi, batch_size: int = 64, device: str = 'cuda'):
    """
    Prepare data for training a normalizing flow network.
    """
    trainset = torch.utils.data.TensorDataset(psi, theta)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True)

    return trainloader

def train(psi, theta, batch_size: int = 64, 
                      num_transforms : int = 1, 
                      num_hidden : Tuple = (64, 64),
                      max_epochs : int = 1000, 
                      patience : int = 100,
                      max_loss : float = np.inf,
                      lr : float = 1e-3,
                      device : str = 'cuda', 
                      seed : int = 0):

    # Set seed
    torch.manual_seed(seed)

    # Set device
    device = torch.device(device)

    theta = torch.tensor(theta).to(device).float()
    psi = torch.tensor(psi).to(device).float()

    # Prepare data
    trainloader = prepare_data(theta, psi, batch_size=batch_size, device=device)

    num_psi     = psi.shape[1]
    num_theta   = theta.shape[1]

    flow = zuko.flows.MAF(features=num_theta, context=num_psi, transforms=num_transforms, hidden_features=num_hidden).to(device)

    # Train to maximize the log-likelihood
    optimizer = torch.optim.Adam(flow.parameters(), lr=lr)

    k = 0
    for epoch in range(max_epochs):
        losses = []

        for psi, theta in trainloader:

            loss = -flow(psi).log_prob(theta).mean()
            loss.backward()

            optimizer.step()
            optimizer.zero_grad()

            losses.append(loss.detach())

        losses = torch.stack(losses)

        # Control sequence for early stopping
        if losses[-1] < max_loss and k < patience:
            max_loss = losses[-1]
            k = 0
        elif k >= patience:
            print(f"Early stopping at epoch {epoch + 1} due to no improvement in loss")
            break
        else:
            k += 1

        print(f"Epoch {epoch + 1} - Loss: {losses.mean()}", end="\r")

    return flow

def sample(flow, psi, num_samples: int = 1000, device: str = 'cuda'):
    
    psi = torch.tensor(psi).to(device).float()

    with torch.no_grad():
        theta_samples = flow(torch.tensor(psi)).sample((num_samples,))

    return theta_samples.clone().detach()
