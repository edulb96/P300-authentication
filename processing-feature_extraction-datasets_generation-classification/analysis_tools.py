import os
from glob import glob
import pandas as pd
from mne import create_info, concatenate_raws
from mne.channels import read_custom_montage, make_standard_montage
from mne.io import RawArray
from collections import OrderedDict
import mne

import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np
import re
import csv
import sys
from scipy.io import loadmat

sns.set_context('talk')
sns.set_style('white')


def load_mat(filename):
    chnames = ['Fp1',
               'Fp2',
               'F5',
               'AFz',
               'F6',
               'T7',
               'Cz',
               'T8',
               'P7',
               'P3',
               'Pz',
               'P4',
               'P8',
               'O1',
               'Oz',
               'O2',
               'STI 014']
    chtypes = ['eeg'] * 16 + ['stim']

    X = loadmat(filename)['s3']['test']
    info = mne.create_info(ch_names=chnames, sfreq=256,
                           ch_types=chtypes, montage='standard_1020',
                           verbose=False)
    raw = mne.io.RawArray(data=X, info=info, verbose=False)

    return raw


def load_raw(filename, sfreq=256., ch_ind=[0, 1, 2, 3],
             stim_ind=5, replace_ch_names=None):

    n_channel = len(ch_ind)
    data = pd.read_csv(filename)

    if "Timestamp" in data.columns:
        del data['Timestamp']
    if "Time" in data.columns:
        del data['Time']

    ch_names = list(data.columns)[0:n_channel] + ['Stim']

    if replace_ch_names is not None:
        ch_names = [c if c not in replace_ch_names.keys()
                    else replace_ch_names[c] for c in ch_names]

    ch_types = ['eeg'] * n_channel + ['stim']
    montage = 'standard_1020'
    data = data.values[:, ch_ind + [stim_ind]].T
    data[:-1] *= 1e-6

    info = create_info(ch_names=ch_names, ch_types=ch_types,
                       sfreq=sfreq)
    raw = RawArray(data=data, info=info)
    raw.set_montage(montage)

    return raw