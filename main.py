from flask import Flask, render_template, request, redirect, url_for, flash, session
from config import Config
from database import db
from models import User, Project, Category, ContactMessage
from auth import auth_required
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Sample data for projects
SAMPLE_PROJECTS = [
    {
        'id': 'P01',
        'category': 'Image Processing',
        'title': 'Adaptive Image Denoising Using Wavelet Transform in MATLAB',
        'description': 'Advanced image processing using wavelet transforms',
        'tags': ['Machine Learning', 'Computer Vision', 'Image Segmentation'],
        'domain': 'electronics',
        'price': 2999,
        'image': 'project1.jpg'
    },
    {
        'id': 'P02',
        'category': 'Deep Learning',
        'title': 'Real-Time Face Mask Detection Using Deep Learning in MATLAB',
        'description': 'CNN-based face mask detection system',
        'tags': ['Machine Learning', 'Deep Learning', 'CNN'],
        'domain': 'electronics',
        'price': 3499,
        'image': 'project2.jpg'
    },
    {
        'id': 'P03',
        'category': 'Medical Imaging',
        'title': 'Image Segmentation for Medical Diagnosis Using Level Set Method',
        'description': 'Medical image analysis and segmentation',
        'tags': ['Machine Learning', 'Computer Vision', 'Image Segmentation'],
        'domain': 'machinelearning',
        'price': 4999,
        'image': 'project3.jpg'
    },
    {
        'id': 'P04',
        'category': 'Image Processing',
        'title': 'Satellite Image Classification Using Deep Learning (ResNet or VGG16)',
        'description': 'Satellite imagery classification using CNNs',
        'tags': ['Machine Learning', 'Deep Learning', 'CNN'],
        'domain': 'machinelearning',
        'price': 5499,
        'image': 'project4.jpg'
    },
    {
        'id': 'P05',
        'category': 'Signal Processing',
        'title': 'EEG Signal Classification for Brain-Computer Interface Using CNN',
        'description': 'Brain-computer interface development',
        'tags': ['Machine Learning', 'Deep Learning', 'CNN'],
        'domain': 'electronics',
        'price': 6999,
        'image': 'project5.jpg'
    },
    {
        'id': 'P06',
        'category': 'Signal Processing',
        'title': 'Speech Emotion Recognition Using MFCC and SVM in MATLAB',
        'description': 'Emotion recognition from speech signals',
        'tags': ['Machine Learning', 'Natural Language Processing', 'Speech Recognition'],
        'domain': 'electronics',
        'price': 3999,
        'image': 'project6.jpg'
    },
    {
        'id': 'P07',
        'category': 'Signal Processing',
        'title': 'Real-Time Noise Reduction in Audio Signals Using Wavelet Transform',
        'description': 'Audio signal processing and noise reduction',
        'tags': ['Machine Learning', 'Natural Language Processing', 'Speech Recognition'],
        'domain': 'machinelearning',
        'price': 2999,
        'image': 'project7.jpg'
    },
    {
        'id': 'P08',
        'category': 'AI & Machine Learning, Finance',
        'title': 'Stock Price Prediction Using LSTM Networks in MATLAB',
        'description': 'Financial forecasting using deep learning',
        'tags': ['Machine Learning', 'Deep Learning', 'RNN'],
        'domain': 'datascience',
        'price': 7999,
        'image': 'project8.jpg'
    }
]

CATEGORIES = [
    {'id': 'electronics', 'name': 'Electronics and Communication', 'icon': '📡'},
    {'id': 'computer', 'name': 'Computer Science', 'icon': '💻'},
    {'id': 'machinelearning', 'name': 'Machine Learning', 'icon': '🤖'},
    {'id': 'datascience', 'name': 'Data Science', 'icon': '📊'}
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/my_projects')
def my_projects():
    domain = request.args.get('domain', 'all')
    
    if domain == 'all':
        filtered_projects = SAMPLE_PROJECTS
    else:
        filtered_projects = [p for p in SAMPLE_PROJECTS if p['domain'] == domain]
    
    return render_template('my_projects.html', 
                         projects=filtered_projects, 
                         categories=CATEGORIES,
                         active_domain=domain)

@app.route('/view_project/<project_id>')
def view_project(project_id):
    project = next((p for p in SAMPLE_PROJECTS if p['id'] == project_id), None)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('my_projects'))
    return render_template('view_project.html', project=project)

@app.route('/category/<category_id>')
def category(category_id):
    filtered_projects = [p for p in SAMPLE_PROJECTS if p['domain'] == category_id]
    category_info = next((c for c in CATEGORIES if c['id'] == category_id), None)
    
    return render_template('category.html', 
                         projects=filtered_projects, 
                         category=category_info,
                         categories=CATEGORIES)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Validation
        if not all([name, email, subject, message]):
            flash('All fields are required!', 'error')
            return render_template('contact.html')
        
        # Save to database
        try:
            contact_message = ContactMessage(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            db.session.add(contact_message)
            db.session.commit()
            flash('Thank you for contacting us! We will get back to you soon.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again later.', 'error')
            print(f"Error saving contact message: {e}")
        
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:  # In production, use hashed passwords
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash(f'Welcome back, {user.username}!', 'success')
            
            # ✅ REDIRECT ADMIN TO DASHBOARD, REGULAR USER TO HOME
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken!', 'error')
            return render_template('register.html')
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password=password  # In production, hash this password
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('home'))

