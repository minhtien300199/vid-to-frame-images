from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from video_processor import VideoProcessor

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'video' not in request.files:
            flash('No video file uploaded')
            return redirect(request.url)
        
        file = request.files['video']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Get and validate frame count
        try:
            frame_count = int(request.form.get('frame_count', 0))
            if frame_count <= 0:
                raise ValueError
        except ValueError:
            flash('Frame count must be a positive integer')
            return redirect(request.url)

        # Get and validate interval
        try:
            interval = int(request.form.get('interval', 0))
            if interval <= 0:
                raise ValueError
        except ValueError:
            flash('Interval must be a positive integer')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Process the video
            try:
                processor = VideoProcessor()
                output_folder = processor.extract_frames(
                    filepath, 
                    frame_count, 
                    interval
                )
                flash('Frames extracted successfully!')
                return render_template('result.html', output_folder=output_folder)
            except Exception as e:
                flash(f'Error processing video: {str(e)}')
                return redirect(request.url)
            finally:
                # Clean up uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)
        else:
            flash('Invalid file type. Allowed types: ' + ', '.join(ALLOWED_EXTENSIONS))
            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 