from flask import Flask, request, redirect, url_for, flash
from flask import jsonify
import TrainTextClassModel as ts
from ClassifyChatText import ClassifyText as ct
from werkzeug.utils import secure_filename
import zipfile
import os
from util import utility as u
import json

# import json as js

from ServiceHandler import TextParser as tp


CONFIGURATION = {}

with open(".\\config\\config.json") as data_file:
    CONFIGURATION = json.load(data_file)

ALLOWED_EXTENSIONS = set(['zip','json'])

service_o = tp.TextLexicalParser()
util_functions = u.utility_functions()

# service implementation starts here
# App configurations is here
app = Flask(__name__);
app.config['UPLOAD_FOLDER'] = CONFIGURATION["DATA_PATH"]
app.secret_key = "super secret key"


# port = int(os.getenv("VCAP_APP_PORT"))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# basically connecting URL to a function....which will return something
# Service implementation starts here
# Start of examples
@app.route('/')
def index():
    return 'This is home page and you asked for %s' %request.method;

#     you can use route as restful service route('exampleService/<int:post_id>')
#     call as <base url>/exampleService/2   same should be passed to function as handle(post_id)

@app.after_request
def apply_caching(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/exampleService/<int:anyNumber>')
def handleExampleService(anyNumber):
    return '<h2> here is your number %d<h2>' %anyNumber;

@app.route('/exampleService/<me>')
def handleService(me):
    return '<h2> here is you %s<h2>';


@app.route('/learnML', methods = ['GET','POST'])
def learnML():
    if request.method == 'POST':
        return "you are using POST method"
    else:
        return "you are using GET"


@app.route('/getService', methods=['GET'])
def getServiceH():
    s = list();
    s.append({
        'name':'hello',
        'desc':'say hello'
    })
    s.append({
        'name':'yo',
        'desc':'yo yo honey singh'
    })

    # return js.dumps({'data':s}), 200, {'Content-Type':'application/json'}
    # TODO : Exception handling
    return jsonify({'data':s})


@app.route('/postService',methods=['POST'])
def postService():
    s = request.json
    response = jsonify({})
    response.status_code = 200
    print("name is ",s["name"])
    return response
# if this script run directly
# End of examples


# Train your own model
@app.route('/trainTextModel', methods=['POST'])
def trainTextModel():
    online = ""
    tf = ts.TextClassificationModelTrain(False)
    tf.handle_learn_path()
    # online = str(request.args.get('online'))
    # b_online = False
    # s = []
    # if online and online.lower() == 'true':
    #     b_online = True
    #     s = request.json
    #
    # m = ts.TextClassificationModelTrain(b_online)
    # m.train_model(s["terms"])
    # print(s)
    response = jsonify({})
    response.status_code = 200
    # TODO : Exception handling
    return response


#  Classify user text
@app.route('/classifyTexts/<string:text_data>',methods=['GET'])
def classify_texts(text_data):
    print(text_data)
    cty = ct([text_data],False)
    class_c = {}
    prediction = cty.classify_text()
    if prediction == "":
        class_c["input_string"] = text_data
        class_c["ERROR"] = "NOMODEL"
        return jsonify(class_c)
    class_c["class"] = cty.classify_text()[0]
    service_o.reload_service()
    service_flag = service_o.set_service_handler(class_c["class"])
    if service_flag:
        class_c["service"] = service_o.parse_text("None")
    else:
        class_c["service"] = {"service":{}}
    class_c["input_string"] = text_data
    # TODO : Exception handling
    return jsonify(class_c)


# another service to upload file
@app.route('/textDataUpload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print("textDataUpload-->File not there")
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print("I didnt get file")
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("Here we are uploading file",filename)
            # filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            zip_ref = zipfile.ZipFile(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            zip_ref.extractall(os.path.join(app.config['UPLOAD_FOLDER']))
            zip_ref.close()

            response = jsonify({})
            response.status_code = 200
            return response
            # TODO : Exception handling
    return ""

# another service to upload file
@app.route('/ServiceUpload', methods=['POST'])
def service_upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print("textDataUpload-->File not there")
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print("I didnt get file")
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print("Here we are uploading file",filename)
            # filename = file.filename
            if os.path.isfile(CONFIGURATION["service path"]):
                os.unlink(CONFIGURATION["service path"])
            file.save(os.path.join(CONFIGURATION["service path"]))
            response = jsonify({})
            response.status_code = 200
            return response
            # TODO : Exception handling
    return ""


# reset model
@app.route('/resetModel', methods=['POST'])
def reset_model():
    util_functions.reset_models()
    response = jsonify({})
    response.status_code = 200
    return response

if __name__ == "__main__":
    app.run(debug=True);
    # app.run(host="0.0.0.0", port=port, debug=True)