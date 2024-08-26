from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QRadioButton, QScrollArea, QFrame, QMessageBox, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 多益測驗")
        self.setFixedSize(800, 800)  # 設置固定大小

        # 初始化主視圖
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.layout.addWidget(self.scroll_area)

        self.button_style = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        """
        self.question_style = """
        QLabel {
            font-size: 18px;
            font-weight: bold;
            margin: 10px 0;
        }
        """
        self.option_style = """
        QRadioButton {
            font-size: 16px;
            padding: 5px;
        }
        QRadioButton::indicator {
            width: 20px;
            height: 20px;
        }
        QRadioButton::indicator:checked {
            background-color: #4CAF50;
        }
        QRadioButton::indicator:unchecked {
            background-color: #fff;
        }
        """
        self.show_main_menu()

    def show_main_menu(self):
        widget = QWidget()
        self.scroll_area.setWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # 添加主選單標題
        title = QLabel("選擇考題單元")
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 創建和添加按鈕
        self.create_button(layout, "Part 5 句子填空", "Part 5")
        self.create_button(layout, "Part 6 段落填空", "Part 6")
        self.create_button(layout, "Part 7 閱讀測驗", "Part 7")

    def create_button(self, layout, text, part):
        button = QPushButton(text)
        button.setStyleSheet(self.button_style)
        button.clicked.connect(lambda: self.show_questions(part))
        layout.addWidget(button)

    def show_questions(self, unit):
        print(f"Showing questions for {unit}")

        widget = QWidget()
        self.scroll_area.setWidget(widget)
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # 添加主選單按鈕
        btn_main_menu = QPushButton("主選單")
        btn_main_menu.setStyleSheet(self.button_style)
        btn_main_menu.clicked.connect(self.show_main_menu)
        layout.addWidget(btn_main_menu)

        # 顯示單元標題
        unit_title = QLabel(unit)
        unit_title.setFont(QFont('Arial', 20, QFont.Bold))
        unit_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(unit_title)

        # 顯示選定單元的考題
        questions = [f"Question {i+1}" for i in range(10)]  # 模擬考題

        self.answers = [None] * len(questions)  # 存儲每題的選擇
        self.radio_buttons = []

        for i, question in enumerate(questions):
            question_label = QLabel(question)
            question_label.setStyleSheet(self.question_style)
            layout.addWidget(question_label)

            self.create_question_options(layout, i)

            # 添加分隔線
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            layout.addWidget(separator)

        # 添加送出按鈕
        submit_button = QPushButton("送出答案")
        submit_button.setStyleSheet(self.button_style)
        submit_button.clicked.connect(self.submit_answers)
        layout.addWidget(submit_button)

    def create_question_options(self, layout, question_index):
        h_layout = QHBoxLayout()
        self.radio_buttons.append([])
        for option in ["A", "B", "C", "D"]:
            rb = QRadioButton(f"Option {option}")
            rb.setStyleSheet(self.option_style)
            rb.toggled.connect(lambda checked, q=question_index, rb=rb: self.select_answer(q, rb, checked))
            h_layout.addWidget(rb)
            self.radio_buttons[question_index].append(rb)
        layout.addLayout(h_layout)

    def select_answer(self, question_index, selected_rb, checked):
        if checked:
            # 清除其他選項的選擇
            for rb in self.radio_buttons[question_index]:
                rb.setStyleSheet(self.option_style)
            # 標記選中的選項
            selected_rb.setStyleSheet("QRadioButton { font-size: 16px; font-weight: bold; padding: 5px; background-color: #4CAF50; color: white; }")
            self.answers[question_index] = selected_rb.text()

    def submit_answers(self):
        # 處理答案提交的邏輯
        if None in self.answers:
            QMessageBox.warning(self, "警告", "請回答所有問題後再提交！")
            return

        answers_summary = "\n".join([f"Question {i+1}: {ans}" for i, ans in enumerate(self.answers) if ans])
        QMessageBox.information(self, "提交", f"答案已提交！\n\n{answers_summary}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
