# -*- coding: utf-8 -*-

# pylint: disable=no-member, missing-docstring, old-style-class, attribute-defined-outside-init, too-many-nested-blocks, too-many-statements, bare-except, too-many-branches, too-many-instance-attributes, too-many-boolean-expressions, too-many-locals, too-many-lines, too-many-public-methods, global-statement, no-self-use, relative-import, redefined-outer-name, invalid-name

import os
import json
import xmltodict
import wx
import wx.adv
import wx.lib.scrolledpanel as scroll
import wx.lib.inspection
import datetime
from jinja2.environment import Environment
from jinja2.loaders import FileSystemLoader
import pdf_exporter
import classes
import create_issue_list
from ConfigParser import ConfigParser
from dialogs import PrefsDialog
from dialogs import PDFDialog

#----------------------------------------------------------------------------------------------------------
import threading
import thread
import time
from wx.lib.expando import ExpandoTextCtrl, EVT_ETC_LAYOUT_NEEDED
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


appname = "XML Editor"
filename = "Untitled"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(CURRENT_DIR, 'icons', 'main.ico')
TEMPLATE_PATH = os.path.join(CURRENT_DIR, 'templates')
BLANK_TEMPLATE = os.path.join(CURRENT_DIR, 'templates', 'xml_blank.template')
CONFIG_PATH = os.path.join(CURRENT_DIR, 'config.ini')

tag_dict = {}
wgt_dict = {}
tc_list = []
sup_ta_list = []
int_ta_list = []
rev_list = []
acr_list = []
ref_list = []
add_tool_list = []
add_data_list = []
limit_list = []
tct_list = []

icon_normal = wx.TreeItemIcon_Normal
icon_exp = wx.TreeItemIcon_Expanded
ap = wx.ArtProvider


release_data = classes.ReleaseData()
swc_data = classes.SWCData()
swc_row = classes.SWC()

myEVT_COUNT = wx.NewEventType()
EVT_COUNT = wx.PyEventBinder(myEVT_COUNT, 1)

