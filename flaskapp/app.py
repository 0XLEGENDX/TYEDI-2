from flask import Flask, render_template, send_file, request
import os 
import modules.optimalpath as op
import modules.optimalsite as osite
import modules.stereo_depth_estimate as sde


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


@app.route('/optimalsite', methods=['POST'])
def optimalsite():

    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    height = int(request.form["height"])
    width = int(request.form["width"])
    filename = "imageUploadedsite.jpeg"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    osite.process_image(r"D:\Projects\EDI TY SEM 2\TYEDI-2\flaskapp\static\uploads\imageUploadedsite.jpeg",height,width)
    path = r"D:\Projects\EDI TY SEM 2\TYEDI-2\flaskapp\processed_image.png"
    return send_file(path)



@app.route('/optimalsite')
def optimalsitepage():
    return render_template("optimalsite.html")

@app.route('/treeheight')
def treeheight():

    return render_template("treeheight.html")


@app.route('/treeheight', methods=['POST'])
def treeheightmap():

    if 'image1' not in request.files:
        return 'No file part'
    file = request.files['image1']
    if 'image2' not in request.files:
        return 'No file part'
    file2 = request.files['image2']

    distance = int(request.form["distance"])

    filename1 = "imageUploadedLeft.jpg"
    filename2 = "imageUploadedRight.jpg"

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
    file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

    # osite.process_image(r"D:\Projects\EDI TY SEM 2\TYEDI-2\flaskapp\static\uploads\imageUploadedsite.jpeg",height,width)
    path = r"out"
    height = sde.heightEstimate(distance)
    return render_template("treeheight2.html",imageurl=path ,status= "The height of tree is ( In Feet ): " +  str(height))


@app.route('/out')
def out():
    return send_file(r"D:\Projects\EDI TY SEM 2\TYEDI-2\flaskapp\out.jpg")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/model')
def download_file():
    file_path = r'static\model\model.onnx'
    return send_file(file_path, as_attachment=True)

@app.route('/historydata')
def historydata():

    return render_template("historicaldata.html")



if __name__ == '__main__':
    app.run(debug=True)
