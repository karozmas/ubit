import pandas as pd # قراءة البيانات من ملف CSV
import numpy as np # التعامل مع المصفوفات
from sklearn.feature_extraction.text import TfidfVectorizer # استخدام TF-IDF لتحويل النصوص إلى متجهات
# استخدام TF-IDF لتحويل النصوص إلى متجهات
#TfidfVectorizer
#يحوّل النصوص (مثل الأسئلة والأجوبة) إلى متجهات رقمية بناءً على TF-IDF.
#TF-IDF = Term Frequency - Inverse Document Frequency، وهي تقنية شائعة لتمثيل الكلمات بعدد يعبّر عن أهميتها.
#TF = عدد تكرار الكلمة في المستند.
#IDF = مدى تميز الكلمة عبر جميع المستندات.
from sklearn.metrics.pairwise import cosine_similarity # لحساب التشابه بين المتجهات
#تُستخدم لحساب التشابه بين السؤال المدخل من المستخدم والأسئلة في قاعدة البيانات باستخدام المسافة الزاويّة (cosine).
#example 5
import re # للتعامل مع التعبيرات النمطية
# مكتبة معالجة التعابير النمطية (Regular Expressions)، تُستخدم لتنظيف النصوص (مثل إزالة الحروف غير المرغوبة من النص العربي).
import os # للتعامل مع مسارات الملفات   
#تُستخدم للتحكم بالملفات والمسارات في النظام (لكنها غير مستخدمة فعليًا هنا في هذا الجزء).
import requests # للتعامل مع طلبات HTTP 
# تُستخدم لإرسال طلبات إلى خوادم الويب (مثل تحميل البيانات من الإنترنت).
from io import BytesIO # للتعامل مع البيانات في الذاكرة
# تُستخدم لقراءة البيانات من الذاكرة بدلاً من الملفات.

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QWidget,
                             QMessageBox, QStatusBar, QStackedWidget, QFrame,
                             QFormLayout, QComboBox, QSpacerItem, QSizePolicy,
                             QDialog, QDialogButtonBox, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QTabWidget,QScrollArea)
# لإنشاء واجهة المستخدم الرسومية
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtCore import Qt, QSize            # لتحديد اتجاه النصوص والأحداث
from PyQt5.QtGui import (QFont, QPixmap, QIcon, QPalette, QColor, 
                         QLinearGradient, QBrush)           # لتخصيص مظهر الواجهة الرسومية
                                    
from firebase_config import db         # استيراد كائن قاعدة البيانات من ملف firebase_config.py



class UserDatabase: 
   
    def add_user(self, username, password, user_type):               # هذه الدالة تقوم بإضافة مستخدم جديد إلى قاعدة البيانات
        self.user_ref = db.collection('users').document(username)
        if self.user_ref.get().exists:                #  تستخدم Firebase للتحقق مما إذا كان اسم المستخدم موجودًا بالفعل في قاعدة البيانات
            return False
                             # إذا كان اسم المستخدم موجودًا بالفعل، تعيد الدالة False
        self.user_ref.set({
            'password': password,
            'type': user_type
        })
        print("User added successfully")
        return True
    
    def validate_user(self, username, password):                            # هذه الدالة تتحقق من صحة اسم المستخدم وكلمة المرور
        self.user_doc = db.collection("users").document(username).get()              # يستخدم Firebase لجلب بيانات المستخدم من قاعدة البيانات
                                                                           #{'password': '1234', 'type': 'admin'} يرجع القاموس الذي يحتوي على كلمة المرور ونوع المستخدم
                                                                           # print(user['type']) #  تطبع نوع المستخدم (admin أو student)
                                                                           # print(user[+'password']) # تطبع كلمة المرور
        if self.user_doc.exists:                                           # إذا كان المستخدم موجودًا و كلمة المرور صحيحة
            data = self.user_doc.to_dict()                                 #  يحول البيانات إلى قاموس
            if data['password'] == password:
                print("User validated successfully")
                return data['type']
        print("User validation failed")
        return None
    
    def get_all_users(self):
        self.users = {}                                                    #  هذه الدالة تقوم بجلب جميع المستخدمين من قاعدة البيانات
        self.docs = db.collection('users').stream()                        #  يستخدم Firebase لجلب جميع وثائق المستخدمين من مجموعة 'users'
        for doc in self.docs:                                              #  يقوم بتكرار كل وثيقة مستخدم
            self.users[doc.id] = doc.to_dict()                            #  ويحفظ اسم المستخدم (doc.id) وبياناته (doc.to_dict()) في القاموس self.users
        return self.users                                              # هذه الدالة تعيد جميع المستخدمين في قاعدة البيانات كقاموس
    
    def delete_user(self, username):
        self.user_ref = db.collection('users').document(username)              #  هذه الدالة تقوم بحذف مستخدم من قاعدة البيانات
        if self.user_ref.get().exists:                                   #  تستخدم Firebase للتحقق مما إذا كان اسم المستخدم موجودًا في قاعدة البيانات
            self.user_ref.delete()                                    #  ثم تحذف المستخدم من قاعدة البيانات باستخدام self.user_ref.delete()
            print("User deleted successfully")
            return True
        return False

 #  user_manager_app.py شرح الداله في    


class DatabaseManager:                     # هذه الكلاس مسؤول عن إدارة قاعدة البيانات الخاصة بالأسئلة والأجوبة
    #تحميل البيانات من ملف CSV fitrbase
