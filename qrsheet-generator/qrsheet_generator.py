#! /usr/bin/env python3

from settings import PRINTERS
import qrcode
import uuid
from PIL import Image, ImageDraw, ImageFont
from sheet_templates import SHEET_DIMENSIONS
from math import ceil
import textwrap
import random
import argparse
import os
from autocrop import Cropper

import sys

class QrSheetGenerator:
    def __init__(self, sheetTemplate, offsetRows = 0, offsetColumns = 0, ppi = 600, margins = None):
        if sheetTemplate not in SHEET_DIMENSIONS:
            raise Exception('Unknown Sheet Configuration')
        self.__sheetTemplateName = sheetTemplate
        self.__sheetDimensions = SHEET_DIMENSIONS[self.__sheetTemplateName]['dimensions']
        self.__pixel_per_mm = ppi/25.4
        self.__margin = 1
        
        self.__sheets = []
        self.__newPage(offsetRows, offsetColumns)
        if margins is not None:
            self.__margins = margins
        else:
            self.__margins = [0, 0, 0, 0]

    def __newPage(self, offsetRows = 0, offsetColumns = 0):
        self.__position_columns = offsetColumns-1
        self.__position_rows = offsetRows
        self.__sheets.append(Image.new(
                str(1),
                (ceil(self.__sheetDimensions['sheet_width']*self.__pixel_per_mm),
                    ceil(self.__sheetDimensions['sheet_height']*self.__pixel_per_mm)),
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
                    + self.__position_columns * self.__sheetDimensions['label_width']) * self.__pixel_per_mm),
            round((self.__sheetDimensions['sheet_margin_top']
                    + self.__position_rows * self.__sheetDimensions['label_height']) * self.__pixel_per_mm))
    
    def insert_label(self, imgObj: Image, repeat: int = 1):
        for j in range(0, repeat):
            pos = self.__next_position_in_pixel()
