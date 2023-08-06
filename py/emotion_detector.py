import py.utils
import py.config
import numpy as np

import py.models.model


channels = ["FP1", "F3", "C3", "P3", "O1", "P7", "T7", "F7"]
win_length = 400
model_class = py.models.model.Transformer_binary
checkpoint_filepath = "py/models/checkpoints/epoch11.pt"
devicename = "cpu"   # "cuda:0"

source_channels = py.config.SEED_channels
get_possibility_binary = py.utils.get_possibility_binary

emotion_recognition_method = py.utils.gen_emotion_recognition_method(model_class, checkpoint_filepath, channels, source_channels,
        win_length, devicename, get_possibility_binary)


def emotion_recognition(data):
    data = data.T.astype(np.float32)
    x = (data - data.mean(axis=1).reshape(8, 1)) / data.std(axis=1).reshape(8, 1)
    
    prediction, possibility = emotion_recognition_method(x)
    print(prediction, possibility)
    return prediction
