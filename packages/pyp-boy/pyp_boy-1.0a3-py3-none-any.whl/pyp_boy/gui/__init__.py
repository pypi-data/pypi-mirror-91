import PySimpleGUI as Gui

from pyp_boy.common.tools import prepare_wordlist
from pyp_boy.gui.hacking import HackingWindow

GUI = Gui

WORD_MAX = 20


class PypBoyGUI(object):
    class MainWindowLayout(object):
        def __init__(self):
            self.header_col = [
                [GUI.Text("PypBoy!", justification="center", )]
            ]

            self.sep_col_1 = [
                [GUI.VSep()]
            ]

            self.sep_col_2 = [
                [GUI.VSep()]
            ]

            self.header_frame = [
                [GUI.Column(layout=self.sep_col_1, justification="left"),
                 GUI.Column(layout=self.header_col, justification="center", size=(200, 20)),
                 GUI.Column(layout=self.sep_col_2, justification="right")]
            ]

            self.word_frame = [
                [GUI.Text("Here's where you'll enter the words on the terminal")],
                [GUI.HSeparator()],
                [GUI.Text("Press 'Add Word' below to get started!")]
            ]

            self.button_frame_left = [
                [GUI.Button("Add Word", key='ADD_WORD_BUTTON')],
                [GUI.Button("Remove Word", key="REMOVE_WORD_BUTTON", visible=False)],

            ]

            self.button_frame_center = [
                [GUI.Button("Lock In!", enable_events=True, key='LOCK_IN_BUTTON', tooltip="Start hacking!",
                            visible=False)],
                [GUI.Button("Clear All", enable_events=True, key='CLEAR_ALL_BUTTON', tooltip="Clear all words",
                            visible=False)],
                [GUI.Button("Output Values to Console", key="VALS_OUT_BUTTON", visible=False)]
            ]

            self.button_frame_right = [
                [GUI.Button("Quit", enable_events=True, key='QUIT_BUTTON')],
            ]

    class MainWindow(object):

        def __init__(self, title):
            self.input_count = 0
            self.invisible_num = 0
            GUI.theme("DarkGreen2")
            self.Layout = PypBoyGUI.MainWindowLayout()

            header_frame = self.Layout.header_frame
            word_frame = self.Layout.word_frame
            bf_left = self.Layout.button_frame_left
            bf_center = self.Layout.button_frame_center
            bf_right = self.Layout.button_frame_right

            layout = [
                [GUI.Frame("", layout=header_frame, )],
                [GUI.VSep(), GUI.Frame('', layout=word_frame, key='WORD_FRAME'), GUI.VSep()],
                [GUI.Frame("", layout=bf_left, key='BF_LEFT'), GUI.Frame("", layout=bf_center, key='BF_CENTER'),
                 GUI.Frame("", layout=bf_right, key='BF_RIGHT')]

            ]

            self.win = GUI.Window(title, layout=layout, element_justification="center")
            self.last_removed = False

        def add_word_box(self):
            if self.invisible_num >= 1:
                self.win[f'WORD_{self.input_count}'].update('', visible=True)
                self.invisible_num -= 1
            else:
                self.win.extend_layout(self.win['WORD_FRAME'], [[GUI.Input(key=f"WORD_{self.input_count}")]])

            self.win['REMOVE_WORD_BUTTON'].update(visible=True)
            self.win['VALS_OUT_BUTTON'].update(visible=True)
            if self.input_count >= 2:
                self.win['LOCK_IN_BUTTON'].update(visible=True)
                self.win['CLEAR_ALL_BUTTON'].update(visible=True)

        def run_window(self):
            while True:
                event, vals = self.win.read(timeout=100)

                if event is None:
                    self.win.close()
                    exit()

                if event == "QUIT_BUTTON":
                    self.win.close()
                    exit()

                if event == 'ADD_WORD_BUTTON':
                    print(self.input_count)

                    if self.input_count >= WORD_MAX:
                        GUI.popup_error("You have the maximum number of words!")
                        continue

                    if self.input_count >= 1:
                        if vals[f'WORD_{self.input_count}'].replace(' ', '') == '':
                            GUI.popup_error(f"Please put a word in slot {self.input_count} before trying to add "
                                            f"another word")
                            continue

                    self.input_count += 1
                    self.add_word_box()

                    #     self.win.refresh()
                    #     continue
                    #
                    # try:
                    #     if vals[f'WORD_{self.input_count}'].replace(' ', '') == '':

                    #         continue
                    #
                    # except KeyError:
                    #     self.input_count += 1
                    #     self.win.extend_layout(self.win['WORD_FRAME'], [[GUI.Input(key=f"WORD_{self.input_count}")]])
                    #     continue

                    #
                    # if self.input_count >= 1:
                    #     self.win["REMOVE_WORD_BUTTON"].update(visible=True)
                    #
                    # self.last_removed = False
                    # self.win['REMOVE_WORD_BUTTON'].update(visible=True)
                    # self.win.refresh()
                    # self.input_count += 1

                if event == "REMOVE_WORD_BUTTON":
                    self.win[f'WORD_{self.input_count}'].update('', visible=False)
                    self.input_count -= 1
                    if self.input_count == 0:
                        self.win['REMOVE_WORD_BUTTON'].update(visible=False)
                        self.win['VALS_OUT_BUTTON'].update(visible=False)
                    self.invisible_num += 1

                    if self.input_count < 2:
                        self.win['LOCK_IN_BUTTON'].update(visible=False)
                        self.win['CLEAR_ALL_BUTTON'].update(visible=False)

                if event == "VALS_OUT_BUTTON":
                    print(vals)
                    print(dir(vals))
                    print(dir(event))

                if event == "LOCK_IN_BUTTON":
                    word_list = []
                    for w in vals.items():
                        word_list.append(w[1])
                    wl = prepare_wordlist(word_list)
                    print(wl)
                    self.win.close()
                    hacking_window = HackingWindow(wl)
