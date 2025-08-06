import pandas as pd
from firebase_config import db
import uuid

# تحميل ملف CSV
df = pd.read_csv("data2.csv", delimiter=';', encoding='utf-8-sig')

# إعادة تسمية الأعمدة (إذا لم تكن مرتبة)
df.columns = ['category', 'question', 'answer']

# حذف القيم الفارغة والمكررة
df = df.dropna().drop_duplicates(subset=['question'])

# رفع البيانات إلى Firestore
for index, row in df.iterrows():
    db.collection("database").document(str(uuid.uuid4())).set({
        "category": row['category'],
        "question": row['question'],
        "answer": row['answer']
    })

print("✅ تم رفع جميع الأسئلة إلى Firebase بنجاح")
