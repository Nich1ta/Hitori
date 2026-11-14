#!/usr/bin/env python3
"""
@author  Michele Tomaiuolo - https://tomamic.github.io/
@license This software is free - https://opensource.org/license/mit
"""
try:
    from __main__ import g2d
except:
    import g2d
from boardgame import BoardGame
from hitori0 import load_level 

W, H = 50, 50
BLACK, GRAY, WHITE = (0, 0, 0), (127, 127, 127), (255, 255, 255)

img1 = "Menu.png"

class BoardGameGui:
    def __init__(self, game: BoardGame,
                 actions={"LeftButton": "", "RightButton": "flag"},
                 annots={"#": (0, GRAY), "!": (2, GRAY), "R": (2, (255, 0, 0)), "H":(2,(255, 0, 0))}):
        self._game = game
        self._actions = actions
        self._annots = annots
        self._menu_visible = False 
        self.update_buttons()

    

    
    def tick(self):
        game = self._game
        mouse_x, mouse_y = g2d.mouse_pos()
        x, y = mouse_x // W, mouse_y // H
        released = set(g2d.previous_keys()) - set(g2d.current_keys())

        self.draw_menu_button()

        if not self._menu_visible and g2d.mouse_clicked() and game.cols() * W - 80 <= mouse_x <= game.cols() * W and game.rows() * H <= mouse_y <= game.rows() * H + 40:
            self.show_level_selection()  # Show the level selection prompt
            return

        if game.finished():
            g2d.alert(game.status())
            g2d.close_canvas()
            return

        if "Escape" in released:  
            g2d.close_canvas()
            return

        
        if "RightButton" in released:
            for y in range(game.rows()):
                for x in range(game.cols()):
                    if game._annots[x + y * game.cols()] == 0:  
                        game.fill(x, y)  
            self.update_buttons((x, y))

        
        if "LeftButton" in released and y < game.rows():
            game.play(x, y,action = "flag")  
            self.update_buttons((x, y))

    

    

    def update_buttons(self, last_move=None):
        cols, rows = self._game.cols(), self._game.rows()
        g2d.clear_canvas(BLACK)
        for y in range(rows):
            for x in range(cols):
                text = self._game.read(x, y)
                self.write(text, (x, y))
        status = self._game.status()
        self.write(status, (0, rows), cols)
        
    def write(self, text, pos, cols=1):
        
        x, y = pos        
        g2d.set_color(WHITE)
        g2d.draw_rect((x * W + 1, y * H + 1), (cols * W - 2, H - 2))
        
        last = text[-1:]
        if cols == 1 and last in self._annots:
            stroke, color = self._annots[last]
            if last == "R":  
                g2d.set_color(color)  
                g2d.draw_circle((x * W + W / 2, y * H + W / 2), min(W, H) / 2 - 2)
            elif last == "H":  
                g2d.set_color(color)
                g2d.set_stroke(2)
                g2d.draw_circle((x * W + W / 2, y * H + W / 2), min(W, H) / 2 - 2)
                g2d.set_stroke()  
            else:
                g2d.set_stroke(stroke)  
                g2d.set_color(color)
                g2d.draw_circle((x * W + W / 2, y * H + W / 2), min(W, H) / 2 - 2)
                g2d.set_stroke()
            text = text[:-1]
        
        chars = max(1, len(text))
        fsize = min(0.75 * H, 1.5 * cols * W / chars)
        center = (x * W + cols * W/2, y * H + H/2)
        g2d.set_color(BLACK)
        g2d.draw_text(text, center, fsize)

    def show_level_selection(self):

        game = self._game
        g2d.clear_canvas((0, 0, 0))  
        g2d.set_color((255, 255, 255))  

        selected_level = g2d.prompt("Enter level (1-6):")  
        
        if selected_level.isdigit() and 1 <= int(selected_level) <= 6:
            # Load the selected level
            self._game = load_level(f"lvl{selected_level}")  
            g2d.init_canvas((self._game.cols() * W, self._game.rows() * H + H))
            g2d.draw_text("CLICK",(((self._game.cols() * W) / 2  ,(self._game.rows() * H) / 2 + 20)), size = 20)
        else:
            g2d.alert("Invalid level.")  # Show error 

    def draw_menu_button(self):
        game = self._game
        button_width = 40
        button_height = 40
        button_x = game.cols() * W - button_width  
        button_y = game.rows() * H  

        g2d.set_color(BLACK)  
        g2d.draw_image(img1, (button_x + 5, button_y + 15))


def gui_play(game: BoardGame):
    g2d.init_canvas((game.cols() * W, game.rows() * H + H))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)

