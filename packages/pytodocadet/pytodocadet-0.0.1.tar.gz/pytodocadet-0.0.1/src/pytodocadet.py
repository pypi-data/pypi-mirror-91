import sys
import os
from PyQt5.QtCore import QBuffer, QSettings
from PyQt5.QtGui import QBrush, QColor, QStandardItem
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class taskerror(QDialog):
    def __init__(self):
        super(taskerror, self).__init__()
        loadUi('taskerror.ui', self)
        self.taskerrorbtn.clicked.connect(self.ok)

    def ok(self):
        taskerror.close(self)


class removeerror(QDialog):
    def __init__(self):
        super(removeerror, self).__init__()
        loadUi('removeerror.ui', self)
        self.removeerrorbtn.clicked.connect(self.ok)

    def ok(self):
        removeerror.close(self)
        
class selectionerror(QDialog):
    def __init__(self):
        super(selectionerror, self).__init__()
        loadUi('selectionerror.ui', self)
        self.selecterrorbtn.clicked.connect(self.ok)

    def ok(self):
        selectionerror.close(self)



class pytodo(QMainWindow):

    def __init__(self):
        super(pytodo, self).__init__()
        loadUi('pytodo.ui', self)
        
        colors = ['white', 'blue', 'green', 'yellow', 'orange', 'red']
        items =['Choose a level', 'Optional', 'Not Important', 'Quite Important', 'Important','Very Important']
        model = self.level.model()
        for row in range(6):
            item = QStandardItem(items[row])
            item.setBackground(QColor(colors[row]))
            font = item.font()
            font.setPointSize(14)
            item.setFont(font)
            model.appendRow(item)

        self.addnewbtn.clicked.connect(self.addnewtask)
        self.removebtn.clicked.connect(self.deleteitem)
        self.clearbtn.clicked.connect(self.clearlist)
        self.level.currentIndexChanged.connect(self.newlevel)
        
        self.save_filenew = 'save_filenew.txt'
        self.read_from_filenew(self.save_filenew)
        self.save_filemake = 'save_filemake.txt'
        self.read_from_filemake(self.save_filemake)
        self.save_filedone = 'save_filedone.txt'
        self.read_from_filedone(self.save_filedone)
        
        self.save_filenewcolor = 'save_filenewcolor.txt'
        self.read_from_filenewcolor(self.save_filenewcolor)
        self.save_filemakecolor = 'save_filemakecolor.txt'
        self.read_from_filemakecolor(self.save_filemakecolor)
        self.save_filedonecolor = 'save_filedonecolor.txt'
        self.read_from_filedonecolor(self.save_filedonecolor)
        
    def sayHello(name):
        if name is None:
            print('Hello User')
        else:
            print(f'Hello {name}')
        
    def write_to_filenew(self, file):
        try:
            list_widget = self.newtask
            entries = '\n'.join(list_widget.item(ii).text() for ii in range(list_widget.count()))
            #colors = '\n'.join(list_widget.item(ii).background().color().name() for ii in range(list_widget.count()))
            with open(file, 'w') as fout:
                fout.write(entries)
                #fout.write(colors)
        except OSError as err:
            print(f"file {file} could not be written")

    def read_from_filenew(self, file):
        try:
            list_widget = self.newtask
            with open(file, 'r') as fin:
                entries = [e.strip() for e in fin.readlines()]
            list_widget.insertItems(0, entries)
        except OSError as err:
            with open(file, 'w'):
                pass
    
    def write_to_filemake(self, file):
        try:
            list_widget = self.maketask
            entries = '\n'.join(list_widget.item(ii).text() for ii in range(list_widget.count()))
            #colors = '\n'.join(list_widget.item(ii).background().color().name() for ii in range(list_widget.count()))
            with open(file, 'w') as fout:
                fout.write(entries)
                #fout.write(colors)
        except OSError as err:
            print(f"file {file} could not be written")

    def read_from_filemake(self, file):
        try:
            list_widget = self.maketask
            with open(file, 'r') as fin:
                entries = [e.strip() for e in fin.readlines()]
            list_widget.insertItems(0, entries)
        except OSError as err:
            with open(file, 'w'):
                pass
    
    def write_to_filedone(self, file):
        try:
            list_widget = self.donetask
            entries = '\n'.join(list_widget.item(ii).text() for ii in range(list_widget.count()))
            #colors = '\n'.join(list_widget.item(ii).background().color().name() for ii in range(list_widget.count()))
            with open(file, 'w') as fout:
                fout.write(entries)
                #fout.write(colors)
        except OSError as err:
            print(f"file {file} could not be written")

    def read_from_filedone(self, file):
        try:
            list_widget = self.donetask
            with open(file, 'r') as fin:
                entries = [e.strip() for e in fin.readlines()]
            list_widget.insertItems(0, entries)
        except OSError as err:
            with open(file, 'w'):
                pass
    
    def write_to_filenewcolor(self, file):
        try:
            list_widget = self.newtask
            #entries = '\n'.join(list_widget.item(ii).text() for ii in range(list_widget.count()))
            colors = '\n'.join(list_widget.item(ii).background().color().name() for ii in range(list_widget.count()))
            with open(file, 'w') as fout:
                #fout.write(entries)
                fout.write(colors)
        except OSError as err:
            print(f"file {file} could not be written")

    def read_from_filenewcolor(self, file):
        try:
            list_widget = self.newtask
            with open(file, 'r') as fin:
                colors = [e.strip() for e in fin.readlines()]
            for item in range(list_widget.count()):
                if colors[item] == '#000000':
                    list_widget.item(item).setBackground(QColor('#ffffff'))
                else:
                    list_widget.item(item).setBackground(QColor(colors[item]))
        except OSError as err:
            with open(file, 'w'):
                pass
    
    def write_to_filemakecolor(self, file):
        try:
            list_widget = self.maketask
            #entries = '\n'.join(list_widget.item(ii).text() for ii in range(list_widget.count()))
            colors = '\n'.join(list_widget.item(ii).background().color().name() for ii in range(list_widget.count()))
            with open(file, 'w') as fout:
                #fout.write(entries)
                fout.write(colors)
        except OSError as err:
            print(f"file {file} could not be written")

    def read_from_filemakecolor(self, file):
        try:
            list_widget = self.maketask
            with open(file, 'r') as fin:
                colors = [e.strip() for e in fin.readlines()]
            for item in range(list_widget.count()):
                if colors[item] == '#000000':
                    list_widget.item(item).setBackground(QColor('#ffffff'))
                else:
                    list_widget.item(item).setBackground(QColor(colors[item]))
        except OSError as err:
            with open(file, 'w'):
                pass
    
    def write_to_filedonecolor(self, file):
        try:
            list_widget = self.donetask
            #entries = '\n'.join(list_widget.item(ii).text() for ii in range(list_widget.count()))
            colors = '\n'.join(list_widget.item(ii).background().color().name() for ii in range(list_widget.count()))
            with open(file, 'w') as fout:
                #fout.write(entries)
                fout.write(colors)
        except OSError as err:
            print(f"file {file} could not be written")

    def read_from_filedonecolor(self, file):
        try:
            list_widget = self.donetask
            with open(file, 'r') as fin:
                colors = [e.strip() for e in fin.readlines()]
            for item in range(list_widget.count()):
                if colors[item] == '#000000':
                    list_widget.item(item).setBackground(QColor('#ffffff'))
                else:
                    list_widget.item(item).setBackground(QColor(colors[item]))
        except OSError as err:
            with open(file, 'w'):
                pass
    
    
    def closeEvent(self, event):
        should_save = QMessageBox.question(self, "Save Tasks", "Do you want to save tasks?", defaultButton = QMessageBox.Yes)
        if should_save == QMessageBox.Yes:
            self.write_to_filenew(self.save_filenew)
            self.write_to_filemake(self.save_filemake)
            self.write_to_filedone(self.save_filedone)
            
            self.write_to_filenewcolor(self.save_filenewcolor)
            self.write_to_filemakecolor(self.save_filemakecolor)
            self.write_to_filedonecolor(self.save_filedonecolor)
        return super().closeEvent(event)
        

    def newlevel(self):
        
        selecteditemsnew = self.newtask.selectedItems()
        selecteditemsmake = self.maketask.selectedItems()
        selecteditemsdone = self.donetask.selectedItems()
        
        if not selecteditemsnew and not selecteditemsmake and not selecteditemsdone:
            self.serr = selectionerror()
            self.serr.show()
            self.serr.exec_()
            
        else:

            if self.level.itemText(self.level.currentIndex()) == 'Optional':
                if selecteditemsmake:
                    for item in selecteditemsmake:
                        item.setBackground(QColor('blue'))
                        item.setSelected(False)
                    
                if selecteditemsnew:
                    for item in selecteditemsnew:
                        item.setBackground(QColor('blue'))
                        item.setSelected(False)

                if selecteditemsdone:
                    for item in selecteditemsdone:
                        item.setBackground(QColor('blue'))
                        item.setSelected(False)

            elif self.level.itemText(self.level.currentIndex()) == 'Not Important':
                if selecteditemsmake:
                    for item in selecteditemsmake:
                        item.setBackground(QColor('green'))
                        item.setSelected(False)

                if selecteditemsnew:
                    for item in selecteditemsnew:
                        item.setBackground(QColor('green'))
                        item.setSelected(False)

                if selecteditemsdone:
                    for item in selecteditemsdone:
                        item.setBackground(QColor('green'))
                        item.setSelected(False)

            elif self.level.itemText(self.level.currentIndex()) == 'Quite Important':
                if selecteditemsmake:
                    for item in selecteditemsmake:
                        item.setBackground(QColor('yellow'))
                        item.setSelected(False)

                if selecteditemsnew:
                    for item in selecteditemsnew:
                        item.setBackground(QColor('yellow'))
                        item.setSelected(False)

                if selecteditemsdone:
                    for item in selecteditemsdone:
                        item.setBackground(QColor('yellow'))
                        item.setSelected(False)

            elif self.level.itemText(self.level.currentIndex()) == 'Important':
                if selecteditemsmake:
                    for item in selecteditemsmake:
                        item.setBackground(QColor('orange'))
                        item.setSelected(False)

                if selecteditemsnew:
                    for item in selecteditemsnew:
                        item.setBackground(QColor('orange'))
                        item.setSelected(False)

                if selecteditemsdone:
                    for item in selecteditemsdone:
                        item.setBackground(QColor('orange'))
                        item.setSelected(False)

            elif self.level.itemText(self.level.currentIndex()) == 'Very Important':
                if selecteditemsmake:
                    for item in selecteditemsmake:
                        item.setBackground(QColor('red'))
                        item.setSelected(False)

                if selecteditemsnew:
                    for item in selecteditemsnew:
                        item.setBackground(QColor('red'))
                        item.setSelected(False)

                if selecteditemsdone:
                    for item in selecteditemsdone:
                        item.setBackground(QColor('red'))
                        item.setSelected(False)
            else:
                return

    def clearlist(self):
        self.newtask.clear()
        self.maketask.clear()
        self.donetask.clear()

    def deleteitem(self):
        selecteditemsnew = self.newtask.selectedItems()
        selecteditemsmake = self.maketask.selectedItems()
        selecteditemsdone = self.donetask.selectedItems()

        if not selecteditemsdone and not selecteditemsmake and not selecteditemsnew:
            self.err = removeerror()
            self.err.show()
            self.err.exec_()
        else:
            if selecteditemsdone:
                for item in selecteditemsdone:
                    self.donetask.takeItem(self.donetask.row(item))
            if selecteditemsmake:
                for item in selecteditemsmake:
                    self.maketask.takeItem(self.maketask.row(item))
            if selecteditemsnew:
                for item in selecteditemsnew:
                    self.newtask.takeItem(self.newtask.row(item))

    def addnewtask(self):
        task = self.tasktext.toPlainText()
        if task == '':
            self.err = taskerror()
            self.err.show()
            self.err.exec_()
        else:
            self.newtask.addItem(task)
            self.tasktext.clear()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = pytodo()
    widget.show()
    sys.exit(app.exec_())
    