#تنظيف البيانات
#إضافة سؤال جديد
#حفظ التغييرات في الملف
#جلب قائمة المجالات (التصنيفات)
    def __init__(self,):    # عند إنشاء كائن جديد من DatabaseManager، يتم تعيين مسار البيانات إلى data2.csv
      
        self.data = None #  لتخزين البيانات المحملة من ملف CSV
        #في البداية يكون None (فارغ) حتى يتم ملؤه من load_data().
        self.load_data() #  تحميل البيانات من ملف firebase عند إنشاء الكائن
      
    def load_data(self): # هذه الدالة تقوم بتحميل البيانات من ملف firebase إلى self.data
        """load_data() مسؤولة عن:
         قراءة ملف firebase.
         معالجة البيانات (تنظيفها، التحقق من الأعمدة).

        تخزينها داخل self.data على شكل DataFrame."""
        try: # يبدأ **كتلة try** لتجربة قراءة البيانات والتعامل مع أي أخطاء ممكنة (مثل: الملف غير موجود، أو تنسيق خاطئ).

            docs = db.collection("database").stream() #  يستخدم Firebase لجلب جميع وثائق الأسئلة من مجموعة 'database'
            
            qustion = []  #  قائمة لتخزين الأسئلة التي سيتم تحميلها
            for doc in docs: #  يقوم بتكرار كل وثيقة سؤال
                data = doc.to_dict() #  ويحفظ بيانات السؤال في متغير data
                if all(key in data for key in ['category', 'question', 'answer']):
                    qustion.append(data) #  يتحقق مما إذا كانت جميع المفاتيح المطلوبة موجودة في البيانات (category, question, answer)
        
            self.data = pd.DataFrame(qustion) #  ثم يحول قائمة الأسئلة إلى DataFrame ويخزنها في self.data
           
            """ 
             مثال:
             columns = {'المجال', 'السؤال', 'الجواب', 'ملاحظات'}
             print({'المجال', 'السؤال'}.issubset(columns))  # ✅ True
             print({'الاسم', 'السؤال'}.issubset(columns))   # ❌ False
             """
            
            self.data = self.data.dropna().drop_duplicates(subset=['question'])
            #  يحذف أي صفوف تحتوي على قيم فارغة (NaN) أو مكررة في عمود 'question'.
            """
            تُستخدم لحذف الصفوف التي تحتوي على قيم فارغة (NaN).
            df = pd.DataFrame({ 'سؤال': ['ما هو القبول؟', None, 'ما هي الشروط؟'],  'إجابة': ['من 1 إلى 10', 'بعد التسجيل', None]})
            print(df.dropna())

            drop_duplicates(subset=...)
            تحذف الصفوف المكررة بناءً على عمود معين أو مجموعة أعمدة.
            يحتفظ فقط بأول تكرار للسؤال ويحذف الباقي.

            """
            self.data = self.data.apply(lambda x: x.astype(str) if x.dtype == object else x)
            #  يحول جميع الأعمدة النصية إلى نوع str (نص) للتأكد من أن جميع البيانات متناسقة.
            
            #مفيد لأن مكتبة `pandas` أحيانًا تفترض نوع العمود بشكل تلقائي.
           
            """
            تُستخدم لتطبيق دالة (مثل lambda) على كل عمود أو صف داخل DataFrame.

          ✅ الاستخدام:
            مثال:
            يحوّل كل القيم النصية في الأعمدة إلى str.
            تستخدم لتحويل نوع البيانات إلى نوع معين، مثل str, int, float.
            
            astype(str)
             يحوّل كل القيم داخل العمود إلى نصوص str.
             s = pd.Series([1, 2, 3])
             print(s.astype(str))

            """
            print("The data has been loaded99999 successfully")
            return True # إذا تمت العملية بنجاح، تعيد الدالة True
        except Exception as e:
            print(f"Data loading error: {e}")
            return False
        

    
    def add_question(self, category, question, answer):# هذه الدالة تقوم بإضافة سؤال جديد إلى قاعدة البيانات
        
       ## new_row = pd.DataFrame({'category': [category], 'question': [question], 'answer': [answer]})
        #  تنشئ صفًا جديدًا (DataFrame) يحتوي على السؤال والإجابة.
        #  new_row هو DataFrame جديد يحتوي على صف واحد فقط.
        print("Adding question to database...")
        try:
            db.collection("database").add(
                {
                   
                    "category": category,
                    "question": question,
                    "answer": answer
                   

                } 
                )
            print("Question added successfully")
            return True # إذا تمت الإضافة بنجاح، تعيد الدالة True
        except Exception as e:
            print(f"Error adding question: {e}")
            return False
        
 
    
    
    def get_categories(self):
            #هذا يتحقق:    هل تم تحميل البيانات بنجاح داخل self.data؟   هذا يتحقق: هل يوجد عمود (column) اسمه "category" داخل الجدول؟   
        if self.data is not None and 'category' in self.data.columns: #  هذه الدالة تقوم بجلب قائمة المجالات (التصنيفات) من قاعدة البيانات
            print("Data not loaded yet 000000000000")
            return self.data['category'].unique().tolist() #  إذا لم يتم تحميل البيانات بعد، تعيد قائمة فريدة من جميع المجالات (التصنيفات) الموجودة في قاعدة البيانات
        """
        self.data['category'] → يأخذ عمود المجال
        .unique() → يستخرج القيم الفريدة (بدون تكرار)
        .tolist() → يحولها إلى قائمة Python عادية
        """
        return [] #  إذا كانت البيانات فارغة أو لا تحتوي على عمود 'category'، تعيد الدالة قائمة فارغة
        #return self.data['category'].unique().tolist() # هذه الدالة تعيد قائمة فريدة من جميع المجالات (التصنيفات) الموجودة في قاعدة البيانات


