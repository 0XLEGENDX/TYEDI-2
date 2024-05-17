from flask import Flask, render_template, send_file

app = Flask(__name__)


@app.route('/')
def status():
    return 'Server is online!'

@app.route('/treecount')
def treecount():
    return render_template("treecount.html")

@app.route('/greencover')
def greencover():
    return render_template("greencover.html")

@app.route('/survey')
def survey():
    return render_template("survey.html")

@app.route('/optimalpath')
def optimalpath():
    return render_template("optimalpath.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/model')
def download_file():
    file_path = 'static\model\model.onnx'
    return send_file(file_path, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
