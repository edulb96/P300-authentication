<!-- PROJECT LOGO -->
<br>
<p align="center">
  <a href="https://github.com/edulb96/P300-authentication">
    <img src="CyberDataLab.png" alt="CDL" width="400" height="260">
  </a>
  <h3 align="center">Evaluation of Data Processing and Machine Learning Techniques in P300-based Biometrics using Brain-Computer Interfaces</h3>
</p>

## About the framework

Implementation of a framework for EEG signal acquisition from a BCI, signal processing, and P300-based authentication or identification using trained classifiers. Besides, it deploys a scenario where P300 evoked potentials are generated through the Oddball paradigm and visual stimuli.

This repository contains a related code for the paper Evaluation of Data Processing and Machine Learning Techniques in P300-based Biometrics using Brain-Computer Interfaces.

In this repository there are two directories. The ```acquisition``` directory contains the implemented code for the data acquisition phase, while the ```processing-feature_extraction-datasets_generation-classification``` directory contains the generated code to perform the processing phases, feature extraction, dataset generation, and authentication or identification.

## Acquisition directory

### Prerequisites
* Python version 3.7 or more, pyenv recommended
* pip3
* Pandas version 1.5.2

### Instalation

1. Clone the repo
```sh
git clone https://github.com/edulb96/P300-authentication.git
```
With ```--branch develop``` you will get the developing branch.
```sh
git clone --branch develop https://github.com/edulb96/P300-authentication.git
```
2. Change to project directory
3. (Optional) Create your virtual environment, and activate it (you can also use ```conda``` to create the virtual environment)
```sh
python -m venv env

source env/bin/activate  # Linux/Mac
env/Scripts/activate  # Windows
```
3. Install required packages
```sh
pip3 install -r requirements.txt
```
4. Enter your API in `main.py`
```python
API = ''

```
API used in Mode 2 (automatic mode) to obtain random images in experiments

See the [API documentation](https://unsplash.com/documentation) for more information on how to get your own API.

### Usage

### ```main.py```

This file is the core of the implementation performed. The user who created the experiment will only have to run this script with the appropriate parameters for optimum performance.
The possibility to vary the parameters allows to have a more dynamic and adjusted experiment.

Run ```main.py```
```sh
python main.py
```

Optional arguments: 

| Parameter                 | Default       | Description   |	
| :------------------------ |:-------------:| :-------------|
| -n --name 	       |	exp_{datetime}           |Name of the experiment
| -dim --dim 	       |	\[1920,1080]           |Size Monitor
| -dm --distmon 	       |	67           |Distance to the monitor (cm)
| -m --mode 	       |	2           |Program execution mode
| -i --images 	       |	200           |Number of different images used in the experiment
| -ph --photos 	       |	30           |Number of images to download in each iteration
| -tt 	       |	5           | Target display time (seconds)
| -io 	       |	1           |Offset time of each image (seconds)
| -v --version 	       |	           |Version of the program
| -a --about 	       |	           |Program developer information
| -h --help 	       |	           |Help on using the program

## Processing, feature extraction, datasets, generation and classification phases

In this directory you will find everything you need to carry out the remaining phases of the BCI life cycle. The ```data``` directory contains the data acquired by the BCI in the acquisition phase. The ```analysis_tools.py``` file contains the necessary code to convert the data acquired in the acquisition phase into RawData in order to apply the different processing techniques.

The evaluation of the performance of the framework has been carried out through three different experiments (close and open-set authentication using binary classification, and subject identification employing multiclass classification), and three testing configurations incrementally analyzing the performance of different processing techniques and the differences between classifying with epochs or statistical values. The first configuration uses the Notch and Butterworth filters, performing the classification using epochs. In contrast, the second considers adding ICA to the processes defined by the first configuration. Finally, the third configuration is cumulative to the previous two. It uses ML classification through statistical values extracted from the epochs using four window sizes, 58, 116, 174, and 232.

In this directory, you can find a notebook for each configuration created in the three experiments. For the third configuration, a notebook has been created for each window size. The name of each notebook indicates which experiment and configuration it refers to.

## Tools

* [Bitbrain Versatile eeg](https://www.bitbrain.com/neurotechnology-products/semi-dry-eeg/versatile-eeg) - EEG Recording
* [Python](https://www.python.org/) - Python and the libraries for the creation of the experiment and EEG signal synchronization

## Roadmap

See the [open issues](https://github.com/edulb96/P300-authentication/issues) for a list of proposed features (as well as known issues).