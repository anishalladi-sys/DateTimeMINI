import wx
import wx.adv
from datetime import date


class DayOfWeekFrame(wx.Frame):
    """GUI for calculating day of the week from a date."""

    def __init__(self, parent=None):
        super().__init__(parent, title="Day of the Week Calculator", size=(420, 180))
        panel = wx.Panel(self)

        # Menu
        menubar = wx.MenuBar()
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "&About\tF1", "About this app")
        menubar.Append(help_menu, "&Help")
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)

        header_font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        default_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        button_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        panel.SetBackgroundColour('#f0fff4')  # soft green
        panel.SetFont(default_font)

        # Header
        header = wx.StaticText(panel, label="Day of the Week Calculator")
        header.SetFont(header_font)
        header.SetForegroundColour('#0b6b3a')

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(header, 0, wx.ALL | wx.ALIGN_CENTER, 18)

        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(wx.StaticText(panel, label="Select date:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 12)

        today = date.today()
        default_dt = wx.DateTime.FromDMY(today.day, today.month - 1, today.year)
        self.datepicker = wx.adv.DatePickerCtrl(panel, wx.ID_ANY, default_dt, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        row.Add(self.datepicker, 0, wx.RIGHT, 12)

        calc_btn = wx.Button(panel, label="Get Day")
        calc_btn.SetFont(button_font)
        calc_btn.Bind(wx.EVT_BUTTON, self.on_calculate)
        row.Add(calc_btn, 0)

        main_sizer.Add(row, 0, wx.ALL | wx.ALIGN_CENTER, 22)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.copy_btn = wx.Button(panel, label="Copy Result")
        self.copy_btn.SetFont(button_font)
        self.copy_btn.Bind(wx.EVT_BUTTON, self.on_copy)
        self.copy_btn.Enable(False)
        btn_sizer.Add(self.copy_btn, 0, wx.RIGHT, 12)

        self.save_btn = wx.Button(panel, label="Save Result")
        self.save_btn.SetFont(button_font)
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_save)
        self.save_btn.Enable(False)
        btn_sizer.Add(self.save_btn, 0, wx.RIGHT, 12)

        clear_btn = wx.Button(panel, label="Clear")
        clear_btn.SetFont(button_font)
        clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)
        btn_sizer.Add(clear_btn, 0)

        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 18)

        self.result_text = wx.StaticText(panel, label="")
        self.result_text.SetFont(header_font)
        self.result_text.SetForegroundColour('#0b6b3a')
        main_sizer.Add(self.result_text, 0, wx.ALIGN_CENTER | wx.ALL, 20)

        panel.SetSizer(main_sizer)
        self.Maximize(True)  # fill the screen

    def on_about(self, event):
        wx.MessageBox("Select a date and press 'Get Day' to find the day of the week.", "About", wx.ICON_INFORMATION)

    def on_clear(self, event):
        today = date.today()
        default_dt = wx.DateTime.FromDMY(today.day, today.month - 1, today.year)
        self.datepicker.SetValue(default_dt)
        self.result_text.SetLabel("")
        self.copy_btn.Enable(False)
        self.save_btn.Enable(False)

    def on_calculate(self, event):
        dt = self.datepicker.GetValue()
        d = dt.GetDay()
        m = dt.GetMonth() + 1
        y = dt.GetYear()

        try:
            weekday = date(y, m, d).strftime("%A")
        except Exception:
            wx.MessageBox("Invalid date selected.", "Error", wx.ICON_ERROR)
            return

        result = f"Day of the week is: {weekday}"
        self.result_text.SetLabel(result)
        self.copy_btn.Enable(True)
        self.save_btn.Enable(True)

    def on_copy(self, event):
        text = self.result_text.GetLabel()
        if not text:
            return
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(text))
            wx.TheClipboard.Close()
            wx.MessageBox("Result copied to clipboard.", "Copied", wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Could not open the clipboard.", "Error", wx.ICON_ERROR)

    def on_save(self, event):
        text = self.result_text.GetLabel()
        if not text:
            return
        with wx.FileDialog(self, "Save result", wildcard="Text files (*.txt)|*.txt", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            path = dlg.GetPath()
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text + "\n")
                wx.MessageBox(f"Result saved to: {path}", "Saved", wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Failed to save file: {e}", "Error", wx.ICON_ERROR)


if __name__ == "__main__":
    try:
        app = wx.App(False)
    except Exception:
        print("wxPython is required to run this GUI. Install it with: pip install wxPython")
        raise

    frame = DayOfWeekFrame()
    frame.Show()
    app.MainLoop()