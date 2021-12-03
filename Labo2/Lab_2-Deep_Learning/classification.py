import torch
from torch.optim import optimizer

from datasets.mnist_dataset import MNISTDataset
from models.models import Classifier, ClassifierVariableLayers
from options.classification_options import ClassificationOptions
from utilities import utils
from utilities.utils import init_pytorch, test_classification_model, train_classification_model, classify_images

if __name__ == "__main__":
    options = ClassificationOptions()
    init_pytorch(options)

    # create and visualize the MNIST dataset
    dataset = MNISTDataset(options)
    dataset.show_examples()

    """START TODO: fill in the missing parts"""
    # create a Classifier instance named model
    model = Classifier(options)
    #model = ClassifierVariableLayers(options)

    # define the opimizer
    opt = torch.optim.SGD(model.parameters(), lr=0.1)

    # train the model
    train_classification_model(model,opt,dataset,options)

    """END TODO"""

    # Test the model
    print("The Accuracy of the model is: ")
    test_classification_model(model, dataset, options)
    classify_images(model, dataset, options)

    # save the model
    utils.save(model, options)
