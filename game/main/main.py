from game.main import config as Config
from game.main import window as Window 

# search from the global environnement variable
Config.debug = True


Window.init()
Window.run()