@app.route('/purchase/<project_id>', methods=['GET', 'POST'])
def purchase(project_id):
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login to purchase projects', 'warning')
        return redirect(url_for('login'))
    
    project = next((p for p in SAMPLE_PROJECTS if p['id'] == project_id), None)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('my_projects'))
    
    if request.method == 'POST':
        # Process purchase
        payment_method = request.form.get('payment_method')
        
        # Here you would integrate with payment gateway
        # For now, we'll simulate a successful purchase
        
        flash(f'🎉 Purchase successful! You now own: {project["title"]}', 'success')
        return redirect(url_for('my_purchases'))
    
    return render_template('purchase.html', project=project)

@app.route('/my_purchases')
def my_purchases():
    if 'user_id' not in session:
        flash('Please login to view your purchases', 'warning')
        return redirect(url_for('login'))
    
    # In a real app, fetch from database
    # For now, return empty or sample data
    return render_template('my_purchases.html', purchases=[])

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login to sell projects', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        description = request.form.get('description')
        price = request.form.get('price')
        tags = request.form.get('tags')
        
        # Validation
        if not all([title, category, description, price, tags]):
            flash('All fields are required!', 'error')
            return render_template('sell.html', categories=CATEGORIES)
        
        try:
            # Create new project
            new_project = Project(
                title=title,
                description=description,
                price=float(price),
                domain=category,
                tags=tags,
                user_id=session['user_id']
            )
            db.session.add(new_project)
            db.session.commit()
            flash('Project submitted successfully!', 'success')
            return redirect(url_for('my_projects'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            print(f"Error saving project: {e}")
    
    return render_template('sell.html', categories=CATEGORIES)

@app.route('/admin_dashboard')
def admin_dashboard():
    # Check if user is admin
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    # Get statistics
    total_messages = ContactMessage.query.count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    total_db_projects = Project.query.count()  # ✅ Count real projects from database
    
    return render_template('admin_dashboard.html', 
                         total_projects=len(SAMPLE_PROJECTS) + total_db_projects,  # Sample + Database projects
                         total_users=User.query.count(),
                         total_categories=len(CATEGORIES),
                         total_messages=total_messages,
                         unread_messages=unread_messages)

@app.route('/admin/messages')
def admin_messages():
    # Check if user is admin
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin_messages.html', messages=messages)

@app.route('/admin/message/<int:message_id>/mark_read', methods=['POST'])
def mark_message_read(message_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    
    message = ContactMessage.query.get_or_404(message_id)
    message.is_read = True
    db.session.commit()
    flash('Message marked as read', 'success')
    return redirect(url_for('admin_messages'))

@app.route('/admin/message/<int:message_id>/delete', methods=['POST'])
def delete_message(message_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    
    message = ContactMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully', 'success')
    return redirect(url_for('admin_messages'))

# ============================================
# ADMIN PROJECTS MANAGEMENT ROUTES
# ============================================

@app.route('/admin/projects')
def admin_projects():
    # Check if user is admin
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    # Get all projects from database
    db_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin_projects.html', projects=db_projects)

@app.route('/admin/project/<int:project_id>/view')
def admin_view_project(project_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    project = Project.query.get_or_404(project_id)
    return render_template('admin_view_project.html', project=project)

@app.route('/admin/project/<int:project_id>/edit', methods=['GET', 'POST'])
def admin_edit_project(project_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.price = float(request.form.get('price'))
        project.domain = request.form.get('domain')
        project.tags = request.form.get('tags')
        
        try:
            db.session.commit()
            flash('Project updated successfully!', 'success')
            return redirect(url_for('admin_projects'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating project', 'error')
            print(f"Error: {e}")
    
    return render_template('admin_edit_project.html', project=project, categories=CATEGORIES)

@app.route('/admin/project/<int:project_id>/delete', methods=['POST'])
def admin_delete_project(project_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied.', 'error')
        return redirect(url_for('home'))
    
    project = Project.query.get_or_404(project_id)
    
    try:
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting project', 'error')
        print(f"Error: {e}")
    
    return redirect(url_for('admin_projects'))

@app.route('/admin/users')
def admin_users():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('home'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)

# ============================================
# END OF ROUTES
# ============================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create a test admin user if database is empty
        if User.query.count() == 0:
            admin = User(
                username='admin',
                email='admin@quickcom.tech',
                password='admin123',  # Change this in production!
                is_admin=True
            )
            test_user = User(
                username='testuser',
                email='test@quickcom.tech',
                password='test123'
            )
            db.session.add(admin)
            db.session.add(test_user)
            db.session.commit()
            print("\n" + "="*50)
            print("✅ TEST USERS CREATED!")
            print("="*50)
            print("Admin Account:")
            print("  Email: admin@quickcom.tech")
            print("  Password: admin123")
            print("\nRegular User Account:")
            print("  Email: test@quickcom.tech")
            print("  Password: test123")
            print("="*50 + "\n")
    
    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
