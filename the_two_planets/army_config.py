import json
import os

from collections import OrderedDict

file_path = (os.path.dirname(__file__)) + "/config.json"
army_data = json.load(open(file_path), object_pairs_hook=OrderedDict)
