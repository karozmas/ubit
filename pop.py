from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1) المستندات (البيانات اللي ندرب عليها)
documents = [
    "جامعة تبوك",
    "شروط القبول في جامعة تبوك",
    "الرسوم الدراسية لجامعة تبوك"
]

# 2) إنشاء وتدريب TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)  # بناء القاموس + تحويل المستندات

# 3) السؤال الجديد
query = "ما هي الرسوم الدراسية في جامعة تبوك"
query_vec = vectorizer.transform([query])  # تحويل السؤال إلى متجه

# 4) حساب التشابه مع كل المستندات
similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

# 5) استخراج أقرب مستند
best_index = np.argmax(similarities)  # أعلى قيمة
best_score = similarities[best_index]

# 6) عرض النتائج
print("السؤال الجديد:", query)
print("\nنسب التشابه مع كل المستندات:")
for i, score in enumerate(similarities):
    print(f"{documents[i]} → {score:.4f}")

print("\nأقرب مستند:")
print(f"{documents[best_index]} (التشابه: {best_score:.4f})")