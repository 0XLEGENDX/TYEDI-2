from flask import Flask, render_template, send_file, request
import os 
import modules.optimalpath as op



app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



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

@app.route('/optimalpath', methods=['POST'])
def optimalpath():


    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    x1 = request.form["X1"]
    x2 = request.form["X2"]
    y1 = request.form["Y1"]
    y2 = request.form["Y2"]
    
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = "imageUploaded.jpeg"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        op.computeValue(x1,x2,y1,y2)
        path = r"D:\Projects\EDI TY SEM 2\TYEDI-2\flaskapp\output.png"
        return send_file(path)
        # op.computeValue()
        # return send_file(r"D:\Projects\EDI TY SEM 2\TYEDI-2\flaskapp\static\uploads\output.png" ,  mimetype='image/png')

    # file = request.files["image"]
    # # startPoint = request.files["image"]
    # return optimalpath.findOptimalPath( file , (0,0) , (200,200))


@app.route('/optimalpath')
def optimalPathPage():
    return render_template("optimalpath.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/model')
def download_file():
    file_path = r'static\model\model.onnx'
    return send_file(file_path, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
