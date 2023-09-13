from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from main import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/", methods=['POST', 'GET'])
def home():
    title = 'Strona główna'

    buy = Product(
        name='name',
        price=0,
        count=0,
        )
    sale = Product(
        name='name',
        price=0,
        count=0,
        )

    operacja = request.form.get('operacja')
    kwota = request.form.get('kwota')

    if buy:
        buy = Product(
            name=request.form.get("nazwa_kupno"),
            price=request.form.get("cena_kupno"),
            count=request.form.get("liczba_kupno"),
        )
        db.session.add(buy)
        db.session.commit()
        manager.save_to_file()

    if sale:
        sale = Product(
            name=request.form.get("nazwa_sprzedaz"),
            price=request.form.get("cena_sprzedaz"),
            count=request.form.get("liczba_sprzedaz"),
        )
        db.session.add(sale)
        db.session.commit()
        manager.save_to_file()

    if operacja and kwota:
        kwota = float(kwota)
        if kwota > 0:
            balance_request(int(operacja), kwota)
            manager.save_to_file()

    context = {
        'title': title,
        'show_balance': show_account_balance(),
        'list': show_list_of_products(),
        'purchase': to_purchase,
        'sale': to_sale,
        'balance_request': balance_request,
        }
    return render_template('index.html', context=context)


@app.route("/historia")
def history():
    title = 'Historia'
    context = {
        'title': title,
        'history': show_action_history(),
    }
    return render_template('historia.html', context=context)


@app.route("/historia/<int:start>/<int:koniec>")
def history_range(start, koniec):
    title = 'Wybrany zakres historii'
    max_range = len(manager.historia_akcji)
    selected_history = manager.historia_akcji[start-1:koniec]
    context = {
        'title': title,
        'history': '<br> * '.join([''] + selected_history),
    }
    if start < 1 or koniec > max_range or start > koniec:
        context['history'] = ''
        message = f"Proszę wybrać zakres od 1 do {max_range}."
        return render_template('historia.html', context=context, message=message)
    return render_template('historia.html', context=context)



