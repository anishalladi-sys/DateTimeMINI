import wx
import sys

# Import the frames from the tool modules (they only create their own wx.App when run directly)
try:
    from agecalculator import AgeCalculator
    from Countdowntoafutureevent import CountdownFrame
    from dayoftheweekcalculator import DayOfWeekFrame
except Exception as e:
    print("Failed to import one or more tools:", e)
    raise


class LauncherFrame(wx.Frame):
    """Launcher window to open the three utility windows."""

    def __init__(self, parent=None):
        super().__init__(parent, title="Mini Tools Launcher", size=(380, 220))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#f7f0ff')  # soft purple

        main = wx.BoxSizer(wx.VERTICAL)

        header = wx.StaticText(panel, label="Mini Tools Launcher", style=wx.ALIGN_CENTER)
        header_font = wx.Font(22, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        header.SetFont(header_font)
        header.SetForegroundColour('#4b0082')
        main.Add(header, 0, wx.ALL | wx.ALIGN_CENTER, 16)

        grid = wx.GridSizer(rows=2, cols=2, hgap=20, vgap=20)

        # Make buttons larger and consistent
        btn_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        age_btn = wx.Button(panel, label="Age Calculator (1)")
        age_btn.SetFont(btn_font)
        age_btn.SetBackgroundColour('#e8f2ff')
        age_btn.Bind(wx.EVT_BUTTON, self.on_open_age)
        grid.Add(age_btn, 0, wx.EXPAND)

        countdown_btn = wx.Button(panel, label="Countdown (2)")
        countdown_btn.SetFont(btn_font)
        countdown_btn.SetBackgroundColour('#fff2e6')
        countdown_btn.Bind(wx.EVT_BUTTON, self.on_open_countdown)
        grid.Add(countdown_btn, 0, wx.EXPAND)

        day_btn = wx.Button(panel, label="Day of Week (3)")
        day_btn.SetFont(btn_font)
        day_btn.SetBackgroundColour('#eaffef')
        day_btn.Bind(wx.EVT_BUTTON, self.on_open_day)
        grid.Add(day_btn, 0, wx.EXPAND)

        open_all_btn = wx.Button(panel, label="Open All")
        open_all_btn.SetFont(btn_font)
        open_all_btn.SetBackgroundColour('#f3e8ff')
        open_all_btn.Bind(wx.EVT_BUTTON, self.on_open_all)
        grid.Add(open_all_btn, 0, wx.EXPAND)

        main.Add(grid, 0, wx.ALL | wx.EXPAND, 12)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        exit_btn = wx.Button(panel, label="Exit")
        exit_btn.SetFont(btn_font)
        exit_btn.SetBackgroundColour('#ffeaea')
        exit_btn.Bind(wx.EVT_BUTTON, lambda e: self.Close())
        btn_sizer.Add(exit_btn, 0, wx.ALIGN_CENTER)
        main.Add(btn_sizer, 0, wx.ALL | wx.ALIGN_CENTER, 6)

        panel.SetSizer(main)

        # status bar
        self.CreateStatusBar()
        self.SetStatusText("Press 1/2/3 or click a button to open a tool")

        # Accelerator table for keyboard shortcuts
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('1'), wx.NewIdRef()),
            (wx.ACCEL_CTRL, ord('2'), wx.NewIdRef()),
            (wx.ACCEL_CTRL, ord('3'), wx.NewIdRef()),
        ])
        self.SetAcceleratorTable(accel_tbl)
        # Bind the key events to handlers via EVT_CHAR_HOOK
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key)

        self.opened_frames = []
        self.Maximize(True)  # fill the screen

    def _show_frame(self, frame):
        # Keep a reference so frames don't get garbage collected
        self.opened_frames.append(frame)
        frame.Show()

    def on_open_age(self, event):
        try:
            frame = AgeCalculator(None)
            self._show_frame(frame)
            self.SetStatusText("Opened Age Calculator")
        except Exception as e:
            wx.MessageBox(f"Failed to open Age Calculator: {e}", "Error", wx.ICON_ERROR)

    def on_open_countdown(self, event):
        try:
            frame = CountdownFrame(None)
            self._show_frame(frame)
            self.SetStatusText("Opened Countdown")
        except Exception as e:
            wx.MessageBox(f"Failed to open Countdown: {e}", "Error", wx.ICON_ERROR)

    def on_open_day(self, event):
        try:
            frame = DayOfWeekFrame(None)
            self._show_frame(frame)
            self.SetStatusText("Opened Day of Week Calculator")
        except Exception as e:
            wx.MessageBox(f"Failed to open Day of Week Calculator: {e}", "Error", wx.ICON_ERROR)

    def on_open_all(self, event):
        self.on_open_age(event)
        self.on_open_countdown(event)
        self.on_open_day(event)

    def on_key(self, event):
        key = event.GetKeyCode()
        if key == ord('1'):
            self.on_open_age(None)
            return
        if key == ord('2'):
            self.on_open_countdown(None)
            return
        if key == ord('3'):
            self.on_open_day(None)
            return
        event.Skip()


if __name__ == "__main__":
    try:
        app = wx.App(False)
    except Exception:
        print("wxPython is required to run this launcher. Install it with: pip install wxPython")
        raise

    frame = LauncherFrame()
    frame.Show()
    app.MainLoop()
