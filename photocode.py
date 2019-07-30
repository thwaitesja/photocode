#!/usr/bin/env python3

#justin Thwaites
from PIL import Image
from PyQt5.QtWidgets import *
import sys

class photocode():
    def __init__(self, type = 'r', filename = '', message = '', messagefile = ''):
        self.myimageName = filename
        self.message = message
        self.type = type
        if not self.myimageName:
            self.myimageName = self.get_file_name()
        if self.type == 'w' and not self.message:
            self.message = self.input_message(messagefile)
        self.myimage = self.prepfile()

    def get_file_name(self):
        file = input('what image filename?')
        if '.png' not in file and '.jpg' not in file:
            file += '.png'
        return file

    def input_message(self, messagefile):
        if messagefile:
            filename = messagefile
            if '.' not in filename:
                filename += '.txt'
            with open(filename, 'r') as my_file:
                header = filename.split('.')[1][:2]
                return '\n' + header + my_file.read()
        else:
            if input('Is desired message in a text file y/n')[0] == 'y':
                filename = input('Enter your text file name')
                if '.' not in filename:
                    filename += '.txt'
                with open(filename, 'r') as my_file:
                    header = filename.split('.')[1][:2]
                    return '\n' + header + my_file.read()
            else:
                return input('Enter your message')

    def prepfile(self, filename = None):
        if not filename:
            filename = self.myimageName
        myimage = Image.open(filename)
        if myimage.mode not in "RGBA":
            print('Not a possible color format')
        return myimage

    def read_message(self):
        header = self.get_chars(2)
        if header == 'jt':
            self.message = self.get_message()
            print(self.message)
        elif header == 'py':
            self.message = self.get_message()
            with open('message.pyw', 'w') as my_file:
                my_file.write(self.message)
        elif header == 'tx':
            self.message = self.get_message()
            with open('message.txt', 'w') as my_file:
                my_file.write(self.message)
        else:
            print('no message')

    def get_chars(self, num):
        bytes = 0b1
        count = 0
        row = self.myimage.size[0]
        col = self.myimage.size[1]
        pixels = self.myimage.load()
        for i in range(row):  # range(1): # for every pixel:
            for j in range(col):
                if count == num * 8 + 3:
                    break
                bytes = (bytes << 1) | pixels[i, j][0] & 1  # bitwise
                count += 1
        m = int(bin(bytes)[3:(len(bin(bytes)) - 2) // 8 * 8 + 2], 2)  # normalizing and trunkating the bytes
        return m.to_bytes((m.bit_length() + 7) // 8, 'big').decode(errors='ignore')

    def send_message(self, message = '', file= ''):
        if not file:
            file = self.myimageName.split('/')[-1].split('.')[0] +'.png'
        print(file)
        if not message:
            message = self.message
        col = self.myimage.size[1]
        pixels = self.myimage.load()
        header = 'jt'
        if len(message) > 2 and message[0] == '\n':
            header = message[1:3]
            message = message[3:]
        message_size = str(len(message))
        message = header + '0' * (5 - len(message_size)) + message_size + message
        message = bin(int.from_bytes(message.encode(), 'big'))
        if len(self.myimage.mode) == 4:
            for num, bits in enumerate(message[2:]):
                pixels[num // col, num % col] = (
                    pixels[num // col, num % col][0] // 2 * 2 + int(bits), pixels[num // col, num % col][1],
                    pixels[num // col, num % col][2], pixels[num // col, num % col][3])
            self.myimage.save(file)
        elif len(self.myimage.mode) == 3:
            for num, bits in enumerate(message[2:]):
                pixels[num // col, num % col] = (
                    pixels[num // col, num % col][0] // 2 * 2 + int(bits), pixels[num // col, num % col][1],
                    pixels[num // col, num % col][2])
            self.myimage.save(file)
        else:
            print('unknown stored type')

    def get_message(self):
        message_length = int(self.get_chars(7)[2:])
        return self.get_chars(message_length + 7)[7:]

    def get_file_name(self):
        file = input('what image filename?')
        if '.png' not in file and '.jpg' not in file:
            file += '.png'
        self.myimageName = file
        return file

    def execute(self):
        if self.type == 'r':
            self.read_message()
        else:
            self.send_message()


class FileEdit(QLineEdit):
    def __init__(self, parent):
        super(FileEdit, self).__init__(parent)
        self.setReadOnly(True)
        self.setDragEnabled(True)
        self.filepath = ''

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            self.filepath = str(urls[0].path())[1:]
            # any file type here
            if self.filepath[-4:].lower() in [".txt", '.jpg', '.png'] or self.filepath[-3:].lower() == ".py":
                self.setText(self.filepath.split('/')[-1])
            else:
                print(self.filepath)
                dialog = QMessageBox()
                dialog.setWindowTitle("Error: Invalid File")
                dialog.setText("Only .txt files are accepted")
                dialog.setIcon(QMessageBox.Warning)
                dialog.exec_()


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("PHOTOCODE")
        layout = QGridLayout()
        self.setLayout(layout)
        plabel = QLabel('Drag Photo')
        mlabel = QLabel('Drag Message')
        self.photo = FileEdit(self)
        self.message = FileEdit(self)
        self.read = QPushButton('Read')
        self.write = QPushButton('Write')
        layout.addWidget(plabel, 0, 0)
        layout.addWidget(mlabel, 1, 0)
        layout.addWidget(self.photo, 0, 1)
        layout.addWidget(self.message, 1, 1)
        self.write.clicked.connect(self.pic_write)
        self.read.clicked.connect(self.pic_read)
        layout.addWidget(self.read, 2, 0)
        layout.addWidget(self.write, 2, 1)

    def pic_read(self):
        if self.photo.filepath:
            photocode('r', self.photo.filepath).execute()
        self.close()

    def pic_write(self):
        if self.photo.filepath and self.message.filepath:
            photocode('w', self.photo.filepath, messagefile=self.message.filepath).execute()
        self.close()



app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())


#photocode(input('Read or Write?').lower()[0]).execute()
