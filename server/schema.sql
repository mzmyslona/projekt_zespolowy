create table uzytkownicy
(
    id                serial primary key,
    nazwa_uzytkownika bpchar not null,
    haslo             text   not null,
    email             bpchar not null,
    data_utworzenia   timestamp default CURRENT_TIMESTAMP
);

create table kanaly
(
    id                  serial primary key,
    liczba_uzytkownikow integer,
    uzytkownicy_kanalu  bpchar,
    nazwa_kanalu        varchar(255) not null,
    id_wlasciciela      bigint       not null references uzytkownicy
);

create table wiadomosc
(
    id                  serial primary key,
    nadawca_wiadomosc   integer not null references uzytkownicy,
    odbiorca_wiadomosci integer not null references kanaly,
    data_wyslania       timestamp default CURRENT_TIMESTAMP,
    zawartosc           bytea
);