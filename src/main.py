import barcode
from barcode.writer import ImageWriter
import base64
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw



class Bars:

    '''
        uses UPC sytem to generate barcodes to lable inventory in a store or a warehouse.
        requires , 
        - the manufacturers/suppliers number in thousands.
        - the product number in ten thousands.
        - a (company/shop/store) logo (optional)
        - a (company/shop/store) name

    '''

    def __init__(self) -> None:
        pass

    def generate(self, manufacturer_number, product_number, name=None, logo_path = None, logo_bytes=None, logo_b64 = None ):

        number = f"{manufacturer_number}{product_number}"

        code = self.make_upc(number)

        code_b64 = self.make_b64(code)

        return code_b64


    def make_upc(self, number):

        upc = barcode.get_barcode_class('upca')
        code = upc(number, ImageWriter())

        return code

    def make_b64(self, image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())
        return img_str

    def make_image_from_b64(self, b64):
        im = Image.open(BytesIO(base64.b64decode(b64)))
        return im






