# photocode
This is a python code that uses Least Significant Bit (LSB) encoding as a way of storing a text file in a png image with minor non-noticeable distortion to the image.
This file allows for encoding into either a .jpg or a .png however when exporting the program will always export as a .png since .png is a lossless file type, while .jpg compressiong will distort the Least Significant Bits of the pixels ruining the message being stored there.
The current version supports messages as either .txt files or as .py files being encoded or decoded.
Each message is stored in each red pixel where the first 2 bytes (16 pixels worth of LSB) of information stores a header specifying the file type and the next 5 bytes specify the length of the file so the message and only the message is decoded.