class AddQuestionDialog(QDialog):
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        
        """
        -- استدعاء دالة `__init__` الخاصة بالكلاس الأب `QDialog`.
        - هذا ضروري حتى تعمل خصائص PyQt مثل التحكم في إغلاق النافذة وواجهة المستخدم بشكل صحيح
        """
        self.db_manager = db_manager # في الدالة validate_input() لإضافة السؤال. نحفظ الكائن db_manager داخل المتغير self.db_manager حتى نستخدمه لاحقً
        
        self.setWindowTitle("إضافة سؤال جديد") # تعيين عنوان النافذة
        self.setMinimumWidth(500)# تعيين الحد الأدنى لعرض النافذة
        self.setLayoutDirection(Qt.RightToLeft)# تعيين اتجاه النصوص من اليمين لليسار (للغة العربية)
        self.init_ui() # استدعاء دالة init_ui() لإنشاء واجهة المستخدم
    
    def init_ui(self):
        # إعداد مظهر النافذة
        """      الغرض:
        بناء وتنسيق الواجهة الرسومية لإدخال:

          المجال (التصنيف)

         السؤال

          الإجابة

            الأزرار (موافق/إلغاء)"""

        with open("style/MainWindows.qss", "r", encoding="utf-8") as f:
             manage_qu = f.read()
        self.setStyleSheet(manage_qu)
        
        layout = QVBoxLayout()# إنشاء تخطيط عمودي لتنسيق العناصر داخل النافذة
        layout.setAlignment(Qt.AlignRight)# تعيين محاذاة التخطيط إلى اليمين
        self.setLayout(layout)# تعيين التخطيط كواجهة النافذة
        
        form = QFormLayout()# إنشاء تخطيط نموذج لتنسيق الحقول
        form.setLabelAlignment(Qt.AlignRight)# تعيين محاذاة التسمية إلى اليمين
        form.setFormAlignment(Qt.AlignRight)# تعيين محاذاة النموذج إلى اليمين
        form.setSpacing(15)# تعيين المسافة بين العناصر في النموذج
        
        # Category selection
        self.category_combo = QComboBox()# إنشاء قائمة منسدلة لاختيار المجال (التصنيف)
        categories = self.db_manager.get_categories()# جلب قائمة المجالات (التصنيفات) من قاعدة البيانات
        self.category_combo.addItems(categories)# إضافة المجالات إلى القائمة المنسدلة
        self.category_combo.setEditable(True)# جعل القائمة قابلة للتحرير
         # تعيين نمط القائمة المنسدلة
        form.addRow(QLabel("المجال:"), self.category_combo) # إضافة حقل اختيار المجال إلى النموذج
        
        # Question input
        self.question_input = QTextEdit() # إنشاء حقل نصي لإدخال السؤال
        self.question_input.setPlaceholderText("أدخل السؤال هنا...") # تعيين نص توضيحي للحقل
        self.question_input.setMaximumHeight(100) # تعيين الحد الأقصى لارتفاع الحقل
       

        form.addRow(QLabel("السؤال:"), self.question_input) # إضافة حقل إدخال السؤال إلى النموذج
        
        # Answer input
        self.answer_input = QTextEdit() # إنشاء حقل نصي لإدخال الإجابة
        self.answer_input.setPlaceholderText("أدخل الإجابة هنا...")
        self.answer_input.setMaximumHeight(200)
       # تعيين نمط حقل الإجابة
        form.addRow(QLabel("الإجابة:"), self.answer_input) # إضافة حقل إدخال الإجابة إلى النموذج
        
        layout.addLayout(form) # إضافة النموذج إلى التخطيط الرئيسي
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel) # إنشاء صندوق أزرار يحتوي على زر "موافق" وزر "إلغاء"
         # تعيين نمط صندوق الأزرار

        buttons.accepted.connect(self.validate_input)# ربط زر "موافق" بدالة validate_input() للتحقق من صحة المدخلات
        buttons.rejected.connect(self.reject) # ربط زر "إلغاء" بدالة reject() لإغلاق النافذة دون حفظ
        layout.addWidget(buttons) # إضافة صندوق الأزرار إلى التخطيط الرئيسي
    
    def validate_input(self):
        category = self.category_combo.currentText().strip()# الحصول على المجال المحدد من القائمة المنسدلة وإزالة المسافات الزائدة
        question = self.question_input.toPlainText().strip()# الحصول على السؤال المدخل وإزالة المسافات الزائدة
        answer = self.answer_input.toPlainText().strip()# الحصول على الإجابة المدخلة وإزالة المسافات الزائدة
        
        if not category or not question or not answer:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال جميع الحقول")
            return
            
        if len(question) < 5:
            QMessageBox.warning(self, "تحذير", "السؤال قصير جدًا")
            return
            
        if len(answer) < 10:
            QMessageBox.warning(self, "تحذير", "الإجابة قصيرة جدًا")
            return
            
        if self.db_manager.add_question(category, question, answer):
            QMessageBox.information(self, "نجاح", "تم إضافة السؤال بنجاح")
            self.accept()
        else:
            QMessageBox.warning(self, "خطأ", "فشل إضافة السؤال")

"""
        | الجزء              | الوظيفة                                 |
| ------------------ | --------------------------------------- |
| `QFormLayout`      | ترتيب الحقول (التصنيف، السؤال، الإجابة) |
| `QComboBox`        | اختيار أو إدخال تصنيف                   |
| `QTextEdit`        | إدخال السؤال والإجابة                   |
| `QDialogButtonBox` | أزرار موافق/إلغاء                       |
| `StyleSheet`       | تنسيق الألوان والخطوط                   |
"""

