
import os
from flask import Flask, render_template, request, redirect, session
#Подключение библиотеки баз данных
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#Задаем секретный ключ для работы session
app.secret_key = 'my_top_secret_123'
#Подключение SQLite
# Адрес базы: на хостинге берётся из переменной DATABASE_URL,
# локально (без неё) используется файл diary.db как раньше
db_url = os.environ.get('DATABASE_URL', 'sqlite:///diary.db')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Создание db
db = SQLAlchemy(app)


class Card(db.Model):

    #id
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_email = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'<Card {self.id}>'


class User(db.Model):
    # Создание полей
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # email пользователя
    user_email = db.Column(db.String(100), nullable=False)
    # пароль пользователя
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f"<User {self.id}>"


# Создание таблиц, если база новая (на хостинге безопасно и повторно)
with app.app_context():
    db.create_all()




#Запуск страницы с контентом
@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']
            
        users_db = User.query.all()
        for user in users_db:
            if form_login == user.user_email and form_password == user.password:
                session['user_email'] = user.user_email
                return redirect('/index')
        error = 'Неправильно указан пользователь или пароль'
        return render_template('login.html', error=error)
    else:
        return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User(user_email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


#Запуск страницы с контентом
@app.route('/index')
def index():
    return render_template('index.html')

#Запуск страницы c картой
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

#Запуск страницы c созданием карты
@app.route('/create')
def create():
    return render_template('create_card.html')

#Форма карты
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']
        card = Card(title=title, subtitle=subtitle, text=text, user_email=session['user_email'])

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)
