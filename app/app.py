from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return self.name


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String, nullable=False)

    def __init__(self, action):
        self.action = action

    def __str__(self):
        return self.action


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.Float)


with app.app_context():
    db.create_all()
    if not Account.query.first():
        default_account = Account(id=0,account=0)
        db.session.add(default_account)
        db.session.commit()


def balance_request(number=1, saldo=0):
    account = Account.query.first()
    if number == 1:
        account.account += saldo
        akcja = f'Dodano {saldo} $ do konta'
    elif number == 2:
        account.account -= saldo
        akcja = f'Odjęto {saldo} $ z konta'
    add_history = History(action=akcja)
    db.session.add_all([add_history, account])
    db.session.commit()


def show_account_balance():
    account = Account.query.first()
    return f'{account.account} $'


def show_history():
    history = History.query.all()
    return history


@app.route("/", methods=['POST', 'GET'])
def home():
    title = 'Strona główna'

    buy_name = request.form.get("nazwa_kupno")
    buy_price = request.form.get("cena_kupno")
    buy_count = request.form.get("liczba_kupno")

    sale_name = request.form.get("nazwa_sprzedaz")
    sale_price = request.form.get("cena_sprzedaz")
    sale_count = request.form.get("liczba_sprzedaz")

    context = {
        'title': title,
        'show_balance': show_account_balance(),
        'balance_request': balance_request,
    }

    operacja = request.form.get('operacja')
    kwota = request.form.get('kwota')

    if buy_name and buy_price and buy_count:
        buy_price = float(buy_price)
        buy_count = int(buy_count)
        laczna_cena = buy_price * buy_count
        account = Account.query.first()
        if laczna_cena > account.account:
            return render_template('index.html', context=context, message1='Za mało środków na koncie')
        else:
            account.account -= laczna_cena
            buy = Product(name=buy_name, price=buy_price, count=buy_count)
            action = f'Kupiono {buy} w ilości {buy_count} za łączną cenę {laczna_cena}'
            history = History(action=action)
            db.session.add_all([buy, history])
            db.session.commit()
            return redirect(url_for("store"))

    if sale_name and sale_price and sale_count:
        sale_price = float(sale_price)
        sale_count = int(sale_count)
        product = db.session.query(Product).filter_by(name=sale_name).first()
        if not product:
            return render_template('index.html', context=context, message2='Brak takiego produktu')
        if product.count < sale_count:
            return render_template('index.html', context=context, message3='Za mało produktów')
        laczna_cena = sale_price * sale_count
        account = Account.query.first()
        account.account += laczna_cena
        product.count -= sale_count
        action = f"Sprzedano {sale_name} w ilości {sale_count} za łączną cenę {laczna_cena}"
        history = History(action=action)
        db.session.add_all([product, history, account])
        db.session.commit()
        if product.count <= 0:
            db.session.delete(product)
            db.session.commit()
        return redirect(url_for("store"))

    if operacja and kwota:
        kwota = float(kwota)
        if kwota > 0:
            balance_request(int(operacja), kwota)
            return redirect(url_for("home"))

    return render_template('index.html', context=context)


@app.route("/magazyn", methods=['POST', 'GET'])
def store():
    title = 'Magazyn'
    products = db.session.query(Product).all()
    context = {
        'title': title,
        'products': products,
    }
    return render_template('store.html', context=context)


@app.route("/delete-product", methods=['POST', 'GET'])
def delete_product():
    product_id = request.form.get('product_id')
    if product_id:
        product = db.get_or_404(Product, int(product_id))
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('store'))


@app.route("/historia")
def history():
    title = 'Historia'

    context = {
        'title': title,
        'show_history': show_history(),
    }
    return render_template('historia.html', context=context)


@app.route("/historia/range", methods=['POST', 'GET'])
def history_range_post():
    start = int(request.form.get('start'))
    koniec = int(request.form.get('end'))
    context = {
        'message': 'Proszę wprowadzić dodatnią liczbę'
    }

    if start < 0 or koniec < 0:
        return render_template('historia.html', context=context)

    return redirect(url_for('history_range', start=start, koniec=koniec))


@app.route("/historia/<int:start>/<int:koniec>")
def history_range(start, koniec):
    title = 'Wybrany zakres historii'
    max_range = db.session.query(History).count()
    history = db.session.query(History).order_by(History.id).slice(start - 1, koniec).all()

    history_texts = [str(h) for h in history]

    context = {
        'title': title,
        'history': history_texts,
        'show_history': show_history()
    }

    if start < 1 or koniec > max_range or start > koniec:
        context['history'] = ''
        message = f"Proszę wybrać zakres od 1 do {max_range}."
        return render_template('historia.html', context=context, message=message)

    return render_template('historia.html', context=context)


