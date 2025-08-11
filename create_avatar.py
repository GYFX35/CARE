from PIL import Image

img = Image.new('RGB', (128, 128), color = 'black')
img.save('static/default_avatar.png')
