import wx

EVT_AUTOCOMPLETE_ENTER_TYPE = wx.NewEventType()
EVT_AUTOCOMPLETE_ENTER = wx.PyEventBinder(EVT_AUTOCOMPLETE_ENTER_TYPE, 1)

class AutoCompleteEnterEvent(wx.PyCommandEvent):
    def __init__(self, event_type, event_id, value):
        super().__init__(event_type, event_id)
        self._value = value

    def GetValue(self):
        return self._value


class AutoCompleteTextCtrl(wx.TextCtrl):
    def __init__(self, parent, choices, *args, **kwargs):
        super(AutoCompleteTextCtrl, self).__init__(parent, *args, **kwargs)
        self.choices = choices
        self.listbox = None
        self.Bind(wx.EVT_TEXT, self.on_text_change)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

    def on_text_change(self, event):
        text = self.GetValue()
        if text:
            matches = [choice for choice in self.choices if text.lower() in choice.lower()]
            if matches:
                self.show_listbox(matches)
            else:
                self.hide_listbox()
        else:
            self.hide_listbox()
        event.Skip()

    def on_key_down(self, event):
        if self.listbox and self.listbox.IsShown():
            if event.GetKeyCode() == wx.WXK_DOWN:
                self.listbox.SetFocus()
                self.listbox.SetSelection(0)
            elif event.GetKeyCode() == wx.WXK_UP:
                self.listbox.SetFocus()
                self.listbox.SetSelection(self.listbox.GetCount() - 1)
        event.Skip()

    def show_listbox(self, choices):
        if not self.listbox:
            self.listbox = wx.ListBox(self.GetParent(), choices=choices)
            self.listbox.Bind(wx.EVT_CHAR_HOOK, self.on_listbox_key_down)
            self.GetParent().json_sizer.Add(self.listbox, 0, wx.EXPAND)
        else:
            self.listbox.Set(choices)
        self.listbox.SetSize((self.GetSize().width, 150))
        self.listbox.SetPosition(self.ClientToScreen((0, self.GetSize().height)))
        self.listbox.Show()

    def hide_listbox(self):
        if self.listbox:
            self.listbox.Hide()

    def on_listbox_key_down(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            if self.listbox.GetSelection() != wx.NOT_FOUND:
                value = self.listbox.GetStringSelection()
                self.SetValue(value)
                self.SetInsertionPointEnd()
                autocomplete_event = AutoCompleteEnterEvent(EVT_AUTOCOMPLETE_ENTER_TYPE, self.GetId(), value)
                wx.PostEvent(self.GetEventHandler(), autocomplete_event)
            self.hide_listbox()
        elif event.GetKeyCode() == wx.WXK_ESCAPE:
            self.SetFocus()
            self.hide_listbox()
        elif event.GetKeyCode() == wx.WXK_BACK:
            self.delete_last_char()
            self.SetFocus()
        elif event.GetKeyCode() == wx.WXK_UP:
            if self.listbox.GetSelection() == 0:
                self.SetFocus()
                self.listbox.SetSelection(wx.NOT_FOUND)
        elif event.GetKeyCode() == wx.WXK_DOWN:
            if self.listbox.GetSelection() == self.listbox.GetCount() - 1:
                self.SetFocus()
                self.listbox.SetSelection(wx.NOT_FOUND)
        event.Skip()

    def delete_last_char(self):
        text = self.GetValue()
        if text:
            self.SetValue(text[:-1])
            self.SetInsertionPointEnd()
            text_event = wx.CommandEvent(wx.wxEVT_TEXT, self.GetId())
            text_event.SetString(self.GetValue())
            wx.PostEvent(self.GetEventHandler(), text_event)

    def set_choices(self, choices):
        self.choices = choices
