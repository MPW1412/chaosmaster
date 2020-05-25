import qrcode
import uuid
from PIL import Image

SHEET_DIMENSIONS = { 
        '100DINA4_BOEGEN_vielzweck_etiketten': {
            'EAN': '4042318015549',
            'article-number': '65020207',
            'manufacteurer': 'endihaft',
            'comment': 'Din A4 sheet of labels 20x20 mm one-sided adhesive',
            'dimensions': {
                'sheet_margin_left': 15,
                'sheet_margin_right': 15,
                'sheet_margin_top': 8.5,
                'sheet_margin_bottom': 8.5,
                'label_width': 20,
                'label_height': 20,
                'sheet_width': 210,
                'sheet_height': 297,
                'rows': 14,
                'columns': 9,
                'row_distance': 0,
                'column_distance': 0
                }
            }
        }


class QrSheetGenerator:
    def __init__(self, count, sheetDimensions, offsetRows = 0, offsetColumns = 0, ppi = 600):
        self.__sheetDimensions = sheetDimensions
        self.__position_columns = offsetColumns-1
        self.__position_rows = offsetRows
        self.__pixel_per_mm = ppi/25.4
        self.__margin = 2

        self.__sheet = Image.new(
                str(1),
                (round(self.__sheetDimensions['sheet_width']*self.__pixel_per_mm),
                    round(self.__sheetDimensions['sheet_height']*self.__pixel_per_mm)),
                color=1)

        while count > 0:
            """
            box_size=13 is an ugly hack so far. Giving the pixel per block seems to be
            the only way to set the size of the resulting qrcode img object. 
            A UUID seems to need 29 blocks.
            Needs a proper FIX
            """
            img = qrcode.make(str(uuid.uuid1()), box_size=13)
            pos = self.__next_position_in_pixel()
            self.__sheet.paste(img, pos)
            count -= 1

    def imageSheet(self):
        return self.__sheet

    def __next_position_in_pixel(self):
        self.__position_columns += 1
        if self.__position_columns == self.__sheetDimensions['columns']:
            self.__position_columns = 0
            self.__position_rows += 1
            if self.__position_rows == self.__sheetDimensions['rows']:
                raise Exception('Number of rows exceeded.')
        return (
            round((self.__sheetDimensions['sheet_margin_left']
                    + self.__position_columns * self.__sheetDimensions['label_width']
                    + self.__margin) * self.__pixel_per_mm),
            round((self.__sheetDimensions['sheet_margin_top']
                    + self.__position_rows * self.__sheetDimensions['label_height']
                    + self.__margin) * self.__pixel_per_mm))


if __name__ == "__main__":
    qrsg = QrSheetGenerator(10, SHEET_DIMENSIONS['100DINA4_BOEGEN_vielzweck_etiketten']['dimensions'])
    qrsg.imageSheet().save('test.png')







