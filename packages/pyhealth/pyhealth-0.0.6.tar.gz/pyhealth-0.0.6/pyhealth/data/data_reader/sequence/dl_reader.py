# -*- coding: utf-8 -*-

# Author: Zhi Qiao <mingshan_ai@163.com>

# License: BSD 2 clause

import os.path
from .base_dataset import BaseDataset
import pandas as pd
import numpy as np
import torch
import pickle

def time_series_get(fpath):
    data = pd.read_csv(fpath, sep=',')
    return data.values

class DatasetReader(BaseDataset):

    def __init__(self, data, reverse = False, data_type = 'distribute', maxlength_seq = 200):
        BaseDataset.__init__(self, data)
        self.data_type = data_type
        self.feat_info = data['x']
        if data_type == 'aggregation':
            self.time = data['t']
        self.label_list = data['y']
        self.seq_len = max(data['l']) if max(data['l'])<maxlength_seq else maxlength_seq
        self.reverse = reverse
        
    def __getitem__(self, index):
        if self.data_type == 'distribute':
            xpath = self.feat_info[index]
            s_data = time_series_get(xpath)
            data = s_data[:self.seq_len, 1: ]
            time = s_data[:self.seq_len, 0]
        else:
            data = self.feat_info[index]
            time = self.time[index]

        l, w = np.shape(data)
        time[1:] = time[1:] - time[:-1]
        time[0] = 0.
        if self.reverse:
            data = data[::-1, :]
            time = time[::-1]
        x_time = np.zeros(self.seq_len)
        x_time[:l] = time
        x_series = np.zeros([self.seq_len, w])
        x_series[:l, :] = data
        x_mask = np.zeros(self.seq_len)
        x_mask[:l] = 1.
        x_mask_cur = np.zeros(self.seq_len)
        if self.reverse:
            x_mask_cur[0] = 1.
        else:
            x_mask_cur[l-1] = 1.
        label = self.label_list[index]
        return {'X': np.array(x_series), 'M': np.array(x_mask), 'cur_M': np.array(x_mask_cur), 'Y': np.array(label), 'T':np.array(x_time)}

    def __len__(self):
        return len(self.feat_info)


