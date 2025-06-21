from PIL import Image, ImageEnhance

# Вроде просто какой-то скрипт для обработки изображений. В бизнес логике не учавствует

im = Image.open("assets/images\\lost_soul_100.png")
enhancer = ImageEnhance.Brightness(im)
# factor = 0.75
# im_output = enhancer.enhance(factor)
# im_output.save('images\\floor_near_wall_75.png')
factor = 0.5
im_output = enhancer.enhance(factor)
im_output.save('images\\lost_soul_50.png')
# factor = 0.25
# im_output = enhancer.enhance(factor)
# im_output.save('images\\floor_near_wall_25.png')
factor = 0.05
im_output = enhancer.enhance(factor)
im_output.save('images\\lost_soul_5.png')