create table wiadomosci
(
    id                 integer   default nextval('wiadomosc_id_seq'::regclass) not null
        constraint wiadomosc_pkey
            primary key,
    nadawca_wiadomosci integer                                                 not null
        constraint wiadomosc_nadawca_wiadomosc_fkey
            references uzytkownicy,
    kanal_odbiorcy     integer
        constraint wiadomosc_odbiorca_wiadomosci_fkey
            references kanaly,
    data_wyslania      timestamp default CURRENT_TIMESTAMP,
    zawartosc          bytea
);

create table uzytkownicy
(
    id                serial
        primary key,
    nazwa_uzytkownika bpchar not null,
    haslo             text   not null,
    email             bpchar not null,
    data_utworzenia   timestamp default CURRENT_TIMESTAMP
);

create table kanaly
(
    id                  serial
        primary key,
    liczba_uzytkownikow integer,
    uzytkownicy_kanalu  bpchar,
    nazwa_kanalu        varchar(255) not null,
    id_wlasciciela      bigint       not null
        references uzytkownicy
);