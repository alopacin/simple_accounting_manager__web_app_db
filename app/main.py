# zainicjowanie klasy manager
class Manager:
    def __init__(self):
        self.data = {}
        self.warunki = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista', 'magazyn', 'przeglad', 'koniec']
        self.historia_akcji = []
        self.akcja = 0
        self.stan_konta = 1000


# utworzenie instacji klasy Manager
manager = Manager()

# funkcja dodajaca i odejmujaca kwote z konta
def balance_request(number=1, saldo=0):
    if number == 1:
        manager.stan_konta += saldo
        akcja = f'Dodano {saldo} $ do konta'
        manager.historia_akcji.append(akcja)
    elif number == 2:
        manager.stan_konta -= saldo
        akcja = f'Odjęto {saldo} $ z konta'
        manager.historia_akcji.append(akcja)






# funkcja ktora sprawdza stan konta
def show_account_balance():
    return f'{manager.stan_konta} $'


# funkcja, ktora odpowiada za przeglad historii zmian
def show_action_history():
    return '<br> * '.join([''] + manager.historia_akcji)





