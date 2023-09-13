from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from main import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:store.db///'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)

db.create_all()


@app.route("/", methods=['POST', 'GET'])
def home():
    title = 'Strona główna'

    Product.name = request.form.get("nazwa_kupno")
    Product.price = request.form.get("cena_kupno")
    Product.count = request.form.get("liczba_kupno")

    Product.name = request.form.get("nazwa_sprzedaz")
    Product.price = request.form.get("cena_sprzedaz")
    Product.count = request.form.get("liczba_sprzedaz")

    operacja = request.form.get('operacja')
    kwota = request.form.get('kwota')

    if nazwa_kupno and cena_kupno and liczba_kupno:
        cena_kupno = int(cena_kupno)
        liczba_kupno = int(liczba_kupno)
        if cena_kupno > 0 and liczba_kupno > 0:
            to_purchase(nazwa_kupno, cena_kupno, liczba_kupno)
            manager.save_to_file()

    if nazwa_sprzedaz and cena_sprzedaz and liczba_sprzedaz:
        cena_sprzedaz = int(cena_sprzedaz)
        liczba_sprzedaz = int(liczba_sprzedaz)
        if cena_sprzedaz > 0 and liczba_sprzedaz > 0:
            to_sale(nazwa_sprzedaz, cena_sprzedaz, liczba_sprzedaz)
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



