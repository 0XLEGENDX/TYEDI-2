from flask import Flask, render_template

app = Flask(__name__)

@app.route('/status')
def status():
    return 'Server is online!'

@app.route('/treecount')
def treecount():
    return render_template("treecount.html")

@app.route('/home')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
