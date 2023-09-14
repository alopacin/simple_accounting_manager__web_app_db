from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from main import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f'{self.name} // {self.price} // {self.count}'


with app.app_context():
    db.create_all()


@app.route("/", methods=['POST', 'GET'])
def home():
    title = 'Strona główna'
    products = db.session.query(Product).all()

    buy_name = request.form.get("nazwa_kupno")
    buy_price = request.form.get("cena_kupno")
    buy_count = request.form.get("liczba_kupno")

    sale_name = request.form.get("nazwa_sprzedaz")
    sale_price = request.form.get("cena_sprzedaz")
    sale_count = request.form.get("liczba_sprzedaz")

    operacja = request.form.get('operacja')
    kwota = request.form.get('kwota')

    if buy_name and buy_price and buy_count:
        buy_price = float(buy_price)
        buy_count = int(buy_count)
        laczna_cena = buy_price * buy_count
        if laczna_cena > manager.stan_konta:
            return None
        elif laczna_cena < manager.stan_konta:
            manager.stan_konta -= laczna_cena
            buy = Product()
            buy.name = buy_name
            buy.price = buy_price
            buy.count = buy_count
            db.session.add(buy)
            db.session.commit()
            return redirect(url_for('/'))

    if sale_name and sale_price and sale_count:
        sale_price = float(sale_price)
        sale_count = int(sale_count)
        product = db.session.query(Product).filter_by(name=sale_name).first()
        if not product:
            return None
        laczna_cena = sale_price * sale_count
        manager.stan_konta += laczna_cena
        Product.count -= sale_count
        sale = Product(sale_name, sale_price, sale_count)
        db.session.add(sale)
        db.session.commit()
        return redirect(url_for('/'))

    if operacja and kwota:
        kwota = float(kwota)
        if kwota > 0:
            balance_request(int(operacja), kwota)

    context = {
        'title': title,
        'show_balance': show_account_balance(),
        'balance_request': balance_request,
        'products': products,
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



