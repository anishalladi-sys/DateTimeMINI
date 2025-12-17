import wx
import wx.adv
from datetime import datetime


class CountdownFrame(wx.Frame):
    """Countdown to a future event GUI using wxPython."""

    def __init__(self, parent=None):
        super().__init__(parent, title="Countdown to Future Event", size=(480, 260))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#fff6f0')  # warm accent

        # Menu
        menubar = wx.MenuBar()
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, "&About\tF1", "About this app")
        menubar.Append(help_menu, "&Help")
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)

        # Fonts
        header_font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        default_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        button_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        panel.SetFont(default_font)

        # Header
        header = wx.StaticText(panel, label="Countdown to Future Event")
        header.SetFont(header_font)
        header.SetForegroundColour('#7a3b00')

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(header, 0, wx.ALL | wx.ALIGN_CENTER, 18)

        # Event name
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_sizer.Add(wx.StaticText(panel, label="Event name:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 12)
        self.name_ctrl = wx.TextCtrl(panel)
        name_sizer.Add(self.name_ctrl, 1, wx.EXPAND)
        sizer.Add(name_sizer, 0, wx.ALL | wx.EXPAND, 12)

        # Date and Time pickers
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(wx.StaticText(panel, label="Event date:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 12)
        today = datetime.now()
        default_dt = wx.DateTime.FromDMY(today.day, today.month - 1, today.year)
        self.datepicker = wx.adv.DatePickerCtrl(panel, wx.ID_ANY, default_dt, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        row.Add(self.datepicker, 0, wx.RIGHT, 14)

        row.Add(wx.StaticText(panel, label="Time (HH:MM:SS):"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 12)
        self.hour = wx.SpinCtrl(panel, min=0, max=23, initial=today.hour)
        self.minu = wx.SpinCtrl(panel, min=0, max=59, initial=today.minute)
        self.sec = wx.SpinCtrl(panel, min=0, max=59, initial=today.second)
        row.Add(self.hour, 0, wx.RIGHT, 6)
        row.Add(self.minu, 0, wx.RIGHT, 6)
        row.Add(self.sec, 0)

        sizer.Add(row, 0, wx.ALL | wx.EXPAND, 12)

        # Buttons
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.start_btn = wx.Button(panel, label="Start")
        self.start_btn.SetFont(button_font)
        self.start_btn.Bind(wx.EVT_BUTTON, self.on_start)
        btn_sizer.Add(self.start_btn, 0, wx.RIGHT, 12)

        self.stop_btn = wx.Button(panel, label="Stop")
        self.stop_btn.SetFont(button_font)
        self.stop_btn.Bind(wx.EVT_BUTTON, self.on_stop)
        self.stop_btn.Enable(False)
        btn_sizer.Add(self.stop_btn, 0, wx.RIGHT, 12)

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

        sizer.Add(btn_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 18)

        # Result
        self.result_text = wx.StaticText(panel, label="")
        self.result_text.SetFont(header_font)
        self.result_text.SetForegroundColour('#7a3b00')
        sizer.Add(self.result_text, 0, wx.ALL | wx.ALIGN_CENTER, 12)

        panel.SetSizer(sizer)

        # Timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_tick, self.timer)
        self.target = None

        self.Maximize(True)  # fill the screen

    def on_about(self, event):
        wx.MessageBox(
            "Countdown to a future event. Select a date and time, then press Start. The countdown updates every second.",
            "About",
            wx.ICON_INFORMATION,
        )

    def get_target_datetime(self):
        dt = self.datepicker.GetValue()
        d = dt.GetDay()
        m = dt.GetMonth() + 1
        y = dt.GetYear()
        hh = int(self.hour.GetValue())
        mm = int(self.minu.GetValue())
        ss = int(self.sec.GetValue())
        try:
            return datetime(y, m, d, hh, mm, ss)
        except Exception:
            return None

    def on_start(self, event):
        target = self.get_target_datetime()
        if target is None:
            wx.MessageBox("The selected date/time is invalid.", "Invalid", wx.ICON_ERROR)
            return
        now = datetime.now()
        if target <= now:
            wx.MessageBox("Please select a future date/time.", "Invalid", wx.ICON_ERROR)
            return

        self.target = target
        self.timer.Start(1000)
        self.start_btn.Enable(False)
        self.stop_btn.Enable(True)
        self.copy_btn.Enable(False)
        self.save_btn.Enable(False)
        self.update_result()

    def on_stop(self, event):
        if self.timer.IsRunning():
            self.timer.Stop()
        self.start_btn.Enable(True)
        self.stop_btn.Enable(False)

    def on_tick(self, event):
        if not self.target:
            return
        now = datetime.now()
        if now >= self.target:
            self.timer.Stop()
            self.result_text.SetLabel("Event reached! 🎉")
            wx.MessageBox("The event time has been reached!", "Event", wx.ICON_INFORMATION)
            self.start_btn.Enable(True)
            self.stop_btn.Enable(False)
            self.copy_btn.Enable(True)
            self.save_btn.Enable(True)
            return
        self.update_result()

    def update_result(self):
        now = datetime.now()
        delta = self.target - now
        days = delta.days
        seconds = delta.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        result = f"Time remaining: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds."
        name = self.name_ctrl.GetValue().strip()
        if name:
            result = f"{name} — {result}"
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

    def on_clear(self, event):
        self.name_ctrl.SetValue("")
        now = datetime.now()
        default_dt = wx.DateTime.FromDMY(now.day, now.month - 1, now.year)
        self.datepicker.SetValue(default_dt)
        self.hour.SetValue(now.hour)
        self.minu.SetValue(now.minute)
        self.sec.SetValue(now.second)
        self.result_text.SetLabel("")
        if self.timer.IsRunning():
            self.timer.Stop()
        self.start_btn.Enable(True)
        self.stop_btn.Enable(False)
        self.copy_btn.Enable(False)
        self.save_btn.Enable(False)


if __name__ == "__main__":
    try:
        app = wx.App(False)
    except Exception:
        print("wxPython is required to run this GUI. Install it with: pip install wxPython")
        raise

    frame = CountdownFrame()
    frame.Show()
    app.MainLoop()
    