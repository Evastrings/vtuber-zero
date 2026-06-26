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

# print("=== Here is a New Section ===")

# print(dir(psd))

# print(psd._layers)
# for ly in psd._layers:
#     print(ly.name)

# x = PixelLayer("handwear-r" size=123x419)
# psd.save


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
    # psd_r._layers = sorted_psd
    print(psd_r._layers)
    output_path = input_path
    psd_r.save(output_path/"output_reordered.psd")
    print(f"psd reordered and saved to {output_path}")
    return output_path/"output_reordered.psd"
    
# def reorder_psd(input_path: str, output_path: str = None):
#     input_path = Path(input_path)
#     output_path = Path(output_path) if output_path else input_path.with_stem(input_path.stem + "_reordered")

#     psd = PSDImage.open(input_path)
    
#     layers = list(psd)
#     print(f"Original order: {[l.name for l in layers]}")

#     # Sort: lower priority index = earlier in list = rendered first (bottom of stack)
#     # psd-tools renders layers in reverse list order (index 0 = top in Photoshop)
#     # so we reverse: highest priority = index 0
#     sorted_layers = sorted(layers, key=lambda l: get_layer_priority(l.name))
    
#     print(f"Reordered: {[l.name for l in sorted_layers]}")

#     # Reassign layer order in PSD
#     psd._layers = sorted_layers
#     psd.save(output_path)
#     print(f"Saved to {output_path}")

# new_psd = 
reorder_psd("test/see_through_output/bluebg6")

# for layer1 in new_psd:
#     print(layer1.name)
# for index, layer in enumerate(psd):
#     print(f"Index {index}: {layer.name} ({type(layer)})")