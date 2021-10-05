# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_v02.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(535, 755)
        self.solution_select_group = QGroupBox(Dialog)
        self.solution_select_group.setObjectName(u"solution_select_group")
        self.solution_select_group.setGeometry(QRect(20, 10, 491, 201))
        font = QFont()
        font.setBold(True)
        self.solution_select_group.setFont(font)
        self.verticalLayoutWidget = QWidget(self.solution_select_group)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(129, 19, 351, 171))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.project_name_input = QComboBox(self.verticalLayoutWidget)
        self.project_name_input.setObjectName(u"project_name_input")

        self.verticalLayout.addWidget(self.project_name_input)

        self.design_name_input = QComboBox(self.verticalLayoutWidget)
        self.design_name_input.setObjectName(u"design_name_input")

        self.verticalLayout.addWidget(self.design_name_input)

        self.solution_setup_input = QComboBox(self.verticalLayoutWidget)
        self.solution_setup_input.setObjectName(u"solution_setup_input")

        self.verticalLayout.addWidget(self.solution_setup_input)

        self.variation_input = QComboBox(self.verticalLayoutWidget)
        self.variation_input.addItem("")
        self.variation_input.setObjectName(u"variation_input")

        self.verticalLayout.addWidget(self.variation_input)

        self.freq_input = QComboBox(self.verticalLayoutWidget)
        self.freq_input.setObjectName(u"freq_input")

        self.verticalLayout.addWidget(self.freq_input)

        self.verticalLayoutWidget_2 = QWidget(self.solution_select_group)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 19, 111, 161))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"Arial"])
        font1.setPointSize(10)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.label)

        self.label_2 = QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.label_3)

        self.label_11 = QLabel(self.verticalLayoutWidget_2)
        self.label_11.setObjectName(u"label_11")
        font2 = QFont()
        font2.setFamilies([u"Arial"])
        font2.setPointSize(10)
        self.label_11.setFont(font2)
        self.label_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.label_11)

        self.label_4 = QLabel(self.verticalLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_2.addWidget(self.label_4)

        self.pd_setup_group = QGroupBox(Dialog)
        self.pd_setup_group.setObjectName(u"pd_setup_group")
        self.pd_setup_group.setGeometry(QRect(20, 280, 491, 201))
        self.pd_setup_group.setFont(font)
        self.verticalLayoutWidget_3 = QWidget(self.pd_setup_group)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(209, 19, 271, 171))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.eval_surf_input = QComboBox(self.verticalLayoutWidget_3)
        self.eval_surf_input.setObjectName(u"eval_surf_input")

        self.verticalLayout_3.addWidget(self.eval_surf_input)

        self.pd_area_input = QComboBox(self.verticalLayoutWidget_3)
        self.pd_area_input.addItem("")
        self.pd_area_input.addItem("")
        self.pd_area_input.addItem("")
        self.pd_area_input.setObjectName(u"pd_area_input")

        self.verticalLayout_3.addWidget(self.pd_area_input)

        self.pd_type_input = QComboBox(self.verticalLayoutWidget_3)
        self.pd_type_input.addItem("")
        self.pd_type_input.addItem("")
        self.pd_type_input.addItem("")
        self.pd_type_input.setObjectName(u"pd_type_input")

        self.verticalLayout_3.addWidget(self.pd_type_input)

        self.pd_renorm_input = QComboBox(self.verticalLayoutWidget_3)
        self.pd_renorm_input.addItem("")
        self.pd_renorm_input.addItem("")
        self.pd_renorm_input.addItem("")
        self.pd_renorm_input.setObjectName(u"pd_renorm_input")

        self.verticalLayout_3.addWidget(self.pd_renorm_input)

        self.verticalLayoutWidget_4 = QWidget(self.pd_setup_group)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 20, 190, 161))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.verticalLayoutWidget_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_4.addWidget(self.label_7)

        self.label_5 = QLabel(self.verticalLayoutWidget_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_4.addWidget(self.label_5)

        self.label_6 = QLabel(self.verticalLayoutWidget_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_4.addWidget(self.label_6)

        self.label_9 = QLabel(self.verticalLayoutWidget_4)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font1)
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_4.addWidget(self.label_9)

        self.multi_run_checkbox = QCheckBox(Dialog)
        self.multi_run_checkbox.setObjectName(u"multi_run_checkbox")
        self.multi_run_checkbox.setGeometry(QRect(70, 670, 111, 20))
        self.codebook_group = QGroupBox(Dialog)
        self.codebook_group.setObjectName(u"codebook_group")
        self.codebook_group.setGeometry(QRect(20, 220, 491, 51))
        self.codebook_group.setFont(font)
        self.codebook_text = QLineEdit(self.codebook_group)
        self.codebook_text.setObjectName(u"codebook_text")
        self.codebook_text.setGeometry(QRect(60, 20, 421, 22))
        self.codebook_browse = QToolButton(self.codebook_group)
        self.codebook_browse.setObjectName(u"codebook_browse")
        self.codebook_browse.setGeometry(QRect(20, 20, 27, 22))
        self.multirun_group = QGroupBox(Dialog)
        self.multirun_group.setObjectName(u"multirun_group")
        self.multirun_group.setEnabled(False)
        self.multirun_group.setGeometry(QRect(170, 650, 341, 51))
        self.multi_run_browse = QToolButton(self.multirun_group)
        self.multi_run_browse.setObjectName(u"multi_run_browse")
        self.multi_run_browse.setGeometry(QRect(20, 20, 27, 22))
        self.multi_run_text = QLineEdit(self.multirun_group)
        self.multi_run_text.setObjectName(u"multi_run_text")
        self.multi_run_text.setEnabled(False)
        self.multi_run_text.setGeometry(QRect(50, 20, 281, 22))
        self.output_group = QGroupBox(Dialog)
        self.output_group.setObjectName(u"output_group")
        self.output_group.setGeometry(QRect(20, 590, 491, 51))
        self.output_group.setFont(font)
        self.output_browse = QToolButton(self.output_group)
        self.output_browse.setObjectName(u"output_browse")
        self.output_browse.setGeometry(QRect(20, 20, 27, 22))
        self.output_text_path = QLineEdit(self.output_group)
        self.output_text_path.setObjectName(u"output_text_path")
        self.output_text_path.setGeometry(QRect(60, 20, 421, 22))
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 490, 491, 91))
        self.groupBox.setFont(font)
        self.cs_input = QComboBox(self.groupBox)
        self.cs_input.addItem("")
        self.cs_input.setObjectName(u"cs_input")
        self.cs_input.setGeometry(QRect(210, 20, 271, 22))
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(70, 20, 131, 21))
        self.label_8.setFont(font1)
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.cdf_renorm_input = QComboBox(self.groupBox)
        self.cdf_renorm_input.addItem("")
        self.cdf_renorm_input.addItem("")
        self.cdf_renorm_input.setObjectName(u"cdf_renorm_input")
        self.cdf_renorm_input.setGeometry(QRect(210, 60, 171, 22))
        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(90, 60, 111, 21))
        self.label_10.setFont(font1)
        self.cdf_dblin_input = QComboBox(self.groupBox)
        self.cdf_dblin_input.addItem("")
        self.cdf_dblin_input.addItem("")
        self.cdf_dblin_input.setObjectName(u"cdf_dblin_input")
        self.cdf_dblin_input.setGeometry(QRect(390, 60, 91, 22))
        self.calculate_pd = QPushButton(Dialog)
        self.calculate_pd.setObjectName(u"calculate_pd")
        self.calculate_pd.setGeometry(QRect(360, 720, 151, 24))
        self.calculate_cdf = QPushButton(Dialog)
        self.calculate_cdf.setObjectName(u"calculate_cdf")
        self.calculate_cdf.setGeometry(QRect(190, 720, 151, 24))
        self.validation_button = QCommandLinkButton(Dialog)
        self.validation_button.setObjectName(u"validation_button")
        self.validation_button.setGeometry(QRect(30, 710, 131, 41))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(9)
        self.validation_button.setFont(font3)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.solution_select_group.setTitle(QCoreApplication.translate("Dialog", u"Solution Select", None))
        self.variation_input.setItemText(0, QCoreApplication.translate("Dialog", u"Nominal", None))

