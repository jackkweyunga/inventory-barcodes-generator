# import EAN13 from barcode module
import barcode
from barcode.writer import ImageWriter
import base64
from io import BytesIO

from PIL import Image


upc = barcode.get_barcode_class('upca')

# Make sure to pass the number as string
number = '00001000001'

# Now, let's create an object of EAN13
# class and pass the number
my_code = upc(number, ImageWriter())
text = "abc"

# Our barcode is ready. Let's save it.
image =my_code.render(text=my_code.get_fullcode())

buffered = BytesIO()
image.save(buffered, format="PNG")
img_str = base64.b64encode(buffered.getvalue())

im = Image.open(BytesIO(base64.b64decode(img_str)))
size = 800, 800
im.thumbnail(size)
im.show()

# print(img_str)