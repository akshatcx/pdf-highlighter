from flask import Flask, render_template, request, make_response, flash, redirect
import fitz
from functools import wraps, update_wrapper
from datetime import datetime
from shutil import copyfile
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/'
app.config['SECRET_KEY'] = 'secret'

@app.route("/", methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        file.save(os.path.join('static', "main.pdf"))
        copyfile('static/main.pdf', 'static/output.pdf')
        print("HI")
        return redirect('/search')
    return render_template("upload.html")

@app.route("/search", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        query = request.form['query']
        doc = fitz.open("static/main.pdf")
        for page in doc: 
            text_instances = page.searchFor(query) 
            for inst in text_instances:
                highlight = page.addHighlightAnnot(inst)
        doc.save("static/output.pdf", garbage=4, deflate=True, clean=True)
    return render_template("search.html")
    
if __name__ == "__main__":
    app.run(debug=True)