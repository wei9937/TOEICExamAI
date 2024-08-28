import google.generativeai as genai
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QRadioButton, QScrollArea, QFrame, QMessageBox, QHBoxLayout, QProgressBar
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

class ApiRequestThread(QThread):
    data_fetched = Signal(list)

    def __init__(self, unit, api_key, prompt_text):
        super().__init__()
        self.unit = unit
        self.api_key = api_key
        self.prompt_text = prompt_text

    def run(self):
        try:
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-pro')

            response = model.generate_content(self.prompt_text)
            content = response.text.strip()
            print("API Response:", content)  # 打印 API 回應以便於調試

            questions = []
            question_blocks = content.split("\n\n")
            for block in question_blocks:

                lines = block.strip().split("\n")
                print("block = ", block, ", len(lines) = ", len(lines))
                if len(lines) < 5:
                    continue
                try:
                    question_text = lines[0].split(":", 1)[1].strip()
                    options = [line.split(".", 1)[1].strip() for line in lines[1:5]]
                    questions.append({
                        "question": question_text,
                        "options": options
                    })
                except IndexError as e:
                    print("Error parsing block:", block)
                    print("Exception:", e)

            self.data_fetched.emit(questions)
        except Exception as e:
            print("Exception in API Request Thread:", e)
            self.data_fetched.emit([])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 多益測驗")
        self.setFixedSize(1200, 600)  # 設置固定大小

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

        # 顯示 loading 指示器
        self.loading_label = QLabel("Loading...")
        self.loading_label.setFont(QFont('Arial', 18, QFont.Bold))
        self.loading_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.loading_label)

        self.loading_bar = QProgressBar()
        self.loading_bar.setRange(0, 0)  # 不確定的範圍
        layout.addWidget(self.loading_bar)

        prompt_text=""" hello world """
        if unit == "Part 5":
            prompt_text = """
            請生成十題多益考題Part5（句子填空），包括以下內容：
            1. 一個句子，其中有一個或多個空格供填寫。
            2. 四個選項，其中只有一個是正確的。
            3. 題目應該涵蓋文法題、單字題、詞性變化和時態題等多益考試可能會出的題型。
            4. 正確答案和每題的詳解。
            5. 題目需要填寫答案的空格處使用 "____" 來表示
            6. 正確答案請設計常態分布在 A,B,C,D 選項之中 
            
            
            題目區不需要標出正確答案，格式如下：

            題目區：
            1. **題目** 1: [句子內容，其中有一個或多個空格]
               - A. [選項A]
               - B. [選項B]
               - C. [選項C]
               - D. [選項D]

            2. **題目** 2: [句子內容，其中有一個或多個空格]
               - A. [選項A]
               - B. [選項B]
               - C. [選項C]
               - D. [選項D]
            ...
            """
        elif unit == "Part 6":
            prompt_text = """
            Please generate three TOEIC Part 6 (Text Completion) questions, similar in style and format to those found on official TOEIC practice tests. Each question should include:

            A brief passage with 3-4 blanks that need to be filled.
            Four answer choices (A, B, C, D) for each blank.
            The content should cover a variety of business-related topics such as emails, announcements, and notices.
            The level of difficulty should be appropriate for intermediate to advanced English learners, similar to what one would find in an official TOEIC test.
            Example Passage: Please refer to the following link for a sample TOEIC Part 6 passage: https://www.toeic.com.tw/sample-test/toeic-listening-reading/sample06.html
            
            格式如下:
            題目區:
            1. **題目** 1:  question 1
               - A. [choices A]
               - B. [choices B]
               - C. [choices C]
               - D. [choices D]
               
            2. **題目** 2:  question 2
               - A. [choices A]
               - B. [choices B]
               - C. [choices C]
               - D. [choices D]
            ...
            """

        # 開啟 API 請求的執行緒
        self.api_thread = ApiRequestThread(unit, api_key='AIzaSyA0l5znOw4cYHL_kBqLxd81OVq3T_cZFj4', prompt_text=prompt_text)
        self.api_thread.data_fetched.connect(self.display_questions)
        self.api_thread.start()

    def display_questions(self, questions):
        # 移除 loading 指示器
        self.loading_label.setVisible(False)
        self.loading_bar.setVisible(False)

        layout = self.scroll_area.widget().layout()

        if not questions:
            QMessageBox.warning(self, "錯誤", "無法獲取題目，請稍後再試！")
            return

        # 顯示考題
        self.answers = [None] * len(questions)  # 存儲每題的選擇
        self.radio_buttons = []

        for i, question_data in enumerate(questions):
            question_label = QLabel(f"{i+1}. {question_data['question']}")
            question_label.setStyleSheet(self.question_style)
            layout.addWidget(question_label)

            self.create_question_options(layout, i, question_data["options"])

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

    def create_question_options(self, layout, question_index, options):
        h_layout = QHBoxLayout()
        self.radio_buttons.append([])
        for option in options:
            rb = QRadioButton(option)
            rb.setStyleSheet(self.option_style)
            rb.toggled.connect(lambda checked, rb=rb, q=question_index: self.select_answer(q, rb, checked))
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
            print("select ans: " + selected_rb.text())

    def submit_answers(self):
        if None in self.answers:
            QMessageBox.warning(self, "錯誤", "請完成所有題目的作答後再提交！")
            return

        # 在這裡可以進一步處理提交的答案，例如通過 API 獲取答案解析

        result_text = "您的答案已提交！\n"
        result_text += "\n".join([f"第 {i+1} 題: {self.answers[i]}" for i in range(len(self.answers))])

        QMessageBox.information(self, "提交成功", result_text)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
