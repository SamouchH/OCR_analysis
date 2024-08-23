import torch
from diffusers import FluxPipeline
from huggingface_hub import login

torch.cuda.empty_cache()

device = torch.device("cuda:0")

torch.cuda.empty_cache()

pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16).to(device)

prompt = " Generate a high-resolution image of a metal label or industrial sticker attached to equipment. The label should have technical details like manufacturer information, serial numbers, model numbers,dateof fabrication and warning signs."

# Vérifier si le GPU est disponible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


image = pipe(
    prompt,
    height = 128,
    width = 128,
    guidance_scale = 2.5,
    num_inference_steps = 16,
    max_sequence_length = 128,
    generator=torch.Generator(device).manual_seed(0)
).images[0]
image.save("generated_image.png")