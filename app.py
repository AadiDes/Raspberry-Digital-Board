from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import uuid
from database import init_db, DB_PATH
from db_manager import get_display_state, update_display_state  # NEW IMPORT
from config import SECRET_KEY

# Load environment variables
load_dotenv()

# Initialize database
init_db()

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_image_expired(expiry):
    return expiry and datetime.now() > expiry

def get_current_image():
    state = get_display_state()
    if state['image_path']:
        if is_image_expired(state['image_expiry']):
            update_display_state({'image_path': None, 'image_expiry': None})
            return None
        return state['image_path']
    return None

def cleanup_uploads_folder():
    current_image = get_display_state()['image_path']
    upload_dir = os.path.join(app.static_folder, 'uploads')
    for filename in os.listdir(upload_dir):
        filepath = os.path.join(upload_dir, filename)
        if f'uploads/{filename}' != current_image:
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"⚠️ Failed to remove old image {filename}: {e}")

@app.route('/')
def display():
    state = get_display_state()
    return render_template('display.html', **{
        'current_time': datetime.now(),
        'production': state['production'],
        'heats': state['heats'],
        'monthly_production': state['monthly_production'],
        'safety_slogan': state['safety_slogan'],
        'manpower_strength': state['manpower_strength'],
        'employee_month': state['employee_month'],
        'image_path': get_current_image(),
        'last_updated': state['last_updated']
    })

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('admin_password', '').strip() != ADMIN_PASSWORD:
            flash('❌ Incorrect password. Please try again.', 'error')
            return redirect(url_for('admin'))

        try:
            updates = {
                'production': int(request.form.get('production', 0)),
                'heats': int(request.form.get('heats', 0)),
                'monthly_production': int(request.form.get('monthly_production', 0)),
                'safety_slogan': request.form.get('safety_slogan', '').strip()[:50],
                'manpower_strength': int(request.form.get('manpower_strength', 0)),
                'employee_month': request.form.get('employee_month', '').strip()[:24],
                'last_updated': datetime.now()
            }

            # Handle image upload
            file = request.files.get('image_file')
            if file and file.filename:
                if allowed_file(file.filename):
                    filename = str(uuid.uuid4()) + '_' + secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    updates['image_path'] = f'uploads/{filename}'

                    duration = request.form.get('image_duration', type=int)
                    updates['image_expiry'] = datetime.now() + timedelta(seconds=duration) if duration else None
                    flash('🖼️ Image uploaded successfully!', 'success')
                else:
                    flash('⚠️ Invalid file type.', 'error')

            # Remove image
            if request.form.get('remove_image'):
                updates['image_path'] = None
                updates['image_expiry'] = None
                flash('🧹 Image removed successfully!', 'success')

            update_display_state(updates)
            cleanup_uploads_folder()
            flash('✅ Factory metrics updated successfully!', 'success')

        except ValueError:
            flash('⚠️ Please enter valid numbers for numeric fields.', 'error')
        except Exception as e:
            flash(f'❗ Error updating data: {e}', 'error')

        return redirect(url_for('admin'))

    state = get_display_state()
    return render_template('admin.html', **{
        'production': state['production'],
        'heats': state['heats'],
        'monthly_production': state['monthly_production'],
        'safety_slogan': state['safety_slogan'],
        'manpower_strength': state['manpower_strength'],
        'employee_month': state['employee_month'],
        'image_path': get_current_image(),
        'image_expiry': state['image_expiry'],
        'last_updated': state['last_updated']
    })

@app.route('/api/data')
def api_data():
    from datetime import datetime

    state = get_display_state()

    # Ensure last_updated is a string (in case it's a datetime object)
    if isinstance(state['last_updated'], datetime):
        last_updated_str = state['last_updated'].strftime('%Y-%m-%d %H:%M:%S')
    else:
        last_updated_str = str(state['last_updated'])

    return {
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'production': state['production'],
        'heats': state['heats'],
        'monthly_production': state['monthly_production'],
        'safety_slogan': state['safety_slogan'],
        'manpower_strength': state['manpower_strength'],
        'employee_month': state['employee_month'],
        'image_path': get_current_image(),
        'last_updated': last_updated_str
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)