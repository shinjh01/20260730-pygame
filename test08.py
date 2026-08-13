import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class LabelExample(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 기본 라벨
        label1 = QLabel("기본 라벨 텍스트")

        # HTML 지원 라벨
        label2 = QLabel("<h2 style='color: blue;'>HTML 형식 라벨</h2>")

        # 정렬 설정
        label3 = QLabel("가운데 정렬 라벨")
        label3.setAlignment(Qt.AlignCenter)

        # 라벨에 배경색 설정
        label4 = QLabel("배경색이 있는 라벨")
        label4.setStyleSheet("background-color: lightblue; padding: 10px;")

        # 레이아웃에 추가
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addWidget(label4)

        self.setLayout(layout)
        self.setWindowTitle("Label 예제")
        self.setGeometry(300, 300, 400, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LabelExample()
    sys.exit(app.exec_())
