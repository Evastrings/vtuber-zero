from gradio_client import Client, handle_file



client = Client("24yearsold/see-through-demo")


result = client.predict(
    image = handle_file('input_images/marin.jpeg'),
    resolution=768,
    seed=42,
    tblr_split=True,
    api_name="/inference",
)

print(result)