#if QT_CONFIG(tooltip)
        self.variation_input.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:600;\">Variation:</span> Design variation to be used for calculation. Nominal is the current design variation set in the interface. When selecting a different variation, the design will be set to this design variation when selected.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Dialog", u"Project Name:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Design Name:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Solution Setup:", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Variation:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Frequency:", None))
        self.pd_setup_group.setTitle(QCoreApplication.translate("Dialog", u"PD Setup", None))
        self.pd_area_input.setItemText(0, QCoreApplication.translate("Dialog", u"1cm^2", None))
        self.pd_area_input.setItemText(1, QCoreApplication.translate("Dialog", u"4cm^2", None))
        self.pd_area_input.setItemText(2, QCoreApplication.translate("Dialog", u"Custom...", None))

        self.pd_type_input.setItemText(0, QCoreApplication.translate("Dialog", u"PD_n+", None))
        self.pd_type_input.setItemText(1, QCoreApplication.translate("Dialog", u"PD_tot+", None))
        self.pd_type_input.setItemText(2, QCoreApplication.translate("Dialog", u"PD_mod+", None))

        self.pd_renorm_input.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))
        self.pd_renorm_input.setItemText(1, QCoreApplication.translate("Dialog", u"1W", None))
        self.pd_renorm_input.setItemText(2, QCoreApplication.translate("Dialog", u"Custom...", None))