#            if self.__position_columns == self.__sheetDimensions['columns'] - 1:
            if self.__position_columns == 0:
                imgObj_rotated = imgObj.copy().rotate(180)
                self.__sheets[-1].paste(imgObj_rotated, pos)
            else: 
                self.__sheets[-1].paste(imgObj, pos)
            
    def save_pages_as_pdf(self):
        del_names = ""
        pdf_names = ""
        crops = (round(6 * self.__pixel_per_mm), round(6 * self.__pixel_per_mm),
                round(6 * self.__pixel_per_mm) + round((self.__sheetDimensions['sheet_width'] - 6 - 5) * self.__pixel_per_mm),
                round(6 * self.__pixel_per_mm) + round((self.__sheetDimensions['sheet_height'] - 6 - 3) * self.__pixel_per_mm))
        
        for j in range(0, len(self.__sheets)):
            name = f".tmp-{j}"
            self.__sheets[j].crop(crops).save(f"{name}.png")
            os.system(f"convert {name}.png -page a4 {name}.pdf")
            pdf_names += f" {name}.pdf"
            del_names += f" {name}.png {name}.pdf"
        os.system(f"pdftk {pdf_names} cat output print-labels.pdf")
        os.system(f"rm {del_names}")
        
    def get_left_margin_complying_with_printer_limitations_in_mm(self) -> int:
        # We're ignoring the case, that the right margin might be bigger than
        # the left, because haven't seen that out in the wild, yet.
        if self.__margins[0] <= self.__sheetDimensions['sheet_margin_left']:
            return 0
        return self.__margins[0] - self.__sheetDimensions['sheet_margin_left']

    def get_top_margin_complying_with_printer_limitations_in_mm(self) -> int:
        if self.__margins[1] <= self.__sheetDimensions['sheet_margin_top']:
            return 0
        return self.__margins[1] - self.__sheetDimensions['sheet_margin_top']

        




        
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
            drawBorders: bool = False, margins  = None) -> None:
        self.uuid = uuid
        self.imhCode = imhCode
        self.description = description
        self.navigationArrow = navigationArrow
        self.navigationText = navigationText
        self.ppi = 600
        self.__pixel_per_mm = self.ppi/25.4
        self.__dimensions = dimensions
        if margins is not None:
            self.__margins = margins
        else:
            self.__margins = [1, 1, 1, 1]

        x = self.__dimensions['label_width']
        y = self.__dimensions['label_height']
        self.img = Image.new(str(1), (self.to_pix(x), self.to_pix(y)), color=1)
        draw = ImageDraw.Draw(self.img)
        x_first_line = round(self.__margins[0] + (x - self.__margins[0] - self.__margins[2])*0.08)
        qrimg = qrcode.make('c0h.de/' + str(uuidObj) + '?c=' + imhCode, box_size=20)

        first_line_coords = [ self.to_pix(z) for z in [x_first_line, self.__margins[1], x_first_line, y - self.__margins[1]]]
        draw.line(first_line_coords, fill=None, width=2)
        self.img.paste(qrimg, (self.to_pix(x_first_line) + 2, self.to_pix(0.01 * y)))
        second_line_coords = list.copy(first_line_coords)
        second_line_coords[0] += qrimg.size[0] + 1
        second_line_coords[2] += qrimg.size[0] + 1
        draw.line(second_line_coords, fill=None, width=2)

        fontSize = 80
        fontObj = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", fontSize, encoding="unic")
        max_width = second_line_coords[0] - first_line_coords[0] - 6 * self.to_pix(0.01 * y)
        while (fontObj.getsize(str(uuidObj)[0:18])[0] > max_width):
            fontSize -= 1
            fontObj = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", fontSize, encoding="unic")
        font_width, font_height = fontObj.getsize(str(uuidObj)[0:18])
        x_font = first_line_coords[0] + 3 * self.to_pix(0.01 * y) + round((max_width - font_width)/2)

        draw.text((x_font, 2 * self.to_pix(0.01 * y) + qrimg.size[1]), str(uuidObj)[0:18], font = fontObj)
        draw.text((x_font, 3 * self.to_pix(0.01 * y) + qrimg.size[1] + font_height), str(uuidObj)[18:], font = fontObj)
        draw.text((x_font, 4 * self.to_pix(0.01 * y) + qrimg.size[1] + 2 * font_height), 'IMH: ' + imhCode, font = fontObj)

        if navigationArrow is not None:
            #max_font_width = first_line_coords[0] - 2 * self.to_pix(self.__margins[0])
            max_font_width = first_line_coords[0] - 2 * self.to_pix(0.01 * y)
            font_size = 350
            fontObj = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSansSymbols2-Regular.ttf', font_size, encoding = 'utf-8')
            while (fontObj.getsize(WideLabel.ORIENTATION_ARROWS[navigationArrow])[0] > max_font_width):
                font_size -= 1
                fontObj = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoSansSymbols2-Regular.ttf', font_size, encoding = 'utf-8')
            w, h = fontObj.getsize(WideLabel.ORIENTATION_ARROWS[navigationArrow])
            x1 = round((first_line_coords[0] - w)/2)
            y1 = round(self.to_pix(0.33 * y) - h/2)-h/2
            draw.text((x1, y1), WideLabel.ORIENTATION_ARROWS[navigationArrow], font = fontObj)
            fontObj = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', fontSize, encoding = 'utf-8')
            orientation_lines = WideLabel.wrap_text(navigationText, max_font_width, fontObj)
            total_height = 0
            for line in orientation_lines:
                w, h = fontObj.getsize(line)
                total_height += h + 0.01*y 
            total_height -= 0.01*y
            height_counter = round(self.to_pix(0.67*y)-total_height/2)
            for line in orientation_lines:
                w, h = fontObj.getsize(line)
                draw.text(((first_line_coords[0]-w)/2, height_counter), line, font = fontObj)
                height_counter += h + 0.01*y

        x_font = second_line_coords[0] + 2 + 3 * self.to_pix(0.01 * y) 
        fontObj = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 150, encoding = 'utf-8')
        description_lines = WideLabel.wrap_text(description, self.to_pix(x) - second_line_coords[0] - self.to_pix(0.03 * y) - self.to_pix(self.__margins[0]), fontObj)
        height_counter = self.to_pix(self.__margins[1] + 0.01*y)
        for line in description_lines:
            draw.text((x_font, height_counter), line, font = fontObj)
            w, h = fontObj.getsize(line)
            height_counter += h + 0.02*y
        fontObj = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', 75, encoding = 'utf-8')
        secondary_description_lines = WideLabel.wrap_text(secondary_description, self.to_pix(x) - second_line_coords[0] - self.to_pix(0.03 * y) - self.to_pix(self.__margins[0]), fontObj)
        height_counter += 0.02*y
        for line in secondary_description_lines:
            draw.text((x_font, height_counter), line, font = fontObj)
            w, h = fontObj.getsize(line)
            height_counter += h + 0.01*y
        if drawBorders:
            draw.line([(0,0), (self.to_pix(x)-1, 0), (self.to_pix(x)-1,self.to_pix(y)-1), (0, self.to_pix(y)-1), (0,0)], fill=None, width=1)
            
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
    
    def to_pix(self, val: int) -> int:
        return round(val * self.__pixel_per_mm)

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
    
    margins = PRINTERS[list(PRINTERS.keys())[0]]['margins']
    
    qrsg = QrSheetGenerator('topStick_8715_Universal_Etiketten_DINA4_105x48mm',
            offsetRows = args.offsetRows, offsetColumns = args.offsetColumns, margins = margins)
    label_left_margin = qrsg.get_left_margin_complying_with_printer_limitations_in_mm()
    label_top_margin = qrsg.get_top_margin_complying_with_printer_limitations_in_mm()

    for label in args.label:
        title, subtitle, count = label.split(';')
        
        if count is None or count == "":
            count = 1
        else:
            count = int(count)

        labelObj = WideLabel(SHEET_DIMENSIONS['topStick_8715_Universal_Etiketten_DINA4_105x48mm']['dimensions'],
                uuid.uuid4(), iMH(), title, subtitle,
                drawBorders=args.print_borders, margins = [label_left_margin, label_top_margin, label_left_margin, label_top_margin])
        qrsg.insert_label(labelObj.img, repeat=count)
    
    qrsg.save_pages_as_pdf()

    
        
    

