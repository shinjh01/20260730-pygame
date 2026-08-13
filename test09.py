import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont


class RobotArmGUI(QWidget):
    def __init__(self):
        super().__init__()

        # 화면 생성 전에 사용할 변수 준비
        self.joint_values = [0, 0, 0, 0, 0, 0]
        self.joint_sliders = []
        self.joint_value_labels = []
        self.monitor_joint_labels = []

        self.gripper_value = 0
        self.emergency_active = False

        # 티칭 포지션 예시
        self.teaching_positions = {
            "Home": {
                "joints": [0, 0, 0, 0, 0, 0],
                "gripper": 0
            },
            "Position 1": {
                "joints": [45, -30, 60, 0, 20, 10],
                "gripper": 30
            },
            "Position 2": {
                "joints": [-40, 20, 30, 45, 0, -20],
                "gripper": 80
            }
        }

        self.init_ui()

    def init_ui(self):
        # 전체 화면: 제목 → 좌우 패널 → 로그
        root_layout = QVBoxLayout()

        # 제목
        title_label = QLabel("로봇암 제어 시스템 v1.0")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("맑은 고딕", 18, QFont.Bold))

        root_layout.addWidget(title_label)

        # 가운데 좌우 패널
        main_layout = QHBoxLayout()

        left_panel = self.create_control_panel()
        right_panel = self.create_monitor_panel()

        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(right_panel, 1)

        root_layout.addLayout(main_layout)

        # 아래 로그 패널
        log_panel = self.create_log_panel()
        root_layout.addWidget(log_panel)

        self.setLayout(root_layout)

        self.setWindowTitle("로봇암 제어 시스템 v1.0")
        self.setGeometry(200, 200, 900, 600)

        # 화면 스타일
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f6f8;
                font-family: "맑은 고딕";
                font-size: 13px;
            }

            QGroupBox {
                background-color: white;
                border: 1px solid #aeb6bf;
                border-radius: 7px;
                margin-top: 12px;
                padding: 10px;
                font-weight: bold;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 5px;
            }

            QPushButton {
                background-color: #2878d0;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1f65b3;
            }

            QPushButton:pressed {
                background-color: #164c87;
            }

            QPushButton:disabled {
                background-color: #a0a0a0;
            }

            QPushButton#emergencyButton {
                background-color: #d63031;
                font-size: 15px;
                padding: 11px;
            }

            QPushButton#emergencyButton:hover {
                background-color: #b71c1c;
            }

            QListWidget, QTextEdit, QSpinBox {
                background-color: white;
                border: 1px solid #b8c2cc;
                border-radius: 4px;
                padding: 4px;
            }

            QSlider::groove:horizontal {
                height: 6px;
                background-color: #dfe6e9;
                border-radius: 3px;
            }

            QSlider::handle:horizontal {
                width: 16px;
                margin: -5px 0;
                background-color: #2878d0;
                border-radius: 8px;
            }
        """)

        self.add_log("로봇암 제어 시스템을 시작했습니다.")
        self.show()

    # 왼쪽 관절 제어 패널
    def create_control_panel(self):
        group_box = QGroupBox("관절 제어")
        layout = QVBoxLayout()

        # Joint 1~6
        for joint_index in range(6):
            joint_layout = QHBoxLayout()

            joint_label = QLabel(f"Joint {joint_index + 1}")
            joint_label.setFixedWidth(65)

            slider = QSlider(Qt.Horizontal)
            slider.setRange(-180, 180)
            slider.setValue(0)
            slider.setTickInterval(30)

            value_label = QLabel("0°")
            value_label.setFixedWidth(45)
            value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            slider.valueChanged.connect(
                lambda angle, index=joint_index:
                self.update_joint_value(index, angle)
            )

            self.joint_sliders.append(slider)
            self.joint_value_labels.append(value_label)

            joint_layout.addWidget(joint_label)
            joint_layout.addWidget(slider)
            joint_layout.addWidget(value_label)

            layout.addLayout(joint_layout)

        # Gripper
        gripper_layout = QHBoxLayout()

        gripper_label = QLabel("Gripper")
        gripper_label.setFixedWidth(65)

        self.gripper_slider = QSlider(Qt.Horizontal)
        self.gripper_slider.setRange(0, 100)
        self.gripper_slider.setValue(0)
        self.gripper_slider.valueChanged.connect(
            self.update_gripper_value
        )

        self.gripper_value_label = QLabel("0 mm")
        self.gripper_value_label.setFixedWidth(55)

        gripper_layout.addWidget(gripper_label)
        gripper_layout.addWidget(self.gripper_slider)
        gripper_layout.addWidget(self.gripper_value_label)

        layout.addLayout(gripper_layout)

        # 속도
        speed_layout = QHBoxLayout()

        speed_layout.addWidget(QLabel("속도"))

        self.speed_spinbox = QSpinBox()
        self.speed_spinbox.setRange(1, 100)
        self.speed_spinbox.setValue(50)
        self.speed_spinbox.setSuffix(" %")

        speed_layout.addWidget(self.speed_spinbox)
        speed_layout.addStretch()

        layout.addLayout(speed_layout)

        # 모드
        mode_layout = QHBoxLayout()

        mode_layout.addWidget(QLabel("모드"))

        self.manual_radio = QRadioButton("수동")
        self.auto_radio = QRadioButton("자동")
        self.manual_radio.setChecked(True)

        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.manual_radio)
        self.mode_group.addButton(self.auto_radio)

        mode_layout.addWidget(self.manual_radio)
        mode_layout.addWidget(self.auto_radio)
        mode_layout.addStretch()

        layout.addLayout(mode_layout)

        # 명령 버튼
        button_layout = QGridLayout()

        self.move_button = QPushButton("이동")
        self.stop_button = QPushButton("정지")
        self.home_button = QPushButton("홈")

        self.move_button.clicked.connect(self.move_robot)
        self.stop_button.clicked.connect(self.stop_robot)
        self.home_button.clicked.connect(self.move_home)

        button_layout.addWidget(self.move_button, 0, 0)
        button_layout.addWidget(self.stop_button, 0, 1)
        button_layout.addWidget(self.home_button, 0, 2)

        # 비상정지
        self.emergency_button = QPushButton("🔴 비상정지")
        self.emergency_button.setObjectName("emergencyButton")
        self.emergency_button.clicked.connect(
            self.toggle_emergency
        )

        button_layout.addWidget(
            self.emergency_button,
            1, 0, 1, 3
        )

        layout.addLayout(button_layout)
        layout.addStretch()

        group_box.setLayout(layout)
        return group_box

    # 오른쪽 모니터링 패널
    def create_monitor_panel(self):
        group_box = QGroupBox("상태 모니터링")
        layout = QVBoxLayout()

        # 상태
        status_layout = QHBoxLayout()

        status_layout.addWidget(QLabel("상태:"))

        self.status_label = QLabel("대기중")
        self.status_label.setStyleSheet(
            "color: #2878d0; font-weight: bold;"
        )

        status_layout.addWidget(self.status_label)
        status_layout.addStretch()

        layout.addLayout(status_layout)

        # Joint 모니터링
        for joint_index in range(6):
            label = QLabel(f"Joint {joint_index + 1}: 0°")

            self.monitor_joint_labels.append(label)
            layout.addWidget(label)

        self.monitor_gripper_label = QLabel("Gripper: 0 mm")
        layout.addWidget(self.monitor_gripper_label)

        layout.addSpacing(15)

        # 티칭 목록
        teaching_title = QLabel("티칭 포지션 목록")
        teaching_title.setFont(
            QFont("맑은 고딕", 12, QFont.Bold)
        )

        layout.addWidget(teaching_title)

        self.teaching_list = QListWidget()

        for position_name in self.teaching_positions:
            self.teaching_list.addItem(position_name)

        layout.addWidget(self.teaching_list)

        # 저장, 불러오기
        teaching_button_layout = QHBoxLayout()

        save_button = QPushButton("저장")
        load_button = QPushButton("불러오기")

        save_button.clicked.connect(
            self.save_teaching_position
        )

        load_button.clicked.connect(
            self.load_teaching_position
        )

        teaching_button_layout.addWidget(save_button)
        teaching_button_layout.addWidget(load_button)

        layout.addLayout(teaching_button_layout)

        group_box.setLayout(layout)
        return group_box

    # 아래 로그 패널
    def create_log_panel(self):
        group_box = QGroupBox("명령 로그")
        layout = QVBoxLayout()

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)

        layout.addWidget(self.log_text)

        group_box.setLayout(layout)
        return group_box

    # 관절 슬라이더 값 변경
    def update_joint_value(self, joint_index, angle):
        self.joint_values[joint_index] = angle

        self.joint_value_labels[joint_index].setText(
            f"{angle}°"
        )

        self.monitor_joint_labels[joint_index].setText(
            f"Joint {joint_index + 1}: {angle}°"
        )

        print(f"Joint {joint_index + 1}: {angle}°")

    # 그리퍼 값 변경
    def update_gripper_value(self, value):
        self.gripper_value = value

        self.gripper_value_label.setText(f"{value} mm")
        self.monitor_gripper_label.setText(
            f"Gripper: {value} mm"
        )

        print(f"Gripper: {value} mm")

    # 이동 버튼
    def move_robot(self):
        if self.emergency_active:
            self.add_log(
                "비상정지 상태이므로 이동할 수 없습니다."
            )
            return

        mode = (
            "수동"
            if self.manual_radio.isChecked()
            else "자동"
        )

        speed = self.speed_spinbox.value()

        self.set_status("동작중", "#e67e22")

        self.add_log(
            f"이동 명령 - 모드: {mode}, "
            f"속도: {speed}%, "
            f"관절: {self.joint_values}, "
            f"Gripper: {self.gripper_value} mm"
        )

        for joint_number, angle in enumerate(
            self.joint_values,
            start=1
        ):
            self.move_joint(joint_number, angle)

        self.set_status("대기중", "#2878d0")
        self.add_log("동작 완료")

    def move_joint(self, joint_num, angle):
        print(
            f"[시뮬레이션] Joint {joint_num}을 "
            f"{angle}도로 이동"
        )

    # 정지 버튼
    def stop_robot(self):
        self.set_status("정지", "#e67e22")
        self.add_log("정지 명령을 실행했습니다.")

    # 홈 버튼
    def move_home(self):
        if self.emergency_active:
            self.add_log(
                "비상정지 상태에서는 홈 이동이 불가능합니다."
            )
            return

        for slider in self.joint_sliders:
            slider.setValue(0)

        self.gripper_slider.setValue(0)

        self.set_status("대기중", "#2878d0")
        self.add_log("홈 위치로 이동했습니다.")

    # 비상정지
    def toggle_emergency(self):
        self.emergency_active = not self.emergency_active

        if self.emergency_active:
            self.set_status("오류", "#d63031")

            self.emergency_button.setText("비상정지 해제")
            self.move_button.setEnabled(False)
            self.home_button.setEnabled(False)

            self.add_log("비상정지가 작동했습니다.")

        else:
            self.set_status("대기중", "#2878d0")

            self.emergency_button.setText("🔴 비상정지")
            self.move_button.setEnabled(True)
            self.home_button.setEnabled(True)

            self.add_log("비상정지가 해제되었습니다.")

    # 현재 위치 저장
    def save_teaching_position(self):
        default_name = (
            f"Position {len(self.teaching_positions)}"
        )

        position_name, ok = QInputDialog.getText(
            self,
            "티칭 위치 저장",
            "위치 이름:",
            text=default_name
        )

        if not ok or position_name.strip() == "":
            return

        position_name = position_name.strip()

        self.teaching_positions[position_name] = {
            "joints": self.joint_values.copy(),
            "gripper": self.gripper_value
        }

        item_names = [
            self.teaching_list.item(index).text()
            for index in range(self.teaching_list.count())
        ]

        if position_name not in item_names:
            self.teaching_list.addItem(position_name)

        self.add_log(
            f"티칭 위치 '{position_name}'을 저장했습니다."
        )

    # 저장 위치 불러오기
    def load_teaching_position(self):
        selected_item = self.teaching_list.currentItem()

        if selected_item is None:
            self.add_log("불러올 위치를 선택하세요.")
            return

        position_name = selected_item.text()
        position = self.teaching_positions[position_name]

        for index, angle in enumerate(position["joints"]):
            self.joint_sliders[index].setValue(angle)

        self.gripper_slider.setValue(
            position["gripper"]
        )

        self.add_log(
            f"티칭 위치 '{position_name}'을 불러왔습니다."
        )

    def set_status(self, status, color):
        self.status_label.setText(status)

        self.status_label.setStyleSheet(
            f"color: {color}; font-weight: bold;"
        )

    # 로그 출력
    def add_log(self, message):
        timestamp = (
            QDateTime.currentDateTime()
            .toString("yyyy-MM-dd HH:mm:ss")
        )

        log_message = f"{timestamp} - {message}"

        self.log_text.append(log_message)
        print(log_message)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = RobotArmGUI()

    sys.exit(app.exec_())