# Copyrighted by Aadit Bansal
from tkinter import *
from random_words import RandomWords
import time
class Hangman:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('300x400')
        self.root.title('hangman')
        self.rw = RandomWords()
        self.word = ""
        self.canvas = Canvas(self.root, width=300, height=400, bg = 'orange')
        self.correct_letters_text = self.canvas.create_text(150, 250, text = "_ "*len(self.word), font='TNR 15 bold')
        self.wrong_letters_text = self.canvas.create_text(75, 320, text = "", font='TNR 15 bold')
        self.value = True
        self.mouth = None
        self.button = None
        self.entry = None
        self.correct_letters = list()
        self.wrong_letters = list()
        self.status_text = self.canvas.create_text(150, 275, text=' ')
        self.stopwatch_state = True
        self.stopwatch_counter = 0
        self.alphabet = 'abcdefghijklmnopqrstuvwxys'

    # end __init__

    def _canvasT(self, txt):
        self.canvas.itemconfig(self.correct_letters_text, text = txt)
    def _canvasT2(self, txt2):
        self.canvas.itemconfig(self.wrong_letters_text, text = txt2)
        
    def _hangman(self):
        if len(self.wrong_letters) == 1:
            self.canvas.create_oval(125, 125, 175, 175)
        if len(self.wrong_letters) == 2:
            self.canvas.create_line(140, 140, 143, 143)
            self.canvas.create_line(143, 140, 140, 143)
        if len(self.wrong_letters) == 3:
            self.canvas.create_line(155, 140, 158, 143)
            self.canvas.create_line(158, 140, 155, 143)
        if len(self.wrong_letters) == 4:
            self.mouth = self.canvas.create_arc(140,150,160,170,extent=180,style=ARC,)
        if len(self.wrong_letters) == 5:
            self.canvas.create_line(150, 175, 150, 200)
        if len(self.wrong_letters) == 6:
            self.canvas.create_line(150, 187, 120, 170)
        if len(self.wrong_letters) == 7:
            self.canvas.create_line(150, 187, 175, 170)
        if len(self.wrong_letters) == 8:
            self.canvas.create_line(150, 200, 125, 215)
        if len(self.wrong_letters) == 9:
            self.canvas.create_line(150, 200, 175, 215)
    # end hangman

    def _new_game(self):
        self.stopwatch_counter = 0
        self.correct_letters = list()
        self.wrong_letters = list()
        txt = ""
        txt2 = ""
        if self.entry is None:
            self.entry = Entry(self.root)
        self.entry.pack()
        if self.button is None:
            self.button = Button(self.root)
        self.button.config(text="Submit", command= self._guess_define,width=10)
        self.button.pack()
        self.entry.bind('<Return>', lambda event=None: self.button.invoke())
        self.canvas.config(bg='orange')
        self.value = True
        self.word = self.rw.random_word()
        self.canvas.delete(ALL)
        self.canvas.pack()
        self.canvas.create_line(100, 100, 100, 200)
        self.canvas.create_line(100, 100, 150, 100)
        self.canvas.create_line(150, 100, 150, 125)
        self.canvas.create_line(125, 125, 175, 125)
        self.canvas.create_text(75, 300, text = "wrong letters: ", font='TNR 15 bold')
        self.correct_letters_text = self.canvas.create_text(150, 250, text = "_ "*len(self.word), font='TNR 15 bold')
        self.wrong_letters_text = self.canvas.create_text(75, 320, text = "", font='TNR 15 bold')
        self.status_text = self.canvas.create_text(150, 275, text=' ')

        # stopwatch
        self.stopwatch_state = True
        self.root.update()
        timer_txt = self.canvas.create_text(275, 10, text=self._format())
        def update_timer():
            self.canvas.itemconfig(timer_txt, text = self._format())
            self.stopwatch_counter += 1
            if self.stopwatch_state == True:
                self.root.after(100, update_timer)
        update_timer()
    # end _new_game
    def _format(self):
        minutes = (self.stopwatch_counter//600)
        seconds = (self.stopwatch_counter//10) %60
        second1 = seconds % 10
        second10 = seconds // 10
        winzero = self.stopwatch_counter%10
        return str(minutes) + ':'+str(second10)+str(second1)+'.'+str(winzero)
    #end _format
    def _guess_define(self):
        def change_color_orange():
            self.canvas.config(bg = 'orange')
        if self.value == True:            
            txt = ""
            txt2 = ""
            guess = self.entry.get().lower()
            self.entry.delete(0, len(guess))
            # guess = raw_input('What letter is you guess? ')
            if guess not in self.alphabet:
                self.canvas.itemconfig(self.status_text, text='You guess must be in the alphabet!')
            elif len(guess) != 1:
                self.canvas.itemconfig(self.status_text, text='You are only allowed to put 1 letter!')
            elif guess in self.correct_letters:
                self.canvas.itemconfig(self.status_text, text='You already got this letter correct!') 
            elif guess in self.wrong_letters:
                self.canvas.itemconfig(self.status_text, text='You already got this letter wrong!')
            elif guess in self.word:
                self.correct_letters = self.correct_letters + [guess]
                for letter in self.word:
                    if letter not in self.correct_letters:
                        txt = txt + "_ "
                    else:
                        txt = txt + letter + ' '
                if '_' not in txt:
                    self.canvas.itemconfig(self.status_text, text='YAY YOU GOT IT! You time was ' + self._format())
                    self.canvas.configure(bg='green')
                    self.button.config(text="New Game", command= self._new_game)
                    self.value = False
                    self.stopwatch_state = False
                    if len(self.wrong_letters) >= 3:
                        self.canvas.delete(self.mouth)
                        self.mouth = self.canvas.create_arc(140,150,160,170,start = 180, extent=180,style=ARC,)
                else:
                    self.canvas.itemconfig(self.status_text, text='IT IS IN THE WORD!')
                    self.canvas.configure(bg = 'green')
                    self.canvas.after(250, change_color_orange)
                self._canvasT(txt)
            else:
                self.wrong_letters = self.wrong_letters + [guess]
                for letter in self.wrong_letters:
                    txt2 = txt2 + letter + ' '
                self._canvasT2(txt2)
                self._hangman()
                self.canvas.configure(bg = 'red')
                if len(self.wrong_letters) == 9:
                    self.canvas.itemconfig(self.status_text,  text='You lost :( The word was "'+self.word+'",\n  and your time was ' + self._format() + '.') 
                    self.canvas.configure(bg='red')
                    self.button.config(text="New Game", command=self._new_game)
                    self.canvas.delete(self.correct_letters_text)
                    self.correct_letters_text = self.canvas.create_text(150, 250, text = self.word, font='TNR 15 bold')
                    self.value = False
                    self.stopwatch_state = False
                else:
                    self.canvas.after(250, change_color_orange)
                    self.canvas.itemconfig(self.status_text, text="Sorry, that letter isn't in the word")
    def new_game(self):
        self._new_game()
        self.root.mainloop()
    # end _guess_define
# end Hangman

hangman = Hangman()
hangman.new_game()