import barcode
from barcode.writer import ImageWriter
import base64
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import pathlib
import os

base_dir = pathlib.Path(__file__).parent.parent



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

    def generate(self, manufacturer_number, product_number, name, logo_path = None, logo_bytes=None, logo_b64 = None ):

        logo = ''
        try:
            if logo_b64:
                logo = self.make_image_from_b64(logo_b64)
            elif logo_bytes:
                logo = self.make_image_from_bytes(logo_bytes)
            elif logo_path:
                logo = Image.open(logo_path)
        except os.error as e:
            print('\n\n')
            print("error occured while trying toload the logo.")
            print(e)
            print('\n\n')

            pass
        

        number = f"{manufacturer_number}{product_number}"
        code = self.make_upc(number) # the barcode

        if type(logo) == Image:
            output = self.add_details_to_image(code, number, name, logo)
            code_b64 = self.make_b64(output) # the barcode in b64
            return code_b64
        else:
            print('\n\n')
            print("logo is not of type image")
            print('\n\n')
            return


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

    def make_image_from_bytes(self, bytes):
        im = Image.open(BytesIO(bytes))
        return im

    def add_details_to_image(self, barcode_image, number, name, logo):
        img1 = barcode_image
        img2 = logo

        output = Image.new('RGBA', (int(img1.size[0]*1.5), img1.size[1] + 100 ), (250, 250, 250, 0))

        img2.thumbnail((int(img1.size[0]/2-80), img1.size[1]-80))
        img1.thumbnail((img1.size[0], img1.size[1]-100))

        output.paste(img2, (0,100))
        output.paste(img1, (int(img1.size[0]/2),100))

        draw = ImageDraw.Draw(output, 'RGBA')

        text = name.upper()

        font = ImageFont.truetype(os.path.join(base_dir, 'resources/fonts/Comfortaa/static/Comfortaa-Bold.ttf'), 80)
        draw.text((0,0), text, (0,0,0), font=font, spacing=1.5, align='right')
        draw.text((img2.size[0], output.size[1]-100), number, (0,0,0), font=font, spacing=30, align='right')

        return output

