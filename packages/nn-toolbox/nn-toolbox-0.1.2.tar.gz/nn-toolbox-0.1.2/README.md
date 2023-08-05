# A Higher-Level Framework for Deep Learning in PyTorch.

## Introduction

Whenever I do a project, I always have to re-implement everything from scratch. At first, this is helpful because it requires me to really learn the concepts and procedures by heart. However, these chores quickly become irritatingly repetitive. So I create this repository, to store all the useful pieces of code.
<br />
This soon extends to the stuff that I see in papers and want to implement. Finally, as I was implementing some of the more difficult stuff (e.g the callbacks) the awesome fastai course comes out, so I decide to use this opportunity to follow along the lessons, adapting the codes (i.e the notebooks) and the library to suit my existing codebase.

## What can you find here?

I organize the codes into core elements (callbacks, components, losses, metrics, optim, transforms, etc.), and applications (vision, sequence, etc.), each having its own elements directory. Some features include:

* Different components for building Deep Learning models at various levels of complexity (ResNext blocks, RNN cells). This includes many state-of-the-art models (such as Ordered Neuron LSTM) or more obscure and experimental models (ever heard of Deep Neural Decision Forest?)
* Training procedures, implemented as callbacks (such as automatic models checkpointing, learning rate scheduling, training visualization with tensorboard, etc.), optimizers, and metrics
* Dedicated learner for each application to seamlessly control the elements above during training.
* "Model", which handles the inference portion of the neural network that you trained: creating ensembles, test-time augmentation, etc.
* Some simple tests to avoid silly bugs: testing output shape, ability to fit random pair of input and output, Rosenbrock optimization test, etc.

## What do I plan to do in the future?

This toolbox is mainly for personal use, so as needs arise or if I see a neat paper I will implement them. These are currently in my plan (in no particular order):

* More debugging tools, possibly in the form of callbacks
* More testing functionalities (possibly incorporating unit tests, and some standard datasets)
* More colab training utilities
* More neural net architectures, especially non-vision ones
* More optimizers
* Move some of the weirder stuffs into another repository
* Fix bugs as they come up

I also plan to use this toolbox for more personal projects (see the "Some Examples" section).

## How do I use the codes?
To install this package:
```
pip install nn-toolbox
```
Also note that I tend to work on my most recent stuffs on the experimental branch, so you should use this branch for the latest updates.
<br/>
Finally, please be aware that this repository is by nature HIGHLY EXPERIMENTAL, so it can be quite volatile. If you encounter a bug, tell me and I'll take a look at it as soon as I have the chance.
## Some Examples:

For quickstart, take a look at the `classification_template.py` script.

I am currently doing some projects with this toolbox. Some of them are still work in progress, but you can visit my [implementation](https://github.com/nhatsmrt/torch-styletransfer) of arbitrary style transfer for some example usage, or look at some [tests](https://github.com/nhatsmrt/nn-toolbox/tree/experimental/nntoolbox/test).

Other examples include (might be work in progress):

* An image super-resolution system: [GitHub Repository](https://github.com/nhatsmrt/superres)
* A simple baseline (MLP) for ogbn-arxiv task: [Notebook](https://colab.research.google.com/drive/15fPSGUzZI0BFIXgKdGNgyLDABd0je0JX?usp=sharing)
* Several application-specific toolboxes (reinforcement learning, generative models, etc.) (NOT YET RELEASED)

## Contributing
Install the developing dependencies in `requirements-dev.txt`, then hack away and send me a PR!

## Documentation

Please visit https://nhatsmrt.github.io/nn-toolbox/
