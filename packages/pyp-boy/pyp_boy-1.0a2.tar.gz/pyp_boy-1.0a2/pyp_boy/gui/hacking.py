import PySimpleGUI as gui

import pyp_boy


class HackingWindow(pyp_boy.PypBoy):

    def _add_buttons(self):
        acc = 0

        while True:

            if acc >= 3:
                break

            for word in self.word_cols[acc]:
                self.window.extend_layout(self.window[f'WCOL_{str(acc + 1)}'],
                                          [[gui.Button(word, key=f"WBUTTON_{word}")]])

            acc += 1

    def _col_sort(self):
        col1 = []
        col2 = []
        col3 = []

        acc = 0

        for word in self.og_wordlist:
            acc += 1
            if acc == 1:
                col1.append(word.upper())
            elif acc == 2:
                col2.append(word.upper())
            elif acc == 3:
                col3.append(word.upper())
                acc = 0

        return col1, col2, col3

    def __init__(self, wordlist):
        super(HackingWindow, self).__init__(wordlist)
        self.og_wordlist = wordlist
        self.word_cols = self._col_sort()
        self.wl = self.og_wordlist
        self.hidden_buttons = []
        self.active_guess = None

        acc = 0

        self.col_1 = []
        self.col_2 = []
        self.col_3 = []

        self.word_frame = [
            [
                gui.Text("Select a word in the terminal you're hacking and then tell PypBoy the number you have "
                         "correct and the word your chose.", key="INSTRUCTION_TEXT")
            ],
            [
                gui.Column(self.col_1, key="WCOL_1"),
                gui.Column(self.col_2, key="WCOL_2"),
                gui.Column(self.col_3, key="WCOL_3")
            ]
        ]

        self.guess_frame = [
            [
                gui.Text("Guessed word:"),
                gui.VSep(),
                gui.Text("", key="GUESSED_WORD", size=(10, 1))
            ],
            [
                gui.Text("Correct:"),
                gui.VSep(),
                gui.Spin(
                    list(range(1, len(wordlist[0]) + 1)),
                    key="NUM_CORRECT"
                )
            ]
        ]

        self.button_frame = [
            [
                gui.Button("Quit", key="HW_QUIT_BUTTON"),
                gui.Button("Guess", key="GUESS_BUTTON", visible=False),
                gui.Button("Undo", key="UNDO_BUTTON", visible=False, )
            ]
        ]

        self.layout = [
            [gui.Frame('', layout=self.word_frame)],
            [gui.Frame('', layout=self.guess_frame, visible=False, key="GUESS_FRAME",
                       element_justification='center')],
            [gui.Frame('', layout=self.button_frame)]
        ]

        self.window = gui.Window("PypBoy (TM)", layout=self.layout, finalize=True)
        self._add_buttons()

        while True:
            event, vals = self.window.read(timeout=100)

            if event is None or event == "HW_QUIT_BUTTON":
                self.window.close()
                break

            if "WBUTTON_" in event:
                g_word = str(event).split("_")[-1]
                self.active_guess = g_word

                self.window["GUESS_FRAME"].update(visible=True)
                self.window["GUESSED_WORD"].update(g_word)
                self.window['UNDO_BUTTON'].update(visible=True)
                self.window['GUESS_BUTTON'].update(visible=True)

                for w in self.wl:
                    button_tag = f"WBUTTON_{w}"
                    if not w == g_word:

                        self.window[button_tag].update(visible=False)
                        self.hidden_buttons.append(button_tag)
                    else:
                        self.window[button_tag].update(disabled=True)

            if event == "UNDO_BUTTON":
                for bttn in self.hidden_buttons:
                    self.window[bttn].update(visible=True)

                self.window["UNDO_BUTTON"].update(visible=False)
                self.window["GUESS_FRAME"].update(visible=False)
                self.window["GUESS_BUTTON"].update(visible=False)
                self.window[f"WBUTTON_{self.active_guess}"].update(disabled=False)
                self.hidden_buttons = []
                self.active_guess = None

            if event == "GUESS_BUTTON":
                print(vals)
                guess_bttn_tag = f"WBUTTON_{self.active_guess}"

                # Make the "guess frame" invisible
                self.window["GUESS_FRAME"].update(visible=False)

                # Use the "guess" function of the PypBoy class to return a list of possibilities
                new_list = self.guess(self.active_guess, vals['NUM_CORRECT'])

                # Dissappear the "Guess" and "Undo" buttons
                self.window["GUESS_BUTTON"].update(visible=False)
                self.window["UNDO_BUTTON"].update(visible=False)

                # Make the guessed word-button invisible since it's already been guessed
                self.window[guess_bttn_tag].update(visible=False)

                # If the length of the list is exactly or less than 1, inform the user that the visible button is the
                # answer they're looking for.
                if len(new_list) >= 1:
                    self.window["INSTRUCTION_TEXT"].update("Success! The button available below is your password!")

                # Iterate over the returned possibilities, making each associated button visible to be guessed next.
                for word in new_list:
                    bttn_tag = f"WBUTTON_{word}"
                    self.window[bttn_tag].update(visible=True, disabled=True)