class AdminPanel(QDialog):
    def __init__(self, user_db, db_manager, qa_engine, parent=None):
        super().__init__(parent) # استدعاء دالة __init__ الخاصة بالكلاس الأب QDialog
        self.user_db = user_db # حفظ كائن UserDatabase لإدارة المستخدمين
        self.db_manager = db_manager # حفظ كائن DatabaseManager لإدارة الأسئلة والأجوبة
        self.qa_engine = qa_engine # حفظ كائن QAEengine لإدارة محرك الأسئلة والأجوبة
        self.setWindowTitle("لوحة تحكم المسؤول")
        self.setMinimumSize(900, 600)
        self.setLayoutDirection(Qt.RightToLeft)
        self.init_ui()
    
    def init_ui(self):
        with open("style/MainWindows.qss", "r", encoding="utf-8") as f:
            Adstyle = f.read()
        self.setStyleSheet(Adstyle) # تعيين نمط الواجهة من ملف QSS
        
        layout = QVBoxLayout() # إنشاء تخطيط عمودي لتنسيق العناصر داخل النافذة
        self.setLayout(layout) # تعيين التخطيط كواجهة النافذة
        
        # Tab widget
        self.tabs = QTabWidget()  # إنشاء تبويب لتقسيم الواجهة إلى أقسام مختلفة
        layout.addWidget(self.tabs)  # إضافة التبويب إلى التخطيط الرئيسي
        #example 6

        # Users tab
        self.users_tab = QWidget() # إنشاء تبويب لإدارة المستخدمين
        self.init_users_tab() # استدعاء دالة init_users_tab() لإنشاء واجهة إدارة المستخدمين
        self.tabs.addTab(self.users_tab, "إدارة المستخدمين")
        
        # Questions tab
        self.questions_tab = QWidget()
        self.init_questions_tab()
        self.tabs.addTab(self.questions_tab, "إدارة الأسئلة")
        
        # Close button
        close_btn = QPushButton("إغلاق")

        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
    
    def init_users_tab(self): # هذه الدالة تقوم بإنشاء واجهة إدارة المستخدمين
        layout = QVBoxLayout() # إنشاء تخطيط عمودي لتنسيق العناصر داخل تبويب المستخدمين
        self.users_tab.setLayout(layout)
        """ 
        تنشئ تخطيط الواجهة.

         تضيف عنوانًا في الأعلى.

           تعرض جدولًا للمستخدمين.

            توفر نموذجًا لإضافة مستخدم جديد.
 
          تضيف زر "إضافة مستخدم".

          في النهاية، تُحمّل المستخدمين الحاليين من قاعدة البيانات.
        
        """
        # Title
        title = QLabel("إدارة المستخدمين")
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)# تعيين محاذاة العنوان إلى المركز
        layout.addWidget(title) # إضافة العنوان إلى التخطيط
        
        # Table of users
        self.users_table = QTableWidget() # إنشاء جدول لعرض المستخدمين
        self.users_table.setColumnCount(3) # تعيين عدد الأعمدة في الجدول إلى 3
        self.users_table.setHorizontalHeaderLabels(["اسم المستخدم", "نوع المستخدم", "الإجراءات"])# تعيين أسماء الأعمدة في الجدول
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)# تعيين حجم الأعمدة لتمتد لتملأ العرض المتاح
        self.users_table.setEditTriggers(QAbstractItemView.NoEditTriggers)# منع تحرير الخلايا في الجدول
        self.users_table.verticalHeader().setVisible(False) # إخفاء رؤوس الصفوف في الجدول
        layout.addWidget(self.users_table) # إضافة جدول المستخدمين إلى التخطيط
        
        # Add user form
        form = QFormLayout() # إنشاء تخطيط نموذج لإضافة مستخدم جديد
        form.setLabelAlignment(Qt.AlignRight)# تعيين محاذاة التسمية إلى اليمين
        form.setFormAlignment(Qt.AlignRight)# تعيين محاذاة النموذج إلى اليمين
        form.setSpacing(15) # تعيين المسافة بين العناصر في النموذج
        
        self.new_username = QLineEdit() # إنشاء حقل نصي لإدخال اسم المستخدم الجديد
        self.new_username.setPlaceholderText("اسم المستخدم الجديد")
        form.addRow(QLabel("اسم المستخدم:"), self.new_username) # إضافة حقل اسم المستخدم إلى النموذج
        
        self.new_password = QLineEdit() # إنشاء حقل نصي لإدخال كلمة المرور الجديدة
        self.new_password.setPlaceholderText("كلمة المرور")
        self.new_password.setEchoMode(QLineEdit.Password)
        form.addRow(QLabel("كلمة المرور:"), self.new_password)
        
        self.new_user_type = QComboBox() # إنشاء قائمة منسدلة لاختيار نوع المستخدم
        self.new_user_type.addItems(["طالب", "مسؤول"])
        form.addRow(QLabel("نوع المستخدم:"), self.new_user_type)
        
        layout.addLayout(form) # إضافة نموذج إضافة المستخدم إلى التخطيط
        
        # Add user button
        self.add_button = QPushButton("إضافة مستخدم") # إنشاء زر لإضافة مستخدم جديد
         # تعيين نمط زر إضافة المستخدم من ملف QSS
        self.add_button.clicked.connect(self.add_user) # ربط زر إضافة المستخدم بدالة add_user() لإضافة المستخدم الجديد
        layout.addWidget(self.add_button, alignment=Qt.AlignRight)# إضافة زر إضافة المستخدم إلى التخطيط
        
        self.load_users()# تحميل المستخدمين الحاليين من قاعدة البيانات وعرضهم في الجدول
    
    def init_questions_tab(self):
        layout = QVBoxLayout()
        self.questions_tab.setLayout(layout)
        
        # Title
        title = QLabel("إدارة الأسئلة")
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Add question button
        add_question_btn = QPushButton("إضافة سؤال جديد")
       
        add_question_btn.clicked.connect(self.show_add_question_dialog)
        layout.addWidget(add_question_btn, alignment=Qt.AlignRight)
        
        # Refresh model button
        refresh_btn = QPushButton("تحديث نموذج الأسئلة")
        
        refresh_btn.clicked.connect(self.refresh_model)
        layout.addWidget(refresh_btn, alignment=Qt.AlignRight)
        
        # Questions table
        self.questions_table = QTableWidget()
        self.questions_table.setColumnCount(3)
        self.questions_table.setHorizontalHeaderLabels(["المجال", "السؤال", "الإجابة"])
        self.questions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.questions_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.questions_table.verticalHeader().setVisible(False)
        layout.addWidget(self.questions_table)
        
        self.load_questions()
    
    def load_users(self):
        users = self.user_db.get_all_users()
        self.users_table.setRowCount(len(users))
        
        for row, (username, user_data) in enumerate(users.items()):
            self.users_table.setItem(row, 0, QTableWidgetItem(username))
            
            user_type = "مسؤول" if user_data['type'] == 'admin' else "طالب"
            self.users_table.setItem(row, 1, QTableWidgetItem(user_type))
            
            # Don't allow deleting admin user
            if username == 'admin':
                self.users_table.setItem(row, 2, QTableWidgetItem("غير مسموح"))
            else:
                delete_btn = QPushButton("حذف")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f44336;
                        color: white;
                        padding: 5px;
                        border-radius: 3px;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #d32f2f;
                    }
                """)
                delete_btn.clicked.connect(lambda _, u=username: self.delete_user(u))
                self.users_table.setCellWidget(row, 2, delete_btn)
    
    def load_questions(self):
        questions = self.db_manager.data
        self.questions_table.setRowCount(len(questions))
        
        for row in range(len(questions)):
            self.questions_table.setItem(row, 0, QTableWidgetItem(questions.iloc[row]['category']))
            self.questions_table.setItem(row, 1, QTableWidgetItem(questions.iloc[row]['question']))
            self.questions_table.setItem(row, 2, QTableWidgetItem(questions.iloc[row]['answer']))
    
    def add_user(self):
        username = self.new_username.text().strip()
        password = self.new_password.text().strip()
        user_type = "admin" if self.new_user_type.currentText() == "مسؤول" else "student"
        
        if not username or not password:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال اسم المستخدم وكلمة المرور")
            return
        
        if len(username) < 3:
            QMessageBox.warning(self, "تحذير", "اسم المستخدم يجب أن يكون 3 أحرف على الأقل")
            return
            
        if len(password) < 4:
            QMessageBox.warning(self, "تحذير", "كلمة المرور يجب أن تكون 4 أحرف على الأقل")
            return
            
        if self.user_db.add_user(username, password, user_type):
            QMessageBox.information(self, "نجاح", "تم إضافة المستخدم بنجاح")
            self.new_username.clear()
            self.new_password.clear()
            self.load_users()
        else:
            QMessageBox.warning(self, "تحذير", "اسم المستخدم موجود مسبقًا")
    
    def delete_user(self, username):
        if QMessageBox.question(self, "تأكيد", f"هل أنت متأكد من حذف المستخدم {username}؟",
                              QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            if self.user_db.delete_user(username):
                QMessageBox.information(self, "نجاح", "تم حذف المستخدم بنجاح")
                self.load_users()
            else:
                QMessageBox.warning(self, "خطأ", "فشل حذف المستخدم")
    
    def show_add_question_dialog(self):
        dialog = AddQuestionDialog(self.db_manager, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_questions()
    
    def refresh_model(self):
        try:
            self.db_manager.load_data()  # إعادة تحميل البيانات من قاعدة البيانات
            self.qa_engine.data = self.db_manager.data.copy()  # تحديث البيانات في محرك الأسئلة والأجوبة
            self.qa_engine.preprocess_data() # إعادة تحميل البيانات في محرك الأسئلة والأجوبة
            self.qa_engine.train_model()  # إعادة تدريب النموذج على البيانات الجديدة
            QMessageBox.information(self, "نجاح", "تم تحديث نموذج الأسئلة بنجاح")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل تحديث النموذج: {str(e)}")


class TabukUniversityQA:
    def __init__(self,data):
        self.arabic_stopwords = set([
            'في', 'من', 'إلى', 'على', 'عن', 'أن', 'لا', 'ما', 'هذا', 'هذه', 
            'ذلك', 'هؤلاء', 'التي', 'الذي', 'الذين', 'كان', 'يكون', 'و', 'ف', 
            'ثم', 'أو', 'أم', 'لكن', 'إن', 'إذا', 'هل', 'إلا', 'قد', 'حيث', 
            'بين', 'حتى', 'عند', 'بعض', 'كل', 'أي', 'هنا', 'هناك', 'مع', 'هو', 
            'هي', 'هم', 'كيف', 'متى', 'أين', 'لماذا', 'كم', 'فيها', 'له', 'لها', 
            'عليه', 'عليها', 'إليه', 'إليها', 'فيه', 'منه', 'منها', 'إياه', 'إياها',
            'عما', 'مما', 'غير', 'سوى', 'حين', 'الآن', 'قط', 'أمس', 'اليوم', 'غدا',
            'قبل', 'بعد'
        ])
        
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_df=0.8)
        self.data = data  # DataFrame containing the questions and answers
        self.tfidf_matrix = None
        
        self.preprocess_data()
        self.train_model()
        print("Data loaded successfully")

    def load_data(self):
        try:
            docs = db.collection("database").stream()
            qustion = []
            for doc in docs:
                data = doc.to_dict()
                if all(key in data for key in ['category', 'question', 'answer']):
                    qustion.append(data)
            self.data = pd.DataFrame(qustion)
            self.data = self.data.dropna().drop_duplicates(subset=['question'])
            self.data = self.data.apply(lambda x: x.astype(str) if x.dtype == object else x)
            self.preprocess_data()
            self.train_model()
            print("Data loaded successfully")
            return True
        except Exception as e:
            print(f"Data loading error: {e}")
            return False
    
    def preprocess_data(self):
        self.data['processed_question'] = self.data['question'].apply(self._clean_arabic_text)
        self.data['processed_answer'] = self.data['answer'].apply(self._clean_arabic_text)
        self.data['combined_text'] = self.data['processed_question'] + " " + self.data['processed_answer']
    
    def _clean_arabic_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ة', 'ه').replace('ى', 'ي')
        text = re.sub(r'[^\w\s\u0600-\u06FF،؛؟]', ' ', text)
        text = re.sub(r'[\u064b-\u0652\u0640]', '', text)
        text = re.sub(r'[a-zA-Z\d]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        words = [word for word in text.split() if word not in self.arabic_stopwords]
        return ' '.join(words)
    
    def train_model(self):
        if self.data is None:
            raise ValueError("No data loaded")
        self.vectorizer.fit(self.data['combined_text'])
        self.tfidf_matrix = self.vectorizer.transform(self.data['combined_text'])
    
    def ask_question(self, question, threshold=0.25):
        try:
            if not question or not isinstance(question, str):
                return "الرجاء إدخال سؤال صحيح"
            clean_question = self._clean_arabic_text(question)
            if len(clean_question.split()) < 2:
                return "السؤال قصير جدًا، يرجى تقديم المزيد من التفاصيل"
            results = self.get_most_similar(clean_question)
            if not results or results[0]['similarity'] < threshold:
                return "عذرًا، لا أمتلك إجابة كافية على هذا السؤال. يرجى الرجوع إلى الموقع الرسمي لجامعة تبوك لمزيد من المعلومات."
            answer = results[0]['answer']
            if not answer.strip():
                return "عذرًا، الإجابة فارغة في قاعدة البيانات"
            return f"{answer}\n\n(هذه الإجابة متعلقة بمجال: {results[0]['category']})"
        except Exception as e:
            print(f"Full error: {e}")
            return "حدث خطأ غير متوقع أثناء معالجة سؤالك. يرجى المحاولة مرة أخرى."

    def get_most_similar(self, query, top_n=3):
        try:
            query_vec = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            top_indices = similarities.argsort()[-top_n:][::-1]
            return [{
                'question': self.data.iloc[idx]['question'],
                'answer': self.data.iloc[idx]['answer'],
                'similarity': similarities[idx],
                'category': self.data.iloc[idx]['category']
            } for idx in top_indices if similarities[idx] > 0.1]
        except Exception as e:
            print(f"Similarity error: {e}")
            return None


class CreateAccountDialog(QDialog):
    def __init__(self, user_db, parent=None):
        super().__init__(parent)
        self.user_db = user_db
        self.setWindowTitle("إنشاء حساب جديد")
        self.setMinimumWidth(400)
        self.setLayoutDirection(Qt.RightToLeft)
        self.init_ui()
    
    def init_ui(self):
        # Set green background
        with open("style/MainWindows.qss", "r", encoding="utf-8") as f:
            create_account_style = f.read()
        self.setStyleSheet(create_account_style)
       
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignRight)
        self.setLayout(layout)
        
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignRight)
        form.setSpacing(15)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("اسم المستخدم")
       
        form.addRow(QLabel("اسم المستخدم:"), self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("كلمة المرور")
        self.password_input.setEchoMode(QLineEdit.Password)

        form.addRow(QLabel("كلمة المرور:"), self.password_input)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("تأكيد كلمة المرور")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        form.addRow(QLabel("تأكيد كلمة المرور:"), self.confirm_password_input)
        
        self.user_type_combo = QComboBox()
        self.user_type_combo.addItems(["طالب"])
        form.addRow(QLabel("نوع المستخدم:"), self.user_type_combo)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.validate_input)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def validate_input(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        user_type = "student" if self.user_type_combo.currentText() == "طالب" else "admin"
        
        if not username or not password:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال اسم المستخدم وكلمة المرور")
            return
        
        if len(username) < 3:
            QMessageBox.warning(self, "تحذير", "اسم المستخدم يجب أن يكون 3 أحرف على الأقل")
            return
            
        if len(password) < 4:
            QMessageBox.warning(self, "تحذير", "كلمة المرور يجب أن تكون 4 أحرف على الأقل")
            return
            
        if password != confirm_password:
            QMessageBox.warning(self, "تحذير", "كلمة المرور وتأكيدها غير متطابقين")
            return
            
        if self.user_db.add_user(username, password, user_type):
            QMessageBox.information(self, "نجاح", "تم إنشاء الحساب بنجاح")
            self.accept()
        else:
            QMessageBox.warning(self, "تحذير", "اسم المستخدم موجود مسبقًا")


class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.user_db = UserDatabase()
        self.setLayoutDirection(Qt.RightToLeft)
        self.init_ui()
    
    def init_ui(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        # Logo
        logo_label = QLabel()
        try:
            response = requests.get("https://iconape.com/wp-content/files/vf/193315/png/193315.png")
            logo_pixmap = QPixmap()
            logo_pixmap.loadFromData(response.content)
            logo_pixmap = logo_pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        except:
            logo_label.setText("جامعة تبوك")
            logo_label.setFont(QFont('Arial', 24, QFont.Bold))
            logo_label.setStyleSheet("color: #2e7d32;")
        
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        # Title
        title = QLabel("Ubot Academic Assistant")
        title.setFont(QFont('Arial', 18, QFont.Bold))
        with open("style/stylesheetTitle.qss", "r", encoding="utf-8") as f:
            title_style = f.read()
        title.setStyleSheet(title_style)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Login Form
        form = QFormLayout()
        form.setFormAlignment(Qt.AlignRight)
        form.setLabelAlignment(Qt.AlignRight)
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(15)
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("اسم المستخدم")
        self.username.setMinimumWidth(300)
        self.username.setMinimumHeight(40)
        form.addRow(QLabel("اسم المستخدم:"), self.username)
        

        self.password = QLineEdit()
        self.password.setPlaceholderText("كلمة المرور")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setMinimumWidth(300)
        self.password.setMinimumHeight(40)
        form.addRow(QLabel("كلمة المرور:"), self.password)
        layout.addLayout(form)
        
        # Login Button
        login_btn = QPushButton("تسجيل الدخول")
        login_btn.setFont(QFont('Arial', 14))
        login_btn.setMinimumHeight(45)
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)
        
        # Create Account Button
        create_account_btn = QPushButton("إنشاء حساب جديد")
        create_account_btn.setFont(QFont('Arial', 12))
        create_account_btn.setStyleSheet("""
            QPushButton {
                color: #ACADB9;
                border: none;
                padding: 5px;
                background-color: transparent;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        create_account_btn.clicked.connect(self.show_create_account)
        layout.addWidget(create_account_btn, alignment=Qt.AlignCenter)
        
        
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "تحذير", "الرجاء إدخال اسم المستخدم وكلمة المرور")
            return
        
        user_type = self.user_db.validate_user(username, password)
        if user_type:
            self.parent.current_user = username
            self.parent.user_type = user_type
            self.parent.switch_to_main_app()
        else:
            QMessageBox.warning(self, "تحذير", "اسم المستخدم أو كلمة المرور غير صحيحة")
    
    def show_create_account(self):
        dialog = CreateAccountDialog(self.user_db, self)
        dialog.exec_()


class QAApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_db = UserDatabase()
        self.db_manager = DatabaseManager()
        self.qa_engine = TabukUniversityQA(self.db_manager.data)
        self.current_user = None
        self.user_type = None
        self.user_info_label = None
        
        # Set green theme
        with open("style/MainWindows.qss", "r", encoding="utf-8") as f:
            main_style = f.read()
        self.setStyleSheet(main_style)
        
        # Set RTL direction for the main window
        self.setLayoutDirection(Qt.LeftToRight)
        
        # Create stacked widget for multiple pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setLayoutDirection(Qt.RightToLeft)
        self.setCentralWidget(self.stacked_widget)
        
        # Create pages
        self.login_page = LoginPage(self)
        self.main_page = QWidget()
        self.main_page.setLayoutDirection(Qt.RightToLeft)
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.main_page)
        
        self.init_main_ui()
        
        # Start with login page
        self.stacked_widget.setCurrentWidget(self.login_page)
        self.setWindowTitle("Ubot")
        self.setMinimumSize(1000, 750)
        
        # Set window icon
        try:
            response = requests.get("https://iconape.com/wp-content/files/vf/193315/png/193315.png")
            icon_pixmap = QPixmap()
            icon_pixmap.loadFromData(response.content)
            self.setWindowIcon(QIcon(icon_pixmap))
        except:
            pass
    
    def switch_to_main_app(self):
        # Reinitialize the main page to update the user info
        self.main_page = QWidget()
        self.main_page.setLayoutDirection(Qt.RightToLeft)
        self.stacked_widget.removeWidget(self.stacked_widget.widget(1))
        self.stacked_widget.addWidget(self.main_page)
        self.init_main_ui()
        
        self.stacked_widget.setCurrentWidget(self.main_page)
        user_type_display = "مسؤول" if self.user_type == "admin" else "طالب"
        self.setWindowTitle(f"نظام الإجابة الآلي لجامعة تبوك - {user_type_display}: {self.current_user}")
        
        if self.user_info_label:
            self.user_info_label.setText(f"المستخدم: {self.current_user} ({user_type_display})")
        
    def init_main_ui(self):
        main_layout = QVBoxLayout(self.main_page)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Header with logo and title
        header = QWidget()
        header.setLayoutDirection(Qt.RightToLeft)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Logo
        logo_label = QLabel()
        try:
            response = requests.get("https://iconape.com/wp-content/files/vf/193315/png/193315.png")
            logo_pixmap = QPixmap()
            logo_pixmap.loadFromData(response.content)
            logo_pixmap = logo_pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        except:
            pass
        
        header_layout.addWidget(logo_label)
        
        # Title
        title = QLabel("Ubot")
        title.setFont(QFont('Arial', 30, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title, alignment=Qt.AlignCenter)
        
        header_layout.addStretch()
        
        # User info - store reference to update later
        user_type_display = "مسؤول" if self.user_type == "admin" else "طالب"
        self.user_info_label = QLabel(f"المستخدم: {self.current_user if self.current_user else 'غير مسجل'} ({user_type_display})")
        self.user_info_label.setFont(QFont('Arial', 12))
        self.user_info_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.user_info_label)
        
        # Admin panel button (only for admin users)
        if self.user_type == "admin":
            admin_btn = QPushButton("لوحة التحكم")
            admin_btn.setFont(QFont('Arial', 12))

            admin_btn.clicked.connect(self.show_admin_panel)
            header_layout.addWidget(admin_btn)
        
        # Logout button
        logout_btn = QPushButton("تسجيل الخروج")
        logout_btn.setFont(QFont('Arial', 12))

        logout_btn.clicked.connect(self.logout)
        header_layout.addWidget(logout_btn)
        
        main_layout.addWidget(header)
        

        # Question input area
        question_layout = QHBoxLayout()
        question_layout.setAlignment(Qt.AlignCenter)
        question_layout.setSpacing(15)

        # Chat area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)#  تعيين قابلية تغيير حجم المحتوى
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_container.setLayout(self.chat_layout)
        self.scroll_area.setWidget(self.chat_container)
        main_layout.addWidget(self.scroll_area)
    

        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setLayoutDirection(Qt.RightToLeft)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("جاهز", 3000)
         
        # Lower layout for question input and ask button
        self.lower_layout = QHBoxLayout() # تخطيط الجزء السفلي
        self.lower_layout.setAlignment(Qt.AlignCenter)
        self.lower_layout.setSpacing(2)

        # Ask button
        self.ask_button = QPushButton("➤")
        self.ask_button.setFont(QFont('Arial', 14))
        self.ask_button.setFixedSize(55, 55)
        with open("style/AskButton.qss", "r", encoding="utf-8") as f:
            ask_button_style = f.read()
        self.ask_button.setStyleSheet(ask_button_style)
        self.ask_button.setLayoutDirection(Qt.RightToLeft)
        self.ask_button.clicked.connect(self.ask_question)
        self.lower_layout.addWidget(self.ask_button, alignment=Qt.AlignRight)   

       
        # Question input field
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("اكتب سؤالك هنا...")
        self.question_input.setFont(QFont('Arial', 14))
        self.question_input.setMinimumHeight(50)
        self.question_input.setMinimumWidth(500)
        with open("style/QuestionInput.qss", "r", encoding="utf-8") as f:
            question_input_style = f.read()
        self.question_input.setStyleSheet(question_input_style)
      
        self.question_input.setLayoutDirection(Qt.LeftToRight)
        self.question_input.returnPressed.connect(self.ask_question)
        question_layout.addWidget(self.question_input)
        self.lower_layout.addLayout(question_layout)

        main_layout.addLayout(self.lower_layout)


    
    def show_admin_panel(self):
        if self.user_type == "admin":
            admin_panel = AdminPanel(self.user_db, self.db_manager, self.qa_engine, self)
            admin_panel.exec_()
    
    def logout(self):
        self.current_user = None
        self.user_type = None
        self.stacked_widget.setCurrentWidget(self.login_page)
    
    def ask_question(self):
        question = self.question_input.text().strip()
        if not question:
            QMessageBox.information(self, "معلومة", "الرجاء إدخال سؤال")
            return
        try:
            self.status_bar.showMessage("جارٍ معالجة السؤال...")
            QApplication.processEvents()  # Update UI immediately
            
            self.add_chat_message(question, sender='user') #عرض سؤال المستخدم 

            answer = self.qa_engine.ask_question(question)
           
            self.add_chat_message(answer, sender='bot')  # عرض إجابة النظام

            ##self.answer_display.setPlainText(answer)

            self.question_input.clear()
            self.status_bar.showMessage("تمت معالجة السؤال", 3000)
        except Exception as e:
            QMessageBox.critical(self, "خطأ", "حدث خطأ أثناء معالجة السؤال")
            self.status_bar.showMessage("خطأ في معالجة السؤال", 3000)

    def add_chat_message(self,text,sender='user'):
            message = QLabel(text)
            message.setWordWrap(True)
            with open("style/Messageuser.qss", "r", encoding="utf-8") as f:
                messageuser_style = f.read()
            with open("style/MessageBot.qss", "r", encoding="utf-8") as f:
                messageBot_style = f.read()
            if sender == 'user':
                message.setStyleSheet(messageuser_style)
                self.chat_layout.addWidget(message, alignment=Qt.AlignRight)

                
            else:
                message.setStyleSheet( messageBot_style)
                self.chat_layout.addWidget(message, alignment=Qt.AlignLeft)
            
            message_container = QWidget()
            layout = QHBoxLayout()
            layout.setContentsMargins(10, 5, 10, 5)
            
            if sender == 'user':
                layout.addStretch()
                layout.addWidget(message)
            else:
                layout.addWidget(message)
                layout.addStretch()

            message_container.setLayout(layout)
            self.chat_layout.addWidget(message_container)

            QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum()))


              

def main():
    app = QApplication([])
    app.setFont(QFont('Arial', 12))
    app.setStyle('Fusion')  # Modern style
    
    # Set RTL layout direction for the entire application
    app.setLayoutDirection(Qt.RightToLeft)
    
    window = QAApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()