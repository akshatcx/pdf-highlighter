from flask import Flask, render_template, request, make_response
import fitz
from functools import wraps, update_wrapper
from datetime import datetime


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
        
    return update_wrapper(no_cache, view)

@app.route("/", methods=['POST', 'GET'])
@nocache
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