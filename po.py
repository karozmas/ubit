import pandas as pd
from firebase_admin import credentials, firestore, initialize_app
from pandas import json_normalize
from datetime import datetime
import os

# ====== إعداد الاتصال بـ Firebase ======
SERVICE_ACCOUNT_PATH = r"C:\Users\Abdulelahh\Documents\Ubit\firebasekey.json"  # <-- عدّل المسار
FIRESTORE_COLLECTION  = "database"                        # <-- عدّل اسم المجموعة إن لزم
OUTPUT_XLSX           = f"firebase_export_{FIRESTORE_COLLECTION}.xlsx"

if not os.path.exists(SERVICE_ACCOUNT_PATH):
    raise FileNotFoundError("مسار ملف الخدمة غير صحيح.")

cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
try:
    initialize_app(cred)
except ValueError:
    # تم التهيئة مسبقاً
    pass

db = firestore.client()

# ====== جلب كل المستندات من المجموعة ======
docs = db.collection(FIRESTORE_COLLECTION).stream()

rows = []
for doc in docs:
    data = doc.to_dict() or {}
    data["_document_id"] = doc.id
    data["_read_time"] = datetime.utcnow().isoformat() + "Z"
    rows.append(data)

if not rows:
    print("لا توجد مستندات في المجموعة المحددة.")
    raise SystemExit

# ====== تسوية الحقول المتداخلة (إن وجدت) وكتابة Excel ======
df = json_normalize(rows)  # يحول القواميس المتداخلة لأعمدة "a.b.c"
# ترتيب أعمدة شائعة أولاً إن وُجدت
preferred = ["_document_id", "category", "question", "answer", "_read_time"]
cols = [c for c in preferred if c in df.columns] + [c for c in df.columns if c not in preferred]
df = df[cols]

# حفظ إلى إكسل
df.to_excel(OUTPUT_XLSX, index=False)
print(f"تم إنشاء الملف: {OUTPUT_XLSX}")
