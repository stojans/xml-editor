# -*- coding: utf-8 -*-

# pylint: disable=no-member, missing-docstring, old-style-class, attribute-defined-outside-init, unused-argument, too-many-statements, too-many-instance-attributes

import os
from ConfigParser import ConfigParser
import wx
import wx.xrc

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(CURRENT_DIR, 'config.ini')
CFG = ConfigParser()
CFG.read(CONFIG_PATH)


class PrefsDialog(wx.Dialog):
    def __init__(self, parent):

        self.tmp_src_path = ""
        self.tmp_dest_path = ""
        self.tmp_issue_path = ""
        self.tmp_test_report_path = ""

        try:
            self.src_path = CFG.get('DEFAULT', 'SOURCE_FOLDER')
        except:
            self.src_path = CURRENT_DIR
        try:
            self.dest_path = CFG.get('DEFAULT', 'DEST_FOLDER')
        except:
            self.dest_path = CURRENT_DIR
        try:
            self.issue_path = CFG.get('DEFAULT', 'ISSUE_DEST_FOLDER')
        except:
            self.issue_path = CURRENT_DIR
        try:
            self.test_report_path = CFG.get('DEFAULT', 'TEST_REPORT_PATH')
        except:
            self.test_report_path = CURRENT_DIR

        wx.Dialog.__init__(self, parent, id=wx.ID_ANY,
                           title=u"Preferences",
                           pos=wx.DefaultPosition,
                           size=wx.Size(700, 300),
                           style=wx.DEFAULT_DIALOG_STYLE)

        b_sizer1 = wx.BoxSizer(wx.VERTICAL)

        sb_sizer1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                   u"Default Open Location"),
                                      wx.HORIZONTAL)

        self.src_text = wx.StaticText(sb_sizer1.GetStaticBox(),
                                      wx.ID_ANY,
                                      u"{}".format(self.src_path),
                                      wx.DefaultPosition,
                                      wx.DefaultSize,
                                      wx.ST_ELLIPSIZE_MIDDLE)
        self.src_text.Wrap(-1)
        font = wx.Font(8, wx.DEFAULT, wx.FONTSTYLE_SLANT, wx.NORMAL)
        self.src_text.SetFont(font)

        sb_sizer1.Add(self.src_text, 1, wx.ALL | wx.EXPAND, 5)

        self.src_btn = wx.Button(sb_sizer1.GetStaticBox(),
                                 wx.ID_ANY, u"Choose...",
                                 wx.DefaultPosition,
                                 wx.DefaultSize, 0)

        sb_sizer1.Add(self.src_btn, 0,
                      wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT |
                      wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        b_sizer1.Add(sb_sizer1, 0, wx.EXPAND, 5)

        sb_sizer2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                   u"Default Save Location"),
                                      wx.HORIZONTAL)

        self.dest_text = wx.StaticText(sb_sizer2.GetStaticBox(),
                                       wx.ID_ANY,
                                       u"{}".format(self.dest_path),
                                       wx.DefaultPosition,
                                       wx.DefaultSize,
                                       wx.ST_ELLIPSIZE_MIDDLE)

        self.dest_text.Wrap(-1)
        font = wx.Font(8, wx.DEFAULT, wx.FONTSTYLE_SLANT, wx.NORMAL)
        self.dest_text.SetFont(font)

        sb_sizer2.Add(self.dest_text, 1, wx.ALL, 5)

        self.dest_btn = wx.Button(sb_sizer2.GetStaticBox(),
                                  wx.ID_ANY, u"Choose...",
                                  wx.DefaultPosition,
                                  wx.DefaultSize, 0)

        sb_sizer2.Add(self.dest_btn, 0,
                      wx.BOTTOM | wx.RIGHT |
                      wx.LEFT, 5)

        b_sizer1.Add(sb_sizer2, 0, wx.EXPAND, 5)

        sb_sizer4 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                   u"TestReport Directory Path"),
                                      wx.HORIZONTAL)

        self.tr_path_text = wx.StaticText(sb_sizer4.GetStaticBox(),
                                          wx.ID_ANY,
                                          u"{}".format(self.test_report_path),
                                          wx.DefaultPosition,
                                          wx.DefaultSize,
                                          wx.ST_ELLIPSIZE_MIDDLE)
        self.tr_path_text.Wrap(-1)
        font = wx.Font(8, wx.DEFAULT, wx.FONTSTYLE_SLANT, wx.NORMAL)
        self.tr_path_text.SetFont(font)

        sb_sizer4.Add(self.tr_path_text, 1, wx.ALL | wx.EXPAND, 5)

        self.tr_path_btn = wx.Button(sb_sizer4.GetStaticBox(),
                                     wx.ID_ANY, u"Choose...",
                                     wx.DefaultPosition,
                                     wx.DefaultSize, 0)

        sb_sizer4.Add(self.tr_path_btn, 0,
                      wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT |
                      wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        b_sizer1.Add(sb_sizer4, 0, wx.EXPAND, 5)

        sb_sizer3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                   u"Default Issue Generation Location"),
                                      wx.HORIZONTAL)

        self.issue_text = wx.StaticText(sb_sizer3.GetStaticBox(),
                                        wx.ID_ANY,
                                        u"{}".format(self.issue_path),
                                        wx.DefaultPosition,
                                        wx.DefaultSize,
                                        wx.ST_ELLIPSIZE_MIDDLE)

        self.issue_text.Wrap(-1)
        font = wx.Font(8, wx.DEFAULT, wx.FONTSTYLE_SLANT, wx.NORMAL)
        self.issue_text.SetFont(font)

        sb_sizer3.Add(self.issue_text, 1, wx.ALL, 5)

        self.issue_btn = wx.Button(sb_sizer3.GetStaticBox(),
                                   wx.ID_ANY, u"Choose...",
                                   wx.DefaultPosition,
                                   wx.DefaultSize, 0)

        sb_sizer3.Add(self.issue_btn, 0,
                      wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)

        b_sizer1.Add(sb_sizer3, 0, wx.EXPAND, 5)

        b_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        b_sizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.save_btn = wx.Button(self, wx.ID_ANY, u"Save Changes",
                                  wx.DefaultPosition,
                                  wx.DefaultSize, 0)

        b_sizer4.Add(self.save_btn, 1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        b_sizer2.Add(b_sizer4, 1, wx.EXPAND, 5)
        b_sizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.cancel_btn = wx.Button(self, wx.ID_ANY, u"Cancel",
                                    wx.DefaultPosition,
                                    wx.DefaultSize, 0)

        b_sizer6.Add(self.cancel_btn, 1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        b_sizer2.Add(b_sizer6, 1, wx.EXPAND, 5)
        b_sizer1.Add(b_sizer2, 1, wx.EXPAND, 5)

        self.SetSizer(b_sizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        self.src_btn.Bind(wx.EVT_BUTTON, self.src_btn_on_click)
        self.dest_btn.Bind(wx.EVT_BUTTON, self.dest_btn_on_click)
        self.issue_btn.Bind(wx.EVT_BUTTON, self.issue_btn_on_click)
        self.tr_path_btn.Bind(wx.EVT_BUTTON, self.tr_path_btn_on_click)
        self.save_btn.Bind(wx.EVT_BUTTON, self.save_btn_on_click)
        self.cancel_btn.Bind(wx.EVT_BUTTON, self.cancel_btn_on_click)
        self.Bind(wx.EVT_CLOSE, self.on_close)


        self.src_text.SetLabel(self.src_path)
        self.dest_text.SetLabel(self.dest_path)
        self.issue_text.SetLabel(self.issue_path)

    def __del__(self):
        pass

    def src_btn_on_click(self, event):
        print "CHOOSE SOURCE"
        dlg = wx.DirDialog(self, 'Open from...',
                           self.src_path,
                           style=wx.DD_DEFAULT_STYLE)

        if dlg.ShowModal() == wx.ID_OK:
            self.tmp_src_path = dlg.GetPath()
            print "You chose the following folder:"
            print self.tmp_src_path
            self.src_text.SetLabel(self.tmp_src_path)
        dlg.Destroy()

    def dest_btn_on_click(self, event):
        print "CHOOSE DESTINATION"
        dlg = wx.DirDialog(self, 'Save to...',
                           self.dest_path,
                           style=wx.DD_DEFAULT_STYLE)

        if dlg.ShowModal() == wx.ID_OK:
            self.tmp_dest_path = dlg.GetPath()
            print "You chose the following folder:"
            print self.tmp_dest_path
            self.dest_text.SetLabel(self.tmp_dest_path)

        dlg.Destroy()

    def issue_btn_on_click(self, event):
        print "CHOOSE ISSUE"
        dlg = wx.DirDialog(self, 'Choose media directory',
                           self.issue_path,
                           style=wx.DD_DEFAULT_STYLE)

        if dlg.ShowModal() == wx.ID_OK:
            self.tmp_issue_path = dlg.GetPath()
            print "You chose the following folder:"
            print self.tmp_issue_path
            self.issue_text.SetLabel(self.tmp_issue_path)

        dlg.Destroy()

    def tr_path_btn_on_click(self, event):
        print "CHOOSE TR"
        dlg = wx.DirDialog(self, 'Select TestReport directory',
                           self.test_report_path,
                           style=wx.DD_DEFAULT_STYLE)

        if dlg.ShowModal() == wx.ID_OK:
            self.tmp_test_report_path = dlg.GetPath()
            print "You chose the following folder:"
            print self.tmp_test_report_path
            self.tr_path_text.SetLabel(self.tmp_test_report_path)

        dlg.Destroy()

    def save_btn_on_click(self, event):
        self.src_path = self.tmp_src_path
        self.dest_path = self.tmp_dest_path
        self.issue_path = self.tmp_issue_path
        self.test_report_path = self.tmp_test_report_path

        if self.src_path:
            CFG.set('DEFAULT', 'SOURCE_FOLDER', self.src_path)
        if self.dest_path:
            CFG.set('DEFAULT', 'DEST_FOLDER', self.dest_path)
        if self.issue_path:
            CFG.set('DEFAULT', 'ISSUE_DEST_FOLDER', self.issue_path)
        if self.test_report_path:
            CFG.set('DEFAULT', 'TEST_REPORT_PATH', self.test_report_path)

        with open(CONFIG_PATH, 'w') as configfile:
            CFG.write(configfile)

        print "XONF SOURCE PREFS: ", self.src_path
        print "XONF DEST PREFS: ", self.dest_path
        print "XONF ISSUE DEST PREFS: ", self.issue_path
        print "CONF TEST REPORT PATH: ", self.test_report_path

        self.Destroy()

    def cancel_btn_on_click(self, event):
        print "PREFS --> CANCEL"
        self.Destroy()



    def on_close(self, event):
        print "PREFS ON CLOSE"
        self.Destroy()

######################################################


class PDFDialog(wx.Dialog):
    def __init__(self, parent, succ_file_list, fail_file_list, tr_path, file_num):
        wx.Dialog.__init__(self, parent, title="PDF generation results")
        
        if len(succ_file_list) + len(fail_file_list) == file_num:

            self.tr_path = tr_path
            text = "FINISHED ALL FILES\n---------------------------------------------------\n"

        else:
    
            self.tr_path = tr_path
            text = "CANCELLED AFTER " + str(len(succ_file_list) + len(fail_file_list)) + "/" + str(file_num) + " FILES"
            text = text + "\n---------------------------------------------------\n"


        if len(succ_file_list) != 0:
            text = text + "\n" + "SUCCESSFUL (" + str(len(succ_file_list)) + "/" + str(len(succ_file_list) + len(fail_file_list)) + "): " + "\n\n"
            for succ in succ_file_list:
                text = text + succ + "\n"
        else:
            text = text + "\nSUCCESSFUL: NONE"

        if len(fail_file_list) != 0:
            text = text + "\n---------------------------------------------------\n"
            text = text + "\n" + "FAILED (" + str(len(fail_file_list)) + "/" + str(len(succ_file_list) + len(fail_file_list)) + "): " + "\n\n"
            for fail in fail_file_list:
                if fail[1]:
                    if fail == fail_file_list[-1]:
                        text = text + fail[0] + "\nError: " + fail[1]
                    else:
                        text = text + fail[0] + "\nError: " + fail[1] + "\n\n"
                else:
                    text = text + fail[0] + "\n\n"
        else:
            text = text + "\n---------------------------------------------------\n"
            text = text + "\nFAILED: NONE"


#---------------------------------------------


        self.text_disp = wx.TextCtrl(self, -1, text, size=(300,200), style=wx.TE_MULTILINE | wx.TE_READONLY)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL )
        
        self.btnsizer = wx.BoxSizer()

        self.open_folder_btn = wx.Button(self, wx.ID_OPEN)
        self.open_folder_btn.SetLabel("Open Folder")
        self.open_folder_btn.Bind(wx.EVT_BUTTON, self.open_folder_on_click)
        self.btnsizer.Add(self.open_folder_btn, 0, wx.ALL|wx.ALIGN_LEFT, 5)
        self.btnsizer.Add((5,-1), 5, wx.ALL, 5)

        self.ok_btn = wx.Button(self, wx.ID_OK)
        self.ok_btn.SetLabel("OK")
        self.btnsizer.Add(self.ok_btn, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        self.sizer.Add(self.text_disp, 0, wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(self.btnsizer, 0, wx.EXPAND|wx.ALL, 5)    
        self.SetSizerAndFit (self.sizer)

        self.Centre(wx.BOTH)


    def open_folder_on_click(self, event):
        os.system("explorer " + self.tr_path) 
        self.Destroy()
