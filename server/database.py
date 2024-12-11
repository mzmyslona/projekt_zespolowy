# Jak ci bedzie wygodniej przepisac zwracane wartosci na obiekty to mozesz to zrobic ;)
# a i nie robimy uploadu plikow bo nie zdaze tego napisac, sam tekst

class Database:
    def __init__():
        pass

    # Jak funkcje zwracaja true/false to ma mowic czy operacja sie udala czy nie

    def check_credentials(username, password):
        return (True, "jak False to przyczyna niepowodzenia operacji, w przeciwnym wypadku puste")

    def sign_up_user(username, email, password):
        # Bierzesz timestamp w tej chwili.
        # nie pozwalamy na 2 takie same username'y czy emaile
        # innymi slowy nie ma takich 2 uzytkownikow o takim samym username
        # to samo dla emaila
        return (True, "to samo co wyzej, dalej nie bede juz pisal tego")

    # operacja bedzie autoryzowana wiec ta funkcja bedzie wolana zawsze na istniejacym username
    # jak pisze ze operacja autoryzowana to kompletnie nie zajmuj sie zadna autoryzacja, z twojego punktu
    # widzenia przyjmij ze funkcja ktora implementujesz bedzie rzeczywiscie wolana przez tego usera co trzeba
    # i ze dane ktore przyjmuje beda prawidlowe
    # nie ma potrzeby zwracania true/false
    def list_channels(username):
        # wylistuj wszystkie kanaly do ktorych uzytkownik nalezy
        # nie pozwalamy zeby wlasciciel kanalu mial 2 takie same kanaly o tej samej nazwie
        # pozwala nam to miec unikalna pare identyfikujaca kanal

        return [('wlasciciel1', 'nazwa_kanalu1'), ('wlasciciel2', 'nazwa_kanalu2'), ('wlasciciel3', 'nazwa_kanalu3')] # itd.

    # operacja autoryzowana
    # channel_owner, channel zawsze beda prawidlowe bo bedziemy korzystac z tej funkcji jak wylistujemy kanaly dla usera
    def channel_length(channel_owner, channel):
        # ma ona zwracac liczbe wiadomosci w kanale
        return 1024

    # operacja autoryzowana
    # channel_owner, channel identyfikuje tobie kanal
    # n - liczba ostatnich wiadomosci na kanale
    def get_channel_messages(channel_owner, channel, n):
        # zwracasz n ostatnich wiadomosc, czyli gdy n = 3 to ma zwrocic 3 ostatnie wiadomosci
        return [('data_wyslania1', 'nadawca_wiadomosci1', 'zawartosc1'), ('data_wyslania2', 'nadawca_wiadomosci2', 'data_wyslania2')]

    # operacja autoryzowana
    # channel_owner, channel identyfikuje tobie kanal
    def channel_delta(channel_owner, channel, timestamp):
        # zwroc wszystkie wiadomosci ktore sa starsze niz dany timestamp
        # bedzie nam to sluzylo do zaciagania nowych wiadomosci
        return [('data_wyslania1', 'nadawca_wiadomosci1', 'zawartosc1'), ('data_wyslania2', 'nadawca_wiadomosci2', 'data_wyslania2')]

    # operacja autoryzowana
    def create_channel(channel_owner, channel):
        # tworzy kanal - inaczej po prostu to dodaje wpis w bazie
        return (True, "komentarz")

    # operacja autoryzowana - zawolac to moze tylko wlasciciel
    # dla uprosczenia przyjmujemy ze dropuje sie caly kanal lacznie z jego wiadomosciami
    # i nie jest przekazywany wlasciciel na nikogo innego
    # po prostu przestaje istniec
    def remove_channel(channel_owner, channel):
        return (True, "komentarz")

    # operacja autoryzowana - tylko wlasciciel kanalu bedzie mogl dodac uzytkownikow
    def add_channel_member(channel_owner, channel, username):
        # w tym przypadku user ktorego dodaje moze nie istniec
        return (True, "komentarz")

    # operacja autoryzowana - tylko wlasciciel kanalu bedzie mogl usunac uzytkownikow
    def add_channel_member(channel_owner, channel, username):
        # w tym przypadku user ktorego usuwa moze nie istniec(dodatkowa implementacja bylaby potrzebna do listowania userow)
        # a nie ma zbytnio czasu na to
        return (True, "komentarz")
