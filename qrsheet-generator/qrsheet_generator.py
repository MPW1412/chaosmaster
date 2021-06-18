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
    def __init__(self, sheetTemplate, offsetRows = 0, offsetColumns = 0, ppi = 600):
        if sheetTemplate not in SHEET_DIMENSIONS:
            raise Exception('Unknown Sheet Configuration')
        self.__sheetTemplateName = sheetTemplate
        self.__sheetDimensions = SHEET_DIMENSIONS[self.__sheetTemplateName]['dimensions']
        self.__pixel_per_mm = ppi/25.4
        self.__margin = 1
        
        self.__sheets = []
        self.__newPage(offsetRows, offsetColumns)

        
    def __newPage(self, offsetRows = 0, offsetColumns = 0):
        self.__position_columns = offsetColumns-1
        self.__position_rows = offsetRows
        self.__sheets.append(Image.new(
                str(1),
                (round(self.__sheetDimensions['sheet_width']*self.__pixel_per_mm),
                    round(self.__sheetDimensions['sheet_height']*self.__pixel_per_mm)),
                color=1))

    def imageSheet(self):
        return self.__sheets

    def __next_position_in_pixel(self):
        self.__position_columns += 1
        if self.__position_columns == self.__sheetDimensions['columns']:
            self.__position_columns = 0
            self.__position_rows += 1
            if self.__position_rows == self.__sheetDimensions['rows']:
                self.__newPage()
                self.__position_columns += 1
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
            self.__sheets[-1].paste(ImgObj, pos)
            
    def save_pages_as_pdf(self):
        del_names = ""
        pdf_names = ""
        for j in range(0, len(self.__sheets)):
            name = f".tmp-{j}"
            self.__sheets[j].save(f"{name}.png")
            os.system(f"convert {name}.png -page a4 {name}.pdf")
            pdf_names += f" {name}.pdf"
            del_names += f" {name}.png {name}.pdf"
        os.system(f"pdftk {pdf_names} cat output print-labels.pdf")
        os.system(f"rm {del_names}")
        
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
    
    def __init__(self, dimensions, uuidObj: uuid, imhCode: str, description: str = None,
            secondary_description: str = None, navigationArrow: chr = None, navigationText: str = None,
            drawBorders: bool = False) -> None:
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
            fontObj = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSansSymbols2-Regular.ttf', 350, encoding = 'utf-8')
            w, h = fontObj.getsize(WideLabel.ORIENTATION_ARROWS[navigationArrow])
            x1 = (x * 0.17 - w)/2
            y1 = (0.33 * y - h)/2
            draw.text((x1, y1), WideLabel.ORIENTATION_ARROWS[navigationArrow], font = fontObj)
            fontObj = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 68, encoding = 'utf-8')
            orientation_lines = WideLabel.wrap_text(navigationText, 0.16*x, fontObj)
            total_height = 0
            for line in orientation_lines:
                w, h = fontObj.getsize(line)
                total_height += h + 0.01*y 
            total_height -= 0.01*y
            height_counter = 0.67*y-total_height/2
            for line in orientation_lines:
                w, h = fontObj.getsize(line)
                draw.text(((0.17*x-w)/2, height_counter), line, font = fontObj)
                height_counter += h + 0.01*y
            
        fontObj = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 150, encoding = 'utf-8')
        description_lines = WideLabel.wrap_text(description, 0.48*x-0.05*y, fontObj)
        height_counter = 0.05*y
        for line in description_lines:
            draw.text((round(x*0.52 ), height_counter), line, font = fontObj)
            w, h = fontObj.getsize(line)
            height_counter += h + 0.02*y
        fontObj = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 75, encoding = 'utf-8')
        secondary_description_lines = WideLabel.wrap_text(secondary_description, 0.48*x-0.05*y, fontObj)
        height_counter += 0.02*y
        for line in secondary_description_lines:
            draw.text((round(x*0.52 ), height_counter), line, font = fontObj)
            w, h = fontObj.getsize(line)
            height_counter += h + 0.01*y
        if drawBorders:
            draw.line([(0,0), (x-1, 0), (x-1,y-1), (0, y-1), (0,0)], fill=None, width=1)
            
    def wrap_text(text, width, font):
        text_lines = []
        text_line = []
        text = text.replace('\n', ' [br] ')
        words = text.split()
        font_size = font.getsize(text)
    
        for word in words:
            if word == '[br]':
                text_lines.append(' '.join(text_line))
                text_line = []
                continue
            text_line.append(word)
            w, h = font.getsize(' '.join(text_line))
            if w > width:
                text_line.pop()
                text_lines.append(' '.join(text_line))
                text_line = [word]
    
        if len(text_line) > 0:
            text_lines.append(' '.join(text_line))
    
        return text_lines

def iMH():
    return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(12))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('label', type=str, nargs='+', 
            help='One Label per argument, subarguments semicolon separated: title; subtitle; count')
    parser.add_argument('--offsetRows', '-oR', type=int, help='Offset count rows', default=0)
    parser.add_argument('--offsetColumns', '-oC', type=int, help='Offset count columns', default=0)
    parser.add_argument('--print-borders', action="store_true", help="Print borders around labels, for testing only")
    args = parser.parse_args()

    qrsg = QrSheetGenerator('topStick_8715_Universal_Etiketten_DINA4_105x48mm',
            offsetRows = args.offsetRows, offsetColumns = args.offsetColumns)

    for label in args.label:
        title, subtitle, count = label.split(';')
        
        if count is None or count == "":
            count = 1
        else:
            count = int(count)

        labelObj = WideLabel(SHEET_DIMENSIONS['topStick_8715_Universal_Etiketten_DINA4_105x48mm']['dimensions'],
                uuid.uuid4(), iMH(), title, subtitle, None, None, drawBorders=args.print_borders)
        qrsg.insert_label(labelObj.img, repeat=count)
    
    qrsg.save_pages_as_pdf()

    
        
    

