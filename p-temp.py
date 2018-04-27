from PIL import Image, ImageDraw, ImageFont
print("Starting script")

'''
v0.001 - 27.04.2018 - Pillow fra Sensehat. Rename til p-temp.py.
'''


# Vet ikke hva unic står for. Kilde: https://stackoverflow.com/questions/24085996/how-i-can-load-a-font-file-with-pil-imagefont-truetype-without-specifying-the-ab
font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 28, encoding="unic")

txt = "Temperaturen er: 23.4 grader"


text_width, text_height = font.getsize(txt)
print(text_width)
print(text_height)

# Ekstra høyde og bredde
text_height = text_height + 10
text_width = text_width + 10


bilde = Image.new('RGB', (text_width,text_height), (240,240,240))

# Må lage draw-objekt
draw = ImageDraw.Draw(bilde)

# Manuell offset
draw.text((3,2), txt,"black",font)


bilde.save("bilde.png", "PNG")
print("Bilde lagret som bilde.png")

