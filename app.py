from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import uuid

# Load environment variables from .env if present
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Set securely in production!

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'changeme')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory factory data
factory_data = {
    'production': 0,
    'heats': 0,
    'monthly_production': 0,
    'safety_slogan': 'Safety First!',
    'manpower_strength': 0,
    'employee_month': 'John Doe',
    'image_path': None,
    'image_expiry': None,
    'last_updated': datetime.now()
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_image_expired():
    expiry = factory_data.get('image_expiry')
    return expiry and datetime.now() > expiry

def get_current_image():
    if factory_data['image_path']:
        if is_image_expired():
            factory_data['image_path'] = None
            factory_data['image_expiry'] = None
            return None
        return factory_data['image_path']
    return None

def cleanup_uploads_folder():
    """Remove all unused images in the uploads folder except the current active image"""
    active_image = factory_data.get('image_path')
    upload_dir = os.path.join(app.static_folder, 'uploads')

    for filename in os.listdir(upload_dir):
        filepath = os.path.join(upload_dir, filename)

        # If it's not the active image, delete it
        if f'uploads/{filename}' != active_image:
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"⚠️ Failed to remove old image {filename}: {e}")


@app.route('/')
def display():
    return render_template('display.html', **{
        'current_time': datetime.now(),
        'production': factory_data['production'],
        'heats': factory_data['heats'],
        'monthly_production': factory_data['monthly_production'],
        'safety_slogan': factory_data['safety_slogan'],
        'manpower_strength': factory_data['manpower_strength'],
        'employee_month': factory_data['employee_month'],
        'image_path': get_current_image(),
        'last_updated': factory_data['last_updated']
    })

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('admin_password', '').strip()
        if password != ADMIN_PASSWORD:
            flash('❌ Incorrect password. Please try again.', 'error')
            return redirect(url_for('admin'))

        try:
            factory_data['production'] = int(request.form.get('production', 0))
            factory_data['heats'] = int(request.form.get('heats', 0))
            factory_data['monthly_production'] = int(request.form.get('monthly_production', 0))
            factory_data['safety_slogan'] = request.form.get('safety_slogan', '').strip()[:50]
            factory_data['manpower_strength'] = int(request.form.get('manpower_strength', 0))
            factory_data['employee_month'] = request.form.get('employee_month', '').strip()[:24]

            if 'image_file' in request.files:
                file = request.files['image_file']
                if file and file.filename and allowed_file(file.filename):
                    filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    factory_data['image_path'] = f'uploads/{filename}'

                    duration = request.form.get('image_duration', type=int)
                    factory_data['image_expiry'] = (
                        datetime.now() + timedelta(seconds=duration)
                        if duration and duration > 0 else None
                    )
                    flash('🖼️ Image uploaded successfully!', 'success')
                elif file and file.filename:
                    flash('⚠️ Invalid file type.', 'error')

            if request.form.get('remove_image'):
                factory_data['image_path'] = None
                factory_data['image_expiry'] = None
                flash('🧹 Image removed successfully!', 'success')

            factory_data['last_updated'] = datetime.now()
            flash('✅ Factory metrics updated successfully!', 'success')

            # Cleanup old uploaded images
            cleanup_uploads_folder()



        except ValueError:
            flash('⚠️ Please enter valid numbers for numeric fields.', 'error')
        except Exception as e:
            flash(f'❗ Error updating data: {e}', 'error')

        return redirect(url_for('admin'))

    return render_template('admin.html', **{
        'production': factory_data['production'],
        'heats': factory_data['heats'],
        'monthly_production': factory_data['monthly_production'],
        'safety_slogan': factory_data['safety_slogan'],
        'manpower_strength': factory_data['manpower_strength'],
        'employee_month': factory_data['employee_month'],
        'image_path': get_current_image(),
        'image_expiry': factory_data['image_expiry'],
        'last_updated': factory_data['last_updated']
    })

@app.route('/api/data')
def api_data():
    return {
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'production': factory_data['production'],
        'heats': factory_data['heats'],
        'monthly_production': factory_data['monthly_production'],
        'safety_slogan': factory_data['safety_slogan'],
        'manpower_strength': factory_data['manpower_strength'],
        'employee_month': factory_data['employee_month'],
        'image_path': get_current_image(),
        'last_updated': factory_data['last_updated'].strftime('%Y-%m-%d %H:%M:%S')
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
