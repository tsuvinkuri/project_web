from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    role = SelectField('Ваша роль', choices=[
        ('Керри', 'Керри'), ('Мидер', 'Мидер'), ('Хардлайнер', 'Хардлайнер'), ('Четверка', 'Четверка'), ('Пятерка', 'Пятерка'), ('Не играю', 'Не играю')],
                         default='Не играю', validators=[DataRequired()])
    pts = SelectField('Ваш текущий ММР', choices=[
        ('0-1000', '0-1000'), ('1000-2000', '1000-2000'), ('2000-3000', '2000-3000'), ('3000-4000', '3000-4000'), ('4000-5000', '4000-5000'), ('5000-6000', '5000-6000'), ('>6000', '>6000'), ('Нет рейтинга', 'Нет рейтинга')],
                       default='Нет рейтинга', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')