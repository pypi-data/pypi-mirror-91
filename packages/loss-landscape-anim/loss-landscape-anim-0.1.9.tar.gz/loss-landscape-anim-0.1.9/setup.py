# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loss_landscape_anim']

package_data = \
{'': ['*'], 'loss_landscape_anim': ['sample_data/*']}

install_requires = \
['importlib_resources>=5.0.0,<6.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'numpy>=1.19.4,<2.0.0',
 'pytorch-lightning>=1.1.2,<2.0.0',
 'sklearn>=0.0,<0.1',
 'torch>=1.7.1,<2.0.0',
 'torchvision>=0.8.2,<0.9.0',
 'tqdm>=4.56.0,<5.0.0']

setup_kwargs = {
    'name': 'loss-landscape-anim',
    'version': '0.1.9',
    'description': 'Animate the optimization trajectory of neural networks',
    'long_description': '# Animating the Optimization Trajectory of Neural Nets\n\n`loss-landscape-anim` lets you create animated optimization path in a 2D slice of the loss landscape of your neural networks. It is based on [PyTorch Lightning](https://github.com/PyTorchLightning/pytorch-lightning), please follow its suggested style if you want to add your own model.\n\nCheck out my article [Visualizing Optimization Trajectory of Neural Nets](https://towardsdatascience.com/from-animation-to-intuition-visualizing-optimization-trajectory-in-neural-nets-726e43a08d85?sk=dae85760fb921ecacddbe1af903e3c69) for more examples and some intuitive explanations.\n\n## 0. Installation\n\nFrom PyPI:\n\n```sh\npip install loss-landscape-anim\n```\n\nFrom source, you need [Poetry](https://python-poetry.org/docs/#installation). Once you cloned this repo, run the command below to install the dependencies.\n\n```sh\npoetry install\n```\n\n## 1. Basic Examples\n\nWith the provided [spirals dataset](https://github.com/logancyang/loss-landscape-anim/blob/master/sample_images/spirals-dataset.png) and the default multilayer perceptron `MLP` model, you can directly call `loss_landscape_anim` to get a sample animated GIF like this:\n\n```py\n# Use default MLP model and sample spirals dataset\nloss_landscape_anim(n_epochs=300)\n```\n\n<img src="./sample_images/sample_mlp_2l_50n.gif" alt="sample gif 1" title="MLP with two 50-node hidden layers on the Spirals dataset, PCA" align="middle"/>\n\nNote: if you are using it in a notebook, don\'t forget to include the following at the top:\n\n```py\n%matplotlib notebook\n```\n\nHere\'s another example – the LeNet5 convolutional network on the MNIST dataset. There are many levers you can tune: learning rate, batch size, epochs, frames per second of the GIF output, a seed for reproducible results, whether to load from a trained model, etc. Check out the function signature for more details.\n\n```py\nbs = 16\nlr = 1e-3\ndatamodule = MNISTDataModule(batch_size=bs, n_examples=3000)\nmodel = LeNet(learning_rate=lr)\n\noptim_path, loss_steps, accu_steps = loss_landscape_anim(\n    n_epochs=10,\n    model=model,\n    datamodule=datamodule,\n    optimizer="adam",\n    giffps=15,\n    seed=SEED,\n    load_model=False,\n    output_to_file=True,\n    return_data=True,  # Optional return values if you need them\n    gpus=1  # Enable GPU training if available\n)\n```\n\nGPU training is supported. Just pass `gpus` into `loss_landscape_anim` if they are available.\n\nThe output of LeNet5 on the MNIST dataset looks like this:\n\n<img src="./sample_images/lenet-1e-3.gif" alt="sample gif 2" title="LeNet5 on the MNIST dataset, PCA" align="middle"/>\n\n## 2. Why PCA?\n\nThe optimization path almost always fall into a low-dimensional space <sup>[[1]](#reference)</sup>. For visualizing the most movement, PCA is the best approach. However, it is not the best approach for all use cases. For instance, if you would like to compare the paths of different optimizers, PCA is not viable because its 2D slice depends on the path itself. The fact that different paths result in different 2D slices makes it impossible to plot them in the same space. In that case, 2 fixed directions are needed.\n\n## 3. Random and Custom Directions\n\nYou can also set 2 fixed directions, either generated at random or handpicked.\n\nFor 2 random directions, set `reduction_method` to `"random"`, e.g.\n\n```py\nloss_landscape_anim(n_epochs=300, load_model=False, reduction_method="random")\n```\n\nFor 2 fixed directions of your choosing, set `reduction_method` to `"custom"`, e.g.\n\n```py\nimport numpy as np\n\nn_params = ... # number of parameters your model has\nu_gen = np.random.normal(size=n_params)\nu = u_gen / np.linalg.norm(u_gen)\nv_gen = np.random.normal(size=n_params)\nv = v_gen / np.linalg.norm(v_gen)\n\nloss_landscape_anim(\n    n_epochs=300, load_model=False, reduction_method="custom", custom_directions=(u, v)\n)\n```\n\nHere is an sample GIF produced by two random directions:\n\n<img src="./sample_images/random_directions.gif" alt="sample gif 3" title="MLP with 1 50-node hidden layer on the Spirals dataset, random directions" align="middle"/>\n\nBy default, `reduction_method="pca"`.\n\n## 4. Custom Dataset and Model\n\n1. Prepare your `DataModule`. Refer to [datamodule.py](https://github.com/logancyang/loss-landscape-anim/blob/master/loss_landscape_anim/datamodule.py) for examples.\n2. Define your custom model that inherits `model.GenericModel`. Refer to [model.py](https://github.com/logancyang/loss-landscape-anim/blob/master/loss_landscape_anim/model.py) for examples.\n3. Once you correctly setup your custom `DataModule` and `model`, call the function as shown below to train the model and plot the loss landscape animation.\n\n```py\nbs = ...\nlr = ...\ndatamodule = YourDataModule(batch_size=bs)\nmodel = YourModel(learning_rate=lr)\n\nloss_landscape_anim(\n    n_epochs=10,\n    model=model,\n    datamodule=datamodule,\n    optimizer="adam",\n    seed=SEED,\n    load_model=False,\n    output_to_file=True\n)\n```\n\n## Reference\n\n[1] [Visualizing the Loss Landscape of Neural Nets](https://arxiv.org/abs/1712.09913v3)\n',
    'author': 'LoganYang',
    'author_email': 'logancyang@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/logancyang/loss-landscape-anim',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