class MyFrame(wx.Frame):

    def __init__(self, parent):

        scr_width = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        scr_height = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
        self.file_modified = 0
        self.stopped = False

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=appname,
                          pos=wx.DefaultPosition,
                          size=wx.Size(scr_width/2,
                                       (scr_height/2 + 100)),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(scr_width/2, scr_height/2), wx.Size(-1, -1))

        self.Centre(wx.BOTH)

        self.b_sizer_all = wx.BoxSizer(wx.HORIZONTAL)

        self.spl_vert = wx.SplitterWindow(self, wx.ID_ANY,
                                          wx.DefaultPosition,
                                          wx.DefaultSize,
                                          wx.SP_3D | wx.SP_3DBORDER |
                                          wx.SP_3DSASH | wx.SP_BORDER |
                                          wx.SP_LIVE_UPDATE)

        clr_window = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        clr_menu = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU)

        self.spl_vert.SetSashGravity(0)
        self.spl_vert.SetSashSize(10)
        self.spl_vert.SetMinimumPaneSize(300)

        self.panel_left = wx.Panel(self.spl_vert, wx.ID_ANY,
                                   wx.DefaultPosition,
                                   wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)

        self.b_sizer_tree = wx.BoxSizer(wx.VERTICAL)

        self.tree = wx.TreeCtrl(self.panel_left, wx.ID_ANY,
                                wx.DefaultPosition,
                                wx.DefaultSize,
                                wx.TR_HAS_BUTTONS |
                                wx.TR_TWIST_BUTTONS |
                                wx.TR_FULL_ROW_HIGHLIGHT)

        self.tree.Bind(wx.EVT_ENTER_WINDOW, self.on_mouse_enter)

        self.search = wx.SearchCtrl(self.panel_left,
                                    wx.ID_ANY,
                                    wx.EmptyString,
                                    wx.DefaultPosition,
                                    wx.Size(-1, -1),
                                    wx.TE_PROCESS_ENTER)

        self.search.ShowSearchButton(True)

        self.search.SetDescriptiveText("Search TestCase...")

        self.Bind(wx.EVT_TEXT_ENTER, self.on_search, self.search)

        self.b_sizer_tree.Add(self.search, 0,
                              wx.EXPAND | wx.TOP | wx.BOTTOM, 2)

        self.b_sizer_tree.Add(self.tree, 1, wx.EXPAND | wx.BOTTOM, 2)

        self.search.Hide()

        self.panel_left.SetSizer(self.b_sizer_tree)
        self.panel_left.Layout()
        self.b_sizer_tree.Fit(self.panel_left)
        self.panel_right = wx.Panel(self.spl_vert, wx.ID_ANY,
                                    wx.DefaultPosition,
                                    wx.DefaultSize,
                                    wx.TAB_TRAVERSAL)

        self.b_sizer_spl = wx.BoxSizer(wx.VERTICAL)

        self.spl_horiz = wx.SplitterWindow(self.panel_right, wx.ID_ANY,
                                           wx.DefaultPosition,
                                           wx.DefaultSize,
                                           wx.SP_3D | wx.SP_3DBORDER |
                                           wx.SP_3DSASH | wx.SP_BORDER |
                                           wx.SP_LIVE_UPDATE)

        self.spl_horiz.SetSashGravity(1)
        self.spl_horiz.SetSashSize(5)
        self.spl_horiz.SetMinimumPaneSize(50)

        self.spl_horiz.SetForegroundColour(clr_window)
        self.spl_horiz.SetBackgroundColour(clr_window)

        self.panel_text = wx.Panel(self.spl_horiz, wx.ID_ANY,
                                   wx.DefaultPosition,
                                   wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)

        self.b_sizer_nb = wx.BoxSizer(wx.VERTICAL)

        self.tab_parsed = scroll.ScrolledPanel(self.panel_text, wx.ID_ANY,
                                               wx.DefaultPosition,
                                               wx.DefaultSize,
                                               wx.TAB_TRAVERSAL)

        self.tab_parsed.Bind(wx.EVT_ENTER_WINDOW, self.on_mouse_enter)
        self.tab_parsed.Bind(wx.EVT_LEAVE_WINDOW, self.on_mouse_leave)

        self.b_sizer_parsed = wx.BoxSizer(wx.VERTICAL)

        self.tab_parsed.SetSizer(self.b_sizer_parsed)

        self.tab_parsed.Layout()
        self.b_sizer_parsed.Fit(self.tab_parsed)

        self.b_sizer_nb.Add(self.tab_parsed, 1, wx.EXPAND, 2)

        self.panel_text.SetSizer(self.b_sizer_nb)
        self.panel_text.Layout()
        self.b_sizer_nb.Fit(self.panel_text)
        self.panel_desc = wx.Panel(self.spl_horiz, wx.ID_ANY,
                                   wx.DefaultPosition,
                                   wx.DefaultSize,
                                   wx.TAB_TRAVERSAL)
        self.panel_desc.Bind(wx.EVT_ENTER_WINDOW, self.on_mouse_enter)
        self.panel_desc.Bind(wx.EVT_LEAVE_WINDOW, self.on_mouse_leave)

        self.b_sizer_desc = wx.BoxSizer(wx.VERTICAL)

        self.desc_text = wx.StaticText(self.panel_desc, wx.ID_ANY, u"",
                                       wx.DefaultPosition, wx.DefaultSize,
                                       wx.ST_NO_AUTORESIZE | wx.STATIC_BORDER)

        self.desc_text.Wrap(-1)
        self.desc_text.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(), 70, 90,
                                       92, False, wx.EmptyString))

        light_col = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT)
        btn_text_col = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT)
        self.desc_text.SetBackgroundColour(light_col)

        self.b_sizer_desc.Add(self.desc_text, 1, wx.EXPAND, 1)

        self.status_text = self.CreateStatusBar(3)
        self.status_text.SetStatusWidths([-5, -2, -2])
        self.status_text.SetForegroundColour(btn_text_col)
        self.status_text.SetBackgroundColour(light_col)
        self.status_text.SetBackgroundColour(clr_menu)



        self.desc_text.SetBackgroundColour(clr_menu)
        self.desc_text.SetFont(wx.Font(wx.NORMAL_FONT.GetPointSize(),
                                       70, 90, 92, False, wx.EmptyString))

        self.desc_text.Wrap(-1)

        self.panel_desc.SetSizer(self.b_sizer_desc)
        self.panel_desc.Layout()
        self.b_sizer_desc.Fit(self.panel_desc)
        self.spl_horiz.SplitHorizontally(self.panel_text,
                                         self.panel_desc, -50)

        self.b_sizer_spl.Add(self.spl_horiz, 1, wx.EXPAND, 5)

        self.panel_right.SetSizer(self.b_sizer_spl)
        self.panel_right.Layout()
        self.b_sizer_spl.Fit(self.panel_right)
        self.spl_vert.SplitVertically(self.panel_left,
                                      self.panel_right, 310)

        self.b_sizer_all.Add(self.spl_vert, 1, wx.EXPAND, 2)

        self.SetSizer(self.b_sizer_all)
        self.Layout()
        self.menubar = wx.MenuBar(0)

        ID_NEW = wx.NewId()
        ID_OPEN = wx.NewId()
        ID_SAVE = wx.NewId()
        ID_SAVE_AS = wx.NewId()
        ID_SEARCH = wx.NewId()
        ID_ADD = wx.NewId()
        ID_DELETE = wx.NewId()
        ID_OPTIONS = wx.NewId()
        ID_ISSUES = wx.NewId()
        ID_HELP = wx.NewId()
        ID_EXIT = wx.NewId()
        self.ID_EXPORT = wx.NewId()
        self.ID_EXPORT_ALL = wx.NewId()

        self.file_menu = wx.Menu()
        self.file_new = wx.MenuItem(self.file_menu, ID_NEW,
                                    "New" + "\t" + "Ctrl+N",
                                    wx.EmptyString, wx.ITEM_NORMAL)

        self.file_menu.Append(self.file_new)

        self.file_open = wx.MenuItem(self.file_menu, ID_OPEN,
                                     "Open" + "\t" + "Ctrl+O",
                                     wx.EmptyString, wx.ITEM_NORMAL)

        self.file_menu.Append(self.file_open)

        self.file_save = wx.MenuItem(self.file_menu, ID_SAVE,
                                     "Save" + "\t" + "Ctrl+S",
                                     wx.EmptyString, wx.ITEM_NORMAL)

        self.file_menu.Append(self.file_save)

        self.file_save_as = wx.MenuItem(self.file_menu, ID_SAVE_AS,
                                        "Save As..." + "\t" + "Ctrl+Shift+S",
                                        wx.EmptyString, wx.ITEM_NORMAL)

        self.file_menu.Append(self.file_save_as)

        self.file_menu.AppendSeparator()

        self.file_create_issues = wx.MenuItem(self.file_menu, ID_ISSUES,
                                              "Create Issues" +
                                              "\t" + "Ctrl+I",
                                              wx.EmptyString,
                                              wx.ITEM_NORMAL)

        self.file_menu.Append(self.file_create_issues)

        self.file_export_pdf = wx.MenuItem(self.file_menu,  self.ID_EXPORT,
                                           "Export file to PDF" +
                                           "\t" + "Ctrl+E",
                                           wx.EmptyString,
                                           wx.ITEM_NORMAL)

        self.file_menu.Append(self.file_export_pdf)

        self.file_export_pdf_all = wx.MenuItem(self.file_menu,
                                               self.ID_EXPORT_ALL,
                                               "Export all files to PDF" +
                                               "\t" + "Ctrl+Shift+E",
                                               wx.EmptyString,
                                               wx.ITEM_NORMAL)

        self.file_menu.Append(self.file_export_pdf_all)

        self.file_menu.AppendSeparator()
        self.file_exit = wx.MenuItem(self.file_menu, ID_EXIT,
                                     "Exit" + "\t" + "Alt+F4",
                                     wx.EmptyString, wx.ITEM_NORMAL)

        self.file_menu.Append(self.file_exit)

        self.menubar.Append(self.file_menu, "File")

        self.edit_menu = wx.Menu()
        self.menu_item_edit_search = wx.MenuItem(self.edit_menu, ID_SEARCH,
                                                 "Search" + "\t" + "Ctrl+F",
                                                 wx.EmptyString,
                                                 wx.ITEM_NORMAL)

        self.edit_menu.Append(self.menu_item_edit_search)

        self.edit_menu.AppendSeparator()
        self.menu_item_edit_add = wx.MenuItem(self.edit_menu, ID_ADD,
                                              "Add Child",
                                              wx.EmptyString, wx.ITEM_NORMAL)

        self.edit_menu.Append(self.menu_item_edit_add)
        self.menu_item_edit_delete = wx.MenuItem(self.edit_menu, ID_DELETE,
                                                 "Delete", wx.EmptyString,
                                                 wx.ITEM_NORMAL)

        self.edit_menu.Append(self.menu_item_edit_delete)
        self.menubar.Append(self.edit_menu, "Edit")

        self.options_menu = wx.Menu()
        self.menu_item_options_pref = wx.MenuItem(self.options_menu,
                                                  ID_OPTIONS,
                                                  "Preferences" +
                                                  "\t" + "Ctrl+P",
                                                  wx.EmptyString,
                                                  wx.ITEM_NORMAL)

        self.options_menu.Append(self.menu_item_options_pref)
        self.menubar.Append(self.options_menu, "Options")

        self.help_menu = wx.Menu()
        self.menu_item_help = wx.MenuItem(self.help_menu, ID_HELP,
                                          "About" + "\t" + "F1",
                                          wx.EmptyString, wx.ITEM_NORMAL)

        self.help_menu.Append(self.menu_item_help)
        self.menubar.Append(self.help_menu, "Help")

        self.SetMenuBar(self.menubar)

        entry_one = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('N'),
                                        ID_NEW,
                                        self.file_new)
        entry_two = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('S'),
                                        ID_SAVE,
                                        self.file_save)
        entry_three = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('O'),
                                          ID_OPEN,
                                          self.file_open)
        entry_four = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('S'),
                                         ID_SAVE,
                                         self.file_save)
        entry_five = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('P'),
                                         ID_OPTIONS,
                                         self.menu_item_help)
        entry_six = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('I'),
                                        ID_ISSUES,
                                        self.file_create_issues)
        entry_seven = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('E'),
                                          self.ID_EXPORT,
                                          self.file_export_pdf)
        entry_eight = wx.AcceleratorEntry((wx.ACCEL_CTRL or wx.ACCEL_SHIFT),
                                          ord('E'),
                                          self.ID_EXPORT,
                                          self.file_export_pdf_all)

        entries = [entry_one, entry_two, entry_three, entry_four,
                   entry_five, entry_six, entry_seven, entry_eight]

        accel_tbl = wx.AcceleratorTable(entries)
        self.SetAcceleratorTable(accel_tbl)

        self.toolbar = self.CreateToolBar()
        self.toolbar.SetToolBitmapSize((30, 30))
        img = wx.Image(os.path.join(CURRENT_DIR, 'icons', 'new.png'))
        img.Rescale(25, 25)
        image = wx.Bitmap(img)
        new_tool = self.toolbar.AddTool(wx.ID_NEW, 'New',
                                        image, shortHelp="New File")
        new_tool.SetLongHelp("Create a new AATR XML file")
        self.Bind(wx.EVT_TOOL, self.file_new_on_menu, new_tool)

        img = wx.Image(os.path.join(CURRENT_DIR, 'icons', 'folder.png'))
        img.Rescale(25, 25)
        image = wx.Bitmap(img)
        open_tool = self.toolbar.AddTool(wx.ID_OPEN, 'Open',
                                         image, shortHelp="Open File...")

        open_tool.SetLongHelp("Open an existing AATR XML file")
        self.Bind(wx.EVT_TOOL, self.file_open_on_menu, open_tool)

        img = wx.Image(os.path.join(CURRENT_DIR, 'icons', 'save.png'))
        img.Rescale(25, 25)
        image = wx.Bitmap(img)
        save_tool = self.toolbar.AddTool(wx.ID_SAVE, 'Save',
                                         image, shortHelp="Save File")

        save_tool.SetLongHelp("Save the currently opened file")
        self.Bind(wx.EVT_TOOL, self.file_save_on_menu, save_tool)

        img = wx.Image(os.path.join(CURRENT_DIR, 'icons', 'pdf.png'))
        img.Rescale(25, 25)
        image = wx.Bitmap(img)
        ID_EXPORT = wx.NewId()
        export_tool = self.toolbar.AddTool(self.ID_EXPORT,
                                           'Export to PDF',
                                           image, shortHelp="Export to PDF")

        export_tool.SetLongHelp("Export the currently opened document to PDF")
        self.Bind(wx.EVT_TOOL, self.export_pdf_on_menu, export_tool)

        self.toolbar.EnableTool(self.ID_EXPORT, False)

        img = wx.Image(os.path.join(CURRENT_DIR, 'icons', 'pdf_all.png'))
        img.Rescale(25, 25)
        image = wx.Bitmap(img)
        ID_EXPORT_ALL = wx.NewId()
        self.export_all_tool = self.toolbar.AddTool(self.ID_EXPORT_ALL,
                                               'Export all to PDF',
                                               image,
                                               shortHelp="Export all to PDF")

        self.export_all_tool.SetLongHelp("Export all AATR XML files in the " +
                                    "TestReport directory to their " +
                                    "respective PDF files")

        self.export_all_tool.Enable(True)

        self.Bind(wx.EVT_TOOL, self.export_pdf_all_on_menu, self.export_all_tool)

        img = wx.Image(os.path.join(CURRENT_DIR, 'icons', 'issue.png'))
        img.Rescale(25, 25)
        image = wx.Bitmap(img)
        self.ID_CREATE_ISSUES = wx.NewId()
        issues_tool = self.toolbar.AddTool(self.ID_CREATE_ISSUES,
                                           'Create Issues',
                                           image, shortHelp="Create Issues")

        issues_tool.SetLongHelp("Create a text document containing a list of issues")
        self.Bind(wx.EVT_TOOL, self.file_create_issues_on_menu, issues_tool)

        self.toolbar.EnableTool(self.ID_CREATE_ISSUES, True)


        self.toolbar.AddSeparator()

        img = wx.Image(os.path.join(CURRENT_DIR,
                                    'icons', 'addchild.png'))

        img.Rescale(25, 25)
        image = wx.Bitmap(img)
        add_tool = self.toolbar.AddTool(wx.ID_ADD, 'Add', image,
                                        shortHelp="Add Child")

        add_tool.SetLongHelp("Add a new tag as a child of the selected tag")
        self.Bind(wx.EVT_TOOL, self.context_menu_add, add_tool)

        self.toolbar.EnableTool(wx.ID_ADD, False)
        self.menu_item_edit_add.Enable(False)

        img = wx.Image(os.path.join(CURRENT_DIR,
                                    'icons', 'delete.png'))

        img.Rescale(25, 25)
        image = wx.Bitmap(img)
        delete_tool = self.toolbar.AddTool(wx.ID_DELETE, 'Delete',
                                           image, shortHelp="Delete Item")

        delete_tool.SetLongHelp("Delete the selected tag")
        self.Bind(wx.EVT_TOOL, self.context_menu_delete, delete_tool)

        self.toolbar.EnableTool(wx.ID_DELETE, False)
        self.menu_item_edit_delete.Enable(False)

        self.toolbar.AddSeparator()

        img = wx.Image(os.path.join(CURRENT_DIR, 'icons', 'settings.png'))
        img.Rescale(25, 25)
        image = wx.Bitmap(img)
        settings_tool = self.toolbar.AddTool(wx.ID_ANY, 'Settings',
                                             image, shortHelp="Settings")

        settings_tool.SetLongHelp("Editor configuration")
        self.Bind(wx.EVT_TOOL, self._options_pref_on_menu, settings_tool)

        img = wx.Image(os.path.join(CURRENT_DIR, 'icons', 'quit.png'))
        img.Rescale(25, 25)
        image = wx.Bitmap(img)
        close_tool = self.toolbar.AddTool(wx.ID_CLOSE, 'Quit',
                                          image, shortHelp="Quit")

        close_tool.SetLongHelp("Close the program")
        self.Bind(wx.EVT_TOOL, self.on_close, close_tool)
        self.toolbar.Realize()

        self.toolbar.SetBackgroundColour(clr_window)

        self.toolbar.EnableTool(wx.ID_SAVE, False)
        self.toolbar.EnableTool( self.ID_EXPORT, False)
        self.file_save.Enable(False)
        self.file_export_pdf.Enable(False)
        self.file_save_as.Enable(False)
        self.file_create_issues.Enable(True)
        self.menu_item_edit_search.Enable(False)
        self.menu_item_edit_delete.Enable(False)
        self.menu_item_edit_add.Enable(False)

        self.tree.AssignImageList(il)

        self.status_text.Bind(wx.EVT_MENU_HIGHLIGHT_ALL, self.statusbar_status)

        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.tree_item_expanded,
                  self.tree, id=wx.ID_ANY)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.tree_item_collapsed,
                  self.tree, id=wx.ID_ANY)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.tree_sel_changed,
                  self.tree, id=wx.ID_ANY)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.tree_item_right_click,
                  self.tree, id=wx.ID_ANY)

        self.Bind(wx.EVT_MENU, self.file_new_on_menu,
                  id=self.file_new.GetId())
        self.Bind(wx.EVT_MENU, self.file_open_on_menu,
                  id=self.file_open.GetId())
        self.Bind(wx.EVT_MENU, self.file_save_on_menu,
                  id=self.file_save.GetId())
        self.Bind(wx.EVT_MENU, self.file_save_as_on_menu,
                  id=self.file_save_as.GetId())
        self.Bind(wx.EVT_MENU, self.file_create_issues_on_menu,
                  id=self.file_create_issues.GetId())
        self.Bind(wx.EVT_MENU, self.export_pdf_on_menu,
                  id=self.file_export_pdf.GetId())
        self.Bind(wx.EVT_MENU, self.export_pdf_all_on_menu,
                  id=self.file_export_pdf_all.GetId())
        self.Bind(wx.EVT_MENU, self.on_close, id=self.file_exit.GetId())
        self.Bind(wx.EVT_MENU, self._edit_search_on_menu,
                  id=self.menu_item_edit_search.GetId())
        self.Bind(wx.EVT_MENU, self._edit_add_on_menu,
                  id=self.menu_item_edit_add.GetId())
        self.Bind(wx.EVT_MENU, self._edit_del_on_menu,
                  id=self.menu_item_edit_delete.GetId())
        self.Bind(wx.EVT_MENU, self._help_on_menu,
                  id=self.menu_item_help.GetId())
        self.Bind(wx.EVT_MENU, self._options_pref_on_menu,
                  id=self.menu_item_options_pref.GetId())
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(EVT_COUNT, self.OnExport)

        self.toolbar.Bind(wx.EVT_LEAVE_WINDOW, self.on_mouse_leave)
        


        self.Bind(wx.EVT_ERASE_BACKGROUND, self.onErase)
    def onErase(self, event):
        pass


    def __del__(self):
        pass


    def tree_sel_changed(self, event):

        root = self.tree.GetRootItem()
        root_txt = self.tree.GetItemText(self.tree.GetRootItem())
        selected = self.tree.GetSelection()
        tag_list_1 = ("Test", "TestCase", "RevisionHistory",
                      "SupliersTestArtefacts", "IntegratorsTestArtefacts",
                      "Acronyms", "References", "AdditionalSoftwareUsed",
                      "TestCaseTable", "TableHeader", "TableRow", root_txt)

        tag_list_2 = ("SuppliersAdditionalInfo", "Revision", "TestArtefact",
                      "AdditionalTool", "KnownLimitation", "Acronym",
                      "Reference", "TestCaseTable", "TableHeader",
                      "TableRow")

        if not selected:
            self.tree.SelectItem(event.GetItem(), True)
        else:
            sel_text = self.tree.GetItemText(selected)

            if sel_text in tag_list_1:

                self.toolbar.EnableTool(wx.ID_ADD, True)
                self.menu_item_edit_add.Enable(True)
            else:
                self.toolbar.EnableTool(wx.ID_ADD, False)
                self.menu_item_edit_add.Enable(False)

            if (sel_text in tag_list_2 or "TestCase" in sel_text):

                self.toolbar.EnableTool(wx.ID_DELETE, True)
                self.menu_item_edit_delete.Enable(True)
            else:
                self.toolbar.EnableTool(wx.ID_DELETE, False)
                self.menu_item_edit_delete.Enable(False)

            if not selected:
                event.Skip()


            self.Freeze()

            if selected:
                self.find_desc(tag_dict.values()[0], sel_text)

                self.b_sizer_parsed.Clear(True)
                wgt_dict.clear()

                parent_sizer = self.create_box(selected, self.b_sizer_parsed)

                if not self.tree.ItemHasChildren(selected):
                    self.create_widget(selected, parent_sizer)

                self.tab_parsed.SetupScrolling()
            self.Thaw()

    def find_desc(self, d, tag):
        if tag == self.tree.GetItemText(self.tree.GetRootItem()):
            self.desc_text.SetLabel("")
        for k, v in d.items():
            if "TestCase" in k and "TestCase" in tag:
                if isinstance(v, list):
                    self.desc_text.SetLabel(v[0]["@desc"])
                    return
                elif isinstance(v, dict):
                    self.desc_text.SetLabel(v["@desc"])
                    return
            elif k == tag:
                if isinstance(v, dict):
                    if '@desc' in v:
                        self.desc_text.SetLabel(v['@desc'])
                        return
                    else:
                        self.desc_text.SetLabel("")
                        self.find_desc(v, tag)
                else:
                    self.desc_text.SetLabel("")
                    return
            elif isinstance(v, dict):
                self.find_desc(v, tag)
            elif "recommendationresult" in tag.lower() or "testcasetable" in tag.lower():
                self.desc_text.SetLabel("")

    def create_box(self, item, parent_sizer):
        tag = self.tree.GetItemText(item)

        self.selection_box = wx.StaticBoxSizer(wx.VERTICAL, self.tab_parsed)
        parent_sizer.Add(self.selection_box, 0, wx.ALL | wx.EXPAND, 5)
        parent_sizer.Layout()
        self.selection_box.Layout()
        self.selection_box.GetStaticBox().SetLabel(tag)

        parent_sizer = self.selection_box

        if self.tree.ItemHasChildren(item):
            child = self.tree.GetFirstChild(item)[0]
            while child:

                if self.tree.IsExpanded(child):
                    self.selection_box = self.create_box(child, parent_sizer)
                else:

                    self.selection_box = wx.StaticBoxSizer(wx.VERTICAL,
                                                           self.tab_parsed)

                    parent_sizer.Add(self.selection_box, 0,
                                     wx.ALL | wx.EXPAND, 5)

                    parent_sizer.Layout()
                    self.selection_box.Layout()
                    text_child = self.tree.GetItemText(child)
                    self.selection_box.GetStaticBox().SetLabel(text_child)
                    text_sizer = self.selection_box

                if not self.tree.ItemHasChildren(child):
                    self.create_widget(child, text_sizer)

                child = self.tree.GetNextSibling(child)

        parent_sizer.Layout()

        return parent_sizer

    def create_widget(self, item, parent_sizer):
        tag = self.tree.GetItemText(item)
        text = self.tree.GetItemData(item)

        tag_used = "used_AIT-FW_ProvidedByIntegrator"
        tag_violation = "allReportedViolationJustified"

        if tag == "SWC_ASIL_Level":
            self.widget = wx.Choice(self.tab_parsed,
                                    choices=["QM", "A", "B", "C", "D"],
                                    name=tag)

            if isinstance(text, int):
                self.widget.SetSelection(text)
            else:
                if text:
                    self.widget.SetSelection(self.widget.FindString(text))

            wgt_dict[self.widget] = {item: self.widget.GetCurrentSelection()}
            self.widget.Bind(wx.EVT_CHOICE, self.on_edit)

        elif tag == "SWC_Host":
            self.widget = wx.Choice(self.tab_parsed,
                                    choices=["APH", "SSH", "SRH"], name=tag)

            if isinstance(text, int):
                self.widget.SetSelection(text)
            else:
                if text:
                    self.widget.SetSelection(self.widget.FindString(text))

            wgt_dict[self.widget] = {item: self.widget.GetCurrentSelection()}
            self.widget.Bind(wx.EVT_CHOICE, self.on_edit)

        elif tag == "DocumentStatus":
            self.widget = wx.Choice(self.tab_parsed,
                                    choices=["Released", "draft", "in_work"],
                                    name=tag)

            if isinstance(text, int):
                self.widget.SetSelection(text)
            else:
                if text:
                    self.widget.SetSelection(self.widget.FindString(text))

            wgt_dict[self.widget] = {item: self.widget.GetCurrentSelection()}
            self.widget.Bind(wx.EVT_CHOICE, self.on_edit)

        elif tag == "align":
            self.widget = wx.Choice(self.tab_parsed,
                                    choices=["left", "center", "right"],
                                    name=tag)

            if isinstance(text, int):
                self.widget.SetSelection(text)
            else:
                if text:
                    self.widget.SetSelection(self.widget.FindString(text))

            wgt_dict[self.widget] = {item: self.widget.GetCurrentSelection()}
            self.widget.Bind(wx.EVT_CHOICE, self.on_edit)

        elif tag == "integrationRecommendationResult":
            self.widget = wx.Choice(self.tab_parsed,
                                    choices=["passed", "failed",
                                             "not_executed",
                                             "failed_integrate",
                                             "previously_failed"],
                                    name=tag)

            if isinstance(text, int):
                self.widget.SetSelection(text)
            else:
                if text:
                    self.widget.SetSelection(self.widget.FindString(text))

            wgt_dict[self.widget] = {item: self.widget.GetCurrentSelection()}
            self.widget.Bind(wx.EVT_CHOICE, self.on_edit)

        elif tag == "result" or tag == "@result":
            self.widget = wx.Choice(self.tab_parsed,
                                    choices=["passed",
                                             "failed",
                                             "not_executed"],
                                    name=tag)

            if isinstance(text, int):
                self.widget.SetSelection(text)
            else:
                if text:
                    self.widget.SetSelection(self.widget.FindString(text))

            wgt_dict[self.widget] = {item: self.widget.GetCurrentSelection()}
            self.widget.Bind(wx.EVT_CHOICE, self.on_edit)

        elif tag == tag_used or tag == tag_violation:
            self.widget = wx.Choice(self.tab_parsed, -1,
                                    choices=["yes", "no"], name=tag)

            if isinstance(text, int):
                self.widget.SetSelection(text)
            else:
                if text:
                    self.widget.SetSelection(self.widget.FindString(text))
            wgt_dict[self.widget] = {item: self.widget.GetCurrentSelection()}
            self.widget.Bind(wx.EVT_CHOICE, self.on_edit)

        elif tag == "priority":
            self.widget = wx.Choice(self.tab_parsed,
                                    choices=["PRIO_A",
                                             "PRIO_B",
                                             "PRIO_C",
                                             "PRIO_D"],
                                    name=tag)

            if isinstance(text, int):
                self.widget.SetSelection(text)
            else:
                if text:
                    self.widget.SetSelection(self.widget.FindString(text))

            wgt_dict[self.widget] = {item: self.widget.GetCurrentSelection()}
            self.widget.Bind(wx.EVT_CHOICE, self.on_edit)

        elif "date" in tag.lower():
            self.widget = wx.adv.DatePickerCtrl(self.tab_parsed,
                                                dt=wx.DefaultDateTime,
                                                pos=wx.DefaultPosition,
                                                size=wx.DefaultSize,
                                                style=wx.adv.DP_DROPDOWN,
                                                validator=wx.DefaultValidator)
            
            if text:
                dt = wx.DateTime(wx.DateTime.Now())
                if "/" in text:
                    day, month, year = text.split('/')
                elif "-" in text:
                    year, month, day = text.split('-')

                date = wx.DateTime.FromDMY(int(day), int(month) - 1, int(year))
                self.widget.SetValue(date)             
            else:
                dt = wx.DateTime(wx.DateTime.Now())
                self.widget.SetValue(dt.Now())
            wgt_dict[self.widget] = {item: self.widget.GetValue()}
            self.widget.Bind(wx.adv.EVT_DATE_CHANGED, self.on_edit)

        elif "time" in tag.lower() and "buildtimestamp" not in tag.lower():
            self.widget = wx.adv.TimePickerCtrl(self.tab_parsed,
                                                dt=wx.DateTime(),
                                                pos=wx.DefaultPosition,
                                                size=wx.DefaultSize,
                                                style=wx.adv.DP_DEFAULT,
                                                validator=wx.DefaultValidator)

            if text:
                text_split = text.split(":")
                if len(text_split) == 2:
                    time = wx.DateTime.FromHMS(int(text_split[0]), int(text_split[1]))
                elif len(text_split) == 3:
                    time = wx.DateTime.FromHMS(int(text_split[0]), int(text_split[1]), int(text_split[2]))
                self.widget.SetValue(time)             
            else:
                dt = wx.DateTime(wx.DateTime.Now())
                self.widget.SetValue(dt.SetToCurrent())
            wgt_dict[self.widget] = {item: self.widget.GetValue()}
            self.widget.Bind(wx.adv.EVT_TIME_CHANGED, self.on_edit)

        else:
            self.widget = ExpandoTextCtrl(self.tab_parsed, name=tag, style=wx.TE_PROCESS_ENTER | wx.TE_MULTILINE | wx.TE_CHARWRAP)
            self.widget.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
            wgt_dict[self.widget] = {item: self.widget.GetValue()}
            if text and not isinstance(text, list):
                if text.startswith("{{"):
                    self.widget.ChangeValue("")
                else:
                    self.widget.ChangeValue(text)
            else:
                self.widget.ChangeValue("")
            self.widget.Bind(wx.EVT_TEXT, self.on_edit)

        if isinstance(self.widget, (wx.Choice, wx.adv.DatePickerCtrl, wx.adv.TimePickerCtrl)):
            parent_sizer.Add(self.widget,
                             wx.ST_NO_AUTORESIZE | wx.STATIC_BORDER)
        else:
            parent_sizer.Add(self.widget,
                             wx.ST_NO_AUTORESIZE | wx.STATIC_BORDER, wx.EXPAND)

        self.b_sizer_parsed.Layout()




    def on_enter(self, event):
        print "ENTER"
        text = event.GetEventObject()
        wind = text.GetParent()
        newsize = text.Size
        newsize.y += 38
        text.SetMinSize(newsize)
        wind.Layout()

        for box in wind.GetChildren():
            if isinstance(box, wx.StaticBox):
                box.Layout()


