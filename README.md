# ThermalEmuPrinter_V2
 Virtual Emulator for a Epson TM-T58 Thermal Printer

This program written in Python, creates a virtual printer emulator via Serial USB to print as an image or with the use of a OCR (Tesseract OCR) extract the text that is printed.

There exist two variants, one using Pillow (v2_1) library and the other with the OpenCV (v2_2) library.

Make sure you install the Tesseract OCR and the Pillow or OpenCV libraries in order to run this program.
Tesseract OCR is wrapped within the pytesseract library for it's use with Python.
All this libraries can be installed via pip as follows:

	- Pytesseract: pip install pytesseract
	- OpenCV: pip install opencv-python
	- Pillow: pip install pillow 
