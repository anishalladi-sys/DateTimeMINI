import wx
import wx.adv
from datetime import date
from calendar import monthrange


class AgeCalculator(wx.Frame):
    """Enhanced Age Calculator GUI using wxPython with DatePicker, copy and save."""

    def __init__(self, parent=None):
        super().__init__(parent, title="Age Calculator", size=(420, 220))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#f0f6ff')  # soft blue background

        # Fonts and styling
        header_font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        default_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        button_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        panel.SetFont(default_font)

        # Header
        header = wx.StaticText(panel, label="Age Calculator")
        header.SetFont(header_font)
        header.SetForegroundColour('#002B5C')

        today = date.today()

        # Menu
        menubar = wx.MenuBar()
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "&About\tF1", "About this app")
        menubar.Append(help_menu, "&Help")
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)

        # Layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(wx.StaticText(panel, label="Birth Date:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 8)

        default_dt = wx.DateTime.FromDMY(today.day, today.month - 1, today.year)
        self.datepicker = wx.adv.DatePickerCtrl(panel, wx.ID_ANY, default_dt, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        row.Add(self.datepicker, 0, wx.RIGHT, 8)

        main_sizer.Add(header, 0, wx.ALL | wx.ALIGN_CENTER, 18)
        main_sizer.Add(row, 0, wx.ALL | wx.ALIGN_CENTER, 22)  # slightly larger padding for symmetry

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.calc_btn = wx.Button(panel, label="Calculate Age")
        self.calc_btn.SetFont(button_font)
        self.calc_btn.Bind(wx.EVT_BUTTON, self.on_calculate)
        btn_sizer.Add(self.calc_btn, 0, wx.RIGHT, 12)

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

        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.BOTTOM, 18)  # balanced spacing

        self.result_text = wx.StaticText(panel, label="")
        self.result_text.SetFont(header_font)
        self.result_text.SetForegroundColour('#004080')
        main_sizer.Add(self.result_text, 0, wx.ALIGN_CENTER | wx.ALL, 22)

        panel.SetSizer(main_sizer)
        panel.Layout()
        self.Maximize(True)  # fill the screen

    def on_about(self, event):
        wx.MessageBox("Age Calculator\nUse the date picker to select a birth date.\nCalculates years, months and days.", "About", wx.ICON_INFORMATION)

    def on_clear(self, event):
        today = date.today()
        default_dt = wx.DateTime.FromDMY(today.day, today.month - 1, today.year)
        self.datepicker.SetValue(default_dt)
        self.result_text.SetLabel("")
        self.copy_btn.Enable(False)
        self.save_btn.Enable(False)

    def on_calculate(self, event):
        # Get date from DatePicker (wx.DateTime uses month indices 0-11)
        dt = self.datepicker.GetValue()
        d = dt.GetDay()
        m = dt.GetMonth() + 1
        y = dt.GetYear()

        try:
            birth_date = date(y, m, d)
        except Exception:
            wx.MessageBox("The date entered is invalid. Please check the selection.", "Invalid Date", wx.ICON_ERROR)
            return

        today = date.today()
        if birth_date > today:
            wx.MessageBox("Birth date is in the future. Please enter a valid past date.", "Invalid Date", wx.ICON_ERROR)
            return

        years = today.year - birth_date.year
        months = today.month - birth_date.month
        days = today.day - birth_date.day

        if days < 0:
            months -= 1
            if today.month == 1:
                prev_month = 12
                prev_year = today.year - 1
            else:
                prev_month = today.month - 1
                prev_year = today.year
            days += monthrange(prev_year, prev_month)[1]
        if months < 0:
            years -= 1
            months += 12

        result = f"Your age is {years} years, {months} months, and {days} days."
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
    except Exception as e:
        print("wxPython is required to run this GUI. Install it with: pip install wxPython")
        raise

    frame = AgeCalculator()
    frame.Show()
    app.MainLoop()