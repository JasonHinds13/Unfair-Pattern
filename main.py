#If on Windows to avoid fullscreen, use the following two lines of code
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

from os import path
from random import choice, randrange

Builder.load_string('''
<BlinkButtons>:

    redBtn: rbt
    bluBtn: bbt
    yelBtn: ybt
    grnBtn: gbt
    scrBtn: scr
    status: stat
    hscrBtn: hsb

    GridLayout:
        cols: 2
        size: 350, 350
        center: root.center
        Button:
            id: rbt
            on_press: root.red()
            background_color: (1, 0, 0, 1)
        Button:
            id: bbt
            on_press: root.blu()
            background_color: (0, 0, 1, 1)
        Button:
            id: ybt
            on_press: root.yel()
            background_color: (1.5, 1, 0, 1)
        Button:
            id: gbt
            on_press: root.grn()
            background_color: (0, 1, 0, 1)

    Label:
        id: stat
        text: "Press Score Button To Begin..."
        center: root.center[0], root.top-25

    Button:
        id: scr
        pos: 0, 0
        size: 100, 50
        text: 'Score: '+str(root.score)
        background_color: (0, 1, 1, 1)
        on_press: root.BlinkPattern()

    Button:
        id: hsb
        size: 100, 50
        text: 'HS: '+str(root.hscore)
        pos: root.width-100, 0
        background_color: (0, 1, 1, 1)
''')

class BlinkButtons(Widget):

    #Variables
    score = 0
    count = 0

    #high score file (hsf) - This deals with retrieving hs from file
    if path.exists('score.dat'):
        hsf = open('score.dat', 'r')
        hscore = hsf.read()
        hscore = int(hscore)
        hsf.close()
    else:
        hscore = 0
        hsf = open('score.dat', 'w')
        hsf.write(str(hscore))
        hsf.close()

    myPattern = [] #Players Pattern
    gamePattern = [] #Game Pattern to Follow

    #Button Objects
    status = ObjectProperty(None)
    scrBtn = ObjectProperty(None)
    redBtn = ObjectProperty(None)
    bluBtn = ObjectProperty(None)
    yelBtn = ObjectProperty(None)
    grnBtn = ObjectProperty(None)
    hscrBtn = ObjectProperty(None)

    #Blink Colors
    lred   = (2.0, 0.0, 0.0, 1.0)
    lblue  = (0.0, 0.0, 2.0, 1.0)
    lyell  = (2.5, 2.0, 0.0, 1.0)
    lgreen = (0.0, 2.0, 0.0, 1.0)

    #Functions for Button Presses
    def red(self):
        self.myPattern.append('red')
    def blu(self):
        self.myPattern.append('blu')
    def yel(self):
        self.myPattern.append('yel')
    def grn(self):
        self.myPattern.append('grn')

    #Functions for blinking buttons
    def blinkred(self, rt):
        self.redBtn.background_color = self.lred
        def changebk(dt):
            self.redBtn.background_color = (1, 0, 0, 1)
        Clock.schedule_once(changebk, 1)
        
    def blinkblu(self, rt):
        self.bluBtn.background_color = self.lblue
        def changebk(dt):
            self.bluBtn.background_color = (0, 0, 1, 1)
        Clock.schedule_once(changebk, 1)
        
    def blinkyel(self, rt):
        self.yelBtn.background_color = self.lyell
        def changebk(dt):
            self.yelBtn.background_color = (1.5, 1, 0, 1)
        Clock.schedule_once(changebk, 1)
        
    def blinkgrn(self, rt):
        self.grnBtn.background_color = self.lgreen
        def changebk(dt):
            self.grnBtn.background_color = (0, 1, 0, 1)
        Clock.schedule_once(changebk, 1)

    #Function For Making, Updating and Displaying Game Pattern
    def BlinkPattern(self):
        self.count = 0
        self.status.text=''
        self.myPattern = []
        self.gamePattern.append(choice(['red','grn','blu','yel']))

        def check(rt):
            if self.count < len(self.gamePattern):
                if self.gamePattern[self.count] == 'red':
                    Clock.schedule_once(self.blinkred, 2+self.count)
                    
                elif self.gamePattern[self.count] == 'blu':
                    Clock.schedule_once(self.blinkblu, 2+self.count)
                    
                elif self.gamePattern[self.count] == 'yel':
                    Clock.schedule_once(self.blinkyel, 2+self.count)
                    
                elif self.gamePattern[self.count] == 'grn':
                    Clock.schedule_once(self.blinkgrn, 2+self.count)

                self.count += 1
                  
        if self.count < len(self.gamePattern):
            Clock.schedule_interval(check, 1.5)

    def update(self, tr):
        if self.gamePattern == self.myPattern and self.gamePattern != []:
            self.score +=1
            self.scrBtn.text='Score: '+str(self.score)

            if self.score > self.hscore:
                self.hscore = self.score
                hsf = open('score.dat', 'w')
                hsf.write(str(self.hscore))
                hsf.close()
                self.hscrBtn.text = 'HS: '+str(self.hscore)

            self.BlinkPattern()

        if len(self.gamePattern) == len(self.myPattern) and self.gamePattern != self.myPattern:
            self.score = 0
            self.gamePattern = []
            self.scrBtn.text='Score: '+str(self.score)
            self.status.text='Game Over. Press Score Button To Try Again...'
      
class PatternManiaApp(App):

    def build(self):
        game = BlinkButtons()
        Clock.schedule_interval(game.update,1/60)
        return game

    def on_pause(self):
        return True

    def on_resume(self):
        pass

if __name__ == "__main__":
    PatternManiaApp().run()
