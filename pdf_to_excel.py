import pdfplumber
import pandas as pd
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
from tkinter import filedialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel

import os

# دالة لتحديد مسار الملف
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):  # إذا كان يعمل كملف تنفيذي
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# تحميل ملف التصميم
ui, _ = loadUiType(resource_path('design.ui'))



# تحميل الواجهة
#ui, _ = loadUiType('design.ui')

class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.setupUi(self)
        self.Handle_Buttons()
        self.progressBar.setValue(0)

    def Handle_Buttons(self):
        # ربط الزر بالدالة مع تأجيل استدعاء الدالة
        self.pushButton.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
    
        # فتح مربع حوار لاختيار ملف PDF
        pdf_path, _ = QFileDialog.getOpenFileName(self, "اختيار ملف PDF", "", "PDF Files (*.pdf)")
        if pdf_path:
            # تحديد مسار لحفظ الملف Excel
            excel_path, _ = QFileDialog.getSaveFileName(self, "حفظ كـ Excel", "", "Excel Files (*.xlsx)")
            if excel_path:
                self.pdf_to_excel(pdf_path, excel_path)

    # دالة لاستخراج النص من PDF وتحويله إلى جدول
    def pdf_to_excel(self, pdf_path, excel_path):
        try:
            self.progressBar.setValue(0)
            with pdfplumber.open(pdf_path) as pdf:
                all_text = []

                # استعراض جميع الصفحات في PDF واستخراج النصوص منها
                for page in pdf.pages:

                    # استخراج النصوص على شكل جدول
                    table = page.extract_table()
                    if table:
                        for row in table:
                            all_text.append(row)

            # تحويل النصوص المستخرجة إلى DataFrame باستخدام pandas
            df = pd.DataFrame(all_text[1:], columns=all_text[0])  # استخدام السطر الأول كعناوين للأعمدة

            # تصدير البيانات إلى ملف Excel
            df.to_excel(excel_path, index=False, engine='openpyxl')

            print(f"تم تحويل ملف PDF إلى Excel بنجاح! الملف تم حفظه في {excel_path}")
            
            self.label_result.setText('تم التحويل بنجاح')
            self.progressBar.setValue(100)
            QMessageBox.information(self, "Download Completed", "تم التحويل بنجاح ")
        except Exception as e:
            print(f"حدث خطأ: {e}")
            self.label_result.setText('حدث خطا   ')
            self.progressBar.setValue(0)

        #==================================
    def Handle_Progress(self, blocknum, blockSize, totalSize):
        read = blocknum * blockSize
        if totalSize>0:
            percent = read * 100 / totalSize
            self.progressBar.setValue(int(percent))
            QApplication.processEvents()
    #=====================================



    #==============
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # حلقة التطبيق لا تنتهي

if __name__ == '__main__':
    main()
