from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Uzytkownicy(Base):
    __tablename__ = "uzytkownicy"

    id = Column(Integer, primary_key=True)
    nazwa_uzytkownika = Column(Text, nullable=False, unique=True)  # Ensure usernames are unique
    haslo = Column(Text, nullable=False)
    email = Column(String(50), nullable=False, unique=True)  # Ensure emails are unique
    data_utworzenia = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)  # Automatically set creation date

    # Relationships
    kanaly = relationship("Kanaly", back_populates="wlasciciel", cascade="all, delete-orphan") 
    wiadomosci_sent = relationship("Wiadomosci", back_populates="sender_user", foreign_keys="Wiadomosci.nadawca_wiadomosci")

class Kanaly(Base):
    __tablename__ = "kanaly"

    id = Column(Integer, primary_key=True)
    liczba_uzytkownikow = Column(Integer, nullable=False, default=0)  # Default count of users in the channel
    uzytkownicy_kanalu = Column(Text, nullable=False)  # Store user information in a structured format
    nazwa_kanalu = Column(String(255), nullable=False, unique=True)  # Ensure channel names are unique
    id_wlasciciela = Column(Integer, ForeignKey(Uzytkownicy.id), nullable=False)  # Ensure that we refer to the correct table name

    # Relationships
    wlasciciel = relationship("Uzytkownicy", back_populates="kanaly")  # Link to the owner of the channel
    wiadomosci = relationship("Wiadomosci", back_populates="recipient_channel")  # Connect messages sent to the channel

class Wiadomosci(Base):
    __tablename__ = "wiadomosci"

    id = Column(Integer, primary_key=True)
    nadawca_wiadomosci = Column(Integer, ForeignKey('uzytkownicy.id'), nullable=False)  # Correct Foreign Key
    kanal_odbiorcy = Column(Integer, ForeignKey('kanaly.id'), nullable=False)  # Channel ID where the message is sent
    data_wyslania = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)  # Set default sent date
    zawartosc = Column(LargeBinary, nullable=False)  # Store the message content

    # Relationships
    sender_user = relationship("Uzytkownicy", back_populates="wiadomosci_sent", foreign_keys=[nadawca_wiadomosci])  # Sends to the user
    recipient_channel = relationship("Kanaly", back_populates="wiadomosci")  # Link to channel receiving the message