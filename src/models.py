import sys
from src.crud import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QLineEdit, QPushButton, QListWidget, QDialogButtonBox, QVBoxLayout, QGridLayout, QWidget
from PyQt5.QtCore import Qt


def create_app():
    app = QApplication(sys.argv)
    return app



TITLE: str = "To-Do-List"

HEADER_MAIN: str = "To-Do-Lists Overview"
HEADER_ENTRIES: str = "Manage entries"

MAIN_WIDTH: int = 1000
MAIN_HEIGHT: int = 800

STYLE_SHEET: str = """
QMainWindow{
    background-color: hsl(246, 72%, 54%);
}
QWidget{
    background-color: hsl(246, 72%, 54%);
}

QLabel{
    color: white;
    font-family: 'Elephant';
    font-size: 36px;
}

QLineEdit{
    background-color: hsl(246, 72%, 54%);
    color: white;
    font-family: 'Elephant';
    font-size: 36px;
}

QListWidget{
    background-color: hsl(246, 72%, 54%);
    color: white;
    font-family: 'Elephant';
    font-size: 32px;
}

QPushButton#UserButtons{
    font-family: 'Informal Roman';
    font-size: 40px;
    font-weight: bold;
    background-color: hsl(246, 96%, 39%);
    color: white;
}
QPushButton#UserButtons:hover{
    background-color: hsl(246, 96%, 69%);
}

QPushButton#SystemButtons{
    font-family: 'Elephant';
    font-size: 36px;
    background-color: hsl(354, 96%, 39%);
    color: white;
}
QPushButton#SystemButtons:hover{
    background-color: hsl(354, 96%, 50%);
}
"""



class OkDialog(QDialog):
    def __init__(self, title: str, text: str):
        super().__init__()
        self.setWindowTitle(title)
        
        lbl_info = QLabel(f"{text}", self)
        lbl_info.setAlignment(Qt.AlignCenter)
        
        button = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(button)
        self.buttonBox.accepted.connect(self.accept)
        
        layout = QVBoxLayout()
        layout.addWidget(lbl_info)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        
class ConfirmDialog(QDialog):
    def __init__(self, title: str, text: str):
        super().__init__()
        self.setWindowTitle(title)
        
        self.lbl_info = QLabel(f"{text}", self)
        self.lbl_info.setAlignment(Qt.AlignCenter)
        
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_info)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)



