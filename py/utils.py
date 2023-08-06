import pickle
import torch

import numpy as np


def get_possibility_binary(result, prediction):
    if prediction == 1:
        return result
    else:
        return 1 - result


def get_position_number(des_chan, source_chan):
    result_list = []
    for e in des_chan:
        result_list.append(source_chan.index(e.upper()))

    return result_list


def normalize_DEAP(x):
    return (x - x.mean()) / x.std()


def nonlinear_and_remove_mean_norm(array, r=55):
    array = array - np.mean(array, axis=0)
    array = np.tanh(array / r)
    return array


def gen_nonlinear_and_remove_mean_norm(r=100):
    def nonlinear_and_remove_mean_norm(array):
        array = array - np.mean(array, axis=0)
        array = np.tanh(array / r)
        return array
    return nonlinear_and_remove_mean_norm


def gen_emotion_recognition_method(model_class, checkpoint_filepath, channels, source_ch, sample_length, devicename, get_possibility_binary):
    device = torch.device(devicename)
    pos_numbers = get_position_number(channels, source_ch)
    model = model_class(pos_numbers, sample_length).to(device)
    if torch.cuda.is_available():
        model.load_state_dict(torch.load(checkpoint_filepath))
    else:
        model.load_state_dict(torch.load(checkpoint_filepath, map_location=torch.device('cpu')))
    model.eval()
    def emotion_recognition_method(data):
        data = torch.Tensor(data).to(device)
        with torch.no_grad():
            result, prediction = model(data)
        result, prediction = float(result), int(prediction)
        possibility =  get_possibility_binary(result, prediction)
        return prediction, possibility
    return emotion_recognition_method




