# -*- encoding: utf-8 -*-
'''
@File    :   model.py
@Time    :   2022/10/24 14:30:00
@Author  :   Jian Zhang
@Contact :   zhangmingjian180@qq.com
HUST, Heilongjiang, China
'''

import torch
import torch.nn as nn

import py.models.layers as ml


class Transformer_binary_origin(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1Dblock = nn.Sequential(
                nn.Conv1d(1, 8, 3, padding=1),
                nn.BatchNorm1d(8),
                nn.ReLU(),
                nn.MaxPool1d(2, stride=2),

                nn.Conv1d(8, 16, 3, padding=1),
                nn.BatchNorm1d(16),
                nn.ReLU(),
                nn.MaxPool1d(2, stride=2),

                nn.Conv1d(16, 32, 3, padding=1),
                nn.BatchNorm1d(32),
                nn.ReLU(),
                nn.MaxPool1d(2, stride=2)
        )

        self.add_positional_encoding_time = ml.AddPositionalEncoding(50, 32)
        self.time_encoder_block1 = ml.EncoderBlock(32, 32, 2)
        self.time_encoder_block2 = ml.EncoderBlock(32, 32, 2)
        self.time_encoder_block3 = ml.EncoderBlock(32, 32, 2)
        self.time_encoder_block4 = ml.EncoderBlock(32, 32, 2)
        self.time_global_pool = ml.GlobalPool(32)
        self.time_decoder_block1 = ml.DecoderBlock(32, 32, 2)
        self.time_decoder_block2 = ml.DecoderBlock(32, 32, 2)
        self.time_decoder_block3 = ml.DecoderBlock(32, 32, 2)
        self.time_decoder_block4 = ml.DecoderBlock(32, 32, 2)

        self.add_positional_encoding = ml.AddPositionalEncoding(62, 32)
        self.encoder_block1 = ml.EncoderBlock(32, 32, 2)
        self.encoder_block2 = ml.EncoderBlock(32, 32, 2) 
        self.encoder_block3 = ml.EncoderBlock(32, 32, 2)
        self.encoder_block4 = ml.EncoderBlock(32, 32, 2)
        self.global_pool = ml.GlobalPool(32)
        self.decoder_block1 = ml.DecoderBlock(32, 32, 2)
        self.decoder_block2 = ml.DecoderBlock(32, 32, 2)
        self.decoder_block3 = ml.DecoderBlock(32, 32, 2)
        self.decoder_block4 = ml.DecoderBlock(32, 32, 2)
         
        self.line = nn.Linear(32, 1)

        self.loss_func = nn.BCELoss()
     
    def forward(self, x):
        x = x.reshape(-1, 1, 400)
        x = self.conv1Dblock(x)
        x = x.reshape(-1, 62*32, 50).transpose(-1, -2).reshape(-1, 62, 32)

        x = self.add_positional_encoding(x)
        x = self.encoder_block1(x)
        x = self.encoder_block2(x)
        x = self.encoder_block3(x)
        x = self.encoder_block4(x)
        encoder_x = x
        x = self.global_pool(encoder_x)
        x = self.decoder_block1(x, encoder_x)
        x = self.decoder_block2(x, encoder_x) 
        x = self.decoder_block3(x, encoder_x)
        x = self.decoder_block4(x, encoder_x)

        x = x.reshape(-1, 50, 32)

        x = self.add_positional_encoding_time(x)
        x = self.time_encoder_block1(x)
        x = self.time_encoder_block2(x)
        x = self.time_encoder_block3(x)
        x = self.time_encoder_block4(x)
        encoder_x = x
        x = self.time_global_pool(encoder_x)
        x = self.time_decoder_block1(x, encoder_x)
        x = self.time_decoder_block2(x, encoder_x)
        x = self.time_decoder_block3(x, encoder_x)
        x = self.time_decoder_block4(x, encoder_x)

        x = x.squeeze(-2)
        x = self.line(x).squeeze(-1)
        x = torch.sigmoid(x)
       
        predictions = torch.trunc(x / 0.5)

        return x, predictions

    def loss(self, output, label):
        loss_value = self.loss_func(output, torch.as_tensor(label, dtype=torch.float32))
        
        return loss_value


class Transformer_binary(nn.Module):
    def __init__(self, position_number, sample_length):
        super().__init__()
        self.position_number = position_number
        self.channels_number = len(position_number)
        self.sample_length = sample_length
        self.time_number = sample_length // 8

        self.conv1Dblock = nn.Sequential(
                nn.Conv1d(1, 8, 3, padding=1),
                nn.BatchNorm1d(8),
                nn.ReLU(),
                nn.MaxPool1d(2, stride=2),

                nn.Conv1d(8, 16, 3, padding=1),
                nn.BatchNorm1d(16),
                nn.ReLU(),
                nn.MaxPool1d(2, stride=2),

                nn.Conv1d(16, 32, 3, padding=1),
                nn.BatchNorm1d(32),
                nn.ReLU(),
                nn.MaxPool1d(2, stride=2)
        )

        self.add_positional_encoding_time = ml.AddPositionalEncoding(50, 32)
        self.time_encoder_block1 = ml.EncoderBlock(32, 32, 2)
        self.time_encoder_block2 = ml.EncoderBlock(32, 32, 2)
        self.time_encoder_block3 = ml.EncoderBlock(32, 32, 2)
        self.time_encoder_block4 = ml.EncoderBlock(32, 32, 2)
        self.time_global_pool = ml.GlobalPool(32)
        self.time_decoder_block1 = ml.DecoderBlock(32, 32, 2)
        self.time_decoder_block2 = ml.DecoderBlock(32, 32, 2)
        self.time_decoder_block3 = ml.DecoderBlock(32, 32, 2)
        self.time_decoder_block4 = ml.DecoderBlock(32, 32, 2)

        self.add_positional_encoding = ml.AddPositionalEncoding(62, 32)
        self.encoder_block1 = ml.EncoderBlock(32, 32, 2)
        self.encoder_block2 = ml.EncoderBlock(32, 32, 2) 
        self.encoder_block3 = ml.EncoderBlock(32, 32, 2)
        self.encoder_block4 = ml.EncoderBlock(32, 32, 2)
        self.global_pool = ml.GlobalPool(32)
        self.decoder_block1 = ml.DecoderBlock(32, 32, 2)
        self.decoder_block2 = ml.DecoderBlock(32, 32, 2)
        self.decoder_block3 = ml.DecoderBlock(32, 32, 2)
        self.decoder_block4 = ml.DecoderBlock(32, 32, 2)
         
        self.line = nn.Linear(32, 1)
     
    def forward(self, x):
        x = x.reshape(-1, 1, self.sample_length)
        x = self.conv1Dblock(x)
        x = x.reshape(-1, self.channels_number*32, self.time_number).transpose(-1, -2).reshape(-1, self.channels_number, 32)

        x = self.add_positional_encoding(x, self.position_number)
        x = self.encoder_block1(x)
        x = self.encoder_block2(x)
        x = self.encoder_block3(x)
        x = self.encoder_block4(x)
        encoder_x = x
        x = self.global_pool(encoder_x)
        x = self.decoder_block1(x, encoder_x)
        x = self.decoder_block2(x, encoder_x) 
        x = self.decoder_block3(x, encoder_x)
        x = self.decoder_block4(x, encoder_x)

        x = x.reshape(-1, self.time_number, 32)

        x = self.add_positional_encoding_time(x, self.time_number)
        x = self.time_encoder_block1(x)
        x = self.time_encoder_block2(x)
        x = self.time_encoder_block3(x)
        x = self.time_encoder_block4(x)
        encoder_x = x
        x = self.time_global_pool(encoder_x)
        x = self.time_decoder_block1(x, encoder_x)
        x = self.time_decoder_block2(x, encoder_x)
        x = self.time_decoder_block3(x, encoder_x)
        x = self.time_decoder_block4(x, encoder_x)

        x = x.squeeze(-2)
        x = self.line(x).squeeze(-1)
        x = torch.sigmoid(x)
       
        predictions = torch.trunc(x / 0.5)

        return x, predictions










