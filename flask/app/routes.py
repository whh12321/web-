from flask import render_template,flash,redirect,url_for,request
from app import app
from app import db
from app.forms import RegistrationForm

#导入表单处理方法
from app.forms import LoginForm
from app.models import User
from flask_login import current_user,login_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username':'duke'}
    posts = [
        {
            'author':{'username':'刘'},
            'body':'这是模板模块中的循环例子～1'

        },
        {
            'author': {'username': '忠强'},
            'body': '这是模板模块中的循环例子～2'
        }
    ]
    return render_template('index.html',title='我的',user=user,posts=posts)


#前面的就不列举出来了，接着前面的写就可以了
#.......


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #判断用户不存在或者密码不正确
        if user is None or not user.check_password(form.password.data):
            #如果用户不存在或者密码不正确就会闪现这条信息
            flash('无效的用户名或密码')
            #然后重定向到登录页面
            return redirect(url_for('login'))
        #这是一个非常方便的方法，当用户名和密码都正确时来解决记住用户是否记住登录状态的问题
        login_user(user,remember=form.remember_me.data)
        next_page=request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page=url_for('index')
            
        return redirect(url_for('index'))
    return render_template('login.html',title='登录',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # 判断当前用户是否验证，如果通过的话返回首页
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜你成为我们网站的新用户!')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


@app.route('/user/<username>')
@login_required
def user(username):

    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user,'body':'测试Post #1号'},
        {'author':user,'body':'测试Post #2号'}
    ]

    return render_template('user.html',user=user,posts=posts)