#        self.Fit()


    def on_edit(self, event):
        item = self.tree.GetSelection()
        widget = event.GetEventObject()
        tag = self.tree.GetItemText(item)
        self.file_modified = 1
        frame.SetTitle(appname + ' - ' + filename + "*")
        self.status_text.SetStatusText("")

        tag_list = ["TestCase", "TestCaseTable", "Acronym", "Reference", "Revision"]

        if isinstance(filename, list):
            frame.SetTitle(appname + ' - ' + os.path.join(*filename) + "*")
        else:
            frame.SetTitle(appname + ' - ' + filename + "*")

        if isinstance(widget, (ExpandoTextCtrl, wx.adv.DatePickerCtrl, wx.adv.TimePickerCtrl)):
            new_value = widget.GetValue()
            if isinstance(widget, wx.adv.DatePickerCtrl):
                dt = wx.DateTime(new_value)
                new_value = dt.FormatDate()
                print "DATE"
            if isinstance(widget, wx.adv.TimePickerCtrl):
                dt = wx.DateTime(wx.DateTime.Now())
                new_value = dt.FormatTime(new_value)
                print "TIME"
            else:
                print "TEXT"
        elif isinstance(widget, wx.Choice):
            new_value = widget.GetCurrentSelection()
            print "CHOICE"


        wgt_dict[widget][item] = new_value
        self.tree.SetItemData(wgt_dict[widget].keys()[0], new_value)

        if any(check in tag for check in tag_list):
            self.update_name(item, tag, new_value)
        
#        self.Fit()
        self.save_data()         # SKLONI NA KRAJU



    def update_name(self, item, tag, new_value):

        if "TestCase" in tag:
            child = self.tree.GetFirstChild(item)[0]

            if "TestCaseTable" in tag:
                tag_update = "TestCaseTable ["
            else:
                tag_update = "TestCase ["

            while child.IsOk():
                if self.tree.GetItemText(child).lower() == "name" and self.tree.GetItemData(child):
                    self.tree.SetItemText(item, tag_update + self.tree.GetItemData(child) + "]",)
                    break
                child = self.tree.GetNextSibling(child)

        if "Reference" in tag:
            child = self.tree.GetFirstChild(item)[0]

            while child.IsOk():
                if self.tree.GetItemText(child).lower() == "name" and self.tree.GetItemData(child):
                    self.tree.SetItemText(item, "Reference [" + self.tree.GetItemData(child) + "]",)
                    break
                child = self.tree.GetNextSibling(child)

        if "Revision" in tag:
            child = self.tree.GetFirstChild(item)[0]

            while child.IsOk():
                if self.tree.GetItemText(child).lower() == "date" and self.tree.GetItemData(child):
                    self.tree.SetItemText(item, "Revision [" + self.tree.GetItemData(child) + "]",)
                    break
                child = self.tree.GetNextSibling(child)

        if "Acronym" in tag:
            child = self.tree.GetFirstChild(item)[0]

            while child.IsOk():
                if self.tree.GetItemText(child).lower() == "name" and self.tree.GetItemData(child):
                    self.tree.SetItemText(item, "Acronym [" + self.tree.GetItemData(child) + "]",)
                    break
                child = self.tree.GetNextSibling(child)

    def tree_item_expanded(self, event):
        self.panel_left.Freeze()
        self.tree_sel_changed(event)
        self.panel_left.Thaw()

    def tree_item_collapsed(self, event):
        self.panel_left.Freeze()
        self.tree_sel_changed(event)
        self.panel_left.Thaw()

    def tree_item_right_click(self, event):
        self.tree_sel_changed(event)
        self.tree.SelectItem(event.GetItem(), True)
        self.tree_item_context_menu(event)

    def tree_item_context_menu(self, event):

        self.panel_left.Freeze()
        self.popup_menu = wx.Menu()

        root = self.tree.GetItemText(self.tree.GetRootItem())
        sel_text = self.tree.GetItemText(self.tree.GetSelection())
        if sel_text == root:

            self.add_menu = wx.Menu()
            self.popup_menu.Append(-1, "Add Child", self.add_menu)
            item_sup = self.add_menu.Append(-1, "Supplier Additional Info")
            self.Bind(wx.EVT_MENU, self.add_info, item_sup)
            item_limit = self.add_menu.Append(-1, "Known Limitation")
            self.Bind(wx.EVT_MENU, self.add_known_lim, item_limit)

        elif sel_text == "Test":

            self.add_menu = wx.Menu()
            self.popup_menu.Append(-1, "Add Child", self.add_menu)
            item_sup = self.add_menu.Append(-1, "TestCase")
            self.Bind(wx.EVT_MENU, self.add_test_case, item_sup)
            item_limit = self.add_menu.Append(-1, "TestCaseTable")
            self.Bind(wx.EVT_MENU, self.add_test_caseTable, item_limit)

        else:

            if sel_text == "TestCase":
                if sel_text != "TestCaseNumber":
                    if sel_text != "TestCaseSummary":
                        item = self.popup_menu.Append(-1, "Add BugReference")
                        self.Bind(wx.EVT_MENU, self.on_select_context, item)

            if sel_text == "TestCaseTable":
                item = self.popup_menu.Append(-1, "Add TableRow")
                self.Bind(wx.EVT_MENU, self.on_select_context, item)

            if sel_text == "RevisionHistory":
                item = self.popup_menu.Append(-1, "Add Revision")
                self.Bind(wx.EVT_MENU, self.on_select_context, item)

            if sel_text in ["SupliersTestArtefacts", "IntegratorsTestArtefacts"]:
                item = self.popup_menu.Append(-1, "Add TestArtefact")
                self.Bind(wx.EVT_MENU, self.on_select_context, item)

            if sel_text == "Acronyms":
                item = self.popup_menu.Append(-1, "Add Acronym")
                self.Bind(wx.EVT_MENU, self.on_select_context, item)

            if sel_text == "References":
                item = self.popup_menu.Append(-1, "Add Reference")
                self.Bind(wx.EVT_MENU, self.on_select_context, item)

            if sel_text == "AdditionalSoftwareUsed":
                item = self.popup_menu.Append(-1, "Add AdditionalTool")
                self.Bind(wx.EVT_MENU, self.on_select_context, item)

            if sel_text in ["SupliersTestArtefacts", "IntegratorsTestArtefacts"]:
                item = self.popup_menu.Append(-1, "Add TestArtefact")
                self.Bind(wx.EVT_MENU, self.on_select_context, item)

            if sel_text in ["TableHeader", "TableRow"]:
                item = self.popup_menu.Append(-1, "Add TableCell")
                self.Bind(wx.EVT_MENU, self.on_select_context, item)
