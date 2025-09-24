from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random
import string
import json
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# 初始化扩展
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录'
mail = Mail(app)

# 用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')  # admin, user
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 验证码模型
class VerificationCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)

# 题目模型
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # single, multiple, text, audio, video
    options = db.Column(db.JSON)  # 存储选项
    correct_answer = db.Column(db.Text, nullable=False)
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.String(20), default='medium')  # easy, medium, hard
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 考试模型
class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    time_limit = db.Column(db.Integer, default=60)  # 分钟
    total_questions = db.Column(db.Integer, default=50)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# 考试记录模型
class ExamRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    score = db.Column(db.Integer, default=0)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, timeout
    
    user = db.relationship('User', backref=db.backref('exam_records', lazy=True))
    exam = db.relationship('Exam', backref=db.backref('exam_records', lazy=True))

# 答题记录模型
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_record_id = db.Column(db.Integer, db.ForeignKey('exam_record.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_answer = db.Column(db.Text)
    is_correct = db.Column(db.Boolean, default=False)
    
    exam_record = db.relationship('ExamRecord', backref=db.backref('answers', lazy=True))
    question = db.relationship('Question', backref=db.backref('answers', lazy=True))

# 错题模型
class WrongQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    exam_record_id = db.Column(db.Integer, db.ForeignKey('exam_record.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('wrong_questions', lazy=True))
    question = db.relationship('Question', backref=db.backref('wrong_questions', lazy=True))

# 收藏题目模型
class FavoriteQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('favorite_questions', lazy=True))
    question = db.relationship('Question', backref=db.backref('favorite_questions', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 工具函数
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

def send_verification_email(email, code):
    msg = Message(
        subject='考试系统验证码',
        recipients=[email],
        body=f'您的验证码是：{code}，有效期5分钟。',
        html=f'''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #333; text-align: center;">考试系统验证码</h2>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center;">
                <p style="font-size: 18px; margin: 10px 0;">您的验证码是：</p>
                <div style="background: #007bff; color: white; font-size: 32px; font-weight: bold; padding: 15px; border-radius: 5px; letter-spacing: 5px; margin: 20px 0;">{code}</div>
                <p style="color: #666; margin: 10px 0;">有效期：5分钟</p>
                <p style="color: #999; font-size: 14px;">请勿泄露给他人。</p>
            </div>
        </div>
        '''
    )
    mail.send(msg)

def verify_code(email, code):
    verification = VerificationCode.query.filter_by(
        email=email, 
        code=code, 
        is_used=False
    ).first()
    
    if not verification:
        return False
    
    if datetime.utcnow() > verification.expires_at:
        return False
    
    verification.is_used = True
    db.session.commit()
    return True

# 路由
@app.route('/')
def index():
    if current_user.is_authenticated:
        exams = Exam.query.all()
        return render_template('index.html', exams=exams)
    else:
        return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('邮箱或密码错误')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        code = request.form['code']
        
        # 验证验证码
        if not verify_code(email, code):
            flash('验证码错误或已过期')
            return render_template('register.html')
        
        # 检查用户是否已存在
        if User.query.filter_by(email=email).first():
            flash('邮箱已注册')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('用户名已存在')
            return render_template('register.html')
        
        # 创建用户
        user = User(
            username=username,
            email=email,
            is_verified=True
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('注册成功！请登录')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/send_code', methods=['POST'])
def send_code():
    email = request.json.get('email')
    
    # 检查邮箱是否已注册
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': '邮箱已注册'})
    
    # 生成验证码
    code = generate_verification_code()
    
    # 保存验证码到数据库
    verification = VerificationCode(
        email=email,
        code=code,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )
    db.session.add(verification)
    db.session.commit()
    
    # 发送邮件
    try:
        send_verification_email(email, code)
        return jsonify({'success': True, 'message': '验证码已发送'})
    except Exception as e:
        return jsonify({'success': False, 'message': '发送失败'})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/exam/<int:exam_id>')
@login_required
def exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    questions = Question.query.limit(exam.total_questions).all()
    return render_template('exam.html', exam=exam, questions=questions)

@app.route('/submit_exam', methods=['POST'])
@login_required
def submit_exam():
    data = request.json
    exam_id = data.get('exam_id')
    answers = data.get('answers', {})
    
    exam = Exam.query.get_or_404(exam_id)
    
    # 创建考试记录
    exam_record = ExamRecord(
        user_id=current_user.id,
        exam_id=exam_id,
        end_time=datetime.utcnow(),
        status='completed'
    )
    db.session.add(exam_record)
    db.session.flush()  # 获取exam_record.id
    
    # 计算分数
    score = 0
    total_questions = 0
    
    for question_id, user_answer in answers.items():
        question = Question.query.get(question_id)
        if question:
            total_questions += 1
            is_correct = False
            
            if question.type == 'single':
                is_correct = user_answer == question.correct_answer
            elif question.type == 'multiple':
                correct_answers = json.loads(question.correct_answer) if isinstance(question.correct_answer, str) else question.correct_answer
                user_answers = user_answer if isinstance(user_answer, list) else [user_answer]
                is_correct = set(user_answers) == set(correct_answers)
            elif question.type == 'text':
                is_correct = user_answer.lower().strip() == question.correct_answer.lower().strip()
            
            if is_correct:
                score += 1
            
            # 记录答案
            answer = Answer(
                exam_record_id=exam_record.id,
                question_id=question_id,
                user_answer=json.dumps(user_answer) if isinstance(user_answer, (list, dict)) else str(user_answer),
                is_correct=is_correct
            )
            db.session.add(answer)
            
            # 记录错题
            if not is_correct:
                wrong_question = WrongQuestion(
                    user_id=current_user.id,
                    question_id=question_id,
                    exam_record_id=exam_record.id
                )
                db.session.add(wrong_question)
    
    # 更新分数
    exam_record.score = int((score / total_questions) * 100) if total_questions > 0 else 0
    db.session.commit()
    
    return jsonify({
        'success': True,
        'score': exam_record.score,
        'total_questions': total_questions,
        'correct_answers': score
    })

@app.route('/profile')
@login_required
def profile():
    exam_records = ExamRecord.query.filter_by(user_id=current_user.id).order_by(ExamRecord.created_at.desc()).all()
    wrong_questions = WrongQuestion.query.filter_by(user_id=current_user.id).all()
    favorite_questions = FavoriteQuestion.query.filter_by(user_id=current_user.id).all()
    
    return render_template('profile.html', 
                         exam_records=exam_records,
                         wrong_questions=wrong_questions,
                         favorite_questions=favorite_questions)

@app.route('/review')
@login_required
def review():
    mode = request.args.get('mode', 'sequential')
    wrong_questions = WrongQuestion.query.filter_by(user_id=current_user.id).all()
    
    if mode == 'random':
        random.shuffle(wrong_questions)
    
    return render_template('review.html', questions=wrong_questions, mode=mode)

# 管理员路由
@app.route('/admin')
@login_required
def admin():
    if current_user.role != 'admin':
        flash('权限不足')
        return redirect(url_for('index'))
    
    questions = Question.query.all()
    exams = Exam.query.all()
    users = User.query.all()
    
    return render_template('admin/index.html', 
                         questions=questions, 
                         exams=exams, 
                         users=users)

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('权限不足')
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/questions')
@login_required
def admin_questions():
    if current_user.role != 'admin':
        flash('权限不足')
        return redirect(url_for('index'))
    
    questions = Question.query.all()
    return render_template('admin/questions.html', questions=questions)

@app.route('/admin/add_question', methods=['GET', 'POST'])
@login_required
def add_question():
    if current_user.role != 'admin':
        flash('权限不足')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        content = request.form['content']
        type = request.form['type']
        correct_answer = request.form['correct_answer']
        explanation = request.form.get('explanation', '')
        difficulty = request.form.get('difficulty', 'medium')
        
        options = None
        if type in ['single', 'multiple']:
            options = request.form.getlist('options')
        
        question = Question(
            content=content,
            type=type,
            options=options,
            correct_answer=correct_answer,
            explanation=explanation,
            difficulty=difficulty
        )
        db.session.add(question)
        db.session.commit()
        
        flash('题目添加成功')
        return redirect(url_for('admin_questions'))
    
    return render_template('admin/add_question.html')

@app.route('/admin/exams')
@login_required
def admin_exams():
    if current_user.role != 'admin':
        flash('权限不足')
        return redirect(url_for('index'))
    
    exams = Exam.query.all()
    return render_template('admin/exams.html', exams=exams)

@app.route('/admin/add_exam', methods=['GET', 'POST'])
@login_required
def add_exam():
    if current_user.role != 'admin':
        flash('权限不足')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description', '')
        time_limit = int(request.form['time_limit'])
        total_questions = int(request.form['total_questions'])
        
        exam = Exam(
            title=title,
            description=description,
            time_limit=time_limit,
            total_questions=total_questions
        )
        db.session.add(exam)
        db.session.commit()
        
        flash('考试添加成功')
        return redirect(url_for('admin_exams'))
    
    return render_template('admin/add_exam.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # 创建默认管理员用户
        admin_user = User.query.filter_by(email='admin@example.com').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@example.com',
                role='admin',
                is_verified=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("默认管理员用户已创建: admin@example.com / admin123")
        else:
            print("管理员用户已存在")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
