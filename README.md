<!-- PROJECT LOGO -->
<br>
<p align="center">
  <a href="https://github.com/edulb96/P300-authentication">
    <img src="CyberDataLab.png" alt="CDL" width="400" height="260">
  </a>
  <h3 align="center">Evaluation of Data Processing and Machine Learning Techniques in P300-based Authentication using Brain-Computer Interfaces</h3>
</p>

## About the framework

<br>
Implementation of a framework for EEG signal acquisition from a BCI, signal processing, and P300-based authentication using trained classifiers. Besides, it deploys a scenario where P300 evoked potentials are generated through the Oddball paradigm and visual stimuli.
<br>

This repository contains a related code for the paper Evaluation of Data Processing and Machine Learning Techniques in P300-based Authentication using Brain-Computer Interfaces.

In this repository there are two directories. The ```acquisition``` directory contains the implemented code for the data acquisition phase, while the ```processing-feature_extraction-datasets_generation-classification``` directory contains the generated code to perform the processing phases , feature extraction, dataset generation, and authentication.

## Acquisition directory

### Prerequisites
* Python version 3.7 or more, pyenv recommended
* pip3

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
| -i --images 	       |	30           |Number of different images used in the experiment
| -p --prob 	       |	0.1           |Probability of appearance of the target in the experiment (per unit)
| -tt 	       |	5           | Target display time (seconds)
| -in 	       |	0.250           |Elapsed time between images (seconds)
| -io 	       |	0.150           |Offset time of each image (seconds)
| -j 	       |	0.2           |Variable jitter time when displaying image (seconds)
| -v --version 	       |	           |Version of the program
| -a --about 	       |	           |Program developer information
| -h --help 	       |	           |Help on using the program

## Processing, feature extraction, datasets, generation and classification phases

In this directory you will find everything you need to carry out the remaining phases of the BCI life cycle. The ```data``` directory contains the data acquired by the BCI in the acquisition phase. 

