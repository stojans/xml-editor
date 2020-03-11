import os
import xml_editor as XE
import wx



app = wx.App()
app.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
ap = wx.ArtProvider
il = wx.ImageList(16, 16)
tree_item_expanded = il.Add(ap.GetBitmap(wx.ART_NORMAL_FILE,
                                         wx.ART_OTHER, (16, 16)))

tree_item_collapsed = il.Add(ap.GetBitmap(wx.ART_LIST_VIEW,
                                          wx.ART_OTHER, (16, 16)))
frame = XE.MyFrame(None)
frame.SetIcon(wx.Icon(ICON_PATH))
frame.Show()
#wx.lib.inspection.InspectionTool().Show()
# frame.Maximize(True)

app.MainLoop()
