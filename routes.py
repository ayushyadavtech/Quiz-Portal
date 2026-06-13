from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from models import User, Question, Result

# Load user for flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role     = request.form['role']

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!')
            return redirect(url_for('register'))

        # Create new user
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check user in database
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('quiz'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Admin dashboard route
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('quiz'))
    questions = Question.query.all()
    results   = Result.query.all()
    return render_template('admin_dashboard.html', questions=questions, results=results)

# Add question route
@app.route('/add_question', methods=['GET', 'POST'])
@login_required
def add_question():
    if current_user.role != 'admin':
        return redirect(url_for('quiz'))
    if request.method == 'POST':
        question = Question(
            text   = request.form['text'],
            opt_a  = request.form['opt_a'],
            opt_b  = request.form['opt_b'],
            opt_c  = request.form['opt_c'],
            opt_d  = request.form['opt_d'],
            answer = request.form['answer']
        )
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully!')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_question.html')

# Delete question route
@app.route('/delete_question/<int:id>')
@login_required
def delete_question(id):
    if current_user.role != 'admin':
        return redirect(url_for('quiz'))
    question = Question.query.get(id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted!')
    return redirect(url_for('admin_dashboard'))

# Quiz route
@app.route('/quiz')
@login_required
def quiz():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    questions = Question.query.all()
    return render_template('quiz.html', questions=questions)

# Submit quiz route
@app.route('/submit', methods=['POST'])
@login_required
def submit():
    questions = Question.query.all()
    score = 0
    for question in questions:
        selected = request.form.get(str(question.id))
        if selected == question.answer:
            score += 1

    # Save result
    result = Result(user_id=current_user.id, score=score, total=len(questions))
    db.session.add(result)
    db.session.commit()
    return redirect(url_for('result', score=score, total=len(questions)))

# Result route
@app.route('/result')
@login_required
def result():
    score = request.args.get('score')
    total = request.args.get('total')
    return render_template('result.html', score=score, total=total)