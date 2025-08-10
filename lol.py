from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QStackedWidget
import sys

# ---------- مثال باستخدام QStackedWidget ----------
class StackExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مثال QStackedWidget")

        # إنشاء الـ Stack
        self.stack = QStackedWidget()

        # الصفحة الأولى
        self.page1 = QWidget()
        layout1 = QVBoxLayout()
        self.page1.setLayout(layout1)
        label1 = QLabel("هذه الصفحة الأولى")
        btn1 = QPushButton("انتقل إلى الصفحة الثانية")
        btn1.clicked.connect(lambda: self.stack.setCurrentWidget(page2))
        layout1.addWidget(label1)
        layout1.addWidget(btn1)

        # الصفحة الثانية
        page2 = Lol(self)
       
       

        # إضافة الصفحات
        self.stack.addWidget(self.page1)
        self.stack.addWidget(page2)

        # وضع الـ Stack في النافذة
        self.setCentralWidget(self.stack)
    def Pop(self):
        self.stack.setCurrentWidget(self.page1)

class Lol(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent

        lol = QVBoxLayout() 
        label2 = QLabel("هذه الصفحة الثانية")
        btn2 = QPushButton("ارجع للصفحة الأولى")
        btn2.clicked.connect(lambda: self.parent.Pop())
        lol.addWidget(label2)
        lol.addWidget(btn2)
        lol.addWidget(QLabel("asdsadasd"))
        self.setLayout(lol)


# ---------- مثال باستخدام setCentralWidget فقط ----------
class CentralWidgetExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مثال setCentralWidget المباشر")

        # عرض الصفحة الأولى
        self.show_page1()

    def show_page1(self):
        page1 = QWidget()
        layout = QVBoxLayout(page1)
        label = QLabel("هذه الصفحة الأولى")
        btn = QPushButton("انتقل للصفحة الثانية")
        btn.clicked.connect(self.show_page2)
        layout.addWidget(label)
        layout.addWidget(btn)
        self.setCentralWidget(page1)

    def show_page2(self):
        page2 = QWidget()
        layout = QVBoxLayout(page2)
        label = QLabel("هذه الصفحة الثانية (لن تستطيع الرجوع إلا بإنشائها من جديد)")
        layout.addWidget(label)
        self.setCentralWidget(page2)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # جرب هذا أولاً:
    window = StackExample()
    # أو جرب هذا بدلاً منه:
    #window = CentralWidgetExample()

    window.show()
    sys.exit(app.exec_())