class EntryWindow(QWidget):
    def __init__(self, parent, listID: int):
        self.parent = parent
        self.list_id = listID
        self.entry_id = 0
        super().__init__()
        self.setWindowTitle(TITLE)
        self.setFixedSize(MAIN_WIDTH, MAIN_HEIGHT)
        self.setStyleSheet(STYLE_SHEET)
        
        self.lbl_Header = QLabel(HEADER_ENTRIES, self)
        self.lbl_Entry = QLabel("Entry:", self)
        self.lbl_Spacer = self.parent.lbl_Spacer
        
        self.lst_Entries = QListWidget(self)
        
        self.txtBox_Entry = QLineEdit(self)
        
        self.btn_AddEntry = QPushButton("Add entry", self)
        self.btn_EditEntry = QPushButton("Edit entry", self)
        self.btn_DeleteEntry = QPushButton("Delete entry", self)
        
        self.btn_Back = QPushButton("Back", self)
        self.btn_Exit = self.parent.btn_Exit
        
        self.initUI()
        
    def initUI(self):
        self.lbl_Header.setAlignment(Qt.AlignCenter)
        self.lst_Entries.itemClicked.connect(self.selected_entry)
        self.btn_AddEntry.clicked.connect(self.add_entry)
        self.btn_AddEntry.setObjectName("UserButtons")
        self.btn_EditEntry.clicked.connect(self.edit_entry)
        self.btn_EditEntry.setObjectName("UserButtons")
        self.btn_DeleteEntry.clicked.connect(self.delete_entry)
        self.btn_DeleteEntry.setObjectName("UserButtons")
        self.btn_Back.clicked.connect(self.back)
        self.btn_Back.setObjectName("SystemButtons")
        
        gBox = QGridLayout()
        gBox.addWidget(self.lbl_Header, 1, 1, 1, 2)
        gBox.addWidget(self.lst_Entries, 2, 1, 1, 2)
        gBox.addWidget(self.lbl_Entry, 3, 1, 1, 2)
        gBox.addWidget(self.txtBox_Entry, 4, 1, 1, 2)
        gBox.addWidget(self.btn_AddEntry, 5, 1, 1, 2)
        gBox.addWidget(self.btn_EditEntry, 6, 1, 1, 2)
        gBox.addWidget(self.btn_DeleteEntry, 7, 1, 1, 2)
        gBox.addWidget(self.lbl_Spacer, 8, 1)
        gBox.addWidget(self.btn_Back, 9, 1)
        gBox.addWidget(self.btn_Exit, 9, 2)
        self.setLayout(gBox)
        
        self.load_entries()
        
    def load_entries(self):
        self.entries: dict = get_entries(self.list_id)
        for entry, entryID in self.entries.items():
            self.lst_Entries.addItem(entry)
            
    def selected_entry(self, item):
        entry: str = item.text()
        self.entry_id = self.entries[entry]
        self.txtBox_Entry.setText(entry)
        
    
    def add_entry(self):
        entry: str = self.txtBox_Entry.text()
        dlg = ConfirmDialog("Add", f"Add entry '{entry}'?")
        if dlg.exec_():
            add_entry(entry, self.list_id)
            self.txtBox_Entry.clear()
            self.lst_Entries.clear()
            self.load_entries()
    
    def edit_entry(self):
        entry: str = self.txtBox_Entry.text()
        dlg = ConfirmDialog("Update", f"Update entry to '{entry}'?")
        if dlg.exec_():
            edit_entry(entry, self.entry_id)
            self.lst_Entries.clear()
            self.load_entries()
    
    def delete_entry(self):
        entry: str = self.txtBox_Entry.text()
        dlg = ConfirmDialog("Delete", f"Delete entry '{entry}'?")
        if dlg.exec_():
            delete_entry(self.entry_id)
            self.lst_Entries.clear()
            self.load_entries()
    
    def back(self):
        self.parent.show()
        self.parent.initUI()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        self.list_id = 0
        super().__init__()
        self.setWindowTitle(TITLE)
        self.setFixedSize(MAIN_WIDTH, MAIN_HEIGHT)
        self.setStyleSheet(STYLE_SHEET)
        
        self.lbl_Header = QLabel(HEADER_MAIN, self)
        self.lbl_Listname = QLabel("List name:", self)
        self.lbl_Spacer = QLabel(self)
        
        self.lst_Lists = QListWidget(self)
        
        self.txtBox_Listname = QLineEdit(self)
        
        self.btn_AddList = QPushButton("Add list", self)
        self.btn_ViewList = QPushButton("View selected list", self)
        self.btn_EditList = QPushButton("Edit selected list name", self)
        self.btn_DeleteList = QPushButton("Delete selected list", self)
        
        self.btn_Exit = QPushButton("Exit", self)
        
        self.initUI()
        
    def initUI(self):
        self.lbl_Header.setAlignment(Qt.AlignCenter)
        self.lst_Lists.clear()
        self.lst_Lists.itemClicked.connect(self.selected_list)
        self.btn_AddList.clicked.connect(self.add_list)
        self.btn_AddList.setObjectName("UserButtons")
        self.btn_ViewList.clicked.connect(self.view_list)
        self.btn_ViewList.setObjectName("UserButtons")
        self.btn_EditList.clicked.connect(self.edit_list)
        self.btn_EditList.setObjectName("UserButtons")
        self.btn_DeleteList.clicked.connect(self.delete_list)
        self.btn_DeleteList.setObjectName("UserButtons")
        self.btn_Exit.clicked.connect(self.ext)
        self.btn_Exit.setObjectName("SystemButtons")
        
        gBox = QGridLayout()
        gBox.addWidget(self.lbl_Header, 1, 1)
        gBox.addWidget(self.lst_Lists, 2, 1)
        gBox.addWidget(self.lbl_Listname, 3, 1)
        gBox.addWidget(self.txtBox_Listname, 4, 1)
        gBox.addWidget(self.btn_AddList, 5, 1)
        gBox.addWidget(self.btn_ViewList, 6, 1)
        gBox.addWidget(self.btn_EditList, 7, 1)
        gBox.addWidget(self.btn_DeleteList, 8, 1)
        gBox.addWidget(self.lbl_Spacer, 9, 1)
        gBox.addWidget(self.btn_Exit, 10, 1)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(gBox)
        
        self.load_lists()
    
    def load_lists(self):
        self.lists: dict = get_lists()
        for lst, lstID in self.lists.items():
            self.lst_Lists.addItem(lst)
            
    def selected_list(self, item):
        list_name: str = item.text()
        self.list_id = self.lists[list_name]
        self.txtBox_Listname.setText(list_name)
    
    
    def add_list(self):
        listname: str = self.txtBox_Listname.text()
        dlg = ConfirmDialog("Create", f"Create the list '{listname}'?")
        if dlg.exec_():
            create_list(listname)
            self.txtBox_Listname.clear()
            self.lst_Lists.clear()
            self.load_lists()
    
    def view_list(self):
        if self.list_id != 0:
            self.new_window = EntryWindow(self, self.list_id)
            self.new_window.show()
            self.hide()
    
    def edit_list(self):
        listname: str = self.txtBox_Listname.text()
        dlg = ConfirmDialog("Edit", f"Update the list name to '{listname}'?")
        if dlg.exec_():
            update_listname(listname, self.list_id)
            self.lst_Lists.clear()
            self.load_lists()
    
    def delete_list(self):
        listname: str = self.txtBox_Listname.text()
        dlg = ConfirmDialog("Delete", f"Delete the list '{listname}'?")
        if dlg.exec_():
            delete_list(self.list_id)
            self.lst_Lists.clear()
            self.load_lists()
    
    
    def ext(self):
        sys.exit()