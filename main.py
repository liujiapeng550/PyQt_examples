import pytesseract
from PIL import Image

# 打开图片
image = Image.open('image.jpg')

# 将图片转换成字符串
text = pytesseract.image_to_string(image, lang='chi_sim')

# 输出识别结果
print(text)