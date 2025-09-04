import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QMessageBox, QDialog, QLineEdit, QGridLayout, QSpacerItem,
    QSizePolicy, QTabWidget
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


# ---------------- PANEL DEL ADMINISTRADOR ----------------
class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel del Administrador")
        self.showMaximized()

        layout = QVBoxLayout()

        tabs = QTabWidget()
        tabs.setFont(QFont("Arial", 16))

        # Pestañas del administrador
        secciones = ["Finanzas", "Peluquería", "Inventario", "Clientes", "Veterinaria"]
        for nombre in secciones:
            tab = QWidget()
            tab_layout = QVBoxLayout()
            tab_layout.addWidget(QLabel(nombre))
            tab.setLayout(tab_layout)
            tabs.addTab(tab, nombre)

        layout.addWidget(tabs)
        self.setLayout(layout)


# ---------------- PANEL DE AUXILIARES ----------------
class AuxPanel(QWidget):
    def __init__(self, role):
        super().__init__()
        self.setWindowTitle(f"Panel de {role}")
        self.showMaximized()

        layout = QVBoxLayout()

        tabs = QTabWidget()
        tabs.setFont(QFont("Arial", 16))

        # Pestañas para auxiliares
        secciones = ["Peluquería", "Inventario", "Clientes"]
        for nombre in secciones:
            tab = QWidget()
            tab_layout = QVBoxLayout()
            tab_layout.addWidget(QLabel(nombre))
            tab.setLayout(tab_layout)
            tabs.addTab(tab, nombre)

        layout.addWidget(tabs)
        self.setLayout(layout)


# ---------------- DIALOGO DE PIN ----------------
class NumPadDialog(QDialog):
    def __init__(self, role, parent=None):
        super().__init__(parent)
        self.role = role
        self.setWindowTitle(f"Ingresar PIN - {role}")
        self.setFixedSize(400, 600)

        font = QFont("Arial", 28)

        # Campo para el PIN
        self.pin_input = QLineEdit()
        self.pin_input.setFont(font)
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setReadOnly(True)
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.setFixedHeight(70)

        # Botones del numpad
        grid = QGridLayout()
        buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            'Borrar', '0', 'Aceptar'
        ]

        for i, btn_text in enumerate(buttons):
            button = QPushButton(btn_text)
            button.setFont(font)
            button.setMinimumSize(100, 80)
            row, col = divmod(i, 3)
            grid.addWidget(button, row, col)

            if btn_text == 'Borrar':
                button.clicked.connect(self.borrar)
            elif btn_text == 'Aceptar':
                button.clicked.connect(self.aceptar)
            else:
                button.clicked.connect(lambda _, x=btn_text: self.agregar_numero(x))

        layout = QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(self.pin_input)
        layout.addSpacing(20)
        layout.addLayout(grid)
        self.setLayout(layout)

    def agregar_numero(self, num):
        if len(self.pin_input.text()) < 6:
            self.pin_input.setText(self.pin_input.text() + num)

    def borrar(self):
        self.pin_input.setText(self.pin_input.text()[:-1])

    def aceptar(self):
        pin = self.pin_input.text()
        pins = {
            "Administrador": "1234",
            "Auxiliar 1": "1111",
            "Auxiliar 2": "2222"
        }

        if pins.get(self.role) == pin:
            self.parent().hide()  # Ocultar ventana de login

            # Abrir panel correspondiente según el rol
            if self.role == "Administrador":
                self.panel = AdminPanel()
            else:
                self.panel = AuxPanel(self.role)

            self.panel.show()
            self.accept()  # Cierra el numpad
        else:
            QMessageBox.warning(self, "Error", "PIN incorrecto")
            self.pin_input.clear()

    def keyPressEvent(self, event):
        try:
            key = event.key()
            if key in (
                Qt.Key.Key_0, Qt.Key.Key_1, Qt.Key.Key_2, Qt.Key.Key_3, Qt.Key.Key_4,
                Qt.Key.Key_5, Qt.Key.Key_6, Qt.Key.Key_7, Qt.Key.Key_8, Qt.Key.Key_9
            ):
                self.agregar_numero(event.text())
            elif key == Qt.Key.Key_Backspace:
                self.borrar()
            elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self.aceptar()
        except Exception as e:
            print("Error en keyPressEvent:", e)


# ---------------- LOGIN PRINCIPAL ----------------
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login PyQt6")
        self.resize(1000, 700)
        self.showMaximized()

        font = QFont("Arial", 36)

        self.label = QLabel("Selecciona tu rol")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_admin = QPushButton("Administrador")
        self.btn_admin.setFont(font)
        self.btn_admin.setMinimumHeight(100)
        self.btn_admin.clicked.connect(lambda: self.abrir_numpad("Administrador"))

        self.btn_aux1 = QPushButton("Auxiliar 1")
        self.btn_aux1.setFont(font)
        self.btn_aux1.setMinimumHeight(100)
        self.btn_aux1.clicked.connect(lambda: self.abrir_numpad("Auxiliar 1"))

        self.btn_aux2 = QPushButton("Auxiliar 2")
        self.btn_aux2.setFont(font)
        self.btn_aux2.setMinimumHeight(100)
        self.btn_aux2.clicked.connect(lambda: self.abrir_numpad("Auxiliar 2"))

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(300, 100, 300, 100)
        main_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        main_layout.addWidget(self.label)
        main_layout.addSpacing(40)
        main_layout.addWidget(self.btn_admin)
        main_layout.addWidget(self.btn_aux1)
        main_layout.addWidget(self.btn_aux2)
        main_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.setLayout(main_layout)

    def abrir_numpad(self, role):
        dialog = NumPadDialog(role, self)
        dialog.exec()


# ---------------- EJECUCIÓN PRINCIPAL ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
