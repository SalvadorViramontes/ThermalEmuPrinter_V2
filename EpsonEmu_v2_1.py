# -*- coding: utf-8 -*-
"""
--- EpsonEmu_V2_1 ---
This program uses the Pillow library for the image creation and OCR reading for text output.
This program was not created with economic interests or recognition, it is only shared 
    for those who may need it.
@author: SalvadorViramontes
"""

import numpy as np
from PIL import Image 
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

class InterMethods():
    bformat = '{:0'+str(8)+'b}'
    
    def __init__(self):
        pass

    def hexstr2char(hexstring):
        str2bytes = []
        for i in range(len(hexstring)//2):
            arg = int(hexstring[2*i:(2*i)+2],16)
            str2bytes.append(arg)
        return str2bytes

    def dedouble(charlist):
        return [charlist[i] for i in range(len(charlist)) if i % 2 == 0]

    def char2binpixel(charlist):
        string = ""
        for num in charlist: 
            string += InterMethods.bformat.format(num)
        return [255*(1-int(digit)) for digit in string]
    
    def padding(mat, rows, cols):
        pad = 255*np.ones((rows,192-cols))
        return np.concatenate((mat, pad), axis=1)
    
    def binpixel2preimage(pixelistup, pixelistdw, shp):
        pixup = np.array(pixelistup).reshape(shp[1],shp[0])
        pixdw = np.array(pixelistdw).reshape(shp[1],shp[0])
        pix = np.concatenate((pixup, pixdw), axis=1)
        return pix.transpose()

    def doublesplit(alist):
        invstring = alist[::-1]
        i = 0
        for i in range(len(invstring)//2):
            start = 2*i
            end = (2*i)+1
            arg = invstring[start:end+1]
            if not (arg[0] == arg[1]):
                break
        return alist[:-(2*i)], alist[-(2*i):]

    def tailtrimmer(alist):
        invstring = alist[::-1]
        ans = []
        i = 0
        for i in range(len(invstring)//3):
            arg = invstring[i:i+3]
            ans.append(arg)
            if (arg[2] == arg[1]):
                break
        return alist[:-(i+1)]

    def rowreader(blist):
        templist_0 = blist
        len1 = 0
        len2 = 0
        rows = []
        while True:
            templist_1 = InterMethods.tailtrimmer(templist_0)
            templist_2, inf_list = InterMethods.doublesplit(templist_1)
            len1 = len(inf_list)
            templist_3 = InterMethods.tailtrimmer(templist_2)
            templist_0, sup_list = InterMethods.doublesplit(templist_3)
            len2 = len(sup_list)
            if len1 == len2:
                row = (sup_list, inf_list)
                rows.append(row)
            else:
                break
        return rows


class Printer(InterMethods):
    def __init__(self, hexstring):
        self.hex_msg = hexstring
        self.char_msg = InterMethods.hexstr2char(self.hex_msg)
        
    def processdata(self):
        renglones = InterMethods.rowreader(self.char_msg)
        self.pixs = []
        for renglon in renglones:
            charline_sup = InterMethods.dedouble(renglon[0])
            charline_inf = InterMethods.dedouble(renglon[1])
            pixelist_sup = InterMethods.char2binpixel(charline_sup)
            pixelist_inf = InterMethods.char2binpixel(charline_inf)
            shape = (8, len(pixelist_sup)//8)
            pic = InterMethods.binpixel2preimage(pixelist_sup, pixelist_inf, shape)
            self.pixs.append(pic)
        
    def printdata(self, mode = 0):
        if mode == 0:
            self.pics = []
            for pix in self.pixs:
                shape = np.shape(pix)
                if not (shape[1] == 192):
                    newpix = InterMethods.padding(pix, shape[0], shape[1])
                    self.pics.append(newpix)
                    continue
                self.pics.append(pix)
            rows = len(self.pics)
            for i in range(rows):
                if i == 0:
                    self.image = self.pics[rows-1]
                else:
                    self.image = np.concatenate((self.image, self.pics[rows-i-1]), axis=0)
            del self.pixs
            del self.pics
            self.image = Image.fromarray(np.uint8(self.image))
            self.image.save('output.png')
            return self.image
        else:
            self.msgs = []
            for i in range(len(self.pixs)):
                self.msgs.append(pytesseract.image_to_string(self.pixs[-(i+1)]))
            file = open("output.txt","w+")
            for msg in self.msgs:
                file.write(msg + "\n")
            file.close()
            del file
            return self.msgs