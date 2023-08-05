# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Flower client example using PyTorch for CIFAR-10 image classification."""


import argparse
import timeit
from collections import OrderedDict
from typing import Dict, List, Tuple

import numpy as np
import torch
import torchvision

import flwr as fl

from . import cifar

# pylint: disable=no-member
DEVICE: str = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# pylint: enable=no-member

# Flower Client
class CifarClient(fl.client.NumPyClient):
    """Flower client implementing CIFAR-10 image classification using PyTorch."""

    def __init__(
        self,
        model: cifar.Net,
        trainloader: torch.utils.data.DataLoader,
        testloader: torch.utils.data.DataLoader,
    ) -> None:
        self.model = model
        self.trainloader = trainloader
        self.testloader = testloader

    def get_parameters(self) -> List[np.ndarray]:
        return [val.cpu().numpy() for _, val in self.model.state_dict().items()]

    def set_parameters(self, parameters: List[np.ndarray]) -> None:
        # Set model parameters from a list of NumPy ndarrays.
        state_dict = OrderedDict(
            {
                k: torch.Tensor(v)
                for k, v in zip(self.model.state_dict().keys(), parameters)
            }
        )
        self.model.load_state_dict(state_dict, strict=True)

    def fit(
        self, parameters: List[np.ndarray], config: Dict[str, str]
    ) -> Tuple[List[np.ndarray], int]:
        # Set model parameters
        self.set_parameters(parameters)

        # Train model
        cifar.train(self.model, self.trainloader, epochs=1, device=DEVICE)

        # Return the updated model parameters
        return self.get_parameters(), len(self.trainloader)

    def evaluate(
        self, parameters: List[np.ndarray], config: Dict[str, str]
    ) -> Tuple[int, float, float]:
        # Use provided parameters to update the local model
        self.set_parameters(parameters)

        # Evaluate the updated model on the local dataset
        loss, accuracy = cifar.test(self.model, self.testloader, device=DEVICE)

        # Return the number of evaluation examples and the evaluation result (loss)
        return len(self.testloader), float(loss), float(accuracy)


def main() -> None:
    """Load data, start CifarClient."""

    # Load model and data
    model = cifar.Net()
    model.to(DEVICE)
    trainloader, testloader = cifar.load_data()

    # Start client
    client = CifarClient(model, trainloader, testloader)
    fl.client.start_numpy_client("[::]:8080", client)


if __name__ == "__main__":
    main()
