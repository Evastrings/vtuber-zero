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
    else:
        base = name

    for i, layers in enumerate(LAYER_ORDER):
        if base == layers:
            return i
    
    return LAYER_ORDER.index("neck")

psd = PSDImage.open("test/see_through_output/bluebg6/output.psd")



def reorder_psd(input_path: str, output_path: str = None):
    #open the psd
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else input_path.with_stem(input_path.stem + "_reordered")
    psd_r = PSDImage.open(input_path)

    # sort psd._layers using get_layer_priority on each layer's name
    sorted_psd = sorted(psd_r._layers, key=lambda layer_i: get_layer_priority(layer_i.name))

    # save to output_path (default: same name with _reordered suffix)
    print("=== THIS IS THE SORTED PSD LIST ===")
    print(sorted_psd)
    print("===== END END END =====")
    for i, lyr in enumerate(psd_r):
        psd_r.remove(psd_r[0])
    for x, j in enumerate(sorted_psd):
        psd_r.insert(x, j)
    print(psd_r._layers)
    psd_r.save(output_path)
    print(f"psd reordered and saved to {output_path}")
    return output_path
    