##

        if (sel_text == "SuppliersAdditionalInfo" or
                sel_text == "Revision" or
                "TestCase" in sel_text or
                sel_text == "TestArtefact" or
                sel_text == "AdditionalTool" or
                sel_text == "KnownLimitation" or
                sel_text == "Acronym" or
                sel_text == "Reference" or
                sel_text == "TestCaseTable" or
                sel_text == "TableHeader" or
                sel_text == "TableRow"):

            item = self.popup_menu.Append(-1, "Delete")
            self.Bind(wx.EVT_MENU, self.on_select_context, item)

        
        self.PopupMenu(self.popup_menu, event.GetPoint())
        self.popup_menu.Destroy()
        self.panel_left.Thaw()

    def on_select_context(self, event):
        item = self.popup_menu.FindItemById(event.GetId())
        if item:
            text = item.GetText()

            if text == "Delete":
                self.context_menu_delete(event)
            else:
                self.context_menu_add(event)


    def context_menu_add(self, event):

        clicked = self.tree.GetSelection()
        selection_text = self.tree.GetItemText(clicked)
        if self.tree.GetItemText(clicked) == "Test":

            self.add_menu = wx.Menu()
            item_case = self.add_menu.Append(-1, "TestCase")
            self.Bind(wx.EVT_MENU, self.add_test_case, item_case)
            item_table = self.add_menu.Append(-1, "TestCaseTable")
            self.Bind(wx.EVT_MENU, self.add_test_caseTable, item_table)
            self.PopupMenu(self.add_menu)

        elif "TestCase" in selection_text or selection_text == "TestCase":
            if "TestCaseTable" in selection_text:
                self.add_table_row(clicked)
            else:
                item = self.tree.AppendItem(clicked, "BugReference", data=None)
                self.tree.SetItemImage(item, 0, which=icon_normal)
                self.tree.SetItemImage(item, 1, which=icon_exp)

        elif selection_text == "Acronyms":
            self.add_acronym(clicked)
        elif selection_text == "References":
            self.add_reference(clicked)
        elif selection_text == "SupliersTestArtefacts":
            self.add_ta(clicked)
        elif selection_text == "IntegratorsTestArtefacts":
            self.add_ta(clicked)
        elif selection_text == "RevisionHistory":
            self.add_revision(clicked)
        elif selection_text == "AdditionalSoftwareUsed":
            self.add_tool(clicked)
        elif selection_text == "TestCaseTable":
            self.add_table_row(clicked)
        elif selection_text == "TableHeader":
            self.add_table_cell(clicked)
        elif selection_text == "TableRow":
            print "EDIT --> ADD CHILD --> TABLE CELL (ROW)"

            item = self.tree.AppendItem(clicked, "TableCell", data=None)
            self.tree.SetItemImage(item, 0, which=icon_normal)
            self.tree.SetItemImage(item, 1, which=icon_exp)

        elif clicked == self.tree.GetRootItem():

            self.add_menu = wx.Menu()
            item_sup = self.add_menu.Append(-1, "Supplier Additional Info")
            self.Bind(wx.EVT_MENU, self.add_info, item_sup)
            item_limit = self.add_menu.Append(-1, "Known Limitation")
            self.Bind(wx.EVT_MENU, self.add_known_lim, item_limit)
            self.PopupMenu(self.add_menu)

        self.tree_sel_changed(event)

    def context_menu_delete(self, event):
        clicked = self.tree.GetSelection()

        if clicked == self.tree.GetRootItem():
            wx.MessageBox("Can't delete the root!", "Error!",
                          wx.OK | wx.ICON_ERROR)
        else:
            string = "Are you sure you want to delete this item?"
            delete_warning = wx.MessageBox(string, "Warning!",
                                           wx.YES_NO | wx.ICON_WARNING)
            if delete_warning == wx.YES:
                print "EDIT --> DELETE --> " + self.tree.GetItemText(clicked)
                del_tag = self.tree.GetItemText(clicked)
                self.tree.Delete(clicked)
                self.status_text.SetStatusText("Element deleted: " + del_tag)
                self.file_modified = 1
                frame.SetTitle(appname + ' - ' + filename + "*")

        self.tree_sel_changed(event)

    def file_new_on_menu(self, event):
        self.file_save.Enable(True)
        self.file_export_pdf.Enable(True)
        self.file_save_as.Enable(True)
        self.file_create_issues.Enable(True)
        self.menu_item_edit_search.Enable(True)
        self.menu_item_edit_delete.Enable(True)
        self.menu_item_edit_add.Enable(True)


        if self.file_modified:
            string = "Save changes before continuing?"
            save_w = wx.MessageBox(string, "File not saved!",
                                   wx.YES_NO |
                                   wx.CANCEL |
                                   wx.ICON_WARNING)

            if save_w == wx.YES:
                self.file_save_as_on_menu(event)
                self.create_blank_file()

            elif save_w == wx.NO:
                self.create_blank_file()

            elif save_w == wx.CANCEL:
                return
        else:
            self.create_blank_file()

    def file_open_on_menu(self, event):
        global filename
        global tag_dict

        self.file_save.Enable(True)
        self.file_export_pdf.Enable(True)
        self.file_save_as.Enable(True)
        self.file_create_issues.Enable(True)
        self.menu_item_edit_search.Enable(True)
        self.menu_item_edit_delete.Enable(True)
        self.menu_item_edit_add.Enable(True)

        if self.file_modified:

            string = "Save changes before continuing?"
            save_w = wx.MessageBox(string, "File not saved!",
                                   wx.YES_NO |
                                   wx.CANCEL |
                                   wx.ICON_WARNING)

            if save_w == wx.CANCEL:
                return

            elif save_w == wx.YES:
                self.file_save_as_on_menu(event)

        cfg = ConfigParser()
        try:
            cfg.read(CONFIG_PATH)

            s_path = os.path.dirname(cfg.get('DEFAULT', 'SOURCE_FOLDER'))
            if os.path.exists(s_path):
                config_source = cfg.get('DEFAULT', 'SOURCE_FOLDER')
            else:
                config_source = CURRENT_DIR

        except Exception as ex:
            config_source = CURRENT_DIR
            print ex

        dlg = wx.FileDialog(self, message="Open file",
                            defaultDir=config_source,
                            defaultFile="",
                            wildcard="XML Files (*.xml)|*.xml|"
                            "All files (*.*)|*.*",
                            style=wx.FD_OPEN | wx.FD_CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()

            try:
                with open(path) as fd:
                    parse_file = xmltodict.parse(fd.read())
                    tag_dict = json.loads(json.dumps(parse_file))
            except Exception as ex:
                self.status_text.SetStatusText("Invalid file!")
                string = "Please select a valid A-AcceptTestReport XML file"
                wx.MessageBox(string, "Opening failed!",
                              wx.OK | wx.ICON_ERROR)
                self.status_text.SetStatusText("")
                print ex
                return


            self.tree.DeleteAllItems()
            filename = path
            self.tree_fill()
            frame.SetTitle(appname + ' - ' + filename)
            self.toolbar.EnableTool(wx.ID_SAVE, True)
            self.toolbar.EnableTool( self.ID_EXPORT, True)
            self.search.Show()
            self.b_sizer_parsed.Clear(True)
            self.status_text.SetStatusText("Opened file at " + path)
            self.file_modified = 0
            self.panel_left.Layout()
            self.tree.SelectItem(self.tree.GetRootItem(), True)

            print "FILE --> OPEN --> " + path

        else:
            return

        dlg.Destroy()

    def file_save_on_menu(self, event):
        if self.tree.GetRootItem():

            if "Untitled" in filename or "Untitled" in filename[0]:
                self.file_save_as_on_menu(event)
            else:
                self.save(filename)

    def file_save_as_on_menu(self, event):
        print "FILE --> SAVE AS..."
        global filename

        del rev_list[:]
        del ref_list[:]
        del tc_list[:]
        del acr_list[:]
        del sup_ta_list[:]
        del int_ta_list[:]
        del add_data_list[:]
        del add_tool_list[:]
        del limit_list[:]
        del tct_list[:]

        cfg = ConfigParser()
        try:
            cfg.read(CONFIG_PATH)
            print("CONFIG_PATH: %s" % CONFIG_PATH)
            dest = cfg.get('DEFAULT', 'dest_folder')
            print("dest: %s" % dest)
        except Exception as ex:
            dest = CURRENT_DIR
            print ex

        if os.path.exists(dest):
            config_dest = dest
            print("Exists : %s" % config_dest)
        else:
            config_dest = CURRENT_DIR
            print("Does Not Exists : %s" % config_dest)
            

        dlg = wx.FileDialog(self, "Save project as...",
                            config_dest, "",
                            "XML Files (*.xml)|*.xml|, All files (*.*)|*.*",
                            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        result = dlg.ShowModal()
        if dlg.GetPath():
            filename = dlg.GetPath()
        filename = str(filename).split("\\")
        flag = 0
        for f in filename:
            if "AATR_TTTech_" in f:
                flag = 1
        if flag != 1:
            filename[-1] = "AATR_TTTech_" + filename[-1]
        save_file = filename[0] + "\\"

        for el in filename[0:]:
            save_file = os.path.join(save_file, el)
        dlg.Destroy()

        if result == wx.ID_OK:
            self.save(save_file)
            return
        elif result == wx.ID_CANCEL:
            return

    def save(self, save_file):

        self.save_data()

        file_system_loader = FileSystemLoader(TEMPLATE_PATH)
        env = Environment(loader=file_system_loader)
        template = env.get_template("create_AATR.template")

        context = {'release_da': release_data,
                   'swc_da': swc_data,
                   'swc_row': swc_row,
                   'AatTestCases': tc_list,
                   'SupTA_list': sup_ta_list,
                   'IntTA_list': int_ta_list,
                   'dbRevisionHistory': rev_list,
                   'References': ref_list,
                   'Acronyms': acr_list,
                   'AdditionalTools': add_tool_list,
                   'AdditionalData': add_data_list,
                   'KnownLimitations': limit_list,
                   'TestCaseTable_list': tct_list}

        output = template.render(context)
        if isinstance(save_file, list):

            filename = save_file[0] + "\\"

            for el in save_file[0:]:
                filename = os.path.join(filename, el)
                save_file = filename

        try:
            with open(save_file, "wb") as fh:
                fh.write(output)
                frame.SetTitle(appname + ' - ' + save_file)
                self.file_modified = 0
                self.status_text.SetStatusText("File saved successfully!\n")
                print "File saved successfully\n"
        except Exception as ex:
            self.status_text.SetStatusText("Save failed!")
            print "Save failed"
            print ex

    def file_create_issues_on_menu(self, event):                        #1
        print "FILE --> CREATE ISSUE"

        cfg = ConfigParser()
        try:
            cfg.read(CONFIG_PATH)
            if os.path.exists(os.path.dirname(cfg.get('DEFAULT', 'ISSUE_DEST_FOLDER'))):
                config_issue_dest = cfg.get('DEFAULT', 'ISSUE_DEST_FOLDER')
            else:
                config_issue_dest = CURRENT_DIR
        except Exception as ex:
            config_issue_dest = CURRENT_DIR
            print ex

        try:
            if os.path.exists(os.path.dirname(cfg.get('DEFAULT', 'TEST_REPORT_PATH'))):
                config_tr_path = cfg.get('DEFAULT', 'TEST_REPORT_PATH')
        except Exception as ex:
            config_tr_path = CURRENT_DIR
            print ex

#--------------------------------------------

        dlg = wx.DirDialog (None, "Create issues at...", config_issue_dest,
                            wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)

        if dlg.ShowModal() == wx.ID_OK:
            config_issue_dest = dlg.GetPath()
            if os.path.exists(config_issue_dest + './issue.txt'):
                self.status_text.SetStatusText("{}\issue.txt".format(config_issue_dest) + " exists!")
                exists_warning = wx.MessageBox("{}\issue.txt".format(config_issue_dest) + " already exists!" + "\nDo you want to overwrite the file?",
                             "Warning!",
                             wx.YES_NO |
                             wx.ICON_WARNING)
                if exists_warning == wx.NO:
                    self.status_text.SetStatusText("")
                    return

            self.status_text.SetStatusText("Generating list of issues...")
            

            if create_issue_list.main(self, config_tr_path, config_issue_dest) != -1:
                self.status_text.SetStatusText("Issues generated at " + config_issue_dest)


                dlg = wx.MessageDialog(self, "Issue path: " + config_issue_dest + "\issue.txt",
                                    "Issues generated successfully!",
                                    style=wx.OK | wx.CANCEL | wx.CENTRE | wx.ICON_INFORMATION)

                dlg.SetOKCancelLabels("Open Folder", "OK")

                result = dlg.ShowModal()
                if result == wx.ID_CANCEL:
                    dlg.Destroy()
                    self.status_text.SetStatusText("")
                elif result == wx.ID_OK:
                    os.system("explorer " + config_issue_dest) 
                    dlg.Destroy()
                    self.status_text.SetStatusText("")
            else:
                self.status_text.SetStatusText("Issue generation failed!")
                wx.MessageBox("No expected XML files!\nPlease select the valid location of your TestReport directory!",
                            "Issue generation failed!",
                            wx.OK | wx.ICON_ERROR)
                self._options_pref_on_menu(None)
        else:
            dlg.Destroy()


    def export_pdf_on_menu(self, event):

        add_info_list = []


        for key in tag_dict.values()[0]:
            if key == "SuppliersAdditionalInfo":
                if not isinstance(tag_dict.values()[0][key], list):
                    add_info_list.append(tag_dict.values()[0][key]["Additional_Data"]) 
                else:
                        for info in tag_dict.values()[0][key]:
                            for key in info.keys():
                                if "Additional_Data" in key:
                                    if info[key]:
                                        add_info_list.append(info[key])
                                    else:
                                        continue


        cfg = ConfigParser()
        try:
            cfg.read(CONFIG_PATH)
            if os.path.exists(os.path.dirname(cfg.get('DEFAULT', 'DEST_FOLDER'))):
                config_dest = cfg.get('DEFAULT', 'DEST_FOLDER')
            else:
                config_dest = CURRENT_DIR
        except Exception as ex:
            config_dest = CURRENT_DIR
            print ex

        dlg = wx.FileDialog(self, "Export PDF to...",
                            config_dest, "",
                            "PDF Files (*.pdf)|*.pdf|, All files (*.*)|*.*",
                            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        result = dlg.ShowModal()
        if result == wx.ID_OK:
            if dlg.GetPath():
                pdf_dest = dlg.GetPath()
            else:
                pdf_dest = os.path.join(CURRENT_DIR, filename, ".pdf")

            try:
                self.save_data()
                pdf_exporter.main(self, pdf_dest, "", release_data, swc_data, swc_row, tc_list, sup_ta_list, int_ta_list, rev_list, add_tool_list, add_info_list)

                self.status_text.SetStatusText("PDF exported successfully at: " + pdf_dest)
                success_dlg = wx.MessageDialog(self, "PDF file path: " + pdf_dest,
                                "PDF generated successfully!",
                                style=wx.OK | wx.CANCEL | wx.CENTRE | wx.ICON_INFORMATION)

                success_dlg.SetOKCancelLabels("Open", "OK")

                result = success_dlg.ShowModal()
                if result == wx.ID_CANCEL:
                    success_dlg.Destroy()
                elif result == wx.ID_OK:
                    os.system("explorer " + pdf_dest) 
                    success_dlg.Destroy()

            except Exception as ex:
                if str(ex) == 'Permission denied':

                    self.status_text.SetStatusText("PDF export failed!")
                    wx.MessageBox("The file is already opened in another program!\nPlease close it and try again.",
                                "Error",
                                wx.OK | wx.ICON_ERROR)
                else:
                    self.status_text.SetStatusText("PDF export failed!")
                    wx.MessageBox("PDF generation failed!",
                                "Error",
                                wx.OK | wx.ICON_ERROR)
                print ex



    def export_pdf_all_on_menu(self, event):            #1
        print "ËXPORT ALL"


        

        cfg = ConfigParser()
        try:
            cfg.read(CONFIG_PATH)
            self.tr_path = cfg.get('DEFAULT', 'TEST_REPORT_PATH')
        except Exception as ex:
            self.tr_path = CURRENT_DIR
            print ex
        if not os.path.exists(self.tr_path):
            wx.MessageBox("No expected XML files!\nPlease select the valid location of your TestReport directory!",
                          "Issue generation failed!", wx.OK | wx.ICON_ERROR)
            self.status_text.SetStatusText("", 2)
            self._options_pref_on_menu(None)
            return

        else:
            try:
                self.tr_path = cfg.get('DEFAULT', 'TEST_REPORT_PATH')
            except Exception as ex:
                self.tr_path = CURRENT_DIR
                print ex

        if not self.tr_path.endswith("TestReport"):
            wx.MessageBox("No expected XML files!\nPlease select the valid location of your TestReport directory!",
                          "Issue generation failed!", wx.OK | wx.ICON_ERROR)
            self.status_text.SetStatusText("", 2)
            self._options_pref_on_menu(None)
            return
 
        
        self.status_text.SetStatusText("Generating PDF files...", 1)

        thread.start_new_thread(self.OnExport, ())



    def OnExport(self):                             #2

        print "ON COUNT"



####################################################################################
        # PROMENITI SLIKU
        self.toolbar.Freeze()
        self.export_all_tool.SetShortHelp("Stop exporting")
        self.export_all_tool.SetLongHelp("Stop the exporting of all files to PDF")
        img = wx.Image(os.path.join(CURRENT_DIR, 'icons', 'ironman.png'))
        img.Rescale(25, 25)
        image = wx.Bitmap(img)
        self.export_all_tool.SetNormalBitmap(image)
        self.toolbar.Realize()
        self.toolbar.Refresh()
        self.toolbar.Thaw()
####################################################################################


        self.status_text.SetStatusText("(Ctrl + Shift + E to stop)", 2)
        self.stopped = False
        self.Bind(wx.EVT_TOOL, self.stop_export, self.export_all_tool)

        self.succ_file_list = []
        self.fail_file_list = []


        self.exported_num = 0
        sub_dir_list = [sub_dir for sub_dir in os.walk(self.tr_path)]
        self.file_num = len(sub_dir_list[1:])

        for sub_dir in sub_dir_list:

            if self.stopped:
                self.stopped = True
                break

            for file_name in sub_dir[2]:
                if file_name.endswith(".xml"):
                    file_path = path = os.path.join(sub_dir[0], file_name)
                    print file_name

                    pdf_release_data = {}
                    pdf_swc_data = {}
                    pdf_swc_row = {}
                    pdf_tc_list = []
                    pdf_sup_ta_list = []
                    pdf_int_ta_list = []
                    pdf_rev_list = []
                    pdf_add_tool_list = []

                    ### ovde gen pdf za jedan fajl sa file_patha
                    with open(file_path) as fp:
                        pdf_dict = json.loads(json.dumps(xmltodict.parse(fp.read())))
                        self.del_namespace(pdf_dict)

                        pdf_release_data["release"] = pdf_dict.values()[0]["Release"]
                        pdf_swc_data["name"] = pdf_dict.values()[0]["DocumentInfo"]["DocumentAuthor"]["Name"]
                        pdf_swc_data["documentcreationdate"] = pdf_dict.values()[0]["DocumentInfo"]["DocumentCreationDate"]
#                            pdf_swc_data["authorname"] = pdf_dict.values()[0]["DocumentInfo"]["DocumentAuthor"]["Name"]
                        pdf_swc_data["documentversion"] = pdf_dict.values()[0]["DocumentInfo"]["DocumentVersion"]
                        pdf_swc_data["documentstatus"] = pdf_dict.values()[0]["DocumentInfo"]["DocumentStatus"]
                        pdf_swc_data["ir_rec_result"] = pdf_dict.values()[0]["Test"]["@integrationRecommendationResult"]
                        pdf_swc_data["testpcswimage"] = pdf_dict.values()[0]["TestEnvironmentDefinition"]["TestPC-SWimage"]
                        pdf_swc_data["ptc_integritybaselinelabel"] = pdf_dict.values()[0]["TestManagement"]["PTC_IntegrityBaselineLabel"]
                        pdf_swc_data["ptc_integritytestsession_id"] = pdf_dict.values()[0]["TestManagement"]["PTC_IntegrityTestSession_ID"]
                        pdf_swc_data["ptc_integrationtestelement"] = pdf_dict.values()[0]["TestManagement"]["PTC_IntegrationTestElement"]
                        pdf_swc_data["testframeworkversion"] = pdf_dict.values()[0]["TestEnvironmentDefinition"]["TestFrameworkInfo"]["TestFrameworkVersion"]
                        pdf_swc_data["changedescription"] = pdf_dict.values()[0]["TestEnvironmentDefinition"]["TestFrameworkDeviation"]["ChangeDescription"]
                        pdf_swc_data["effects"] = pdf_dict.values()[0]["TestEnvironmentDefinition"]["TestFrameworkDeviation"]["Effects"]

                        for key in pdf_swc_data.keys():
                            if not pdf_swc_data[key]:
                                pdf_swc_data[key] = ""

                        pdf_swc_row["swc_name"] = pdf_dict.values()[0]["SWC"]["SWC_Name"]
                        pdf_swc_row["releaseversion"] = pdf_dict.values()[0]["SWC"]["SWC_Version"]["ReleaseVersion"]
                        pdf_swc_row["swc_asil_level"] = pdf_dict.values()[0]["SWC"]["SWC_ASIL_Level"]
                        pdf_swc_row["swc_host"] = pdf_dict.values()[0]["SWC"]["SWC_Host"]
                        pdf_swc_row["description"] = pdf_dict.values()[0]["SWC"]["Description"]

                        for key in pdf_swc_row.keys():
                            if not pdf_swc_row[key]:
                                pdf_swc_row[key] = ""


                        add_info_list = []

                        for key in pdf_dict.values()[0]:
                            if key == "SuppliersAdditionalInfo":
                                if not isinstance(pdf_dict.values()[0][key], list):
                                    add_info_list.append(pdf_dict.values()[0][key]["Additional_Data"]) 
                                else:
                                        for info in pdf_dict.values()[0][key]:
                                            for key in info.keys():
                                                if "Additional_Data" in key:
                                                    if info[key]:
                                                        add_info_list.append(info[key])
                                                    else:
                                                        continue
                                                




                        if not isinstance(pdf_dict.values()[0]["Test"]["TestCase"], dict):

                            for tc in pdf_dict.values()[0]["Test"]["TestCase"]:
                            
                                self.del_namespace(tc)

                                pdf_tc = {}
                                pdf_tc["bug_ref_list"] = []
                                pdf_tc["tcpriority"] = tc["@priority"]
                                pdf_tc["result"] = tc["TestCaseSummary"]["@result"]
                                pdf_tc["ID"] = tc["@ID"]
                                pdf_tc["Description"] = tc["Description"]
                                pdf_tc["begindate"] = tc["Begin"]["Date"]
                                pdf_tc["begintime"] = tc["Begin"]["Time"]
                                pdf_tc["enddate"] = tc["End"]["Date"]
                                pdf_tc["endtime"] = tc["End"]["Time"]
                                pdf_tc["Comment"] = tc["Comment"]

                                for item in tc.keys():
                                    if item == "BugReference":
                                        if tc[item] == None:
                                            pdf_tc["bug_ref_list"].append("")
                                        else:
                                            pdf_tc["bug_ref_list"].append(tc[item])
                                            break
                                        
                                pdf_tc_list.append(pdf_tc)
                        else:
                            tc = pdf_dict.values()[0]["Test"]["TestCase"]

                            pdf_tc = {}
                            pdf_tc["bug_ref_list"] = []
                            pdf_tc["tcpriority"] = tc["@priority"]
                            pdf_tc["result"] = tc["TestCaseSummary"]["@result"]
                            pdf_tc["ID"] = tc["@ID"]
                            pdf_tc["Description"] = tc["Description"]
                            pdf_tc["begindate"] = tc["Begin"]["Date"]
                            pdf_tc["Comment"] = tc["Comment"]


                        for key in pdf_tc.keys():
                            if not pdf_tc[key]:
                                pdf_tc[key] = ""
                            if key.startswith("@"):
                                pdf_tc[key[1:]] = pdf_tc[key]
                                del pdf_tc[key]

                        pdf_tc_list.append(pdf_tc)


                        for tc in pdf_tc_list:
                            for key in tc.keys():
                                if not tc[key]:
                                    tc[key] = ""



                        pdf_sup_ta_list = pdf_dict.values()[0]["SupliersTestArtefacts"]["TestArtefact"]

                        for ta in pdf_sup_ta_list:
                            for key in ta.keys():
                                if not ta[key]:
                                    ta[key] = ""

                        pdf_int_ta_list = pdf_dict.values()[0]["IntegratorsTestArtefacts"]["TestArtefact"]

                        for ta in pdf_int_ta_list:
                            for key in ta.keys():
                                if not ta[key]:
                                    ta[key] = ""
                        
                        if isinstance(pdf_dict.values()[0]["RevisionHistory"]["Revision"], list):
                            for rev in pdf_dict.values()[0]["RevisionHistory"]["Revision"]:
                                pdf_rev = {}
                                pdf_rev["Document_Version"] = rev["Document_Version"]
                                pdf_rev["Date"] = rev["Date"]
                                pdf_rev["ResponsiblePerson"] = rev["ResponsiblePerson"]
                                pdf_rev["Description"] = rev["Description"]

                                for key in pdf_rev.keys():
                                    if not pdf_rev[key]:
                                        pdf_rev[key] = ""

                                pdf_rev_list.append(pdf_rev)

                        elif isinstance(pdf_dict.values()[0]["RevisionHistory"]["Revision"], dict):
                            pdf_rev = {}
                            for data in pdf_dict.values()[0]["RevisionHistory"]["Revision"]:
                                pdf_rev[data] = pdf_dict.values()[0]["RevisionHistory"]["Revision"][data]

                                for key in pdf_rev.keys():
                                    if not pdf_rev[key]:
                                        pdf_rev[key] = ""


                            pdf_rev_list.append(pdf_rev)

                            pdf_tool = {}
                            pdf_tool["SoftwareName"] = pdf_dict.values()[0]["TestEnvironmentDefinition"]["AdditionalSoftwareUsed"]["AdditionalTool"].values()[1]
                            pdf_tool["Version"] = pdf_dict.values()[0]["TestEnvironmentDefinition"]["AdditionalSoftwareUsed"]["AdditionalTool"].values()[2]
                            pdf_tool["Description"] = pdf_dict.values()[0]["TestEnvironmentDefinition"]["AdditionalSoftwareUsed"]["AdditionalTool"].values()[3]

                            for key in pdf_tool.keys():
                                    if not pdf_tool[key]:
                                        pdf_tool[key] = ""
                            pdf_add_tool_list.append(pdf_tool)

                        try:
                            for ta in pdf_sup_ta_list:
                                self.del_namespace(ta)
                            for ta in pdf_int_ta_list:
                                self.del_namespace(ta)


                            

                            pdf_exporter.main(self, sub_dir[0], file_name, pdf_release_data, pdf_swc_data, pdf_swc_row,
                            pdf_tc_list, pdf_sup_ta_list, pdf_int_ta_list, pdf_rev_list, pdf_add_tool_list, add_info_list)
                            self.succ_file_list.append(file_name)
                            self.exported_num += 1
                            self.status_text.SetStatusText("Generating PDF files... " + "(" + str(self.exported_num) + "/" + str(len(sub_dir_list[1:])) + ")", 1)
                        except Exception as ex:
                            self.exported_num += 1
                            self.status_text.SetStatusText("Generating PDF files... " + "(" + str(self.exported_num) + "/" + str(len(sub_dir_list[1:])) + ")", 1)

                            if "Permission denied" in str(ex):
                                err_desc = "File open in another program"
                            self.fail_file_list.append((file_name, err_desc))
                            print ex

        wx.CallAfter(self.export_done)


    def export_done(self):                     #3


####################################################################################
        # VRATITI SLIKU
        self.toolbar.Freeze()
        self.export_all_tool.SetShortHelp("Export all to PDF")
        self.export_all_tool.SetLongHelp("Export all AATR XML files in the " +
                                    "TestReport directory to their " +
                                    "respective PDF files")
        img = wx.Image(os.path.join(CURRENT_DIR, 'icons', 'pdf_all.png'))
        img.Rescale(25, 25)
        image = wx.Bitmap(img)
        self.export_all_tool.SetNormalBitmap(image)
        self.toolbar.Realize()
        self.toolbar.Refresh()
        self.toolbar.Thaw()
####################################################################################

        if self.stopped == False:
            self.status_text.SetStatusText("PDF generation complete!", 1)
        else:
            self.status_text.SetStatusText("PDF generation interrupted!", 1)

        self.status_text.SetStatusText("", 2)


        result_dlg = PDFDialog(self, self.succ_file_list, self.fail_file_list, self.tr_path, self.file_num)
        
        result = result_dlg.ShowModal()


        self.status_text.SetStatusText("", 1)

        self.Bind(wx.EVT_TOOL, self.export_pdf_all_on_menu, self.export_all_tool)

    def stop_export(self, e):
        self.stopped = True
        print "EXPORT STOPPED"


    def statusbar_status(self, event):
        """Polemos: Change default statusbar field for showing menu help."""
        event_catcher = event.GetId()
        try: msg = self.menubar.GetHelpString(event_catcher)
        except: pass
        try: self.status_text.SetStatusText(msg, 1)
        except: self.status_text.SetStatusText('', 1) # Resets.


    def _edit_search_on_menu(self, event):

        if self.FindFocus() != self.search:
            self.old_focus = self.FindFocus()

        if self.FindFocus() == self.search:
            self.old_focus.SetFocus()
            print "SEARCH OFF"

        else:
            self.search.SetFocus()
            print "SEARCH ON"


    def _edit_add_on_menu(self, event):
        self.context_menu_add(event)

    def _edit_del_on_menu(self, event):
        self.context_menu_delete(event)

    def _options_pref_on_menu(self, event):
        print "OPTIONS --> PREFS"

        dialogs = PrefsDialog(self)
        dialogs.ShowModal()

    def _help_on_menu(self, event):
        print "HELP --> ABOUT"

        info = wx.adv.AboutDialogInfo()
        info.SetName("XML Editor")
        info.SetVersion("4.20")
        info.SetDescription("AAT Test Report XML Editor")
        info.SetCopyright("(C) 2019")
        info.AddDeveloper("Stefan Stojanović")

        wx.adv.AboutBox(info)

    def spl_vert_on_idle(self):
        self.spl_vert.SetSashPosition(270)
        self.spl_vert.Unbind(wx.EVT_IDLE)


    def spl_horiz_on_idle(self):
        self.spl_horiz.SetSashPosition(-50)
        self.spl_horiz.Unbind(wx.EVT_IDLE)


    def on_mouse_enter(self, event):
        if event.GetEventObject() == self.tree:
            if self.FindFocus() == self.search:
                return
            else:
                self.tree.SetFocus()
        elif event.GetEventObject() == self.toolbar:

            tool_id = event.GetSelection()
            if tool_id != -1:
                event_object = event.GetEventObject()
                tool = event_object.FindById(tool_id)  
                text = tool.GetLongHelp()

        elif event.GetEventObject() == self.tab_parsed or event.GetEventObject() == self.panel_desc:
            if self.FindFocus() == self.search:
                return
            else:
                panel = event.GetEventObject()
                panel.SetFocus()
            if isinstance(self.FindFocus(), wx.Choice):
                child_list = panel.GetChildren()
                for child in child_list:
                    if isinstance(child, ExpandoTextCtrl):
                        child.SetFocus()
                        break
                    if child == child_list[-1]:
                        self.panel_desc.SetFocus()
                
            if isinstance(self.FindFocus(), ExpandoTextCtrl):
                self.FindFocus().SetInsertionPointEnd()

    def on_mouse_leave(self, event):
        if event.GetEventObject() == self.toolbar:
            self.status_text.SetStatusText("")


    def tree_fill(self):

        global tag_dict
        tree = self.tree

        self.del_namespace(tag_dict)

        root = tag_dict.keys()[0]
        root = tree.AddRoot(root)

        self.tree.SetItemImage(root, 0,
                               which=icon_normal)
        self.tree.SetItemImage(root, 1,
                               which=icon_exp)

        dikt = tag_dict.values()[0]

        def add_elem(dikt, parent):
            for k, v in dikt.items():
                if isinstance(v, dict):

                    if k == "TestCaseTable":

                        if v["@name"]:
                            tct_name = "TestCaseTable [" + v["@name"] + "]"
                            item = self.tree.AppendItem(parent,
                                                        tct_name,
                                                        data=None)
                        else:
                            item = self.tree.AppendItem(parent, k, data=None)
                        self.tree.SetItemImage(item, 0,
                                               which=icon_normal)
                        self.tree.SetItemImage(item, 1,
                                               which=icon_exp)

                        self.tree.SetItemData(item, v)
                        self.load_table(v, item)

                        break
                    item = self.tree.AppendItem(parent, k, data=None)
                    self.tree.SetItemImage(item, 0,
                                           which=icon_normal)
                    self.tree.SetItemImage(item, 1,
                                           which=icon_exp)

                    if self.tree.GetItemText(item) == "Test":
                        val = v["@integrationRecommendationResult"]
                        rec_item = self.tree.AppendItem(item,
                                                        "integrationRecommendationResult",
                                                        data=val)

                        self.tree.SetItemImage(rec_item, 0,
                                            which=icon_normal)
                        self.tree.SetItemImage(rec_item, 1,
                                            which=icon_exp)



                    add_elem(v, item)

                else:

                    if k == "TestCase":
                        self.load_test_case(v, parent)
                        continue

                    text_parent = self.tree.GetItemText(parent)
                    if text_parent == "SupliersTestArtefacts":
                        for ta in v:
                            if ta == "{":
                                self.add_ta(parent)
                                break
                            else:
                                for ta in v:
                                    self.load_sup_ta(ta, parent)
                                break

                    if text_parent == "IntegratorsTestArtefacts":
                        for ta in v:
                            if ta == "{":
                                self.add_ta(parent)
                                break
                            else:
                                for ta in v:
                                    self.load_int_ta(ta, parent)
                                break

                    if (k.startswith("@x") or k.startswith("#") or
                            k.startswith("@desc")):
                        continue

                    if k.startswith("@"):
                        k = k[1:]
                        if k == "integrationRecommendationResult":
                            continue
                    if k != "TestArtefact":
                        item = self.tree.AppendItem(parent, k, data=None)
                        self.tree.SetItemImage(item, 0,
                                               which=icon_normal)
                        self.tree.SetItemImage(item, 1,
                                               which=icon_exp)

                    if isinstance(v, list):
                        continue
                    else:
                        self.tree.SetItemData(item, v)

        add_elem(dikt, root)
        tree.Expand(root)

        if "Acronyms" in tag_dict.values()[0]:
            for acronym in tag_dict.values()[0]["Acronyms"]:
                if acronym == "@desc":
                    continue

    def load_table(self, v, parent):

        if isinstance(v, dict):
            self.del_namespace(v)
            for a, b in v.items():
                if a.startswith("@"):
                    item = self.tree.AppendItem(parent, a[1:], data=None)
                    self.tree.SetItemImage(item, 0,
                                           which=icon_normal)
                    self.tree.SetItemImage(item, 1,
                                           which=icon_exp)

                    self.tree.SetItemData(item, b)
                else:
                    item = self.tree.AppendItem(parent, a, data=None)
                    self.tree.SetItemImage(item, 0,
                                           which=icon_normal)
                    self.tree.SetItemImage(item, 1,
                                           which=icon_exp)

                    self.tree.SetItemData(item, b)

                if isinstance(b, (dict, list)):
                    if self.tree.GetItemText(item) == "TableHeader":
                        if "TableCell" in b and isinstance(b["TableCell"], list):
                            self.loadCells(item, b)
                            continue

                    elif self.tree.GetItemText(item) == "TableRow":
                        self.load_row(item, b)
                        continue

                    self.load_table(b, item)

        elif isinstance(v, list):
            for a in v:
                self.load_table(a, parent)

    def loadCells(self, parent, cell_list):
        cell_list = cell_list.values()[0]
        for cell in cell_list:
            item = self.tree.AppendItem(parent, "TableCell", data=None)
            self.tree.SetItemImage(item, 0, which=icon_normal)
            self.tree.SetItemImage(item, 1, which=icon_exp)

            for i in cell:
                if i.startswith("@"):
                    child = self.tree.AppendItem(item, i[1:], data=None)
                    self.tree.SetItemImage(item, 0,
                                           which=icon_normal)
                    self.tree.SetItemImage(item, 1,
                                           which=icon_exp)

                elif i == "#text":
                    child = self.tree.AppendItem(item, "value", data=None)
                    self.tree.SetItemImage(item, 0,
                                           which=icon_normal)
                    self.tree.SetItemImage(item, 1,
                                           which=icon_exp)

                self.tree.SetItemData(child, cell[i])

    def load_row(self, parent, cell_list):

        for cell in cell_list:
            item = self.tree.AppendItem(parent, "TableRow", data=None)
            self.tree.SetItemImage(item, 0,
                                   which=icon_normal)
            self.tree.SetItemImage(item, 1,
                                   which=icon_exp)

            self.del_namespace(cell)
            for i in range(0, 3):
                child = self.tree.AppendItem(item, "TableCell", data=None)
                self.tree.SetItemImage(child, 0,
                                       which=icon_normal)
                self.tree.SetItemImage(child, 1,
                                       which=icon_exp)

                if isinstance(cell, dict):
                    self.tree.SetItemData(child, cell.values()[0][i])
                else:
                    self.tree.SetItemData(child, "")

    def load_test_case(self, v, parent):

        for case in v:
            self.del_namespace(case)
            if case["Name"]:
                item = self.tree.AppendItem(parent,
                                            "TestCase [" + case["Name"] + "]",
                                            data=None)
            else:
                item = self.tree.AppendItem(parent,
                                            "TestCase",
                                            data=None)


            self.tree.SetItemImage(item, 0,
                                   which=icon_normal)
            self.tree.SetItemImage(item, 1,
                                   which=icon_exp)

            for key in case:

                if key == "BugReference":
                    if isinstance(case[key], list):

                        for bug_ref in case[key]:
    
                            child = self.tree.AppendItem(item, key, data=None)
                            self.tree.SetItemImage(child, 0,
                                                which=icon_normal)
                            self.tree.SetItemImage(child, 1,
                                                which=icon_exp)
                            if bug_ref != "None":
                                self.tree.SetItemData(child, bug_ref)
                    else:

                        child = self.tree.AppendItem(item, key, data=None)
                        self.tree.SetItemImage(child, 0,
                                            which=icon_normal)
                        self.tree.SetItemImage(child, 1,
                                            which=icon_exp)

                    continue

                elif key.startswith("@"):
                    if key == "@desc":
                        continue
                    child = self.tree.AppendItem(item, key[1:], data=None)
                    self.tree.SetItemImage(child, 0,
                                           which=icon_normal)
                    self.tree.SetItemImage(child, 1,
                                           which=icon_exp)
                else:
                    child = self.tree.AppendItem(item, key, data=None)
                    self.tree.SetItemImage(child, 0,
                                           which=icon_normal)
                    self.tree.SetItemImage(child, 1,
                                           which=icon_exp)

                if isinstance(case[key], dict):
                    for g in case[key]:
                        g_child = self.tree.AppendItem(child, g, data=None)

                        self.tree.SetItemImage(g_child, 0,
                                               which=icon_normal)
                        self.tree.SetItemImage(g_child, 1,
                                               which=icon_exp)

                        self.tree.SetItemData(g_child, case[key][g])
                self.tree.SetItemData(child, case[key])

    def load_sup_ta(self, v, parent):

        if isinstance(v, dict):
            self.del_namespace(v)

        if "Filename" in v and v["Filename"]:
            item = self.tree.AppendItem(parent,
                                        "TestArtefact [" + v["Filename"] + "]",
                                        data=None)

            self.tree.SetItemImage(item, 0,
                                   which=icon_normal)
            self.tree.SetItemImage(item, 1,
                                   which=icon_exp)

        else:
            item = self.tree.AppendItem(parent, "TestArtefact", data=None)
            self.tree.SetItemImage(item, 0,
                                   which=icon_normal)
            self.tree.SetItemImage(item, 1,
                                   which=icon_exp)

        for case in v:
            child = self.tree.AppendItem(item, case, data=None)
            self.tree.SetItemImage(child, 0,
                                   which=icon_normal)
            self.tree.SetItemImage(child, 1,
                                   which=icon_exp)

            self.tree.SetItemData(child, v[case])

    def load_int_ta(self, v, parent):

        if isinstance(v, dict):
            self.del_namespace(v)

        if "Filename" in v and v["Filename"]:
            item = self.tree.AppendItem(parent,
                                        "TestArtefact [" + v["Filename"] + "]",
                                        data=None)

            self.tree.SetItemImage(item, 0,
                                   which=icon_normal)
            self.tree.SetItemImage(item, 1,
                                   which=icon_exp)

        else:
            item = self.tree.AppendItem(parent, "TestArtefact", data=None)

            self.tree.SetItemImage(item, 0,
                                   which=icon_normal)
            self.tree.SetItemImage(item, 1,
                                   which=icon_exp)

        for case in v:
            child = self.tree.AppendItem(item, case, data=None)

            self.tree.SetItemImage(item, 0,
                                   which=icon_normal)
            self.tree.SetItemImage(item, 1,
                                   which=icon_exp)

            self.tree.SetItemData(child, v[case])

    def add_test_case(self, parent):
        print "EDIT --> ADD CHILD --> TEST CASE"
        parent = self.tree.GetSelection()
        new_case = {}
        self.file_modified = 1
        frame.SetTitle(appname + ' - ' + filename + "*")

        path = os.path.join(CURRENT_DIR, 'templates', 'test_case.template')
        with open(path) as fd:
            new_case = json.loads(json.dumps(xmltodict.parse(fd.read())))

        item = self.tree.AppendItem(parent, "TestCase", data=None)

        self.tree.SetItemImage(item, 0,
                               which=icon_normal)
        self.tree.SetItemImage(item, 1,
                               which=icon_exp)

        for e in new_case["TestCase"]:
            if "desc" in e:
                continue
            elif e.startswith("@") and "desc" not in e:
                child = self.tree.AppendItem(item, e[1:], data=None)

                self.tree.SetItemImage(child, 0,
                                       which=icon_normal)
                self.tree.SetItemImage(child, 1,
                                       which=icon_exp)

            else:
                child = self.tree.AppendItem(item, e, data=None)

                self.tree.SetItemImage(child, 0,
                                       which=icon_normal)
                self.tree.SetItemImage(child, 1,
                                       which=icon_exp)

            if isinstance(new_case['TestCase'][e], dict):
                for g in new_case['TestCase'][e]:
                    if g.startswith("@"):
                        g_child = self.tree.AppendItem(child, g[1:], data=None)

                        self.tree.SetItemImage(g_child, 0,
                                               which=icon_normal)
                        self.tree.SetItemImage(g_child, 1,
                                               which=icon_exp)

                    else:
                        g_child = self.tree.AppendItem(child, g, data=None)

                        self.tree.SetItemImage(g_child, 0,
                                               which=icon_normal)
                        self.tree.SetItemImage(g_child, 1,
                                               which=icon_exp)

                    self.tree.SetItemData(g_child, new_case['TestCase'][e][g])

            self.tree.SetItemData(item, new_case["TestCase"][e])
        self.status_text.SetStatusText("Element added: TestCase")

    def add_test_caseTable(self, parent):
        print "EDIT --> ADD CHILD --> TEST CASE TABLE"

        parent = self.tree.GetSelection()
        new_table = {}
        self.file_modified = 1
        frame.SetTitle(appname + ' - ' + filename + "*")

        path = os.path.join(CURRENT_DIR, 'templates', 'tct.template')
        with open(path) as fd:
            new_table = json.loads(json.dumps(xmltodict.parse(fd.read())))

        item = self.tree.AppendItem(parent, "TestCaseTable", data=None)

        self.tree.SetItemImage(item, 0, which=icon_normal)
        self.tree.SetItemImage(item, 1, which=icon_exp)

        for e in new_table["TestCaseTable"]:

            if e.startswith("@"):
                f = e[1:]
                child = self.tree.AppendItem(item, f, data=None)
            else:
                child = self.tree.AppendItem(item, e, data=None)

            self.tree.SetItemImage(child, 0, which=icon_normal)
            self.tree.SetItemImage(child, 1, which=icon_exp)

            if isinstance(new_table["TestCaseTable"][e], dict):

                for g in new_table['TestCaseTable'][e]:
                    if g.startswith("@"):
                        g_child = self.tree.AppendItem(child, g[1:], data=None)

                        self.tree.SetItemImage(g_child, 0,
                                               which=icon_normal)
                        self.tree.SetItemImage(g_child, 1,
                                               which=icon_exp)

                    else:
                        g_child = self.tree.AppendItem(child, g, data=None)

                        self.tree.SetItemImage(g_child, 0,
                                               which=icon_normal)
                        self.tree.SetItemImage(g_child, 1,
                                               which=icon_exp)

                    if isinstance(new_table['TestCaseTable'][e], dict):
                        if new_table['TestCaseTable'][e][g]:
                            for gg in new_table['TestCaseTable'][e][g]:
                                if gg.startswith("@"):
                                    gg_child = self.tree.AppendItem(g_child,
                                                                    gg[1:],
                                                                    data=None)

                                    self.tree.SetItemImage(gg_child, 0,
                                                           which=icon_normal)
                                    self.tree.SetItemImage(gg_child, 1,
                                                           which=icon_exp)

                                else:
                                    gg_child = self.tree.AppendItem(g_child,
                                                                    gg,
                                                                    data=None)

                                    self.tree.SetItemImage(gg_child, 0,
                                                           which=icon_normal)
                                    self.tree.SetItemImage(gg_child, 1,
                                                           which=icon_exp)

                                gg_Text = new_table['TestCaseTable'][e][g][gg]
                                self.tree.SetItemData(gg_child,
                                                      gg_Text)

            self.status_text.SetStatusText("Element added: TestCaseTable")

    def add_table_row(self, parent):
        print "EDIT --> ADD CHILD --> TABLE ROW"

        self.file_modified = 1
        frame.SetTitle(appname + ' - ' + filename + "*")

        item = self.tree.AppendItem(parent, "TableRow", data=None)
        self.tree.SetItemImage(item, 0,
                               which=icon_normal)
        self.tree.SetItemImage(item, 1,
                               which=icon_exp)

        child = self.tree.AppendItem(item, "TableCell", data=None)
        self.tree.SetItemImage(child, 0,
                               which=icon_normal)
        self.tree.SetItemImage(child, 1,
                               which=icon_exp)
        
        self.status_text.SetStatusText("Element added: TableRow")

    def add_table_cell(self, parent):
        print "EDIT --> ADD CHILD --> TABLE CELL (HEADER)"

        self.file_modified = 1
        frame.SetTitle(appname + ' - ' + filename + "*")

        item = self.tree.AppendItem(parent, "TableCell", data=None)
        self.tree.SetItemImage(item, 0,
                               which=icon_normal)
        self.tree.SetItemImage(item, 1,
                               which=icon_exp)

        align_item = self.tree.AppendItem(item, "align", data=None)
        self.tree.SetItemImage(align_item, 0,
                               which=icon_normal)
        self.tree.SetItemImage(align_item, 1,
                               which=icon_exp)

        width_item = self.tree.AppendItem(item, "width", data=None)
        self.tree.SetItemImage(width_item, 0,
                               which=icon_normal)
        self.tree.SetItemImage(width_item, 1,
                               which=icon_exp)

        value_item = self.tree.AppendItem(item, "value", data=None)
        self.tree.SetItemImage(value_item, 0,
                               which=icon_normal)
        self.tree.SetItemImage(value_item, 1,
                               which=icon_exp)

        self.status_text.SetStatusText("Element added: TableCell")

    def add_acronym(self, parent):
        print "EDIT --> ADD CHILD --> ACRONYM"

        self.file_modified = 1
        frame.SetTitle(appname + ' - ' + filename + "*")

        new_acronym = {}
        path = os.path.join(CURRENT_DIR, 'templates', 'acronym.template')
        with open(path) as fd:
            new_acronym = json.loads(json.dumps(xmltodict.parse(fd.read())))

        item = self.tree.AppendItem(parent, "Acronym", data=None)

        self.tree.SetItemImage(item, 0,
                               which=icon_normal)
        self.tree.SetItemImage(item, 1,
                               which=icon_exp)

        for e in new_acronym["Acronym"]:
            child = self.tree.AppendItem(item, e, data=None)

            self.tree.SetItemImage(child, 0,
                                   which=icon_normal)
            self.tree.SetItemImage(child, 1,
                                   which=icon_exp)

            self.tree.SetItemData(item, new_acronym["Acronym"][e])
        self.status_text.SetStatusText("Element added: Acronym")

    def add_reference(self, parent):
        print "EDIT --> ADD CHILD --> REFERENCE"

        self.file_modified = 1
        frame.SetTitle(appname + ' - ' + filename + "*")

        new_reference = {}
        path = os.path.join(CURRENT_DIR, 'templates', 'reference.template')
        with open(path) as fd:
            new_reference = json.loads(json.dumps(xmltodict.parse(fd.read())))

        item = self.tree.AppendItem(parent, "Reference", data=None)

        self.tree.SetItemImage(item, 0,
                               which=icon_normal)
        self.tree.SetItemImage(item, 1,
                               which=icon_exp)

        for e in new_reference["Reference"]:
            child = self.tree.AppendItem(item, e, data=None)

            self.tree.SetItemImage(child, 0,
                                   which=icon_normal)
            self.tree.SetItemImage(child, 1,
                                   which=icon_exp)

            self.tree.SetItemData(item, new_reference["Reference"][e])
        self.status_text.SetStatusText("Element added: Reference")

    def add_ta(self, parent):
        print "EDIT --> ADD CHILD --> TEST ARTEFACT"

        self.file_modified = 1
        frame.SetTitle(appname + ' - ' + filename + "*")

        new_ta = {}
        path = os.path.join(CURRENT_DIR, 'templates', 'test_artefact.template')
        with open(path) as fd:
            new_ta = json.loads(json.dumps(xmltodict.parse(fd.read())))

        item = self.tree.AppendItem(parent, "TestArtefact", data=None)

        self.tree.SetItemImage(item, 0,
                               which=icon_normal)
        self.tree.SetItemImage(item, 1,
                               which=icon_exp)

        for e in new_ta["TestArtefact"]:
            child = self.tree.AppendItem(item, e, data=None)

            self.tree.SetItemImage(child, 0,
                                   which=icon_normal)
            self.tree.SetItemImage(child, 1,
                                   which=icon_exp)

            self.tree.SetItemData(item, new_ta["TestArtefact"][e])
        self.status_text.SetStatusText("Element added: TestArtefact")

    def add_tool(self, parent):
        print "EDIT --> ADD CHILD --> TOOL"

        self.file_modified = 1
        frame.SetTitle(appname + ' - ' + filename + "*")

        new_tool = {}
        path = os.path.join(CURRENT_DIR,
                            'templates',
                            'add_tool.template')

        with open(path) as fd:
            new_tool = json.loads(json.dumps(xmltodict.parse(fd.read())))

        item = self.tree.AppendItem(parent, "AdditionalTool", data=None)

        self.tree.SetItemImage(item, 0,
                               which=icon_normal)
        self.tree.SetItemImage(item, 1,
                               which=icon_exp)

        for e in new_tool["AdditionalTool"]:
            child = self.tree.AppendItem(item, e, data=None)

            self.tree.SetItemImage(child, 0,
                                   which=icon_normal)
            self.tree.SetItemImage(child, 1,
                                   which=icon_exp)

            self.tree.SetItemData(item, new_tool["AdditionalTool"][e])
        self.status_text.SetStatusText("Element added: AdditionalTool")

    def add_info(self, event):
        print "EDIT --> ADD CHILD --> INFO"

        self.file_modified = 1
        frame.SetTitle(appname + ' - ' + filename + "*")

        root = self.tree.GetRootItem()
        item = self.tree.AppendItem(root, "SuppliersAdditionalInfo", data=None)

        self.tree.SetItemImage(item, 0,
                               which=icon_normal)

        self.tree.SetItemImage(item, 1,
                               which=icon_exp)

        child = self.tree.AppendItem(item, "Additional_Data", data=None)

        self.tree.SetItemImage(child, 0,
                               which=icon_normal)

        self.tree.SetItemImage(child, 1,
                               which=icon_exp)

        self.status_text.SetStatusText("Element added: SuppliersAdditionalInfo")

    def add_known_lim(self, event):
        print "EDIT --> ADD CHILD --> KNOWN LIM"

        self.file_modified = 1
        frame.SetTitle(appname + ' - ' + filename + "*")

        root = self.tree.GetRootItem()

        item = self.tree.AppendItem(root, "KnownLimitation", data=None)
        self.tree.SetItemImage(item, 0,
                               which=icon_normal)
        self.tree.SetItemImage(item, 1,
                               which=icon_exp)

        child = self.tree.AppendItem(item, "CompanyIssueIdentifier", data=None)
        self.tree.SetItemImage(child, 0,
                               which=icon_normal)
        self.tree.SetItemImage(child, 1,
                               which=icon_exp)

        child_2 = self.tree.AppendItem(item, "Description", data=None)
        self.tree.SetItemImage(child_2, 0,
                               which=icon_normal)
        self.tree.SetItemImage(child_2, 1,
                               which=icon_exp)

        self.status_text.SetStatusText("Element added: KnownLimitation")
        

    def add_revision(self, parent):
        print "EDIT --> ADD CHILD --> REVISION"

        self.file_modified = 1
        frame.SetTitle(appname + ' - ' + filename + "*")

        new_revision = {}
        path = os.path.join(CURRENT_DIR, 'templates', 'revision.template')
        with open(path) as fd:
            new_revision = json.loads(json.dumps(xmltodict.parse(fd.read())))

        item = self.tree.AppendItem(parent, "Revision", data=None)

        self.tree.SetItemImage(item, 0,
                               which=icon_normal)
        self.tree.SetItemImage(item, 1,
                               which=icon_exp)

        for e in new_revision["Revision"]:
            if e == "@desc":
                continue
            child = self.tree.AppendItem(item, e, data=None)

            self.tree.SetItemImage(child, 0,
                                   which=icon_normal)
            self.tree.SetItemImage(child, 1,
                                   which=icon_exp)

            self.tree.SetItemData(item, new_revision["Revision"][e])
        self.status_text.SetStatusText("Element added: Revision")

    def del_namespace(self, dikt):
        try:
            for k, v in dikt.items():
                if k.startswith("ns"):
                    new_key = k[4:]
                    dikt[new_key] = v
                    del dikt[k]
                if isinstance(v, dict):
                    self.del_namespace(v)
        except Exception as ex:
            pass

    def create_blank_file(self):
        print "FILE --> NEW"
        global tag_dict
        global filename

        self.tree.DeleteAllItems()
        self.b_sizer_parsed.Clear(True)
        with open(BLANK_TEMPLATE) as fd:
            parse_file = xmltodict.parse(fd)
        tag_dict = json.loads(json.dumps(parse_file))

        self.tree_fill()
        filename = "Untitled"
        frame.SetTitle(appname + ' - ' + filename)
        self.toolbar.EnableTool(wx.ID_SAVE, True)
        self.toolbar.EnableTool( self.ID_EXPORT, True)
        self.search.Show()
        self.status_text.SetStatusText("New file created!")
        self.file_modified = 0
        self.panel_left.Layout()

    def save_data(self):

        del rev_list[:]         # SKLONI NA KRAJU
        del ref_list[:]
        del tc_list[:]
        del acr_list[:]
        del sup_ta_list[:]
        del add_tool_list[:]
        del add_data_list[:]
        del int_ta_list[:]
        del limit_list[:]
        del tct_list[:]

        root = self.tree.GetRootItem()

        if root:
            child = self.tree.GetFirstChild(root)[0]
            while child:
                child_text = self.tree.GetItemText(child)
                child_data = self.tree.GetItemData(child)

                if child_text == "Platform":
                    if child_data:
                        release_data["platform"] = child_data
                    else:
                        release_data["platform"] = ""
                    child = self.tree.GetNextSibling(child)
                    continue
                elif child_text == "Release":
                    if child_data:
                        release_data["release"] = child_data
                    else:
                        release_data["release"] = ""
                    child = self.tree.GetNextSibling(child)
                    continue
                elif child_text == "Comment":
                    if child_data:
                        swc_data["comment"] = child_data
                    else:
                        swc_data["comment"] = ""
                    child = self.tree.GetNextSibling(child)
                    continue
                elif child_text == "SWC":
                    self.save_class(child, swc_row)
                    child = self.tree.GetNextSibling(child)
                    continue
                elif (child_text == "DocumentInfo" or
                    child_text == "TestEnvironmentDefinition" or
                    child_text == "MisraMeasurement" or
                    child_text == "TestManagement"):

                    self.save_class(child, swc_data)
                    child = self.tree.GetNextSibling(child)
                    continue

                elif (child_text == "RevisionHistory" or
                    child_text == "Test" or
                    child_text == "SupliersTestArtefacts" or
                    child_text == "IntegratorsTestArtefacts" or
                    child_text == "Acronyms" or
                    child_text == "References"):

                    self.save_instance(child)

                elif child_text == "SuppliersAdditionalInfo":
                    self.save_instance(child)

                elif child_text == "KnownLimitation":
                    klasa = classes.Limitation()
                    sub_child = self.tree.GetFirstChild(child)[0]
                    while sub_child.IsOk():
                        s_child_text = self.tree.GetItemText(sub_child)
                        s_child_data = self.tree.GetItemData(sub_child)

                        if s_child_data:
                            s_child_data = s_child_data
                            klasa[s_child_text] = s_child_data
                        else:
                            klasa[s_child_text] = ""
                        sub_child = self.tree.GetNextSibling(sub_child)
                    limit_list.append(klasa)

                child = self.tree.GetNextSibling(child)

    def save_class(self, item, klasa):
        (child, cookie) = self.tree.GetFirstChild(item)
        while child.IsOk():
            c_text = self.tree.GetItemText(child)
            c_data = self.tree.GetItemData(child)

            if not self.tree.ItemHasChildren(child):


                if c_text.lower() == "swc_asil_level":

                    if isinstance(c_data, int):
                        if c_data == 0:
                            klasa[c_text.lower()] = "QM"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data == 1:
                            klasa[c_text.lower()] = "A"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data == 2:
                            klasa[c_text.lower()] = "B"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data == 3:
                            klasa[c_text.lower()] = "C"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data == 4:
                            klasa[c_text.lower()] = "D"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                    elif isinstance(c_data, (str, unicode)):
                        if c_data.lower() == "qm":
                            klasa[c_text.lower()] = "QM"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data.lower() == "a":
                            klasa[c_text.lower()] = "A"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data.lower() == "b":
                            klasa[c_text.lower()] = "B"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data.lower() == "c":
                            klasa[c_text.lower()] = "C"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data.lower() == "d":
                            klasa[c_text.lower()] = "D"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                    else:
                        (child, cookie) = self.tree.GetNextChild(item, cookie)
                        continue

                elif c_text.lower() == "swc_host":

                    if isinstance(c_data, int):
                        if c_data == 0:
                            klasa[c_text.lower()] = "APH"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data == 1:
                            klasa[c_text.lower()] = "SSH"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data == 2:
                            klasa[c_text.lower()] = "SRH"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                    elif isinstance(c_data, (str, unicode)):
                        if c_data.lower() == "aph":
                            klasa[c_text.lower()] = "APH"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data.lower() == "ssh":
                            klasa[c_text.lower()] = "SSH"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data.lower() == "srh":
                            klasa[c_text.lower()] = "SRH"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                    else:
                        (child, cookie) = self.tree.GetNextChild(item, cookie)
                        continue

                elif c_text.lower() == "documentstatus":

                    if isinstance(c_data, int):
                        if c_data == 0:
                            klasa[c_text.lower()] = "Released"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data == 1:
                            klasa[c_text.lower()] = "draft"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data == 2:
                            klasa[c_text.lower()] = "in_work"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue

                    elif isinstance(c_data, (str,unicode)):
                        if c_data.lower() == "released":
                            klasa[c_text.lower()] = "Released"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data.lower() == "draft":
                            klasa[c_text.lower()] = "draft"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data.lower() == "in_work":
                            klasa[c_text.lower()] = "in_work"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                    else:
                        (child, cookie) = self.tree.GetNextChild(item, cookie)
                        continue

                elif c_text.lower() == "used_ait-fw_providedbyintegrator":

                    if isinstance(c_data, int):
                        if c_data == 0:
                            klasa[c_text.lower().replace("-", "")] = "yes"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data == 1:
                            klasa[c_text.lower().replace("-", "")] = "no"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                    elif isinstance(c_data, (str, unicode)):
                        if c_data.lower() == "yes":
                            klasa[c_text.lower().replace("-", "")] = "yes"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data.lower() == "no":
                            klasa[c_text.lower().replace("-", "")] = "no"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                    else:
                        (child, cookie) = self.tree.GetNextChild(item, cookie)
                        continue


                elif c_text.lower() == "allreportedviolationjustified":

                    if isinstance(c_data, int):
                        if c_data == 0:
                            klasa[c_text.lower()] = "yes"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data == 1:
                            klasa[c_text.lower()] = "no"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        else:
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                    elif isinstance(c_data, (str, unicode)):
                        if c_data.lower() == "yes":
                            klasa[c_text.lower()] = "yes"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        elif c_data.lower() == "no":
                            klasa[c_text.lower()] = "no"
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                        else:
                            (child, cookie) = self.tree.GetNextChild(item, cookie)
                            continue
                    else:
                        (child, cookie) = self.tree.GetNextChild(item, cookie)
                        continue

                else:
                    if "-" in c_text:
                        c_text_lower = c_text.lower()
                        if c_data:
                            klasa[c_text_lower.replace("-", "")] = c_data
                        else:
                            klasa[c_text_lower] = ""
                    else:
                        if c_data:
                            klasa[c_text.lower().replace("-", "")] = c_data
                        else:
                            klasa[c_text.lower()] = ""
                    (child, cookie) = self.tree.GetNextChild(item, cookie)
            else:
                if c_text.lower() == "additionalsoftwareused":
                    self.save_instance(child)
                else:
                    self.save_class(child, klasa)
                (child, cookie) = self.tree.GetNextChild(item, cookie)

    def save_instance(self, item):

        tag_int = "IntegratorsTestArtefacts"
        tag_sup = "SupliersTestArtefacts"
        tag_add_soft = "AdditionalSoftwareUsed"
        tag_add_info = "SuppliersAdditionalInfo"

        tag = self.tree.GetItemText(item)

        child = self.tree.GetFirstChild(item)[0]
        while child.IsOk():

            c_text = self.tree.GetItemText(child)
            c_data = self.tree.GetItemData(child)

            if tag == "RevisionHistory":
                klasa = classes.Revision()
            elif tag == "Test":
                klasa = classes.TestCase()
                klasa_1 = classes.TestCaseTable()
            elif tag == "References":
                klasa = classes.Reference()
            elif tag == "Acronyms":
                klasa = classes.Acronym()
            elif tag == tag_sup or tag == tag_int:
                klasa = classes.TestArtefact()
            elif tag == tag_add_soft:
                klasa = classes.AdditionalTool()

            elif tag == tag_add_info:
                klasa = classes.SupAddInfo()

                if c_data:
                    klasa[c_text] = c_data
                else:
                    klasa[c_text] = ""


            sub_child = self.tree.GetFirstChild(child)[0]
            while sub_child.IsOk():
                s_child_text = self.tree.GetItemText(sub_child)
                s_child_data = self.tree.GetItemData(sub_child)

                if s_child_text == "BugReference":
                    if s_child_data:
                        klasa.bug_ref_list.append(s_child_data)
                    else:
                        klasa.bug_ref_list.append("")

                elif s_child_text == "Begin":
                    sub = self.tree.GetFirstChild(sub_child)[0]
                    while sub.IsOk():
                        sub_text = self.tree.GetItemText(sub)
                        sub_data = self.tree.GetItemData(sub)
                        if sub_text == "Date":
                            if sub_data:
                                dt = wx.DateTime(wx.DateTime.Now())
                                klasa['begindate'] = sub_data
                            else:
                                dt = wx.DateTime(wx.DateTime.Now())
                                klasa['begindate'] = ""
                            sub = self.tree.GetNextSibling(sub)
                        elif sub_text == "Time":
                            if sub_data:
                                dt = wx.DateTime(wx.DateTime.Now())
                                klasa['begintime'] = sub_data
                            else:
                                dt = wx.DateTime(wx.DateTime.Now())
                                klasa['begintime'] = ""
                            sub = self.tree.GetNextSibling(sub)
                        else:
                            continue
                elif s_child_text == "End":
                    sub = self.tree.GetFirstChild(sub_child)[0]
                    while sub.IsOk():
                        sub_text = self.tree.GetItemText(sub)
                        sub_data = self.tree.GetItemData(sub)
                        if sub_text == "Date":
                            if sub_data:
                                klasa['enddate'] = sub_data
                            else:
                                dt = wx.DateTime
                                klasa['enddate'] = ""
                            sub = self.tree.GetNextSibling(sub)
                        elif sub_text == "Time":
                            if sub_data:
                                klasa['endtime'] = sub_data
                            else:
                                dt = wx.DateTime
                                klasa['endtime'] = ""
                            sub = self.tree.GetNextSibling(sub)
                        else:
                            continue

                elif s_child_text == "TestCaseSummary":
                    sub = self.tree.GetFirstChild(sub_child)[0]
                    while sub.IsOk():
                        sub_text = self.tree.GetItemText(sub)
                        sub_data = self.tree.GetItemData(sub)
                        if "result" in sub_text:

                            if isinstance(sub_data, int):
                                if sub_data == 0:
                                    klasa['result'] = "passed"
                                elif sub_data == 1:
                                    klasa['result'] = "failed"
                                elif sub_data == 2:
                                    klasa['result'] = "not_executed"
                            elif isinstance(sub_data, (str, unicode)):
                                if sub_data.lower() == "passed":
                                    klasa['result'] = "passed"
                                elif sub_data.lower() == "failed":
                                    klasa['result'] = "failed"
                                elif sub_data.lower() == "not_executed":
                                    klasa['result'] = "not_executed"

                            sub = self.tree.GetNextSibling(sub)
                        elif sub_text == "Ratio_A":
                            if sub_data:
                                klasa['Ratio_A'] = sub_data
                            else:
                                klasa['Ratio_A'] = ""
                            sub = self.tree.GetNextSibling(sub)
                        elif sub_text == "Ratio_B":
                            if sub_data:
                                klasa['Ratio_B'] = sub_data
                            else:
                                klasa['Ratio_B'] = ""
                            sub = self.tree.GetNextSibling(sub)
                        else:
                            continue
                elif s_child_text == "priority":

                    if isinstance(s_child_data, int):
                        if s_child_data == 0:
                            klasa['tcpriority'] = "PRIO_A"
                        elif s_child_data == 1:
                            klasa['tcpriority'] = "PRIO_B"
                        elif s_child_data == 2:
                            klasa['tcpriority'] = "PRIO_C"
                        elif s_child_data == 3:
                            klasa['tcpriority'] = "PRIO_D"

                    elif isinstance(s_child_data, (str, unicode)):
                        if s_child_data.lower() == "prio_a":
                            klasa['tcpriority'] = "PRIO_A"
                        elif s_child_data.lower() == "prio_b":
                            klasa['tcpriority'] = "PRIO_B"
                        elif s_child_data.lower() == "prio_c":
                            klasa['tcpriority'] = "PRIO_C"
                        elif s_child_data.lower() == "prio_d":
                            klasa['tcpriority'] = "PRIO_D"

                else:
                    if s_child_text == "Name" and "TestCase" not in c_text:
                        if s_child_data:
                            klasa[s_child_text.lower()] = s_child_data
                        else:
                            klasa[s_child_text.lower()] = ""
                    else:
                        if s_child_data:
                            klasa[s_child_text] = s_child_data
                        else:
                            klasa[s_child_text] = ""
                sub_child = self.tree.GetNextSibling(sub_child)

            if tag == "RevisionHistory":
                rev_list.append(klasa)
            elif tag == "Test":
                if "TestCase" in c_text and "Table" not in c_text:
                    tc_list.append(klasa)
                    child = self.tree.GetNextSibling(child)
                    continue
                elif c_text == "result":

                    if isinstance(c_data, int):
                        if c_data == 0:
                            swc_data.overallresult = "passed"
                        elif c_data == 1:
                            swc_data.overallresult = "failed"
                        elif c_data == 2:
                            swc_data.overallresult = "not_executed"
                    elif isinstance(c_data, (str, unicode)):
                        if c_data.lower() == "passed":
                            swc_data.overallresult = "passed"
                        elif c_data.lower() == "failed":
                            swc_data.overallresult = "failed"
                        elif c_data.lower() == "not_executed":
                            swc_data.overallresult = "not_executed"

                    child = self.tree.GetNextSibling(child)
                    continue



                elif "TestCaseTable" in c_text:

                    sub_child = self.tree.GetFirstChild(child)[0]
                    while sub_child.IsOk():
                        s_child_text = self.tree.GetItemText(sub_child)
                        s_child_data = self.tree.GetItemData(sub_child)

                        if s_child_text == "ref":
                            klasa_1.ref = s_child_data
                            sub_child = self.tree.GetNextSibling(sub_child)
                            continue

                        elif s_child_text.lower() == "name":
                            klasa_1.name = s_child_data
                            sub_child = self.tree.GetNextSibling(sub_child)
                            continue


                        elif s_child_text == "TableHeader":
                            h_cell = self.tree.GetFirstChild(sub_child)[0]
                            while h_cell.IsOk():

                                h_cell_obj = classes.TableCell()
                                val = self.tree.GetFirstChild(h_cell)[0]
                                while val.IsOk():
                                    val_text = self.tree.GetItemText(val)
                                    val_data = self.tree.GetItemData(val)

                                    if val_text == "align":
                                        if isinstance(val_data, int):
                                            if val_data == 0:
                                                h_cell_obj[val_text] = "left"
                                            if val_data == 1:
                                                h_cell_obj[val_text] = "center"
                                            if val_data == 2:
                                                h_cell_obj[val_text] = "right"
                                        elif isinstance(val_data, (str, unicode)):
                                            if val_data.lower() == "left":
                                                h_cell_obj[val_text] = "left"
                                            if val_data.lower() == "center":
                                                h_cell_obj[val_text] = "center"
                                            if val_data.lower() == "right":
                                                h_cell_obj[val_text] = "right"
                                    else:
                                        h_cell_obj[val_text] = val_data

                                    val = self.tree.GetNextSibling(val)

                                klasa_1.header.append(h_cell_obj)

                                h_cell = self.tree.GetNextSibling(h_cell)

                            sub_child = self.tree.GetNextSibling(sub_child)

                        elif s_child_text == "TableRow":

                            if s_child_data:
                                for r_cell in s_child_data:
                                    row = []
                                    if isinstance(r_cell, dict):
                                        for val in r_cell.values()[0]:
                                            row.append(val)
                                        else:
                                            row.append("")
                                    klasa_1.row_list.append(row)
                            else:
                                row = []
                                row.append("None")
                                klasa_1.row_list.append(row)


                            sub_child = self.tree.GetNextSibling(sub_child)



                elif c_text == "integrationRecommendationResult":

                    if isinstance(c_data, int):
                        if c_data == 0:
                            swc_data.ir_rec_result = "passed"
                        elif c_data == 1:
                            swc_data.ir_rec_result = "failed"
                        elif c_data == 2:
                            swc_data.ir_rec_result = "not_executed"
                        elif c_data == 3:
                            swc_data.ir_rec_result = "failed_integrate"
                        elif c_data == 4:
                            swc_data.ir_rec_result = "previously_failed"
                    elif isinstance(c_data, (str, unicode)):
                        if c_data.lower() == "passed":
                            swc_data.ir_rec_result = "passed"
                        elif c_data.lower() == "failed":
                            swc_data.ir_rec_result = "failed"
                        elif c_data.lower() == "not_executed":
                            swc_data.ir_rec_result = "not_executed"
                        elif c_data.lower() == "failed_integrate":
                            swc_data.ir_rec_result = "failed_integrate"
                        elif c_data.lower() == "previously_failed":
                            swc_data.ir_rec_result = "previously_failed"

                    child = self.tree.GetNextSibling(child)
                    continue


            elif tag == "References":
                ref_list.append(klasa)
            elif tag == "Acronyms":
                acr_list.append(klasa)
            elif tag == "SupliersTestArtefacts":
                sup_ta_list.append(klasa)
            elif tag == "IntegratorsTestArtefacts":
                int_ta_list.append(klasa)
            elif tag == "AdditionalSoftwareUsed":
                add_tool_list.append(klasa)
            elif tag == "SuppliersAdditionalInfo":
                add_data_list.append(klasa)

            if "TestCaseTable" in c_text:
                tct_list.append(klasa_1)

            child = self.tree.GetNextSibling(child)

    def on_search(self, event):

        root = self.tree.GetRootItem()
        child = self.tree.GetFirstChild(root)[0]
        searched = event.GetString()
        selection = self.tree.GetSelection()
        sel_text = self.tree.GetItemText(selection)
        check_num = 0

        while child.IsOk():
            if self.tree.GetItemText(child) == "Test":
                break
            child = self.tree.GetNextSibling(child)

        if "TestCase" in sel_text and searched.lower() in sel_text.lower():
            t_child = self.tree.GetNextSibling(selection)
        else:
            t_child = self.tree.GetFirstChild(child)[0]

        while t_child.IsOk():
            check_num += 1
            t_text = self.tree.GetItemText(t_child)
            if "TestCase" in t_text and searched.lower() in t_text.lower():
                self.tree.Expand(child)
                self.tree.SelectItem(t_child)
                break

            if t_child == self.tree.GetLastChild(child):
                t_child = self.tree.GetFirstChild(child)[0]
                if check_num >= self.tree.GetChildrenCount(child):
                    self.status_text.SetStatusText("No TestCase named " +
                                            searched + "!")
                    break
            else:
                t_child = self.tree.GetNextSibling(t_child)


        print "SEARCH"


    def on_close(self, event):

        if self.tree.GetRootItem():

            if isinstance(filename, list):
                os.path.join(*filename)

            if self.file_modified:
                save_w = wx.MessageBox("Save changes to {}?".format(filename),
                                    "Unsaved changes!",
                                    wx.YES_NO |
                                    wx.ICON_WARNING |
                                    wx.CANCEL)

                if save_w == wx.YES:
                    self.file_save_as_on_menu(event)
                    self.Destroy()
                if save_w == wx.NO:
                    self.Destroy()
                elif save_w == wx.CANCEL:
                    event.Veto(True)
            else:
                string = "Are you sure you want to close the program?"
                close_warning = wx.MessageBox(string, "Please confirm",
                                            wx.YES_NO |
                                            wx.ICON_WARNING)

                if close_warning == wx.YES:
                    self.Destroy()
                else:
                    event.Veto(True)

        else:
            string = "Are you sure you want to close the program?"
            close_warning = wx.MessageBox(string, "Please confirm",
                                          wx.YES_NO |
                                          wx.ICON_WARNING)

            if close_warning == wx.YES:
                self.Destroy()
            else:
                event.Veto(True)


app = wx.App()
app.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
il = wx.ImageList(16, 16)
tree_item_expanded = il.Add(ap.GetBitmap(wx.ART_NORMAL_FILE,
                                         wx.ART_OTHER, (16, 16)))

tree_item_collapsed = il.Add(ap.GetBitmap(wx.ART_LIST_VIEW,
                                          wx.ART_OTHER, (16, 16)))
frame = MyFrame(None)
frame.SetIcon(wx.Icon(ICON_PATH))
frame.Show()
#wx.lib.inspection.InspectionTool().Show()
#frame.Maximize(True)

app.MainLoop()
