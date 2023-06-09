from diffusers import StableDiffusionPipeline
from transformers import Swin2SRForImageSuperResolution
from transformers import Swin2SRImageProcessor 
from PIL import Image
import torch
import numpy as np

ENHANCER = "RAW photo, subject, (high detailed skin:1.2), 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3"

def make_image(prompt, image_file="image.png", image_res=720,enhance=True):
    mult = round(image_res/(9*8))*8
    image_size = [16*mult, 9*mult]
    print(f'Prompt :{prompt}')
    models = ["Joeythemonster/sci-fi-landscape",'sinkinai/cheese-daddys-landscapes-mix','SG161222/Realistic_Vision_V2.0']
    model_id = models[2]
    print('Image and prompt settings loaded...')
    if enhance:
        prompt += " "+ENHANCER
    print('Calculating image size')
    for i in range(len(image_size)):
        tmp = image_size[i]+(image_size[i] % 8)
        if tmp % 8 != 0:
            tmp = image_size[i]-(image_size[i] % 8)
    image_size[i] = tmp
    print(f'Size = {[str(i) for i in image_size]}')
    print('Using: '+model_id)
    print('Making Pipeline...')
    pipe = StableDiffusionPipeline.from_pretrained(model_id)
    print('Making Cuda...')
    cuda = pipe.to("cuda")
    print('made cuda!...')
    image = pipe(
        prompt,
        num_inference_steps=100,
        width=image_size[0],
        height=image_size[1],
    ).images[0]
    image.save(image_file)
    return image


def upscale4x(image=False,image_file='image.png'):
    model_id = 'caidas/swin2SR-realworld-sr-x4-64-bsrgan-psnr'
    model = Swin2SRForImageSuperResolution.from_pretrained(model_id)
    if image:
        small_image = image
    else:
        small_image = Image.open(image_file)
    processor = Swin2SRImageProcessor()
    pixel_values = processor(small_image, return_tensors="pt").pixel_values
    outputs = []
    with torch.no_grad():
        outputs = model(pixel_values)
    print('Outputs: '+str(type(outputs)))
    output = outputs.reconstruction.data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.moveaxis(output, source=0, destination=-1)
    output = (output * 255.0).round().astype(np.uint8)  # float32 to uint8
    new_img = Image.fromarray(output)
    new_img.save('big_image.png')