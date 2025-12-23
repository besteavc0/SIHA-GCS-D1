import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget
from PySide6.QtCore import QTimer, Qt

class SIHAGui(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("TEKNOFEST SİHA Yer Kontrol İstasyonu (PySide6)")
        self.setGeometry(100, 100, 450, 350)

        # Ana Düzen
        self.layout = QVBoxLayout()

        self.lbl_status = QLabel("Durum: Bağlantı Bekleniyor", self)
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.lbl_status)

        self.lbl_telemetry = QLabel("Telemetri: --", self)
        self.layout.addWidget(self.lbl_telemetry)

        self.btn_connect = QPushButton("İHA'ya Bağlan", self)
        self.btn_connect.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold;")
        self.btn_connect.clicked.connect(self.connect_action)
        self.layout.addWidget(self.btn_connect)

        self.btn_takeoff = QPushButton("Kalkış Yap (5m)", self)
        self.btn_takeoff.setStyleSheet("background-color: #e67e22; color: white;")
        self.btn_takeoff.clicked.connect(self.takeoff_action)
        self.layout.addWidget(self.btn_takeoff)

        container = QWidget()
        container.setLayout(self.layout)
        setCentralWidget(container)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_telemetry)

    def connect_action(self):
        try:
            self.controller.connect_uav()
            self.lbl_status.setText("Durum: SİSTEM BAĞLI")
            self.lbl_status.setStyleSheet("color: green;")
            self.timer.start(1000)
        except Exception as e:
            self.lbl_status.setText(f"Hata: {str(e)}")

    def takeoff_action(self):
        self.controller.arm_and_takeoff(5)

    def update_telemetry(self):
        data = self.controller.get_telemetry()
        text = f"Mod: {data['mode']} | İrtifa: {data['altitude']:.2f}m | Pil: %{data['battery']}"
        self.lbl_telemetry.setText(text)