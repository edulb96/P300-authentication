from termcolor import colored
import numpy as np
import pandas as pd
from time import time, strftime, gmtime
from optparse import OptionParser
from pylsl import StreamInlet, resolve_byprop
from sklearn.linear_model import LinearRegression
from datetime import datetime
import argparse

VERSION = '1.0beta'

def printInfo(string):
    print(colored('[Thread] ' + string, 'yellow'))


def printError(string):
    print(colored('[Thread] ' + string, 'red'))


def printSuccess(string):
    print(colored('[Thread] ' + string, 'green'))


def record_experiment(experiment, experiment_time):

    printSuccess("Hilo inicializado correctamente")

    dejitter = True

    now = datetime.now()
    name_file = "experiments/{}/records/{}.csv".format(experiment, experiment)

    printInfo("Looking for EEG stream...")
    print()
    streams = resolve_byprop('type', 'EEG', timeout=60)

    if len(streams) == 0:
        raise (RuntimeError("No EEG stream could be found, try restarting the LSL module."))

    printInfo("Connecting with the EEG signal stream...")
    inlet_eeg = StreamInlet(streams[0])

    info = inlet_eeg.info()
    description = info.desc()

    frec_lsl = info.nominal_srate()
    chs_lsl = info.channel_count()
    printInfo("Frequency obtained by LSL = {}".format(frec_lsl))
    printInfo("Number of channels obtained by LSL = {}".format(chs_lsl))

    ch_names_default = ['Fp1', 'Fp2', 'C3', 'C4', 'P7', 'P8', 'O1', 'O2']

    ch = description.child('channels').first_child()
    ch_names = [ch.child_value('label')]
    if (not ch_names or len(ch_names) < 8):
        ch_names = ch_names_default

    data_input = []
    timestamps = []

    printInfo("Looking for Stimulus stream...")
    stimulus_stream = resolve_byprop('name', 'stimulus', timeout=120)

    if stimulus_stream:
        printInfo("Connecting to the Stimulus stream...")
        inlet_stimulus = StreamInlet(stimulus_stream[0])
    else:
        inlet_stimulus = False
        printError("No Stimulus stream could be found.")
        printInfo("Initializing capture without Stimulus stream.")



    stimuli = []
    start_capture = time()
    printInfo('Starting to capture experiment t=%.3f' % start_capture)

    while (time() - start_capture) < experiment_time:
        try:
            data, timestamp = inlet_eeg.pull_chunk(timeout=0.0)
            if timestamp:
                data_input.append(data)
                timestamps.extend(timestamp)
            if inlet_stimulus:
                stimulus, timestamp = inlet_stimulus.pull_sample(timeout=0.0)
                if timestamp:
                    stimuli.append([stimulus, timestamp])
        except KeyboardInterrupt:
            printError('Canceling EEG capture...')
            break

    time_correction = inlet_eeg.time_correction()

    data_input = np.concatenate(data_input, axis=0)
    if chs_lsl > 8:
        data_input = data_input[:, :8]
    timestamps = np.array(timestamps) + time_correction

    if dejitter:
        y = timestamps
        X = np.atleast_2d(np.arange(0, len(y))).T
        linear_reg = LinearRegression().fit(X, y)
        timestamps = linear_reg.predict(X)

    data_input = np.c_[timestamps, data_input]
    data = pd.DataFrame(data=data_input, columns=['Timestamp'] + ch_names)

    data.insert(0, 'Time', np.arange(0, len(data) * 0.004, 0.004))

    if len(stimuli) != 0:
        data['stimulus'] = 0
        for estim in stimuli:
            ix = np.argmin(np.abs(estim[1] - timestamps))
            data.loc[ix, 'stimulus'] = estim[0][0]

    data.to_csv(name_file, float_format='%.3f', index=False)

    printSuccess('File ' + name_file + ' save correctly.')


if __name__ == "__main__":
    printInfo("Starting record.py")
    record_experiment("last_exp", 5)