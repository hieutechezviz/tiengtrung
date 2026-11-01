# Tách nền trắng ảnh sản phẩm DL06 -> PNG trong suốt, cắt logo EZVIZ
import sys, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
UP = sys.argv[1]
def cutout(img, thr=246):
    a = np.asarray(img.convert('RGB')).astype(int)
    white = (a.min(axis=2) >= thr)
    lab, n = ndimage.label(white)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border))
    alpha = np.where(bg, 0, 255).astype(np.uint8)
    # viền mềm: pixel nền sát vật thể lấy alpha theo độ tối
    edge = ndimage.binary_dilation(~bg, iterations=2) & bg
    dark = 255 - a.min(axis=2)
    alpha[edge] = np.clip(dark[edge] * 255 / (255 - thr + 1), 0, 255).astype(np.uint8)
    out = Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), 'RGBA')
    m = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(.6))
    out.putalpha(m)
    return out.crop(out.getbbox())
img3 = Image.open(f'{UP}/9e98bfe0-image.jpg').convert('RGB')
logo_src = img3.copy()
from PIL import ImageDraw
ImageDraw.Draw(img3).rectangle((0, 0, 320, 115), fill=(255, 255, 255))  # xoá logo khỏi ảnh khoá
front = cutout(img3.crop((150, 50, 900, 900)))
front.save('anh/dl06_front.png'); print('front', front.size)
logo = cutout(logo_src.crop((20, 20, 310, 110)), thr=240)
logo.save('anh/logo.png'); print('logo', logo.size)
img2 = Image.open(f'{UP}/dc4a1b50-image.png')
side = cutout(img2); side.save('anh/dl06_side_back.png'); print('side', side.size)
pair = Image.open(f'{UP}/08e0a24d-image.png').convert('RGBA'); pair = pair.crop(pair.getbbox())
pair.save('anh/dl06_pair.png'); print('pair', pair.size)
w = side.width
back = side.crop((int(w*.5), 0, w, side.height)); back = back.crop(back.getbbox()); back.save('anh/dl06_back.png'); print('back', back.size)
