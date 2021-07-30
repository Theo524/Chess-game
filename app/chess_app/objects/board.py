from tkinter import *
from tkinter import messagebox, ttk
import string
import os
from PIL import Image, ImageTk
import csv
import chess


class Board(Frame):

    def __init__(self, master, **kwargs):
        Frame.__init__(self, master)

        # Game attributes
        self.player_one_turn = True
        self.player_two_turn = False
        self.AI_turn = False
        self.moves = 1

        # Trackers
        self.chess_notation = []
        self.deleted_pieces = []
        self.tracker = []

        # ai_board = []
        # Initialize chess board
        self.ai_board = chess.Board()
        print(self.ai_board)
        # self.ai_board.legal_moves

        # required data
        self.letters = list(string.ascii_lowercase[:8])  # chess letters (a-h)
        self.alphabet = list(string.ascii_letters)  # alphabet
        self.nums = [str(i) for i in range(10)]  # Numbers as str (0-9)

        # data structures
        self.board = {}  # game board around which game revolves
        self.coordinates = []  # 2d array of all chess positions
        self.pieces = []  # 1d array of all chess positions
        self.add_chess_pieces_positions()

        # frame containing chess notation tab
        if kwargs:
            self.widgets_frame = kwargs['widgets_frame']
        else:
            self.widgets_frame = Frame(self.master)

        # game mode
        mode = master.master.mode

        # game_settings
        self.difficulty = None
        self.time = None
        self.game_type = None
        self.player_piece_color = None
        self.opponent_piece_color = None
        self.border_color = None
        self.board_color = None
        self.set_game_settings(mode)  # sets game settings

        # colors for board
        self.board_colors = [
                                'white', self.board_color, 'white', self.board_color, 'white', self.board_color,
                                'white', self.board_color,
                                self.board_color, 'white', self.board_color, 'white', self.board_color, 'white',
                                self.board_color, 'white',
                            ] * 4

        # file paths
        self.pieces_file_path = os.getcwd() + '\\app\\chess_app\\pieces'
        self.settings_file_path = os.getcwd() + '\\app\\chess_app\\all_settings'

        # Dictionaries storing piece images file names
        self.black_pieces, self.white_pieces = self.get_piece_img()

        # Frame attributes border
        self.configure(highlightthickness=5, highlightbackground=self.border_color)

        # deleted_pieces tracking pos
        self.b_x = 0
        self.b_y = 0
        self.w_x = 0
        self.w_y = 0

        # add notation if needed
        if self.widgets_frame:
            self.add_notation_tab()

        self.game_fen = self.get_game_fen_string()

    def add_chess_pieces_positions(self):
        """Populate 1d and 2d array chess"""

        # get coordinates, e.g. 'a1', 'b1', etc into a 2 dimensional array
        for row in range(8):
            temp = []
            for letter in self.letters:
                temp.append(f'{letter}{row + 1}')
            self.coordinates.append(temp)

        for row in self.coordinates:
            print(row, ',')

        # get coordinates, e.g. 'a1', 'b1', etc into a 1 dimensional array
        for row in self.coordinates:
            for piece in row:
                self.pieces.append(piece)

    def set_game_settings(self, mode):
        """Sets Game settings"""

        if mode == 'guest':

            # open default settings file
            with open(os.getcwd() + '\\app\\chess_app\\all_settings\\guest\\default_game_settings.csv', 'r') as f:
                csv_reader = csv.reader(f, delimiter='-')
                next(csv_reader)

                for row in csv_reader:
                    print(row)
                    # retrieve settings in file
                    self.difficulty = row[0]
                    self.time = row[1]
                    self.game_type = row[2]
                    self.player_piece_color = row[3]
                    self.opponent_piece_color = row[4]
                    self.border_color = row[5]
                    self.board_color = row[6]

        elif mode == 'user':
            # fetch settings for that specific user
            with open(os.getcwd() + '\\app\\chess_app\\all_settings\\user\\user_game_settings.csv', 'r') as f:
                csv_reader = csv.reader(f, delimiter='-')
                next(csv_reader)

                for row in csv_reader:
                    print(row)
                    # retrieve these personalized settings from user file
                    self.difficulty = row[0]
                    self.time = row[1]
                    self.game_type = row[2]
                    self.player_piece_color = row[3]
                    self.opponent_piece_color = row[4]
                    self.border_color = row[5]
                    self.board_color = row[6]

    def add_notation_tab(self):
        """Implement game tabs"""

        # ---------------NOTEBOOK--------------
        # notebook for chess notation
        self.notebook = ttk.Notebook(self.widgets_frame, height=600, width=600)
        self.notebook.pack(pady=(7, 0), padx=5)

        # first tab
        self.notation_tab = Text(self.notebook)
        self.notation_tab.pack()

        # third tab
        self.deleted_pieces_tab = Text(self.notebook)
        self.deleted_pieces_tab.pack()

        # second tab
        self.deleted_tab_visual = Frame(self.notebook, bg=self.board_colors[1])
        self.deleted_tab_visual.configure(highlightthickness=5, highlightbackground='black')

        self.deleted_tab_visual.pack()

        # add  tabs to chess notebook
        self.notebook.add(self.notation_tab, text='Notation')
        self.notebook.add(self.deleted_tab_visual, text='Deleted pieces')
        self.notebook.add(self.deleted_pieces_tab, text='Deleted pieces (text)')

    def make_board(self):
        """Make the board dict"""

        # Create a dictionary with the main key being a coordinate
        # Assign coordinates to their corresponding button
        x = 0
        y = 7
        # repeat 64 times (number of coordinates in chess)
        for i in range(len(self.board_colors)):
            # Store the current coordinate in a variable e.g in the first iteration it represents a8
            # in terms of y and x (from self.coordinates)
            current_position = self.coordinates[y][x]

            # make board
            self.board[current_position] = {'button': Button(self, bg=self.board_colors[i],
                                                             text=f'\t        {current_position}',
                                                             font=('arial', 7),
                                                             compound=BOTTOM,
                                                             activebackground='light blue',
                                                             relief=SOLID,
                                                             bd=1,
                                                             cursor='tcross',
                                                             highlightbackground="black",
                                                             highlightcolor="black",
                                                             command=lambda p=current_position:
                                                             self.update_current_piece(p)),
                                            'piece': {'piece_name': None, 'piece_color': None},
                                            'color': self.board_colors[i],
                                            'selected': False
                                            }

            # coordinates in first iteration are 'x=0, y=7', where the data is 'a8'
            # next coordinates are 'x=1, y=7' where the val is 'b8'
            # hence we move to the next item in the current list by adding 1 to x
            x += 1
            # Once we reach the end of the list, the x coordinate is 8, so we move up one in the y axis
            # by subtracting 1 (from 8 to 7 to 6 and so on...)
            if x == 8:
                y -= 1
                x = 0

    def place_buttons(self):
        """Place the actual buttons on the screen"""

        x = 0
        y = 0
        for button in self.board.values():
            # We access the button object and use tkinter 'grid()' to set the column and row with x and y
            button['button'].grid(column=x, row=y)

            # We place the buttons on the frame in a linear way, so the first row would be placed
            # and x represents each button/column in this first row
            x += 1
            # When we reach th end of the row, which is 8 buttons per row, we move to the next row
            if x == 8:
                # Set x to 0 to start a series of columns from the begging and increase y by one to move one row down
                x = 0
                y += 1

    def place_default_pieces_on_screen(self):
        """Place default starting pieces on the screen"""

        # Thanks to the method 'place_piece' I've made, we can easily move and delete any piece from the screen
        # We enter the piece, the color and the position we want to place it at as parameters

        # use a FEN string (Forsyth-Edwards Notation)
        staring_fen_string = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

        self.place_fen_string(staring_fen_string)

    def place_fen_string(self, fen_str):
        """Convert fen string and place pieces on board"""

        # Thanks to the method 'place_piece' I've made, we can easily move and delete any piece from the screen
        # We enter the piece, the color and the position we want to place it at as parameters

        # create two lists, one for a dict containing useful data and another for key vals
        coordinates_copy = self.coordinates[:]
        coordinates = []
        for row in range(8):
            temp = []
            for letter in self.letters:
                temp.append({f'{letter}{row + 1}': 'blank'})
            coordinates.append(temp)

        # reverse them so they match required indexes
        coordinates.reverse()
        coordinates_copy.reverse()

        # fen value
        full_str = list(fen_str)

        # coordinates
        x = 0
        y = 0

        # iterate trough each value in the fen string
        for symbol in full_str:
            if symbol in ['/']:
                # if bracket
                # move one row down
                y += 1

                # and return to starting col
                x = 0

            if symbol in self.alphabet:
                # if letter, assign letter to dictionary
                coordinates[y][x] = {f'{coordinates_copy[y][x]}': symbol}
                x += 1

            if symbol in self.nums:
                # if number move jump spaces
                x += int(symbol)

        # place pieces on board
        for row in coordinates:
            for val in row:
                # get the key as a list (position)
                position = [key for key in val.keys()]
                # get the piece as a list
                piece = [value for value in val.values()]

                # convert the lists to str
                piece = ''.join(piece)
                position = ''.join(position)

                # get the color from the letter type
                # according to the rules - white, lower case and black uppercase
                if piece in list(string.ascii_lowercase):
                    color = self.opponent_piece_color
                elif piece in list(string.ascii_uppercase):
                    color = self.player_piece_color
                else:
                    color = 'blank'

                piece_dict = {'P': 'prawn', 'p': 'prawn',
                              'R': 'rook', 'r': 'rook',
                              'N': 'knight', 'n': 'knight',
                              'B': 'bishop', 'b': 'bishop',
                              'Q': 'queen', 'q': 'queen',
                              'K': 'king', 'k': 'king',
                              'blank': 'blank'}

                # finally place the piece
                self.place_piece(piece_dict[piece], color, position)

    def update_current_piece(self, position):
        """Command assigned to every button in the board"""

        # color of the button, piece and piece color the user just clicked
        current_button_color = self.board[position]['color']
        piece_name = self.board[position]['piece']['piece_name']
        piece_color = self.board[position]['piece']['piece_color']

        if self.tracker:
            # color of the button, piece and piece color the last clicked
            # It can be retrieved because the tracker is only updated at the end of this function
            old_piece_name = self.tracker[-1]['selected_piece']['piece_name']
            old_piece_color = self.tracker[-1]['selected_piece']['piece_color']
            old_piece_position = self.tracker[-1]['player_clicked']

        # HIGHLIGHTING MOVES
        # allowing turns (two player mode)
        # if the game type is 'two_player' mode and a piece was clicked
        if self.game_type == 'two_player':
            if self.player_one_turn:
                # If it is player one turn
                if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                    self.reset_board_colors()

                    # We only allow player pieces to be highlighted
                    # rooks
                    if self.board[position]['piece']['piece_name'] == 'rook':
                        self.piece_highlighting(f'{position}', 'rook', self.player_piece_color)

                    # prawn
                    if self.board[position]['piece']['piece_name'] == 'prawn':
                        self.piece_highlighting(f'{position}', 'prawn', self.player_piece_color)

                    # bishop
                    if self.board[position]['piece']['piece_name'] == 'bishop':
                        self.piece_highlighting(f'{position}', 'bishop', self.player_piece_color)

                    # knight
                    if self.board[position]['piece']['piece_name'] == 'knight':
                        self.piece_highlighting(f'{position}', 'knight', self.player_piece_color)

                    # queen
                    if self.board[position]['piece']['piece_name'] == 'queen':
                        self.piece_highlighting(f'{position}', 'queen', self.player_piece_color)

                    # king
                    if self.board[position]['piece']['piece_name'] == 'king':
                        self.piece_highlighting(f'{position}', 'king', self.player_piece_color)

                # If the piece is enemy
                if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                    print('\n-------------------ACTION-------------------')
                    print('Action: Player selected piece')
                    print(f'Selected piece: {piece_name}')
                    print(f'Piece color: {piece_color}')
                    print('-------------------END-------------------')
                    self.reset_board_colors()

            if self.player_two_turn:
                # If it is the second player turn
                if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                    print('\n-------------------ACTION-------------------')
                    print('Action: Player selected piece')
                    print(f'Selected piece: {piece_name}')
                    print(f'Piece color: {piece_color}')
                    print('-------------------END-------------------')
                    self.reset_board_colors()

                    # We only allow enemy pieces to be highlighted

                    # rooks
                    if self.board[position]['piece']['piece_name'] == 'rook':
                        self.piece_highlighting(f'{position}', 'rook', self.opponent_piece_color)

                    # prawn
                    if self.board[position]['piece']['piece_name'] == 'prawn':
                        self.piece_highlighting(f'{position}', 'prawn', self.opponent_piece_color)

                    # bishop
                    if self.board[position]['piece']['piece_name'] == 'bishop':
                        self.piece_highlighting(f'{position}', 'bishop', self.opponent_piece_color)

                    # knight
                    if self.board[position]['piece']['piece_name'] == 'knight':
                        self.piece_highlighting(f'{position}', 'knight', self.opponent_piece_color)

                    # queen
                    if self.board[position]['piece']['piece_name'] == 'queen':
                        self.piece_highlighting(f'{position}', 'queen', self.opponent_piece_color)

                    # king
                    if self.board[position]['piece']['piece_name'] == 'king':
                        self.piece_highlighting(f'{position}', 'king', self.opponent_piece_color)

                # If the piece is black
                if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                    print('\n-------------------ACTION-------------------')
                    print('Action: Player selected piece')
                    print(f'Selected piece: {piece_name}')
                    print(f'Piece color: {piece_color}')
                    print('-------------------END-------------------')
                    self.reset_board_colors()

        # If the color of the button is green
        # It would mean the player had already clicked a piece previously which marked possible moves in green
        if current_button_color == 'light green':
            # make the move
            self.make_move(old_piece_name, old_piece_color, old_piece_position, position)

            # Add to notation
            self.update_notation('moved_piece', position, old_piece_name, new_piece_name=None)

            # increase number of moves by one
            self.moves += 1

            # We now swap turns so only one side can make moves
            self.swap_turns()

        # if the button clicked is red, that means the piece is to be deleted
        if current_button_color == 'red':

            # Console output
            print('\n-------------------ACTION-------------------')
            print('Action: Player deleted a piece')
            print(f'Piece used: {old_piece_name}')
            print(f'Deleted piece: {piece_name}')
            print(f'PLayer piece color: {old_piece_color}')
            print('-------------------END_OF_ACTION-------------------\n')

            # make move
            self.make_move(old_piece_name, old_piece_color, old_piece_position, position)

            # add to notation
            self.update_notation('deleted_piece', position, old_piece_name, piece_name)

            # increase number of moves by one
            self.moves += 1

            # add this deleted piece to the deleted pieces list
            self.deleted_pieces.append([piece_name, piece_color])
            self.deleted_pieces_tab.insert('end', '(')
            self.deleted_pieces_tab.insert('end', self.board[position]['piece']['piece_color'])
            self.deleted_pieces_tab.insert('end', ', ')
            self.deleted_pieces_tab.insert('end', self.board[position]['piece']['piece_name'])
            self.deleted_pieces_tab.insert('end', '), ')

            # swap turns
            self.swap_turns()

        # Whenever the user clicks a non piece or empty space, a messagebox appears
        # reset the board colors
        if current_button_color in ['white', self.board_colors[1]] and piece_name is None:

            # message
            messagebox.showerror('Error', f'{position} is an invalid move')

            # Console output
            print('\n-------------------ACTION-------------------')
            print('Action: Player clicked an empty space')
            print(f'Position: {position}')
            print(f'Output: Reset board to normal')
            print('-------------------END-------------------\n')
            self.reset_board_colors()

        # Make AI board (Not done yet)

        # Allows to track user history of clicks, appends the current move
        self.tracker.append({'player_clicked': position,
                             'selected_piece': self.board[position]['piece'],
                             'color': self.board[position]['color']})

        # checkmate?
        print(self.ai_board.is_checkmate())

        # stalmate? Game ends in draw.
        print(self.ai_board.is_stalemate())

    def make_move(self, piece_name, color, old_position, new_position):
        """Make a move in the chess board"""

        # place the selected piece in the selected spot
        self.place_piece(piece_name, color, new_position)
        # replace the place where that piece originally was with a blank space img
        self.place_piece('blank', 'blank', old_position)

        # move for virtual board
        move = chess.Move.from_uci(f'{old_position}{new_position}')

        # legal moves available
        legal_moves = list(self.ai_board.legal_moves)

        # Make move in virtual board
        self.ai_board.push(move)

        # Console
        print(self.ai_board)

        # new game fen
        self.game_fen = self.get_game_fen_string()

        # reset board colors back to normal
        self.reset_board_colors()
        self.master.master.update()

    def update_notation(self, mode, position, old_piece_name, new_piece_name):
        """CHESS NOTATION"""

        if mode == 'moved_piece':
            # chess notation tracker(list)
            self.chess_notation.append(f'{old_piece_name[0].upper()}{position}')
            # The moves variable is updated every turn, so every even number of moves corresponds to a player
            # while every odd number of moves corresponds to the other player
            if self.moves % 2 == 0:
                # even number of moves, 'P2' used to mark player2
                self.notation_tab.insert('end', f'{self.moves}.(P2:{self.chess_notation[-1]}) ')
            else:
                # even number of moves, 'P1' used to mark player1
                self.notation_tab.insert('end', f'{self.moves}.(P1:{self.chess_notation[-1]}) ')

        if mode == 'deleted_piece':
            # This time we add an 'x' in the middle to show that a piece is being destroyed
            self.chess_notation.append(f'{old_piece_name[0].upper()}x{position}')
            # also add piece image
            # w_x and w_y represent white x and white y
            if self.board[position]['piece']['piece_color'] == 'black':
                img = PhotoImage(file=self.white_pieces[f'{new_piece_name}'])
            else:
                img = PhotoImage(file=self.black_pieces[f'{new_piece_name}'])
            l = Label(self.deleted_tab_visual, image=img)
            l.configure(borderwidth=5, bg=self.board_colors[1])
            l.grid(column=self.b_x, row=self.b_y)
            l.image = img
            self.b_x += 1
            if self.b_x == 8:
                self.b_x = 0
                self.b_y += 1

            # add the move to chess notation
            if self.moves % 2 == 0:
                self.notation_tab.insert('end', f'{self.moves}.(P2:{self.chess_notation[-1]}) ')
            else:
                self.notation_tab.insert('end', f'{self.moves}.(P1:{self.chess_notation[-1]}) ')

    def swap_turns(self):
        """Swap turns between players"""

        if self.game_type == 'two_player':
            if self.moves % 2 == 0:
                self.player_two_turn = True
                self.player_one_turn = False
            else:
                self.player_two_turn = False
                self.player_one_turn = True

        if self.game_type == 'computer':
            pass

    def reset_board_colors(self):
        """Reset board colors to normal(to eliminate highlighting)"""

        i = 0
        coordinates = self.coordinates[:]
        coordinates.reverse()
        # iterate through the entire board and set the color of each button back to its corresponding one
        # by iterating over the board colors at the same time
        for row in coordinates:
            for col in row:
                self.board[col]['button'].configure(bg=self.board_colors[i])
                self.board[col]['color'] = self.board_colors[i]
                i += 1

    def piece_highlighting(self, position, piece, piece_color):
        """Highlights all possible moves for a given piece"""

        # We highlight the piece color to blue, so it is evident what piece the user selected
        self.board[position]['button'].configure(bg='light blue')

        # rook
        if piece == 'rook':
            # rook moves horizontally and vertically in a straight line

            # The function returns a list of possible moves for the piece
            all_possible_rook_moves = self.get_all_possible_moves('rook', 'none', position)

            if piece_color == self.player_piece_color:
                # black piece
                for move_pattern in all_possible_rook_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # Empty button with no piece
                        if self.board[position]['piece']['piece_color'] is None:
                            # Highlight the button, by converting it to 'light green'
                            self.board[position]['button'].configure(bg='light green')
                            # Set the color variable of that button to light green (no longer black/white)
                            self.board[position]['color'] = 'light green'

                        # check if the piece is for the enemy
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            # if it is white, highlight it with red so it becomes availible to delete
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # Detect a black piece, if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color \
                                and self.board[position]['piece']['piece_name'] != 'rook':
                            break

            if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                # white piece
                for move_pattern in all_possible_rook_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if the piece is not white
                        if self.board[position]['piece']['piece_color'] is None:
                            # Highlight the button, by converting it to 'light green'
                            self.board[position]['button'].configure(bg='light green')
                            # Set the color variable of that button to light green (no longer black/white)
                            self.board[position]['color'] = 'light green'

                        # check if the piece is black
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # Detect a white piece, if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color \
                                and self.board[position]['piece']['piece_name'] != 'rook':
                            break

        # bishop
        if piece == 'bishop':
            # bishop moves diagonally in all directions
            all_possible_bishop_moves = self.get_all_possible_moves('bishop', 'none', position)

            if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                # black piece
                for move_pattern in all_possible_bishop_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # check if enemy piece
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            # if enemy piece, highlight to red
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # check if black piece
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            # if black piece stop highlighting
                            break

                        # if there is no piece, convert to green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

            if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:

                for move_pattern in all_possible_bishop_moves:
                    for position in move_pattern:
                        # check if enemy piece
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # check if black piece
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            break

                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

        # knight
        if piece == 'knight':
            # knight moves two blocks forward and marks the side in all directions
            all_possible_knight_moves = self.get_all_possible_moves('knight', 'none', position)

            if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                # black piece
                for move_pattern in all_possible_knight_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if the piece is black, move to the next move
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            break

                        # if the piece is white, highlight red and mark as enemy
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            continue



                        # if there is no piece, highlight and mark green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

            if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                # white piece
                for move_pattern in all_possible_knight_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if the piece is black, highlight red and mark as enemy
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            continue

                        # if the piece is white, move to the next move
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            continue

                        # if there is no piece, highlight and mark green green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

        # queen
        if piece == 'queen':
            # queen moves are just a combination of a rook and a bishop
            all_possible_queen_moves = self.get_all_possible_moves('queen', 'none', position)

            if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                # black piece
                for move_pattern in all_possible_queen_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if there is no piece highlight the button to green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

                        # check if the piece is white, if so make it red
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # Detect a black piece, if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            break

            if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                # white piece
                for move_pattern in all_possible_queen_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        if self.board[position]['piece']['piece_color'] is None:
                            # if there is no piece, highlight the button to green
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

                        # check if the piece is black, if it is make it red
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            break

                        # Detect a black piece,if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            break

        # king
        if piece == 'king':
            all_possible_king_moves = self.get_all_possible_moves('king', 'none', position)

            if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                # black piece
                for move_pattern in all_possible_king_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        # if there is no piece highlight the button to green
                        if self.board[position]['piece']['piece_color'] is None:
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

                        # check if the piece is white, if so make it red
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            continue

                        # Detect a black piece, if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            continue

            if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                # white piece
                for move_pattern in all_possible_king_moves:
                    # loop through each list in this list of all possible moves
                    for position in move_pattern:
                        if self.board[position]['piece']['piece_color'] is None:
                            # if there is no piece, highlight the button to green
                            self.board[position]['button'].configure(bg='light green')
                            self.board[position]['color'] = 'light green'

                        # check if the piece is black, if it is make it red
                        if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                            self.board[position]['button'].configure(bg='red')
                            self.board[position]['color'] = 'red'
                            continue

                        # Detect a black piece,if there is one,we stop highlighting
                        if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                            continue

        # prawns
        if piece_color == self.player_piece_color and piece == 'prawn':
            # Prawns only move 2 up and 1 up to the side to delete piece
            all_prawns = self.get_all_possible_moves('prawn', self.player_piece_color, position)

            # The moves generated in a list which was part of a larger list
            prawn_up = all_prawns[0]
            right_diagonal = all_prawns[1]
            left_diagonal = all_prawns[2]

            for position in prawn_up:
                # only loops twice, e.g. 'e5' would generate 'e6' and 'e7'

                # if white or black piece stop highlight
                if self.board[position]['piece']['piece_color'] in [self.opponent_piece_color, self.player_piece_color]:
                    break

                # else highlight as green
                self.board[f'{position}']['button'].configure(bg='light green')
                self.board[f'{position}']['color'] = 'light green'

            for position in left_diagonal:
                # left diagonal is just one position e.g. for 'b2' it would be 'b1'
                # if we detect an enemy piece there, we highlight red
                if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                    self.board[position]['button'].configure(bg='red')
                    self.board[position]['color'] = 'red'

            for position in right_diagonal:
                # right diagonal is just one position e.g. for 'b2' it would be 'b3'
                # if we detect an enemy piece there, we highlight red
                if self.board[position]['piece']['piece_color'] == self.opponent_piece_color:
                    self.board[position]['button'].configure(bg='red')
                    self.board[position]['color'] = 'red'

        if piece_color == self.opponent_piece_color and piece == 'prawn':
            # Prawns only move 2 up and 1 up to the side to delete piece
            all_prawns = self.get_all_possible_moves('prawn', self.opponent_piece_color, position)

            # The moves generated in a list which was part of a larger list
            prawn_up = all_prawns[0]
            left_diagonal = all_prawns[1]
            right_diagonal = all_prawns[2]

            for position in prawn_up:
                # if the piece is white we stop highlighting
                if self.board[position]['piece']['piece_color'] in [self.opponent_piece_color, self.player_piece_color]:
                    break

                self.board[f'{position}']['button'].configure(bg='light green')
                self.board[f'{position}']['color'] = 'light green'

            for position in left_diagonal:
                # if the piece is black, highlight red
                if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                    self.board[position]['button'].configure(bg='red')
                    self.board[position]['color'] = 'red'

            for position in right_diagonal:
                # if the piece is black, highlight to red
                if self.board[position]['piece']['piece_color'] == self.player_piece_color:
                    self.board[position]['button'].configure(bg='red')
                    self.board[position]['color'] = 'red'

    def place_piece(self, piece, color, position):
        """Placement of pieces"""

        # if the color parameter equals black
        if color == 'black':
            # get the black piece image in place with the piece name parameter
            # 'self.black_pieces[piece]' returns file path for that piece img
            temp = ImageTk.PhotoImage(Image.open(self.black_pieces[piece]))
            # configure the tkinter button object at that position and set the 'image' to 'temp'
            self.board[position]['button'].configure(image=temp)
            self.board[position]['button'].image = temp

            # assign the piece to that position in the chess self.board dictionary
            self.board[position]['piece']['piece_name'] = piece

            # assign the piece color to that position in the chess 'self.board' dictionary
            self.board[position]['piece']['piece_color'] = 'black'

        # if the piece color is white
        if color == 'white':
            # get the image
            temp = ImageTk.PhotoImage(Image.open(self.white_pieces[piece]))
            # configure the tkinter button object at that position and set the 'image' to 'temp'
            self.board[position]['button'].configure(image=temp)
            self.board[position]['button'].image = temp

            # assign the piece to that position in the chess self.board dictionary
            self.board[position]['piece']['piece_name'] = piece

            # assign the piece color to that position in the chess 'self.board' dictionary
            self.board[position]['piece']['piece_color'] = 'white'

        # Allows us to delete pieces by placing a 'blank' image on the button
        # will be essential for moving pieces in board
        elif color == 'blank':
            # get the blank image, in this case 'self.white_pieces[piece]' retrieves from the white pieces directory
            # But both 'self.white_pieces and self.black_pieces' directories blank files are the same
            # so it doesnt really matter which one is retrieved from
            temp = ImageTk.PhotoImage(Image.open(self.white_pieces[piece]))
            self.board[position]['button'].configure(image=temp)
            self.board[position]['button'].image = temp

            # set the board piece name to None
            self.board[position]['piece']['piece_name'] = None

            # set the board piece color to None
            self.board[position]['piece']['piece_color'] = None

    def get_all_possible_moves(self, piece, piece_color, position):
        """Generates a list of all possible moves for a piece basedon its color and board position"""

        # With this list we can get the new positions for this move by modifying only one part
        temp = list(position)

        full_column = [f'{temp[0]}{i}' for i in range(1, 9)]
        full_row = [f'{letter}{temp[1]}' for letter in self.letters]

        index_in_col = full_column.index(position)
        index_in_row = full_row.index(position)

        if piece == 'rook':
            # up
            rook_up = [f'{i}' for i in full_column[index_in_col + 1:]]

            #  Down
            rook_down = [f'{i}' for i in full_column[:index_in_col]]
            rook_down.reverse()

            # right
            rook_right = [f'{i}' for i in full_row[index_in_row + 1:]]

            # left
            rook_left = [f'{i}' for i in full_row[:index_in_row]]
            rook_left.reverse()

            # all possible moves combined
            all_possible_rook_moves = [rook_up] + [rook_down] + [rook_left] + [rook_right]

            return all_possible_rook_moves

        if piece == 'bishop':

            # up right diagonal
            bishop_up_right = self.get_diagonal(position, 'up_right')

            # down right diagonal
            bishop_down_right = self.get_diagonal(position, 'down_right')

            # up left diagonal
            bishop_up_left = self.get_diagonal(position, 'up_left')

            # down left diagonal
            bishop_down_left = self.get_diagonal(position, 'down_left')

            # all
            all_possible_bishop_moves = [bishop_up_right] + [bishop_down_right] + \
                                        [bishop_up_left] + [bishop_down_left]

            return all_possible_bishop_moves

        if piece == 'knight':
            # Generate moves, by moving positions in board (clockwise)
            move_one = self.move_column(self.move_row(self.move_row(position, 'increase'), 'increase'), 'increase')
            move_two = self.move_row(self.move_column(self.move_column(position, 'increase'), 'increase'), 'increase')

            move_three = self.move_row(self.move_column(self.move_column(position, 'increase'), 'increase'),
                                        'decrease')
            move_four = self.move_column(self.move_row(self.move_row(position, 'decrease'), 'decrease'), 'increase')

            move_five = self.move_column(self.move_row(self.move_row(position, 'decrease'), 'decrease'), 'decrease')
            move_six = self.move_row(self.move_column(self.move_column(position, 'decrease'), 'decrease'), 'decrease')

            move_seven = self.move_row(self.move_column(self.move_column(position, 'decrease'), 'decrease'),
                                        'increase')
            move_eight = self.move_column(self.move_row(self.move_row(position, 'increase'), 'increase'), 'decrease')

            # all moves
            all_possible_knight_moves = [move_one] + [move_two] + [move_three] + [move_four] + [move_five] + [move_six] + [move_seven] + [move_eight]
            all_possible_knight_moves = [[move] for move in all_possible_knight_moves if move is not None]

            return all_possible_knight_moves

        if piece == 'queen':
            # basically a copy of the rook and the bishops moves

            # up
            queen_up = [f'{i}' for i in full_column[index_in_col + 1:]]

            #  Down
            queen_down = [f'{i}' for i in full_column[:index_in_col]]
            queen_down.reverse()

            # right
            queen_right = [f'{i}' for i in full_row[index_in_row + 1:]]

            # left
            queen_left = [f'{i}' for i in full_row[:index_in_row]]
            queen_left.reverse()

            # up right diagonal
            queen_up_right = self.get_diagonal(position, 'up_right')

            # down right diagonal
            queen_down_right = self.get_diagonal(position, 'down_right')

            # up left diagonal
            queen_up_left = self.get_diagonal(position, 'up_left')

            # down left diagonal
            queen_down_left = self.get_diagonal(position, 'down_left')
            # all
            all_possible_queen_moves = [queen_down_right] + [queen_right] + [queen_up_right] + [queen_up] + \
                                       [queen_up_left] + [queen_left] + [queen_down_left] + [queen_down]

            return all_possible_queen_moves

        if piece == 'king':
            # clockwise pattern for king
            move_one = self.move_row(position, 'increase')
            move_two = self.move_column(self.move_row(position, 'increase'), 'increase')
            move_three = self.move_column(position, 'increase')
            move_four = self.move_row(self.move_column(position, 'increase'), 'decrease')
            move_five = self.move_row(position, 'decrease')
            move_six = self.move_row(self.move_column(position, 'decrease'), 'decrease')
            move_seven = self.move_column(position, 'decrease')
            move_eight = self.move_row(self.move_column(position, 'decrease'), 'increase')

            # all
            all_possible_king_moves = [move_one] + [move_two] + [move_three] + [move_four] + [move_five] + \
                                      [move_six] + [move_seven] + [move_eight]
            all_possible_king_moves = [[move] for move in all_possible_king_moves if move is not None]

            return all_possible_king_moves

        if piece == 'prawn' and piece_color == self.player_piece_color:
            up_one = self.move_row(position, 'increase')
            up_two = self.move_row(self.move_row(position, 'increase'), 'increase')

            if int(position[1]) >= 3:
                prawn_up = list(filter(self.remove_nones, [up_one]))
            else:
                prawn_up = list(filter(self.remove_nones, [up_one, up_two]))

            # diagonal
            right_diagonal = list(filter(self.remove_nones,
                                         [self.move_column(self.move_row(position, 'increase'), 'increase')]))
            left_diagonal = list(filter(self.remove_nones,
                                         [self.move_column(self.move_row(position, 'increase'), 'decrease')]))

            all_possible_prawn_moves = [prawn_up] + [right_diagonal] + [left_diagonal]

            #
            # check it is not the last row
            #if int(position[1]) == 8:
               # return 'end'

            # all
            return all_possible_prawn_moves

        if piece == 'prawn' and piece_color == self.opponent_piece_color:
            # up
            down_one = self.move_row(position, 'decrease')
            down_two = self.move_row(self.move_row(position, 'decrease'), 'decrease')

            if int(position[1]) <= 6:
                prawn_up = list(filter(self.remove_nones, [down_one]))
            else:
                prawn_up = list(filter(self.remove_nones, [down_one, down_two]))

            # diagonal
            right_diagonal = list(filter(self.remove_nones,
                                         [self.move_column(self.move_row(position, 'decrease'), 'increase')]))
            left_diagonal = list(filter(self.remove_nones,
                                        [self.move_column(self.move_row(position, 'decrease'), 'decrease')]))

            all_possible_prawn_moves = [prawn_up] + [right_diagonal] + [left_diagonal]
            #
            # check it is not the last row
            ##if int(position[1]) == 1:
              #  return ['end']

            # all
            return all_possible_prawn_moves

    def get_piece_img(self):
        """Easy way to access file paths for pieces"""

        # Get the name for all the black pieces and white pieces paths in lists
        # Format of each piece name is 'piece.png'
        black = [piece for (root, dirs, piece) in os.walk(self.pieces_file_path + '//black')]
        white = [piece for (root, dirs, piece) in os.walk(self.pieces_file_path + '//white')]

        # Create a dictionary were the key is the name of the piece and the value is the file path
        # Each loop in the list comprehension returns the file path e.g. 'piece.png'
        # To shorten this we slice this name and remove 4 characters from the end: '.png' in the key
        # The value is simply the full path
        black_pieces = {f'{str(piece[:len(piece) - 4])}':
                        f'{self.pieces_file_path}\\black\\{piece}' for piece in black[0]}
        white_pieces = {f'{str(piece[:len(piece) - 4])}':
                        f'{self.pieces_file_path}\\white\\{piece}' for piece in white[0]}

        # We return both lists, now we can access any image
        # For example, black rook would be 'black_pieces['rook']', this returns its file path

        return black_pieces, white_pieces

    def get_game_fen_string(self):
        """Get fen string of board"""
        return self.ai_board.board_fen()

    @staticmethod
    def remove_nones(val):
        """Remove None from array"""
        if val is None:
            return False

        else:
            return val

    def move_row(self, position, operation):
        """Returns position above to or below parameter"""

        # ensure chess position is entered
        if position in self.pieces:
            if operation == 'increase':
                # '8' shouldn't be in the position, because it is the highest row there is, so it can't be increased
                if '8' in position:
                    return

                # Get index of item in 'pieces' list
                my_index = self.pieces.index(position)

                # return item next to that index
                return self.pieces[my_index + 8]

            if operation == 'decrease':
                # '2' shouldn't be in the position, because it is the lowest row there is, so it can't be decreased
                if '1' in position:
                    return
                # Get index of item in 'pieces' list
                my_index = self.pieces.index(position)

                # return item next to that index
                return self.pieces[my_index - 8]
        else:
            return

    def move_column(self, position, operation):
        """Returns position next to or behind parameter"""

        # ensure chess position is entered
        if position in self.pieces:

            if operation == 'increase':
                # 'h' shouldn't be in the position, because it is the last element in a row, so it can't be increased
                if 'h' in position:
                    return

                # Get index of item in 'pieces' list
                my_index = self.pieces.index(position)

                # return item next to that index
                return self.pieces[my_index + 1]

            if operation == 'decrease':
                # 'a' shouldn't be in the position, because it is the first element in a row, so it can't be decreased
                if 'a' in position:
                    return

                # Get index of item in 'pieces' list
                my_index = self.pieces.index(position)

                # return item next to that index
                return self.pieces[my_index - 1]
        else:
            return

    def get_diagonal(self, position, direction):
        """Returns diagonal for a specific position"""

        # lists
        letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        list_position = list(position)
        columns_to_right = letters[list_position[0]] + 8
        columns_to_left = letters[list_position[0]]

        diagonal_values = []

        if direction == 'up_right':

            next_diagonal = position
            for i in range(columns_to_right):
                # get diagonal for next value
                next_diagonal = self.move_row(self.move_column(next_diagonal, 'increase'), 'increase')
                # append to diagonal list
                diagonal_values.append(next_diagonal)

            # return final filtered list
            return list(filter(self.remove_nones, diagonal_values))

        if direction == 'down_right':

            next_diagonal = position
            for i in range(columns_to_right):
                # get diagonal for next value
                next_diagonal = self.move_row(self.move_column(next_diagonal, 'increase'), 'decrease')
                # append to diagonal list
                diagonal_values.append(next_diagonal)

            # return final filtered list
            return list(filter(self.remove_nones, diagonal_values))

        if direction == 'up_left':
            next_diagonal = position
            for i in range(columns_to_left):
                # get diagonal for next value
                next_diagonal = self.move_row(self.move_column(next_diagonal, 'decrease'), 'increase')
                # append to diagonal list
                diagonal_values.append(next_diagonal)

            # return final filtered list
            return list(filter(self.remove_nones, diagonal_values))

        if direction == 'down_left':
            next_diagonal = position
            for i in range(columns_to_left):
                # get diagonal for next value
                next_diagonal = self.move_row(self.move_column(next_diagonal, 'decrease'), 'decrease')
                # append to diagonal list
                diagonal_values.append(next_diagonal)

            # return final filtered list
            return list(filter(self.remove_nones, diagonal_values))

    def build(self, type='default'):
        if type == 'default':
            self.make_board()
            self.place_buttons()
            self.place_default_pieces_on_screen()

        if type == 'empty':
            self.make_board()
            self.place_buttons()
            for piece in self.pieces:
                self.place_piece('blank', 'blank', piece)


