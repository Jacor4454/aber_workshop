from PIL import Image

im = Image.open("a.jpeg")
im = im.resize((64, 64))
rgb_im = im.convert('RGB')
rgb_im.save('img1.bmp')
