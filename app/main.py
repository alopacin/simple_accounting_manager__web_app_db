# zainicjowanie klasy manager
class Manager:
    def __init__(self):
        self.data = {}
        self.warunki = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista', 'magazyn', 'przeglad', 'koniec']
        self.stan_magazynu = dict()
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


# funkcja odpowiadajaca za sprzedaz z magazynu
def to_sale(nazwa_sprzedaz='nazwa_sprzedaz', cena_sprzedaz=0, liczba_sprzedaz=0):
    if nazwa_sprzedaz not in manager.stan_magazynu:
        return None
    else:
        laczna_cena = cena_sprzedaz * liczba_sprzedaz
        produkt_do_sprzedazy = manager.stan_magazynu[nazwa_sprzedaz]['ilosc']
        if produkt_do_sprzedazy < liczba_sprzedaz:
            return None
        else:
            produkt_do_sprzedazy -= liczba_sprzedaz
            manager.stan_konta += laczna_cena
            manager.stan_magazynu[nazwa_sprzedaz]['ilosc'] -= liczba_sprzedaz
            akcja = f'Sprzedano {nazwa_sprzedaz} w ilosci {liczba_sprzedaz} za {laczna_cena} $'
            manager.historia_akcji.append(akcja)


# funkcja odpowiadajaca za zakup produktow na magazyn
def to_purchase(nazwa_kupno='nazwa_kupno', cena_kupno=0, ilosc_kupno=0):
    laczna_cena = cena_kupno * ilosc_kupno
    if laczna_cena > manager.stan_konta:
        return None
    elif laczna_cena < manager.stan_konta:
        manager.stan_magazynu[nazwa_kupno] = {'ilosc': ilosc_kupno, 'cena': cena_kupno}
        manager.stan_konta -= laczna_cena
        akcja = f'Zakupiono {nazwa_kupno} w ilosci {ilosc_kupno} za {laczna_cena} $'
        manager.historia_akcji.append(akcja)


# funkcja ktora sprawdza stan konta
def show_account_balance():
    return f'{manager.stan_konta} $'


# funkcja, ktora odpowiada za przeglad historii zmian
def show_action_history():
    return '<br> * '.join([''] + manager.historia_akcji)





