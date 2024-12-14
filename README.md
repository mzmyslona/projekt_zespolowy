# Projekt_zespolowy
Aplikacja szyfrująca + Digital Ocean

Link do Trello: https://trello.com/invite/b/670bb2aa0bb9b1145a031be7/ATTI12ecdc54c585bf4b1a7262ffca1e20bb527B6D77/01i-pz

# Wymagania
    python3
    virtualenv

# Schemat bazy danych

```
create table wiadomosci (
  id integer default nextval('wiadomosc_id_seq' :: regclass) not null constraint wiadomosc_pkey primary key, 
  nadawca_wiadomosci integer not null constraint wiadomosc_nadawca_wiadomosc_fkey references uzytkownicy, 
  kanal_odbiorcy integer constraint wiadomosc_odbiorca_wiadomosci_fkey references kanaly, 
  data_wyslania timestamp default CURRENT_TIMESTAMP, 
  zawartosc bytea
);
create table uzytkownicy (
  id serial primary key, nazwa_uzytkownika bpchar not null, 
  haslo text not null, email bpchar not null, 
  data_utworzenia timestamp default CURRENT_TIMESTAMP
);
create table kanaly (
  id serial primary key, 
  liczba_uzytkownikow integer, 
  uzytkownicy_kanalu bpchar, 
  nazwa_kanalu varchar(255) not null, 
  id_wlasciciela bigint not null references uzytkownicy
);
```

# Aktywacja środowiska
W przypadku inicjalizowania środowiska od zera użyj argumentu `--force`.
Możesz go użyc również w przypadku kiedy chcesz zresetować wcześniej postawione środowisko.

Inicjalizacja/reset:
```console
foo@bar:~$ source bootstrap.sh setup server --force
```
Aktywacja:
```console
foo@bar:~$ source bootstrap.sh setup server
```
Te same linie poleceń dostępne są również dla klienta. W tym celu wystarczy podmienić `server` na `client`.

W przypadku inicjalizacji/resetowania środowiska jest ono domyślnie aktywowane.

# Serwer HTTPS
Serwer domyślnie nasłuchuje localhost na porcie 5000 więc żaden ruch z zewnątrz nie jest możliwy. W celu konfiguracji serwera pod HTTPS wymagane jest użycie reverse proxy. W naszym wypadku jest to nginx skonfigurowany na maszynie serwerowej. Poniżej znajduje się przykładowy plik konfiguracyjny:

```
server {
    listen 443 ssl;
    server_name your_domain.com;  # Replace with your domain or server IP

    ssl_certificate /path/to/cert.pem;       # Correct SSL certificate path
    ssl_certificate_key /path/to/key.pem;    # Correct SSL key path

    location / {
        proxy_pass http://127.0.0.1:5000;   # Flask app address
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name your_domain.com;  # Replace with your domain or server IP

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}
```

# Przywracanie projektu do stanu fabrycznego
Możliwe jest przywrócenie projektu do stanu fabrycznego(bez dodatkowo wygenrowanych plików):
```console
foo@bar:~$ ./bootstrap.sh clean
```
