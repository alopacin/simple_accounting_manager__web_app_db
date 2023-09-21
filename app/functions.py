from models import *
from flask import render_template, redirect, url_for
from models import Account, Product, History


# funkcja dodajaca i odejmujaca z konta
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


# funckja wyswietlajaca stan konta
def show_account_balance():
    account = Account.query.first()
    return f'{account.account} $'


# funkcja wyswietlajaca historie
def show_history():
    history = History.query.all()
    return history


# funkcja odpowiadajaca za zakup produktow
def to_buy(buy_name, buy_price, buy_count, context):
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


# funkcja odpowiadajaca za sprzedaz produktow
def to_sale(sale_name, sale_price, sale_count, context):
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