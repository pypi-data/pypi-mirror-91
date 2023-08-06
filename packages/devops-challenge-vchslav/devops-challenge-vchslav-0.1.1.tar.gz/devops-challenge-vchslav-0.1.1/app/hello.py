#app.py
from flask import Flask
app = Flask(__name__)


#views.py
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/greet')
def greet():
    return 'greetings'

#main.py
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')