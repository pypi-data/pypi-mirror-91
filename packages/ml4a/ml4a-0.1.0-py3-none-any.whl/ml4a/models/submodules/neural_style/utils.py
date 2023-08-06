import os
import IPython
from decimal import Decimal
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import requests
import urllib.parse
from io import BytesIO


class EasyDict(dict):
    def __init__(self, *args, **kwargs):
        super(EasyDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def load_image(image, image_size=None, to_numpy=False, normalize=False):
    if isinstance(image, str):
        if is_url(image):
            image = url_to_image(image)
        elif os.path.exists(image):
            image = Image.open(image).convert('RGB')
        else:
            raise ValueError('no image found at %s'%image)
    elif isinstance(image, np.ndarray):
        image = Image.fromarray(image.astype(np.uint8)).convert('RGB')
    if image_size is not None and isinstance(image_size, tuple):
        image = resize(image, image_size)
    elif image_size is not None and not isinstance(image_size, tuple):
        aspect = get_aspect_ratio(image)
        image_size = (int(aspect * image_size), image_size)
        image = resize(image, image_size)
    if to_numpy:
        image = np.array(image)
        if normalize:
            image = image / 255.0        
    return image


def mask_to_image(mask):
    mask = (255.0 * mask).astype(np.uint8)
    mask_pil = Image.fromarray(mask).convert('RGB')
    return mask_pil


def get_size(image):
    if isinstance(image, str):
        image = load_image(image, 1024)
        w, h = image.size
    elif isinstance(image, Image.Image):    
        w, h = image.size
    elif isinstance(image, np.ndarray):
        w, h = image.shape[1], image.shape[0]
    return w, h


def get_aspect_ratio(image):
    w, h = get_size(image)
    return float(w) / h


def resize(img, new_size, mode=None, align_corners=True):
    sampling_modes = {
        'nearest': Image.NEAREST, 
        'bilinear': Image.BILINEAR,
        'bicubic': Image.BICUBIC, 
        'lanczos': Image.LANCZOS
    }
    assert isinstance(new_size, tuple), \
        'Error: image_size must be a tuple.'
    assert mode is None or mode in sampling_modes.keys(), \
        'Error: resample mode %s not understood: options are nearest, bilinear, bicubic, lanczos.'
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img.astype(np.uint8)).convert('RGB')
    w1, h1 = img.size
    w2, h2 = new_size
    if (h1, w1) == (w2, h2):
        return img
    if mode is None:
        mode = 'bicubic' if w2*h2 >= w1*h1 else 'lanczos'
    resample_mode = sampling_modes[mode]
    return img.resize((w2, h2), resample=resample_mode)


def save(img, filename):
    folder = os.path.dirname(filename)
    if folder and not os.path.isdir(folder):
        os.mkdir(folder)
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img.astype(np.uint8)).convert('RGB')
    img.save(str(filename))

    
def display(img):
    if isinstance(img, list):
        return frames_to_movie(img, fps=30)
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img.astype(np.uint8)).convert('RGB')
    IPython.display.display(img)

    
def resize_tensor(image, image_size, mode='bicubic', align_corners=True):
    assert isinstance(image_size, tuple), 'Error: image_size must be a tuple'
    _, _, h1, w1 = image.shape
    if (w1, h1) == image_size:
        return image
    return torch.nn.functional.interpolate(
        image, 
        tuple(reversed(image_size)), 
        mode=mode, 
        align_corners=align_corners
    )


def random_tensor(w, h, c=3):
    tensor = torch.randn(c, h, w).mul(0.001).unsqueeze(0)
    return tensor


def random_tensor_like(base_image):
    w, h = base_image.size
    return random_tensor(w, h, 3)


def preprocess(image, image_size=None, to_normalize=True):
    if isinstance(image, str):
        image = Image.open(image).convert('RGB')
    elif isinstance(image, np.ndarray):
        image = Image.fromarray(image.astype(np.uint8)).convert('RGB')
    if image_size is None:
        image_size = (image.height, image.width)
    elif type(image_size) is not tuple:
        image_size = tuple([int((float(image_size) / max(image.size)) * x) for x in (image.height, image.width)])
    Loader = transforms.Compose([transforms.Resize(image_size), transforms.ToTensor()])
    rgb2bgr = transforms.Compose([transforms.Lambda(lambda x: x[torch.LongTensor([2,1,0])])])
    if to_normalize:
        Normalize = transforms.Compose([transforms.Normalize(mean=[103.939, 116.779, 123.68], std=[1,1,1])])
        tensor = Normalize(rgb2bgr(Loader(image) * 255)).unsqueeze(0)
    else:
        tensor = rgb2bgr(Loader(image)).unsqueeze(0)
    return tensor


def deprocess(tensor):
    Normalize = transforms.Compose([transforms.Normalize(mean=[-103.939, -116.779, -123.68], std=[1,1,1])])
    bgr2rgb = transforms.Compose([transforms.Lambda(lambda x: x[torch.LongTensor([2,1,0])])])
    tensor = bgr2rgb(Normalize(tensor.squeeze(0).cpu())) / 255
    tensor.clamp_(0, 1)
    Image2PIL = transforms.ToPILImage()
    image = Image2PIL(tensor.cpu())
    return image


def original_colors(content, generated):
    #content, generated = deprocess(content.clone()), deprocess(generated.clone())    
    content_channels = list(content.convert('YCbCr').split())
    generated_channels = list(generated.convert('YCbCr').split())
    content_channels[0] = generated_channels[0]
    return Image.merge('YCbCr', content_channels).convert('RGB')


def url_to_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def is_url(path):
    path = urllib.parse.urlparse(path)
    return path.netloc != ''
   

def log(message, verbose=True):
    if not verbose:
        return
    print(message)

    
def warn(condition, message, verbose=True):
    if not condition:
        return
    log('Warning: %s' % message, verbose)
    

def get_style_image_paths(style_image_input):
    style_image_list = []
    for path in style_image_input:
        if os.path.isdir(path):
            images = (os.path.join(path, file) for file in os.listdir(path) 
                      if os.path.splitext(file)[1].lower() in [".jpg", ".jpeg", ".png", ".tiff"])
            style_image_list.extend(images)
        else:
            style_image_list.append(path)
    return style_image_list


def maybe_update(net, t, update_iter, num_iterations, loss):
    if update_iter != None and t % update_iter == 0:
        IPython.display.clear_output()
        print('Iteration %d/%d: '%(t, num_iterations))
        if net.content_weight > 0:
            print('  Content loss = %s' % ', '.join(['%.1e' % Decimal(module.loss.item()) for module in net.content_losses]))
        print('  Style loss = %s' % ', '.join(['%.1e' % Decimal(module.loss.item()) for module in net.style_losses if module.strength > 0]))
        print('  Histogram loss = %s' % ', '.join(['%.1e' % Decimal(module.loss.item()) for module in net.hist_losses if module.strength > 0]))
        if net.tv_weight > 0:
            print('  TV loss = %s' % ', '.join(['%.1e' % Decimal(module.loss.item()) for module in net.tv_losses]))
        print('  Total loss = %.2e' % Decimal(loss.item()))

        
def maybe_save_preview(img, t, save_iter, num_iterations, output_path):
    should_save = save_iter > 0 and t % save_iter == 0
    if not should_save:
        return
    output_filename, file_extension = os.path.splitext(output_path)
    #output_filename = output_filename.replace('results', 'results/preview')
    filename = '%s_%04d%s' % (output_filename, t, file_extension)
    save(deprocess(img), filename)

    