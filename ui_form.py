# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGraphicsView,
    QKeySequenceEdit, QLCDNumber, QLabel, QLineEdit,
    QProgressBar, QPushButton, QSizePolicy, QTabWidget,
    QTextBrowser, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(800, 600)
        self.tabWidget = QTabWidget(Widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, -1, 801, 601))
        self.MainTab = QWidget()
        self.MainTab.setObjectName(u"MainTab")
        self.DebugWindow = QTextBrowser(self.MainTab)
        self.DebugWindow.setObjectName(u"DebugWindow")
        self.DebugWindow.setGeometry(QRect(490, 40, 256, 481))
        self.label_2 = QLabel(self.MainTab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(490, 10, 201, 21))
        self.Counter = QLCDNumber(self.MainTab)
        self.Counter.setObjectName(u"Counter")
        self.Counter.setGeometry(QRect(680, 530, 64, 31))
        self.label_3 = QLabel(self.MainTab)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(630, 540, 41, 16))
        self.FlashButton = QPushButton(self.MainTab)
        self.FlashButton.setObjectName(u"FlashButton")
        self.FlashButton.setEnabled(True)
        self.FlashButton.setGeometry(QRect(130, 40, 221, 51))
        self.FlashButton.setMouseTracking(False)
        self.FlashButton.setCheckable(False)
        self.FlashButton.setFlat(False)
        self.auto_label = QLabel(self.MainTab)
        self.auto_label.setObjectName(u"auto_label")
        self.auto_label.setEnabled(True)
        self.auto_label.setGeometry(QRect(160, 20, 161, 16))
        self.StatusGraphic = QGraphicsView(self.MainTab)
        self.StatusGraphic.setObjectName(u"StatusGraphic")
        self.StatusGraphic.setGeometry(QRect(130, 150, 221, 201))
        self.FlashProgress = QProgressBar(self.MainTab)
        self.FlashProgress.setObjectName(u"FlashProgress")
        self.FlashProgress.setGeometry(QRect(130, 110, 221, 23))
        self.FlashProgress.setValue(0)
        self.FlashProgress.setInvertedAppearance(False)
        self.tabWidget.addTab(self.MainTab, "")
        self.SettingsTab = QWidget()
        self.SettingsTab.setObjectName(u"SettingsTab")
        self.AutoFlash = QCheckBox(self.SettingsTab)
        self.AutoFlash.setObjectName(u"AutoFlash")
        self.AutoFlash.setEnabled(True)
        self.AutoFlash.setGeometry(QRect(20, 30, 291, 22))
        self.AutoFlash.setCheckable(True)
        self.SetFlashHotkey = QKeySequenceEdit(self.SettingsTab)
        self.SetFlashHotkey.setObjectName(u"SetFlashHotkey")
        self.SetFlashHotkey.setGeometry(QRect(20, 120, 281, 24))
        self.SetFlashHotkey.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.SetFlashHotkey.setClearButtonEnabled(True)
        self.label = QLabel(self.SettingsTab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 100, 161, 16))
        self.FlashChooser = QComboBox(self.SettingsTab)
        self.FlashChooser.addItem("")
        self.FlashChooser.addItem("")
        self.FlashChooser.addItem("")
        self.FlashChooser.setObjectName(u"FlashChooser")
        self.FlashChooser.setGeometry(QRect(20, 190, 101, 21))
        self.label_4 = QLabel(self.SettingsTab)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(20, 170, 161, 16))
        self.MCUPathBox = QLineEdit(self.SettingsTab)
        self.MCUPathBox.setObjectName(u"MCUPathBox")
        self.MCUPathBox.setGeometry(QRect(20, 260, 281, 24))
        self.label_5 = QLabel(self.SettingsTab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 240, 161, 16))
        self.BrowseMCUFile = QPushButton(self.SettingsTab)
        self.BrowseMCUFile.setObjectName(u"BrowseMCUFile")
        self.BrowseMCUFile.setGeometry(QRect(320, 260, 80, 24))
        self.TelitPathBox = QLineEdit(self.SettingsTab)
        self.TelitPathBox.setObjectName(u"TelitPathBox")
        self.TelitPathBox.setGeometry(QRect(20, 330, 281, 24))
        self.BrowseTelitFile = QPushButton(self.SettingsTab)
        self.BrowseTelitFile.setObjectName(u"BrowseTelitFile")
        self.BrowseTelitFile.setGeometry(QRect(320, 330, 80, 24))
        self.label_6 = QLabel(self.SettingsTab)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 310, 161, 16))
        self.BrowserIPECMD = QPushButton(self.SettingsTab)
        self.BrowserIPECMD.setObjectName(u"BrowserIPECMD")
        self.BrowserIPECMD.setGeometry(QRect(320, 400, 80, 24))
        self.IPECMDPathBox = QLineEdit(self.SettingsTab)
        self.IPECMDPathBox.setObjectName(u"IPECMDPathBox")
        self.IPECMDPathBox.setGeometry(QRect(20, 400, 281, 24))
        self.IPECMDPath = QLabel(self.SettingsTab)
        self.IPECMDPath.setObjectName(u"IPECMDPath")
        self.IPECMDPath.setGeometry(QRect(20, 380, 161, 16))
        self.ClearDebug = QCheckBox(self.SettingsTab)
        self.ClearDebug.setObjectName(u"ClearDebug")
        self.ClearDebug.setEnabled(True)
        self.ClearDebug.setGeometry(QRect(20, 60, 291, 22))
        self.ClearDebug.setCheckable(True)
        self.ClearDebug.setChecked(True)
        self.tabWidget.addTab(self.SettingsTab, "")

        self.retranslateUi(Widget)

        self.tabWidget.setCurrentIndex(0)
        self.FlashButton.setDefault(True)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"IRepell Programmer", None))
        self.DebugWindow.setHtml(QCoreApplication.translate("Widget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Widget", u"Debug Fenster", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"Z\u00e4hler", None))
        self.FlashButton.setText(QCoreApplication.translate("Widget", u"Programmieren", None))
        self.auto_label.setText(QCoreApplication.translate("Widget", u"Wird automatisch  ausgef\u00fchrt", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.MainTab), QCoreApplication.translate("Widget", u"Flashing", None))
        self.AutoFlash.setText(QCoreApplication.translate("Widget", u"Automatisches Flashing beim einlegen der Platine", None))
        self.label.setText(QCoreApplication.translate("Widget", u"Hotkey f\u00fcr Flashing", None))
        self.FlashChooser.setItemText(0, QCoreApplication.translate("Widget", u"Beide", None))
        self.FlashChooser.setItemText(1, QCoreApplication.translate("Widget", u"Nur MCU", None))
        self.FlashChooser.setItemText(2, QCoreApplication.translate("Widget", u"Nur Telit", None))

        self.label_4.setText(QCoreApplication.translate("Widget", u"Was wird geflasht?", None))
        self.label_5.setText(QCoreApplication.translate("Widget", u"MCU Hex Datei", None))
        self.BrowseMCUFile.setText(QCoreApplication.translate("Widget", u"Durchsuchen", None))
        self.BrowseTelitFile.setText(QCoreApplication.translate("Widget", u"Durchsuchen", None))
        self.label_6.setText(QCoreApplication.translate("Widget", u"Telit Bin Datei", None))
        self.BrowserIPECMD.setText(QCoreApplication.translate("Widget", u"Durchsuchen", None))
        self.IPECMDPath.setText(QCoreApplication.translate("Widget", u"IPECMD Pfad", None))
        self.ClearDebug.setText(QCoreApplication.translate("Widget", u"L\u00f6schen des Output Fensters vor jedem Flash", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SettingsTab), QCoreApplication.translate("Widget", u"Einstellungen", None))
    # retranslateUi

