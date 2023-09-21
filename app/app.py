from flask import render_template, request, redirect, url_for
from models import *
from functions import balance_request, show_account_balance, show_history, to_buy, to_sale


with app.app_context():
    db.create_all()
    if not Account.query.first():
        default_account = Account(id=0,account=0)
        db.session.add(default_account)
        db.session.commit()


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
        return to_buy(buy_name, buy_price, buy_count, context)

    if sale_name and sale_price and sale_count:
        return to_sale(sale_name, sale_price, sale_count, context)

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


