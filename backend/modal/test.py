from psd_tools import PSDImage
psd = PSDImage.open("test/see_through_output/bluebg6/output.psd")
for index, layer in enumerate(psd):
    print(f"Index {index}: {layer.name} ({type(layer)})")
# for layer in psd:
#     print(layer.name, type(layer))
#     print(layer.index())

# from pathlib import Path

# import modal

# app = modal.App("example-inference")
# image = modal.Image.debian_slim().uv_pip_install("transformers[torch]")


# @app.function(gpu="h100", image=image)
# def chat(prompt: str | None = None) -> list[dict]:
#     from transformers import pipeline

#     if prompt is None:
#         prompt = f"/no_think Read this code.\n\n{Path(__file__).read_text()}\nIn one paragraph, what does the code do?"

#     print(prompt)
#     context = [{"role": "user", "content": prompt}]

#     chatbot = pipeline(
#         model="Qwen/Qwen3-1.7B", device_map="cuda", max_new_tokens=1024
#     )
#     result = chatbot(context)
#     print(result[0]["generated_text"][-1]["content"])

#     return result