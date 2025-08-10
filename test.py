# -*- coding: utf-8 -*-
"""
Evaluator using your project's DatabaseManager + TabukUniversityQA.

ماذا يفعل السكربت؟
1) يستورد DatabaseManager و TabukUniversityQA من ملف مشروعك.
2) ينشئ DatabaseManager ويحمّل البيانات من Firebase.
3) يهيّئ TabukUniversityQA على نفس البيانات (تمامًا مثل التطبيق).
4) يقرأ ملف test_questions.xlsx (الأعمدة: ref_id, variant, test_question, expected_category).
5) يشغّل كل سؤال، يأخذ أفضل نتيجة (Top-1)، ويقارن التصنيف المتوقّع مع المتنبّأ.
6) يحسب الدقة (Top-1 Accuracy) ويولّد ملف eval_results.xlsx يحتوي:
   - predictions (تفاصيل النتائج)
   - confusion_matrix (مصفوفة الالتباس)
   - summary (ملخص الدقة)

طريقة التشغيل:
python evaluate_with_dbmanager.py
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# اجعل مسار المشروع قابلاً للاستيراد
# عدّل هذا المسار إذا كان ملفك في مكان مختلف
PROJECT_DIR = Path(".").resolve()
if str(PROJECT_DIR) not in sys.path:
    sys.path.append(str(PROJECT_DIR))

# استيراد الكلاسات من مشروعك
from university_qa9_FinalProject import DatabaseManager, TabukUniversityQA

# ---------- إعدادات الملفات ----------
# ملف أسئلة الاختبار الذي أنشأناه من قبل
TEST_QUESTIONS_XLSX = Path("C:\\Users\\Abdulelahh\\Documents\\Ubit\\test_questions.xlsx")  # أو ضع المسار الكامل إذا لزم
# ملف الإخراج
OUT_XLSX = Path("eval_results.xlsx")

def main():
    # 1) تحميل البيانات عبر DatabaseManager
    print("[INFO] Initializing DatabaseManager and loading data from Firebase...")
    db_manager = DatabaseManager()
    if db_manager.data is None or db_manager.data.empty:
        raise RuntimeError("DatabaseManager.data is empty. تأكد أن الاتصال بـ Firebase صحيح وأن مجموعة 'database' تحتوي بيانات.")

    # توقع أن الأعمدة: category, question, answer
    data = db_manager.data.copy()
    for col in ["category", "question", "answer"]:
        if col not in data.columns:
            raise RuntimeError(f"Missing required column '{col}' in db_manager.data.")

    # 2) تهيئة محرّك الأسئلة والأجوبة على نفس الداتا
    print("[INFO] Initializing TabukUniversityQA with loaded data...")
    qa_engine = TabukUniversityQA(data[["category", "question", "answer"]].copy())

    # 3) قراءة ملف أسئلة الاختبار
    print(f"[INFO] Loading test questions from: {TEST_QUESTIONS_XLSX}")
    if not TEST_QUESTIONS_XLSX.exists():
        raise FileNotFoundError(f"لم أجد ملف الاختبار: {TEST_QUESTIONS_XLSX}. تأكد من المسار.")

    test_df = pd.read_excel(TEST_QUESTIONS_XLSX)
    for col in ["test_question", "expected_category"]:
        if col not in test_df.columns:
            raise RuntimeError(f"ملف الاختبار يجب أن يحتوي الأعمدة: 'test_question', 'expected_category' — العمود الناقص: {col}")

    # 4) التشغيل والتقييم
    print("[INFO] Running evaluation (Top-1 by category)...")
    records = []
    for _, row in test_df.iterrows():
        q_raw = str(row["test_question"])
        expected_cat = str(row["expected_category"])

        # نفس مسار المعالجة المستخدم داخل النظام
        clean_q = qa_engine._clean_arabic_text(q_raw)
        results = qa_engine.get_most_similar(clean_q, top_n=3)

        if results and len(results) > 0:
            top1 = results[0]
            pred_cat = str(top1["category"])
            pred_sim = float(top1["similarity"])
            matched_q = str(top1["question"])
            matched_ans = str(top1["answer"])
            topk_preview = [{"category": r["category"], "similarity": r["similarity"], "question": r["question"]} for r in results]
        else:
            pred_cat = None
            pred_sim = None
            matched_q = None
            matched_ans = None
            topk_preview = []

        is_correct = (pred_cat == expected_cat)
        records.append({
            "test_question": q_raw,
            "expected_category": expected_cat,
            "predicted_category": pred_cat,
            "similarity_top1": pred_sim,
            "matched_question_top1": matched_q,
            "matched_answer_top1": matched_ans,
            "topk_preview": str(topk_preview[:3]),
            "is_correct": is_correct,
        })

    results_df = pd.DataFrame(records)

    # 5) حساب الدقّة ومصفوفة الالتباس
    total = len(results_df)
    correct = int(results_df["is_correct"].sum())
    accuracy = correct / total if total else 0.0
    confusion = pd.crosstab(results_df["expected_category"], results_df["predicted_category"], dropna=False)

    print(f"[INFO] Evaluation done. Accuracy (Top-1): {accuracy:.4f}  [{correct}/{total}]")

    # 6) إخراج النتائج لملف Excel
    print(f"[INFO] Writing results to: {OUT_XLSX}")
    with pd.ExcelWriter(OUT_XLSX, engine="xlsxwriter") as writer:
        results_df.drop(columns=["is_correct"]).to_excel(writer, index=False, sheet_name="predictions")
        confusion.to_excel(writer, sheet_name="confusion_matrix")
        summary_df = pd.DataFrame([{
            "total": total,
            "correct": correct,
            "accuracy_top1": round(accuracy, 4)
        }])
        summary_df.to_excel(writer, index=False, sheet_name="summary")

    print("[INFO] Done.")

if __name__ == "__main__":
    main()
