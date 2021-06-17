#! /usr/bin/env python3

import qrcode
import uuid
from PIL import Image, ImageDraw, ImageFont
from sheet_templates import SHEET_DIMENSIONS
import textwrap
import random
import argparse
import os

class QrSheetGenerator:
    def __init__(self, sheetDimensions, offsetRows = 0, offsetColumns = 0, ppi = 600):
        self.__sheetDimensions = sheetDimensions
        self.__position_columns = offsetColumns-1
        self.__position_rows = offsetRows
        self.__pixel_per_mm = ppi/25.4
        self.__margin = 1

        self.__sheet = Image.new(
                str(1),
                (round(self.__sheetDimensions['sheet_width']*self.__pixel_per_mm),
                    round(self.__sheetDimensions['sheet_height']*self.__pixel_per_mm)),
                color=1)

#        while count > 0:
#            """
#            box_size=13 is an ugly hack so far. Giving the pixel per block seems to be
#            the only way to set the size of the resulting qrcode img object. 
#            A UUID seems to need 29 blocks.
#            Needs a proper FIX
#            """
#            uuidObj = uuid.uuid1()
#            print (str(uuidObj))
#            img = qrcode.make('c0h.de/' + str(uuidObj) + 'yah6Tai7Fi', box_size=10)
#            pos = self.__next_position_in_pixel()
#            self.__sheet.paste(img, pos)
#            count -= 1

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
                    + self.__position_rows * self.__margin) * self.__pixel_per_mm))
    
    def insert_label(self, ImgObj: Image, repeat: int = 1):
        for j in range(0, repeat):
            pos = self.__next_position_in_pixel()
            self.__sheet.paste(ImgObj, pos)
            


class WideLabel:
    ORIENTATION_ARROWS = {
        'N': u'\U0001f871',
        'NE': u'🡵',
        'E': u'🡲',
        'SE': u'🡶',
        'S': u'🡳',
        'SW': u'🡷',
        'W': u'🡰',
        'NW': u'🡴'
    }
    
    def __init__(self, dimensions, uuidObj: uuid, imhCode: str, description: str = None, secondary_description: str = None, navigationArrow: chr = None, navigationText: str = None) -> None:
        self.uuid = uuid
        self.imhCode = imhCode
        self.description = description
        self.navigationArrow = navigationArrow
        self.navigationText = navigationText
        self.ppi = 600
        self.__pixel_per_mm = self.ppi/25.4
        self.__dimensions = dimensions
        x = round(self.__dimensions['label_width']*self.__pixel_per_mm)
        y = round(self.__dimensions['label_height']*self.__pixel_per_mm)
        self.img = Image.new(str(1), (x, y), color=1)
        draw = ImageDraw.Draw(self.img)
        draw.line([x * 0.17, y * 0.04, x * 0.17, y * 0.96], fill=None, width=2)
        draw.line([x * 0.171 + 0.73 * y, y * 0.04, x * 0.171 + 0.73 * y, y * 0.96], fill=None, width=2)
        qrimg = qrcode.make('c0h.de/' + str(uuidObj) + '?c=' + imhCode, box_size=20)
        self.img.paste(qrimg, (round(x * 0.171), 0))
        fontObj = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 68, encoding="unic")
        draw.text((round(x * 0.19), round(0.78*y)), str(uuidObj)[0:18], font = fontObj)
        draw.text((round(x * 0.19), round(0.83*y)), str(uuidObj)[18:], font = fontObj)
        draw.text((round(x * 0.19), round(0.9*y)), 'IMH: ' + imhCode, font = fontObj)
        if navigationArrow is not None:
            fontObj = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 150, encoding = 'utf-8')
            draw.text((round(x*0.07), round(0.4*y)), WideLabel.ORIENTATION_ARROWS[navigationArrow], font = fontObj)
        fontObj = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 150, encoding = 'utf-8')
        draw.text((round(x*0.52 ), round(y * 0.05)), description, font = fontObj)
        fontObj = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 75, encoding = 'utf-8')
        draw.text((round(x*0.52 ), round(y * 0.51)), secondary_description, font = fontObj)

def iMH():
    return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(12))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('label', type=str, nargs='+', 
            help='One Label per argument, subarguments semicolon separated: title; subtitle; count')
    parser.add_argument('--offsetRows', '-oR', type=int, help='Offset count rows', default=0)
    parser.add_argument('--offsetColumns', '-oC', type=int, help='Offset count columns', default=0)
    args = parser.parse_args()

    qrsg = QrSheetGenerator(SHEET_DIMENSIONS['topStick_8715_Universal_Etiketten_DINA4_105x48mm']['dimensions'],
            offsetRows = args.offsetRows, offsetColumns = args.offsetColumns)

    for label in args.label:
        title, subtitle, count = label.split(';')
        
        if count is None or count == "":
            count = 1
        else:
            count = int(count)

        labelObj = WideLabel(SHEET_DIMENSIONS['topStick_8715_Universal_Etiketten_DINA4_105x48mm']['dimensions'],
                uuid.uuid4(), iMH(), textwrap.fill(title, width=14),
                textwrap.fill(subtitle, width=28),
                None, None )
        qrsg.insert_label(labelObj.img, repeat=count)

    qrsg.imageSheet().save('labels-p1.png')
    os.system("convert labels-p1.png -page a4 print-labels.pdf")
    
        
    

