import traceback

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)  # создаем объект на основе Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///three.db'  # подключение к бд
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Art(db.Model):  # класс для работы с бд
    id = db.Column(db.Integer, primary_key=True)  # создание поля где будут содержаться наши данные
    intro = db.Column(db.String(300), nullable=False)  
    title = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    style = db.Column(db.Text, nullable=False)
    technic = db.Column(db.Text, nullable=False)
    country = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)  # время устанавливается по умолчанию, те в момент времени

    def __repr__(self):
        return '<Art %r>' % self.id  # выдается сам обьект Art + его id
    # для того чтобы что то получить из бд

class Technic(db.Model):
    id_tec = db.Column(db.Integer, primary_key=True)  # создание поля где будут содержаться наши данные
    technic_name = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Technic %r>' % self.id  # выдается сам обьект Art + его id
    # для того чтобы что то получить из бд


@app.route('/')  # обрабатываем главную страницу
@app.route('/home')  # обрабатываем home страницу
def index():
    return render_template("index.html")


@app.route('/second')  # обрабатываем second страницу
def second():
    return render_template("second.html")


@app.route('/posts')  # обрабатываем second страницу
def posts():
    art = Art.query.order_by(Art.date.desc()).all()  # .first в art будет установлена первая запись
    # order_by(name) все будет отсортировано по имени
    return render_template("posts.html", art=art)


@app.route('/posts/<int:id>')
def post_detail(id):
    arts = Art.query.get(id)
    technics = Technic.query.get(id)
    return render_template("post_detail.html", arts=arts, technics=technics)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    arts = Art.query.get_or_404(id)
    db.session.delete(arts)
    db.session.commit()
    return redirect('/posts')


# добавление данных в бд
@app.route('/create_art', methods=['POST', 'GET'])  # обрабатываем second страницу
def create_art():
    if request.method == "POST":
        intro = request.form['intro']
        title = request.form['title']
        birthday = request.form['birthday']
        text = request.form['text']
        style = request.form['style']
        technic = request.form['technic']
        country = request.form['country']

        art = Art(intro=intro, title=title, birthday=birthday, text=text, style=style, technic=technic, country=country)
        db.session.add(art)
        db.session.commit()
        technic_db = Technic(technic_name=technic)
        db.session.add(technic_db)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template("create_art.html")



@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    arts = Art.query.get(id)
    technics = Technic.query.get(id)
    if request.method == "POST":  # проверяем есть ли значения в бд
        arts.intro = request.form['intro']
        arts.title = request.form['title']  # проверяем и получаем эти значения
        arts.birthday = request.form['birthday']
        arts.text = request.form['text']
        arts.style = request.form['style']
        arts.technic = request.form['technic']
        arts.country = request.form['country']
        technics.technic_name = request.form['technic']
        try:
            db.session.commit()  # обновление бд
            return redirect('/posts')
        except:
            return "При изменении данных произошла ошибка"
    else:
        return render_template("post_update.html", arts=arts)


if __name__ == "__main__":  # основной файл
    app.run(debug=True)  # запускает наш основной проект
    # все ошибки будут показываться на основной странице, пока у нас стоит TRue

