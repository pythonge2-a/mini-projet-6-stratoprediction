from strato_prediction.simulation import Balloon
from strato_prediction.GRIB import load_grib_data
from strato_prediction.display import plot_trajectory_3d, show_on_map
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import message_dialog, button_dialog, input_dialog, radiolist_dialog

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