#if QT_CONFIG(tooltip)
        self.pd_renorm_input.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:600;\">Power renormalization:</span> Scaleling of Poynting Vector used for PD Calculations</p><p><span style=\" font-weight:600;\">None:</span> No renormilization of PD will be applied, total radiated power is determined by values used in codebook</p><p><span style=\" font-weight:600;\">1W:</span> All beams will be renormalized to 1W of radiated power. Poynting vector is scaled by 1/ (Original Radiated Power ) for each beam. </p><p><span style=\" font-weight:600;\">Custom</span>: User specified rescalling in Watts. Entry can be a single value, or a series of values seperated by comma's. If a series of values is used, the number of values should equal the number of beam IDs in the codebook. All values are assumed to be in units of W when a custom value is used. An example entry for series of value for a codebook with 5 beams would be <span style=\" font-style:italic;\">1,2,3,4,5. </span>This would be equal to renormalizing beam 1 to 1W, beam 2 to 2W...etc.</p></b"
                        "ody></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Evaluation Surface:", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"PD Averaging Area:", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"PD Type:", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Power Renormalization:", None))
#if QT_CONFIG(tooltip)
        self.multi_run_checkbox.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:600;\">Use Multi-Run:</span> Compute CDF or PD over multiple setups. The setups are to be defined in a seperate .csv file, where each column of the csv file will represent the user selections in this GUI and each row (refered to as a job) will be a seperate computation. This will allow one to automate PD or CDF over many different surfaces, frequencies, PD types, averaging areas and projects/designs. For CDF, it will also compute the CDF for each individual job and the overall CDF across all jobs. This would allow multiple projects/designs to be used for a single CDF calculation.</p><p><span style=\" font-weight:600;\">Note: </span>Only the nominal design variation can be run using multi-run setup</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.multi_run_checkbox.setText(QCoreApplication.translate("Dialog", u"Use Multi-Run", None))
        self.codebook_group.setTitle(QCoreApplication.translate("Dialog", u"Codebook", None))
        self.codebook_browse.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.multirun_group.setTitle(QCoreApplication.translate("Dialog", u"Multi-Run", None))
        self.multi_run_browse.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.output_group.setTitle(QCoreApplication.translate("Dialog", u"Output Directory", None))
#if QT_CONFIG(tooltip)
        self.output_browse.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Browse to output directory location. The default location is ./output/, which is relative to the location of the wizard.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.output_browse.setText(QCoreApplication.translate("Dialog", u"...", None))
#if QT_CONFIG(tooltip)
        self.output_text_path.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Save results to this directory. A sub-directory with the date/time will be created to prevent previous results from being overwritten.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"CDF Setup", None))
        self.cs_input.setItemText(0, QCoreApplication.translate("Dialog", u"Global", None))

#if QT_CONFIG(tooltip)
        self.cs_input.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Coordinate System: The CS defines the orientation where the far field pattern will be computed relative to. This needs to be defined in your HFSS design before starting the wizard</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Coordinate System:", None))
        self.cdf_renorm_input.setItemText(0, QCoreApplication.translate("Dialog", u"None", None))
        self.cdf_renorm_input.setItemText(1, QCoreApplication.translate("Dialog", u"Custom...", None))

#if QT_CONFIG(tooltip)
        self.cdf_renorm_input.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:600;\">Renormalization:</span></p><p>CDF can be renormalied to a peak EIRP value. The value entered here will be use to renormalized the peak CDF value (100th percentile). When renormalization is selected, the CDF report will be generated for both the original data and the renormalized data.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Renormalization:", None))
        self.cdf_dblin_input.setItemText(0, QCoreApplication.translate("Dialog", u"dB", None))
        self.cdf_dblin_input.setItemText(1, QCoreApplication.translate("Dialog", u"Linear", None))

#if QT_CONFIG(tooltip)
        self.cdf_dblin_input.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>The renormalization value can be defined in dB or linear scale. This is the peak value to renoarmalize CDF to. </p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.calculate_pd.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:600;\">Calculate PD:</span>  computes power density, both averaged and localized for each beam ID</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.calculate_pd.setText(QCoreApplication.translate("Dialog", u"Calculate PD", None))
#if QT_CONFIG(tooltip)
        self.calculate_cdf.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Calculate CDF: computes the cumulative distributtion function of multiple beams</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.calculate_cdf.setText(QCoreApplication.translate("Dialog", u"Calculate CDF", None))
#if QT_CONFIG(tooltip)
        self.validation_button.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:600;\">Run Validation</span>: Perform validation of algorithms used in the 5G wizard with results provided in the reference data set. The reference data set includes local PD, PD_N_Plus, PD_Mod_Plus and PLD_Tot_plus on a 10cm x 10cm grid, with 2mm spacing. Averaged values are perfromed using 1cm^2 and 4cm^2. Using the local PD reference data, the validation performed here will first calculate  PD_N/Mod/Tot_Plus and compare the results with the provided reference data for local evalulation of each quantity. Using the local PD_N/Mod/Tot_Plus results, it will perform averaging process as desribed in the standard and compare the results with the provied rerference data for the averaged quanitites. The results will be be displayed. Results can be used to demonstrate the 5G wizard conforms to the standard requirments for PD quantities and averaging algorithms. </p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.validation_button.setText(QCoreApplication.translate("Dialog", u"Run Validation", None))
    # retranslateUi

