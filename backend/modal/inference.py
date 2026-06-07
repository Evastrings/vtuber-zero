from pathlib import Path
import modal
import subprocess



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

# image = (
#     modal.Image.from_registry("nvidia/cuda:12.8.0-cudnn-devel-ubuntu22.04", add_python="3.12")
#     .pip_install(
#         "torch==2.8.0+cu128",
#         "torchvision==0.23.0+cu128", 
#         extra_index_url="https://download.pytorch.org/whl/cu128"
#     )
#     .add_local_dir(
#         "C:/Users/Evatea/Videos/Evatea/projects/see-through",
#         remote_path="/see-through",
#         copy=True
#     )
#     .pip_install_from_requirements("C:/Users/Evatea/Videos/Evatea/projects/see-through/requirements.txt")
# )

# image = (
#     modal.Image.from_registry("nvidia/cuda:12.8.0-cudnn-devel-ubuntu22.04", add_python="3.12")
#     .pip_install(
#         "torch==2.8.0+cu128",
#         "torchvision==0.23.0+cu128", 
#         extra_index_url="https://download.pytorch.org/whl/cu128"
#     )
#     .pip_install_from_requirements("C:/Users/Evatea/Videos/Evatea/projects/see-through/requirements.txt")
# )

volume = modal.Volume.from_name("see-through-models", create_if_missing=True)

# see_through_mount = modal.Mount.from_local_dir(
#     "C:/Users/Evatea/Videos/Evatea/projects/see-through",
#     remote_path="/see-through"
# )

@app.function(gpu="A100", image=image, volumes={"/cache": volume}, secrets=[modal.Secret.from_name("huggingface")])
def run_inference(img_bytes) -> bytes:
    psd_path = Path("/see-through/workspace/layerdiff_output")

    temp_input = Path("/tmp/input.png")
    temp_input.write_bytes(img_bytes)
    # subprocess.run(["python", "/see-through/inference/scripts/inference_psd.py", "--srcp", img_path, "--save_to_psd"])
    subprocess.run(["python", "/see-through/inference/scripts/inference_psd.py", "--srcp", str(temp_input), "--save_to_psd"])
    # psd_files = list(psd_path.glob("*.psd"))
    # psd_file = Path("/see-through/workspace/layerdiff_output/input.psd")
    psd_file = Path("/root/workspace/layerdiff_output/input.psd")
    with open(psd_file, "rb") as f:
         return f.read()
    
@app.local_entrypoint()
def main():

    with open("test/input_images/nino.jpeg", "rb") as f:
        img_bytes = f.read()

    # img_path = "test/input_images/nino.jpeg"
    psd_bytes = run_inference.remote(img_bytes)
    with open("output.psd", "wb") as f:
        f.write(psd_bytes)
    print("Done — output.psd saved")

