# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/builds/clients/python/sakia/src/sakia/gui/main_window/toolbar/toolbar.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SakiaToolbar(object):
    def setupUi(self, SakiaToolbar):
        SakiaToolbar.setObjectName("SakiaToolbar")
        SakiaToolbar.resize(1000, 241)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SakiaToolbar.sizePolicy().hasHeightForWidth())
        SakiaToolbar.setSizePolicy(sizePolicy)
        SakiaToolbar.setMaximumSize(QtCore.QSize(1000, 16777215))
        SakiaToolbar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        SakiaToolbar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout = QtWidgets.QHBoxLayout(SakiaToolbar)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_network = QtWidgets.QPushButton(SakiaToolbar)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/wot_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_network.setIcon(icon)
        self.button_network.setIconSize(QtCore.QSize(32, 32))
        self.button_network.setObjectName("button_network")
        self.horizontalLayout.addWidget(self.button_network)
        self.button_identity = QtWidgets.QPushButton(SakiaToolbar)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/explorer_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_identity.setIcon(icon1)
        self.button_identity.setIconSize(QtCore.QSize(32, 32))
        self.button_identity.setObjectName("button_identity")
        self.horizontalLayout.addWidget(self.button_identity)
        spacerItem = QtWidgets.QSpacerItem(200, 221, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_contacts = QtWidgets.QPushButton(SakiaToolbar)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/connect_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_contacts.setIcon(icon2)
        self.button_contacts.setIconSize(QtCore.QSize(32, 32))
        self.button_contacts.setObjectName("button_contacts")
        self.horizontalLayout.addWidget(self.button_contacts)
        self.toolbutton_menu = QtWidgets.QToolButton(SakiaToolbar)
        self.toolbutton_menu.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/menu_icon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolbutton_menu.setIcon(icon3)
        self.toolbutton_menu.setIconSize(QtCore.QSize(32, 32))
        self.toolbutton_menu.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolbutton_menu.setAutoRaise(False)
        self.toolbutton_menu.setArrowType(QtCore.Qt.NoArrow)
        self.toolbutton_menu.setObjectName("toolbutton_menu")
        self.horizontalLayout.addWidget(self.toolbutton_menu)
        self.label = QtWidgets.QLabel(SakiaToolbar)
        self.label.setMaximumSize(QtCore.QSize(40, 40))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icons/sakia_logo"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(SakiaToolbar)
        QtCore.QMetaObject.connectSlotsByName(SakiaToolbar)

    def retranslateUi(self, SakiaToolbar):
        _translate = QtCore.QCoreApplication.translate
        SakiaToolbar.setWindowTitle(_translate("SakiaToolbar", "Frame"))
        self.button_network.setText(_translate("SakiaToolbar", "Network"))
        self.button_identity.setText(_translate("SakiaToolbar", "Search an identity"))
        self.button_contacts.setText(_translate("SakiaToolbar", "Contacts"))

import sakia.icons_rc
