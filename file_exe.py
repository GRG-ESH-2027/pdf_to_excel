import os
import subprocess

# اسم ملف الواجهة وملف البايثون
ui_file = "design.ui"  # اسم ملف الواجهة
script_file = "pdf_to_excel.py"  # اسم ملف الكود الرئيسي

# بناء الأمر لإنشاء ملف تنفيذي باستخدام PyInstaller
command = f"pyinstaller --noconfirm --onefile --windowed --add-data \"{ui_file};.\" {script_file}"

# تنفيذ الأمر
try:
    subprocess.run(command, shell=True, check=True)
    print("تم إنشاء الملف التنفيذي بنجاح!")
except subprocess.CalledProcessError as e:
    print("حدث خطأ أثناء إنشاء الملف التنفيذي:", e)
