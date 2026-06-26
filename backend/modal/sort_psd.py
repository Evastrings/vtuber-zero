from psd_tools import PSDImage
from psd_tools.api.psd_image import PSDImage as PSD
from pathlib import Path


# Fixed draw order — index = priority (0 = bottom/back, higher = front)
LAYER_ORDER = [
    "back hair",
    "legwear", "footwear", "bottomwear",
    "tail", "wings",
    "topwear",
    "neckwear", "neck",
    "objects",
    "ears", "earwear",
    "head", "face",
    "eyewhite", "irides", "eyelash", "eyebrow",
    "nose", "mouth",
    "eyewear",
    "headwear",
    "front hair",
    "handwear",
]

def get_layer_priority(layer_name: str) -> int:
    # pseudo code obj: i want irides-l to become irides so it can give me index 15 etc
    name = layer_name.lower().strip() #removes trailing white spaces and converts to lowercase

    parts = name.rsplit('-', 1)
    if len(parts) == 2 and parts[1] in ['0', '1', '2', 'l', 'r']:
        base = parts[0]

    # for suffix in ["-0", "-1", "-2", "-l", "-r", "l", "r"]:
    #     if name.endswith(suffix):
    #         base = name[:-len(suffix)].strip('-').strip()
    #         break
    else:
        base = name
        pass
    for i, layers in enumerate(LAYER_ORDER):
        if base == layers:
            return i
    
    return LAYER_ORDER.index("neck")

psd = PSDImage.open("test/see_through_output/bluebg6/output.psd")

for layer in psd:
    print(f"Layer name: {layer.name}, Index: {get_layer_priority(layer.name)}")


# for index, layer in enumerate(psd):
#     print(f"Index {index}: {layer.name} ({type(layer)})")