from pathlib import Path
import modal
import subprocess
import itertools
import shutil

directory = "test/input_images"

app = modal.App("see_through")
image = (
    modal.Image.from_registry("nvidia/cuda:12.8.0-cudnn-devel-ubuntu22.04", add_python="3.12")
    .pip_install(
        "torch==2.8.0+cu128",
        "torchvision==0.23.0+cu128", 
        extra_index_url="https://download.pytorch.org/whl/cu128"
    )
    .add_local_dir(
        "C:/Users/Evatea/Videos/Evatea/projects/see-through",
        remote_path="/see-through",
        copy=True
    )
    .run_commands(
        "apt-get update && apt-get install -y git libgl1 libglib2.0-0 libsm6 libxrender1 libxext6",
        "cd /see-through && pip install -r requirements.txt"
    )
)


volume = modal.Volume.from_name("see-through-models", create_if_missing=True)


@app.function(gpu="A100", image=image, volumes={"/cache": volume}, secrets=[modal.Secret.from_name("huggingface")])
def run_inference(img_bytes) -> bytes:
    
    output_dir = Path("/root/workspace/layerdiff_output")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


    temp_input = Path("/tmp/input.png")
    temp_input.write_bytes(img_bytes)
    subprocess.run([
        "python", "/see-through/inference/scripts/inference_psd.py",
        "--srcp", str(temp_input),
        "--save_to_psd",
        "--tblr_split"
        ])
    psd_files = list(Path("/root/workspace/layerdiff_output").glob("*.psd"))
    print(f"PSD files found: {psd_files}")
    if not psd_files:
        raise FileNotFoundError("No PSD file found in output directory")
    
    psd_file = psd_files[0]
    with open(psd_file, "rb") as f:
         return f.read()
    
@app.local_entrypoint()
def main():
    images = itertools.chain(Path(directory).glob('*.png'), Path(directory).glob('*.jpeg'), Path(directory).glob('*.jpg'))
    for path in images:
        with open(str(path), "rb") as f:
            img_bytes = f.read()

        image_stem = Path(path).stem
        print(f"Processing: {image_stem}")

        psd_bytes = run_inference.remote(img_bytes)
        output_dir = Path(f"test/see_through_output/{image_stem}")
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_dir/"output.psd", "wb") as f:
            f.write(psd_bytes)
        print(f"Done — {image_stem} saved")

