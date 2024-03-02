from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"




''' # It will validate the posts only in these three logic
    " model_name.value >> .value indicates the right side Value
    # You could need the parameter to contain /home/johndoe/myfile.txt, with a leading slash (/).
    # In that case, the URL would be: /files//home/johndoe/myfile.txt, with a double slash (//) between files and home.

'''