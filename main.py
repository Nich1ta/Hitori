from boardgamegui import BoardGameGui, W, H
from hitori0 import Hitori0, load_level   
import g2d
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))



def main():
   
    initial_game = load_level("lvl1")  


    g2d.init_canvas((initial_game.cols() * W, initial_game.rows() * W + H))

    
    gui = BoardGameGui(initial_game, actions={"LeftButton": "play", "RightButton": "flag"})

    
    g2d.main_loop(gui.tick)  

if __name__ == "__main__":
    main()
