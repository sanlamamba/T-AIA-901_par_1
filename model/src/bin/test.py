import os
import sys

src_dir = os.path.join(os.getcwd(), "..", "..")

sys.path.append(os.path.abspath(src_dir))

from src.helpers.city_to_train_station import VisualizerHelper

print(VisualizerHelper.get_nearest_station("st remimont"))
