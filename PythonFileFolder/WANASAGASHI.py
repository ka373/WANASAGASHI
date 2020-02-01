# *****************************************************************************#
"""

WANASAGASHI

- Simple code Description: WANASAGASHI game
- Date of production and release: Saturday 1 February 2020 (JST / KST)
(I made a improvement in the program I made in 2009)

- Code production: ka373
- github: https://github.com/ka373

"""
# *****************************************************************************#

# -*-coding:cp949-*-
# !/usr/bin/env python

import wx
import random
import wx.adv  # about
from operator import itemgetter


class Wanasagashi(wx.Frame):

    hide = 0

    const_state_init = 0
    const_state_glance = 1
    const_state_choice = 2
    const_state_game_over = 3
    state_game = const_state_init

    num_wanas10 = 15
    num_wanas7 = 8

    # Number of Wanas to find to clear the stage
    # ステージクリアのために必要なWanaの数
    # 스테이지 클리어를 위해 찾아야 할 Wana들의 수
    condition_stage_clear10 = 9
    condition_stage_clear7 = 5
    condition_stage_clear = condition_stage_clear10

    accumulated_score = 0  # Score accumulated from the start / スタートからの累積されてきたスコア / 스타트부터 누적되어 온 스코어
    current_stage_score = 0

    current_stage = 0  # Current stage / 現在のステージ / 현재 스테이지
    length_board = 10  # Board size / ボードサイズ / 보드 사이즈 => (10, 7)
    time_limit = 11
    elapsed_time = 0  # Elapsed time in the current state / 現在stateで経過した時間 / 현재 state에서 경과된 시간

    btn10_list = []
    btn7_list = []

    cover7_list = []
    cover10_list = []

    btn_enable = 0

    gap_btn = 35
    btn_start_x = 10
    btn_start_y = 140

    line1_y = 8
    line2_y = 38
    line3_y = 92
    line4_y = 110
    line5_y = btn_start_y
    line6_y = 490

    name_confirm = ""
    rank_user = 7

    can_game_over = True

    # __________________________________________________________________________________________________________
    def __init__(self):

        wx.Frame.__init__(self, None, wx.NewIdRef(count=1), 'WANASAGASHI', pos=wx.Point(10, 10), size=(370, 580),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        self.panel = wx.Panel(self)

        # ______________________________________________________
        # First line / 最初の行 / 첫 번째 라인

        # Name text
        self.text_name = wx.StaticText(self.panel, wx.NewIdRef(count=1), u"Name:", pos=(8, self.line1_y+3))
        font_score = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        self.text_name.SetFont(font_score)

        # Name box
        self.username = wx.TextCtrl(self.panel, wx.NewIdRef(count=1), "MWK", pos=(58, self.line1_y), size=(80, -1))

        # Stage text
        self.text_stage = wx.StaticText(self.panel, wx.NewIdRef(count=1), u"Stage: 0", pos=(150, self.line1_y+3))
        self.text_stage.SetFont(font_score)

        # Score text
        self.text_score = wx.StaticText(self.panel, wx.NewIdRef(count=1), u"Score: 0", pos=(225, self.line1_y+3))
        self.text_score.SetFont(font_score)

        # Stage clear condition
        self.text_clear_condition = wx.StaticText(self.panel, wx.NewIdRef(count=1),
                                                  "( " + "0 / "+str(self.condition_stage_clear) + " )",
                                                  pos=(300, self.line1_y+3))

        self.text_clear_condition.SetFont(font_score)

        # _________________________________________________________
        # Second line / 二行目 / 두 번째 라인

        sizer = wx.BoxSizer(wx.VERTICAL)
        grade_list = [u'Large (10x10), 15 Wanas', u'Medium (7x7), 8 Wanas']
        self.rb_size = wx.RadioBox\
            (self.panel, -1, u"Size", (8, self.line2_y), wx.DefaultSize, grade_list, 2, wx.RA_SPECIFY_COLS)
        sizer.Add(self.rb_size, 0, wx.ALL, 20)
        self.Bind(wx.EVT_RADIOBOX, self.set_board_size, self.rb_size)

        self.btn_sp = wx.Button(self.panel, label="S.P.", pos=(336, self.line2_y + 6), size=(28, 45))
        self.btn_sp.Bind(wx.EVT_BUTTON, self.oper_btn_sp)

        # _________________________________________________________
        # Third line / 第三のライン / 세 번째 라인

        self.text_description = wx.StaticText(self.panel, wx.NewIdRef(count=1), u"WANASAGASHI", (15, self.line3_y))
        self.text_sec = wx.StaticText(self.panel, wx.NewIdRef(count=1), u"0s / 10s", (305, self.line3_y))

        # _________________________________________________________
        # Fourth line / 4行目 / 네 번째 라인
        # Gauge (progress bar) / ゲージ（プログレスバー） / 게이지(프로그레스 바)

        self.gauge_time = wx.Gauge(self.panel, -1, 30, pos=(8, self.line4_y), size=(347, 20))  # (470,95)(240, 굵기25)

        # _________________________________________________________
        # Buttons on the bottom / 下部のボタン / 하단 버튼

        self.btn_start = wx.Button(self.panel, label="Start", pos=(8, self.line6_y), size=(111, 30))
        self.btn_new_game = wx.Button(self.panel, label="New Game", pos=(8, self.line6_y), size=(111, 30))
        self.btn_choice = wx.Button(self.panel, label="Choice", pos=(125, self.line6_y), size=(111, 30))
        self.btn_next = wx.Button(self.panel, label="Next", pos=(242, self.line6_y), size=(111, 30))

        # _________________________________________________________

        self.timer = wx.Timer(self)

        self.Bind(wx.EVT_CLOSE, self.oper_close_window)
        self.Bind(wx.EVT_TIMER, self.handler_timer)

        self.Bind(wx.EVT_BUTTON, self.oper_btn_start, self.btn_start)
        self.Bind(wx.EVT_BUTTON, self.oper_btn_new_game, self.btn_new_game)
        self.Bind(wx.EVT_BUTTON, self.oper_btn_choice, self.btn_choice)
        self.Bind(wx.EVT_BUTTON, self.oper_btn_next, self.btn_next)

        # _________________________________________________________
        # Make boards first / 最初にボードを作っておく / 처음에 보드를 만들어 둠

        self.mk_first_10board()
        self.mk_first_7board()

        # _________________________________________________________

        # _________________________________________________________
        # menu / メニュー / 메뉴

        menu_file = wx.Menu()
        menu_bar = wx.MenuBar()
        menu_bar.Append(menu_file, "[Ranking and Information]")

        menu_file.Append(21, "Ranking")
        menu_file.AppendSeparator()

        menu_file.Append(22, "Game Information")
        menu_file.AppendSeparator()

        menu_file.Append(23, "Creator Information and GitHub")
        menu_file.AppendSeparator()

        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.oper_menu_view_rec, id=21)
        self.Bind(wx.EVT_MENU, self.oper_about_game, id=22)
        self.Bind(wx.EVT_MENU, self.oper_about_me, id=23)

        self.mk_cover(7)
        self.mk_cover(10)

        self.go_init()

    # _________________________________________________________

    # ____________________________________________________________________________________________________________________________
    # ____________________________________________________________________________________________________________________________
    # Functions / 関数 / 함수들

    # __________________________________________________________________________________________________
    def oper_menu_view_rec(self, event):
        self.view_rec()

    def view_rec(self):
        # _________________________________________________________
        # Show in frame / フレームで見せる / 프레임으로 보이기

        try:
            f = open("b_ranking.wana", "rt", encoding='utf-8')
            text = f.read()
            if text == "":
                text = "No records have been saved yet."
                wx.MessageBox(text, "Ranking", wx.OK)

            else:
                obtained_lines = text.splitlines()
                split_obtained_lines = []

                for i in range(len(obtained_lines)):
                    split_obtained_lines.append(obtained_lines[i].split())

                # _________________________________________________________
                self.frame_temp = wx.Frame(self, title="Ranking", size=wx.Size(700, 500), pos=wx.Point(100, 100))
                self.frame_temp.SetIcon(wx.Icon('a_wana_icon.ico', wx.BITMAP_TYPE_ICO))

                panel_back = wx.Panel(self.frame_temp)

                grid = wx.GridSizer(15, 5, 15, 15)
                panel_back.SetSizer(grid)

                for i in range (0, 5):
                    dummy_text = wx.StaticText(panel_back, wx.NewIdRef(count=1), "", style=wx.ALIGN_CENTER)
                    grid.Add(dummy_text, 0, wx.EXPAND)

                text_temp = wx.StaticText(panel_back, wx.NewIdRef(count=1), "Ranking", style=wx.ALIGN_CENTER)
                grid.Add(text_temp, 0, wx.EXPAND)

                text_temp = wx.StaticText(panel_back, wx.NewIdRef(count=1), "Name", style=wx.ALIGN_CENTER)
                grid.Add(text_temp, 0, wx.EXPAND)

                text_temp = wx.StaticText(panel_back, wx.NewIdRef(count=1), "Size", style=wx.ALIGN_CENTER)
                grid.Add(text_temp, 0, wx.EXPAND)

                text_temp = wx.StaticText(panel_back, wx.NewIdRef(count=1), "Stage", style=wx.ALIGN_CENTER)
                grid.Add(text_temp, 0, wx.EXPAND)

                text_temp = wx.StaticText(panel_back, wx.NewIdRef(count=1), "Score", style=wx.ALIGN_CENTER)
                grid.Add(text_temp, 0, wx.EXPAND)

                for i in range(len(split_obtained_lines)):
                    for j in range(len(split_obtained_lines[i])):
                        text_temp = wx.StaticText\
                            (panel_back, wx.NewIdRef(count=1), split_obtained_lines[i][j], style=wx.ALIGN_CENTER)
                        grid.Add(text_temp, 0, wx.EXPAND)

                btn_exit = wx.Button(panel_back, label="Close", pos=(300, 410))
                btn_exit.Bind(wx.EVT_BUTTON, self.oper_small_close)

                box = wx.BoxSizer(wx.VERTICAL)
                frame.SetSizer(box)
                box.Add(panel_back)

                self.frame_temp.Show(True)

                # _________________________________________________________

            f.close()
        except FileNotFoundError:
            text = "No records have been saved yet."
            wx.MessageBox(text, "Ranking", wx.OK)

    # __________________________________________________________________________________________________
    def oper_small_close(self, event):
        self.frame_temp.Destroy()
    # __________________________________________________________________________________________________
    def oper_about_me(self, event):
        info = wx.adv.AboutDialogInfo()
        info.SetName('ka373')
        info.SetWebSite('https://github.com/ka373', '[GitHub]')
        wx.adv.AboutBox(info)
    # __________________________________________________________________________________________________
    def oper_about_game(self, event):

        try:
            f_how = open("c_game_information.wana", "rt", encoding='utf-8')
            text = f_how.read()
            f_how.close()
        except FileNotFoundError:
            text = "The file related to the game information is missing.\n" \
                   "Please refer to the creator's Github (https://github.com/ka373)."

        wx.MessageBox(text, "How to play", wx.OK)

    # __________________________________________________________________________________________________
    # Radio button click event handler / ラジオボタンクリックイベントハンドラ / 라디오버튼 클릭 이벤트 핸들러

    def set_board_size(self, event):
        temp = event.GetInt()
        if temp == 0:
            self.length_board = 10
            self.show_only_one_board(10, True)
            self.condition_stage_clear = self.condition_stage_clear10
            self.text_clear_condition.SetLabel(
                "( " + str(self.current_stage_score) + " / " + str(self.condition_stage_clear) + " )")

        if temp == 1:
            self.length_board = 7
            self.show_only_one_board(7, True)
            self.condition_stage_clear = self.condition_stage_clear7
            self.text_clear_condition.SetLabel(
                "( " + str(self.current_stage_score) + " / " + str(self.condition_stage_clear) + " )")

    # __________________________________________________________________________________________________
    # Timer event handler / タイマーイベントハンドラ / 타이머 이벤트 핸들러

    def handler_timer(self, event):
        self.elapsed_time += 1

        self.text_sec.SetLabel(str(self.elapsed_time) + "s / " + str(self.time_limit) + "s")

        self.gauge_time.SetValue(self.elapsed_time)  # Gauge value increase
        if self.elapsed_time > self.time_limit:  # Exit state when timeout is exceeded

            if self.state_game == self.const_state_glance:
                self.elapsed_time = 0
                self.gauge_time.SetValue(self.elapsed_time)

                self.go_choice()

            elif self.state_game == self.const_state_choice:
                if self.current_stage == 5 or self.current_stage_score < self.condition_stage_clear:
                    if self.can_game_over:
                        self.go_game_over()
                        self.elapsed_time = 0
                        self.gauge_time.SetValue(self.elapsed_time)
                else:
                    self.go_glance()
                    self.elapsed_time = 0
                    self.gauge_time.SetValue(self.elapsed_time)

    # __________________________________________________________________________________________________
    # Stage increase / ステージ増加 / 스테이지 증가

    def increase_stage(self):
        self.current_stage += 1
        self.current_stage_score = 0
        self.elapsed_time = 0
        self.gauge_time.SetValue(self.elapsed_time)

        self.time_limit -= 1

        self.text_clear_condition.SetLabel(
            "( " + str(self.current_stage_score) + " / " + str(self.condition_stage_clear) + " )")
        self.text_sec.SetLabel(str(self.elapsed_time) + "s / " + str(self.time_limit)+"s")
        self.text_stage.SetLabel(u"Stage: " + str(self.current_stage))

    # __________________________________________________________________________________________________
    # Initial board creation / 最初のボードの作成 / 최초 판 생성

    def mk_first_10board(self):
        for i in range(0, 10):
            for j in range(0, 10):
                temp_btn = wx.Button(self.panel, id=wx.NewIdRef(count=1), label=str(i * j + j),
                                    pos=(j * self.gap_btn + self.btn_start_x, i * self.gap_btn + self.btn_start_y),
                                    size=(25, 25))

                self.btn10_list.append(temp_btn)
                self.Bind(wx.EVT_BUTTON, self.oper_board_btn, temp_btn)
                temp_btn.Hide()

    def mk_first_7board(self):
        for i in range(0, 7):
            for j in range(0, 7):
                temp_btn = wx.Button(self.panel, id=wx.NewIdRef(count=1), label=str(i * j + j),
                                     pos=(j * self.gap_btn + self.btn_start_x, i * self.gap_btn + self.btn_start_y),
                                     size=(25, 25))

                self.btn7_list.append(temp_btn)
                self.Bind(wx.EVT_BUTTON, self.oper_board_btn, temp_btn)
                temp_btn.Hide()

    # __________________________________________________________________________________________________
    # Button click on board / ボードのボタンをクリック / 보드의 버튼 클릭

    def oper_board_btn(self, event):

        if self.state_game == self.const_state_choice:
            event.GetEventObject().Disable()

            label_clicked_btn = event.GetEventObject().GetLabelText()

            # Wana click: add score
            if label_clicked_btn == "*":
                self.accumulated_score += 1
                self.current_stage_score += 1
                self.text_score.SetLabel(u"Score: " + str(self.accumulated_score))
                self.text_clear_condition.SetLabel(
                    "( " + str(self.current_stage_score) + " / " + str(self.condition_stage_clear) + " )")

                event.GetEventObject().SetLabel(u"O")

            # Wana X: game over
            else:
                self.go_game_over()

    # __________________________________________________________________________________________________
    # Board deformation / ボードの変形 / 판 변형

    def mk_ex_board_from_seed(self, size):
        if size == 10:
            for i in range(0, size*size):
                self.btn10_list[i].SetLabel(str(i))
        elif size == 7:
            for i in range(0, size*size):
                self.btn7_list[i].SetLabel(str(i))

    def mk_game_board_from_seed(self, size):
        if size == 10:
            for i in range(0, size*size):
                self.btn10_list[i].SetLabel("")

            sample_btn10_list = random.sample(self.btn10_list, self.num_wanas10)
            for i in range(0, self.num_wanas10):
                sample_btn10_list[i].SetLabel("*")

        elif size == 7:
            for i in range(0, size*size):
                self.btn7_list[i].SetLabel("")

            sample_btn7_list = random.sample(self.btn7_list, self.num_wanas7)
            for i in range(0, self.num_wanas7):
                sample_btn7_list[i].SetLabel("*")

    # __________________________________________________________________________________________________
    # Show or hide boards / ボード表示・非表示 / 보드 보이거나 없애기

    # Size 7
    def set_visibility_enable_7board(self, want_v, want_enable):
        if want_v:
            for i in range(0, 49):
                self.btn7_list[i].Show()

                if want_enable:         self.btn7_list[i].Enable()
                else:                   self.btn7_list[i].Disable()
        else:
            for i in range(0, 49):
                self.btn7_list[i].Hide()

                if want_enable:         self.btn7_list[i].Enable()
                else:                   self.btn7_list[i].Disable()

    # Size 10
    def set_visibility_enable_10board(self, want_v, want_enable):
        if want_v:
            for i in range(0, 100):
                self.btn10_list[i].Show()

                if want_enable:         self.btn10_list[i].Enable()
                else:                   self.btn10_list[i].Disable()
        else:
            for i in range(0, 100):
                self.btn10_list[i].Hide()

                if want_enable:         self.btn10_list[i].Enable()
                else:                   self.btn10_list[i].Disable()

    # __________________________________________________________________________________________________
    # cover / カバー / 커버

    def over_hide(self, event):
        event.GetEventObject().Hide()

    def mk_cover(self, size):
        for i in range(0, size):
            for j in range(0, size):
                temp_cover = wx.StaticText(self.panel, wx.NewIdRef(count=1), label=" ", size=(20, 20),
                                           pos=(j * self.gap_btn + self.btn_start_x + 7,
                                                i * self.gap_btn + self.btn_start_y+3)
                                           )
                temp_cover.SetBackgroundColour((0, 65, 0))
                temp_cover.Bind(wx.EVT_ENTER_WINDOW, self.over_hide)
                temp_cover.Hide()

                if size == 7:           self.cover7_list.append(temp_cover)
                elif size == 10:        self.cover10_list.append(temp_cover)

    def hide_covers(self):
        for i in range(0, 10):
            for j in range(0, 10):
                self.cover10_list[i * 10 + j].Hide()

        for i in range(0, 7):
            for j in range(0, 7):
                self.cover7_list[i * 7 + j].Hide()

    def show_only_one_cover(self, size):
        for i in range(0, 10):
            for j in range(0, 10):
                if size == 10:
                    self.cover10_list[i * 10 + j].Show()
                else:
                    self.cover10_list[i * 10 + j].Hide()

        for i in range(0, 7):
            for j in range(0, 7):
                if size == 10:
                    self.cover7_list[i * 7 + j].Hide()
                else:
                    self.cover7_list[i * 7 + j].Show()

    def show_only_one_board(self, size_board, want_enable):
        if size_board == 10:
            self.set_visibility_enable_10board(True, want_enable)
            self.set_visibility_enable_7board(False, False)

        if size_board == 7:
            self.set_visibility_enable_10board(False, False)
            self.set_visibility_enable_7board(True, want_enable)

    # __________________________________________________________________________________________________
    # state_init

    def oper_btn_new_game(self, event):
        self.hide_covers()
        self.go_init()

    def go_init(self):
        self.state_game = self.const_state_init

        self.rb_size.SetSelection(0)

        self.elapsed_time = 0
        self.accumulated_score = 0
        self.text_score.SetLabel(u"Score: 0")

        self.current_stage = 0
        self.text_stage.SetLabel(u"Stage: 0")

        self.length_board = 10
        self.time_limit = 11
        self.elapsed_time = 0

        self.btn_enable = 0

        self.username.Enable()
        self.rb_size.Enable()
        self.btn_sp.Disable()

        self.gauge_time.SetValue(0)
        self.text_description.SetLabel(u"WANASAGASHI")
        self.rb_size.Show()
        self.username.Show()

        self.btn_start.Show()
        self.btn_start.Enable()

        self.btn_new_game.Hide()

        self.btn_choice.Disable()
        self.btn_next.Disable()

        # Set up example boards and see only one
        self.mk_ex_board_from_seed(self.length_board)
        self.mk_ex_board_from_seed(7)
        self.show_only_one_board(self.length_board, True)

    # __________________________________________________________________________________________________
    # Jump into glance: Start button, Next button
    # glance状態に移る：スタートボタン、ネクストボタン
    # glance로 넘어감: 시작 버튼, 넥스트 버튼

    def oper_btn_start(self, event):
        self.btn_enable = 0
        self.go_glance()

    def oper_btn_next(self, event):
        if self.current_stage == 5:
            self.go_game_over()
        elif self.current_stage_score >= self.condition_stage_clear:
            self.go_glance()

    def go_glance(self):
        self.show_only_one_board(self.length_board, True)

        # switch to glance state
        self.state_game = self.const_state_glance
        self.increase_stage()

        # Hide covers
        self.hide_covers()

        self.timer.Start(1000)  # Timer event occurs every second
        g = self.length_board

        self.text_description.SetLabel(u"Please see the locations of the Wanas.")

        self.gauge_time.SetRange(self.time_limit)
        self.elapsed_time = 0
        self.rb_size.Disable()

        self.btn_start.Disable()
        self.btn_choice.Enable()
        self.btn_next.Disable()
        self.btn_sp.Enable()

        self.mk_game_board_from_seed(self.length_board)

    # __________________________________________________________________________________________________
    # Jump into choice: Choice button
    # choice状態に移る：チョイスボタン
    # choice로 넘어감: 초이스 버튼

    def oper_btn_choice(self, event):
        self.go_choice()

    def go_choice(self):

        # switch to choice state
        self.state_game = self.const_state_choice

        # Show Cover
        self.show_only_one_cover(self.length_board)

        self.gauge_time.SetRange(self.time_limit)
        self.elapsed_time = 0

        # Button Validation Settings
        self.btn_choice.Disable()
        self.btn_start.Disable()
        self.btn_next.Enable()

        self.btn_enable = 1

        self.timer.Start(1000)  # Timer event occurs every second
        self.elapsed_time = 0

        self.gauge_time.SetValue(0)
        self.text_description.SetLabel(u"Find the Wanas!")

    # __________________________________________________________________________________________________
    # state_game_over

    def oper_btn_sp(self, event):
        self.can_game_over = False
        msg = wx.MessageBox("Do you want to stop playing the game?",
                            "Stop Playing",
                            wx.OK | wx.CANCEL | wx.ICON_WARNING)

        if msg == wx.OK:
            self.go_game_over()

        self.can_game_over = True

    def go_game_over(self):
        self.text_description.SetLabel(u"Game Over!")

        self.state_game = self.const_state_game_over
        self.timer.Stop()

        self.save_rec()
        self.view_rec()

        self.show_only_one_board(self.length_board, True)

        self.btn_start.Hide()
        self.btn_new_game.Show()

        self.btn_sp.Disable()

        self.btn_next.Disable()
        self.btn_start.Disable()
        self.btn_choice.Disable()

    # __________________________________________________________________________________________________
    # Save score after game over / ゲームオーバー後のスコア保存 / 게임 종료시 점수 저장

    def show_save_dlg(self):
        name = self.username.GetValue()
        name = name.replace(" ", "")

        self.show_save_dlg_onemore_return = False

        # Name check
        dlg = wx.TextEntryDialog(self, 'Please check your name (within 10 characters).\n'
                                       '\n'
                                       '* Spaces between characters will be removed.\n'
                                       '* Letters longer than 10 characters will be truncated.',
                                 'Your record can be added!')
        dlg.SetValue(name)

        if dlg.ShowModal() == wx.ID_OK:
            self.name_confirm = dlg.GetValue().strip()
            self.name_confirm = self.name_confirm.replace(" ", "")

            if len(self.name_confirm) > 10:
                self.name_confirm = self.name_confirm[0:10]

            return True

        dlg.Destroy()
        return False  # True if saved, False if not saved

    def save_rec(self):
        str_format = '%-17s%-15s%-15s%-15s%-15s\n'
        temp_str = ""

        # _________________________________________________________

        try:
            f_rec = open("b_ranking.wana", "rt", encoding='utf-8')
            text = f_rec.read()
            f_rec.close()
        except FileNotFoundError:
            text = ""

        if text == "":

            if self.show_save_dlg():
                temp_str = str_format % ('1',
                                         self.name_confirm,
                                         str(self.length_board) + "x" + str(self.length_board),
                                         str(self.current_stage),
                                         str(self.accumulated_score))

        else:
            obtained_lines = text.splitlines()
            split_obtained_lines = []

            for i in range(len(obtained_lines)):
                split_obtained_lines.append(obtained_lines[i].split())

                # Note: I put int values where the string was for sorting
                # This method may omit the conversion code but may not be neat.
                split_obtained_lines[i][4] = int(split_obtained_lines[i][4])

            # Sort list
            split_obtained_lines.sort(key=itemgetter(4), reverse=True)

            # Check and add the current user's score
            is_inserted = False
            for i in range(len(split_obtained_lines)):

                if is_inserted == False:
                    if int(split_obtained_lines[i][4]) <= self.accumulated_score:

                        if self.show_save_dlg():
                            split_obtained_lines.insert(i, [str(i + 1),
                                                            self.name_confirm,
                                                            str(self.length_board) + "x" + str(self.length_board),
                                                            str(self.current_stage),
                                                            int(self.accumulated_score)])

                            if len(split_obtained_lines) == 11:
                                del split_obtained_lines[10]

                            is_inserted = True
                        else:
                            break

                    if i == len(split_obtained_lines) - 1 and len(split_obtained_lines) < 10:
                        if self.show_save_dlg():
                            split_obtained_lines.insert(i+1, [str(i + 2),
                                                              self.name_confirm,
                                                              str(self.length_board) + "x" + str(self.length_board),
                                                              str(self.current_stage),
                                                              int(self.accumulated_score)])

                            if len(split_obtained_lines) == 11:
                                del split_obtained_lines[10]

                            is_inserted = True
                        else:
                            break

                else:
                    split_obtained_lines[i][0] = str(int(split_obtained_lines[i][0]) + 1)

            # Sort list=> Double check
            split_obtained_lines.sort(key=itemgetter(4), reverse=True)

            temp_str = ""

            for i in range(len(split_obtained_lines)):

                split_obtained_lines[i][0] = str(i+1)
                temp_str += str_format % (split_obtained_lines[i][0],
                                          split_obtained_lines[i][1],
                                          split_obtained_lines[i][2],
                                          split_obtained_lines[i][3],
                                          split_obtained_lines[i][4])

        # Save to file
        f = open("b_ranking.wana", "wt", encoding='utf-8')
        f.write(temp_str)

        f.close()
        # _________________________________________________________

    # __________________________________________________________________________________________________
    def oper_close_window(self, event):
        self.Destroy()

# end of Functions / 関数 / 함수들
# ____________________________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________________________


if __name__ == '__main__':
    app = wx.App()
    # frame = Wanasagashi(parent=None, id=-1)
    frame = Wanasagashi()
    frame.SetIcon(wx.Icon('a_wana_icon.ico', wx.BITMAP_TYPE_ICO))

    frame.Show()
    app.MainLoop()


# ____________________________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________________________
