from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
import os
from datetime import datetime
from urllib.parse import urlencode
from process_image import detect_deforestation  # Custom OpenCV function

app = Flask(__name__)

# Folder to save uploaded images
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ✅ MongoDB Atlas Connection
app.config["MONGO_URI"] = "mongodb+srv://saeemohite0305:XjISz4XjZUcvhFkp@saeeradb.fv0hf4z.mongodb.net/saeeradb?retryWrites=true&w=majority&appName=SaeeraDB"
mongo = PyMongo(app)

# Create uploads folder if not exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ------------------ Routes ------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/connect')
def gallery():
    return render_template('gallery.html')

@app.route('/detect', methods=['GET', 'POST'])
def detect():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "⚠️ No file selected!"
        file = request.files['image']
        if file.filename == '':
            return "⚠️ No file selected!"
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            year = datetime.now().year
            deforested_area, deforestation_percentage = detect_deforestation(filepath)
            status = "High" if deforestation_percentage > 50 else "Moderate"

            # ✅ Save to MongoDB Atlas
            mongo.db.analysis.insert_one({
                "filename": file.filename,
                "year": year,
                "area": deforested_area,
                "percentage": deforestation_percentage,
                "status": status,
                "uploaded_at": datetime.now()
            })

            analysis = {
                "year": year,
                "area": f"{deforested_area} sq.km",
                "percentage": f"{deforestation_percentage}%",
                "status": status
            }
            query_string = urlencode(analysis)
            return redirect(f"{url_for('success', filename=file.filename)}?{query_string}")
    return render_template('detect.html')

@app.route('/success/<filename>')
def success(filename):
    year = request.args.get('year', 'Unknown')
    area = request.args.get('area', 'Unknown')
    percentage = request.args.get('percentage', 'Unknown')
    status = request.args.get('status', 'Unknown')
    return render_template('success.html',
                           filename=filename,
                           year=year,
                           area=area,
                           percentage=percentage,
                           status=status)

@app.route('/history')
def history():
    results = mongo.db.analysis.find().sort("uploaded_at", -1)
    return render_template('history.html', results=results)

# ------------------ Run App ------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

