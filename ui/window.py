import netlock  # Import the NetLock module

class NetworkManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NetCut-Like Tool")
        self.setGeometry(200, 100, 800, 500)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["IP Address", "MAC Address", "Vendor", "Hostname"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.scan_btn = QPushButton("Scan Network")
        self.cut_btn = QPushButton("Cut Selected Device")
        self.restore_btn = QPushButton("Restore Device")
        self.netlock_btn = QPushButton("Toggle NetLock")

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.scan_btn)
        layout.addWidget(self.cut_btn)
        layout.addWidget(self.restore_btn)
        layout.addWidget(self.netlock_btn)  # Add NetLock button

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.scan_btn.clicked.connect(self.scan_network)
        self.cut_btn.clicked.connect(self.cut_device)
        self.restore_btn.clicked.connect(self.restore_device)
        self.netlock_btn.clicked.connect(self.toggle_netlock)  # Connect NetLock button

        # Store spoofing threads to restore later
        self.spoofed_devices = set()

        # Initialize logger
        logger.init_db()

        self.netlock_enabled = False  # Track NetLock state

    def toggle_netlock(self):
        if not self.netlock_enabled:
            netlock.start_netlock()  # Start NetLock in background
            self.netlock_btn.setText("Stop NetLock")
            self.netlock_enabled = True
            QMessageBox.information(self, "NetLock Activated", "NetLock is now monitoring the network.")
        else:
            self.netlock_enabled = False
            self.netlock_btn.setText("Start NetLock")
            QMessageBox.information(self, "NetLock Deactivated", "NetLock has been disabled.")

    # The rest of your methods (scan_network, cut_device, restore_device) remain unchanged...
