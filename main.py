#from website file import function create_app
from website import create_app

app = create_app()

## __name__ = means this file (main.py) is running
## run (app.run) only from main.py
## run main.py directly launch app.run()
if __name__ == '__main__':
    app.run(debug=True) 
  