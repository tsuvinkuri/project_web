from flask import Flask
from data import db_session
from flask import render_template, redirect
from flask_login import LoginManager, login_user, logout_user
from data.users import User
from forms.user import RegisterForm
from forms.users import LoginForm
from flask import request
from flask_restful import Api
from data import users_resources

app = Flask(__name__)
api = Api(app)
api.add_resource(users_resources.UserResource, '/api/v2/users/<int:user_id>')
api.add_resource(users_resources.UserListResource, '/api/v2/users')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/users.db")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    return render_template('main_html.html')


@app.route('/first_pos')
def first_pos():
    return render_template('first_pos.html')


@app.route('/second_pos')
def second_pos():
    return render_template('second_pos.html')


@app.route('/third_pos')
def third_pos():
    return render_template('third_pos.html')


@app.route('/fourth_pos')
def fourth_pos():
    return render_template('fourth_pos.html')


@app.route('/fifth_pos')
def fifth_pos():
    return render_template('fifth_pos.html')


@app.route('/personal_area', methods=['POST', 'GET'])
def personal_area():
    if request.method == 'POST':
        file = request.files['file_ava']
        file_name = file.filename or ''
        file_true_name = str('static/img/'+str(file_name))
        return render_template('personal_area.html', name_file=file_true_name)
    return render_template('personal_area.html', name_file="static/img/defolt_avatar.jpg")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login_input_test.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login_input_test.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('login_registration_test.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('login_registration_test.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            role=form.role.data,
            pts=form.pts.data
        )
        user.set_password(form.password.data)
        with open('pts_users.txt', 'a') as f:
            f.write(form.pts.data+'\n')
            f.close()
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('login_registration_test.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/users.db")
    app.run(port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()
