from main import createApp
from config import DevConfig

if __name__ == '__main__':
    app = createApp(DevConfig)
    app.run()