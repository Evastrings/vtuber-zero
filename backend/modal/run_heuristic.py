from pathlib import Path
import subprocess

def run_heuristic_on_psd(psd_path):
    psd = Path(psd_path)
    tags = ["legwear", "footwear", "bottomwear", "topwear", "handwear", "hair", "arm", "skirt"]

    print(f"Processing: {psd.name}")

    # Depth split
    subprocess.run([
        "python", "inference/scripts/heuristic_partseg.py", "seg_wdepth",
        "--srcp", str(psd),
        "--target_tags", ",".join(tags)
    ], cwd=r"C:\Users\Evatea\Videos\Evatea\projects\see-through", check=True)


    #Left right split
    wdepth_psd = psd.with_name(psd.stem + "_wdepth.psd")
    if wdepth_psd.exists():
        subprocess.run([
            "python", "inference/scripts/heuristic_partseg.py", "seg_wlr",
            "--srcp", str(wdepth_psd),
            "--target_tags", ",".join(tags)
        ], cwd=r"C:\Users\Evatea\Videos\Evatea\projects\see-through", check=True)


if __name__ == "__main__":
    run_heuristic_on_psd(r"C:\Users\Evatea\Videos\Evatea\projects\vtuber-zero\backend\test\see_through_output\bluebg1\output.psd")