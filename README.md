14 - Motor pentru executia de script-uri la distanta

Clientii se conecteaza la server si publica o lista de script-uri identificate prin nume unic la nivelul server-ului;

- unicitatea este asigurata de dictionar;

Server-ul tine lista clientilor impreuna cu asocierea ce script pe care client se gaseste;

-  functionalirate implementata de dictionar;

Pe durata unei sesiuni cu server-ul un client nu-si poate modifica lista de script-uri disponibile;

- lista nu poate fi modificata, doar rescrisa;

Un client poate publica pe server o comanda compusa identificata printr-un nume
unic la nivelul server-ului, constand intr-o secventa de script-uri apelabile in
conducta cu un fisier de intrare primit ca argument, urmand ca iesirea generata de
primul script din secventa sa fie trimisa ca intrare pentru cel de-al doilea si tot asa
pana la ultimul script a carui iesire va constitui rezultatul executiei comenzii;

- unicitate data de dictionar -  am simulat executarea scriptului 

Clientii pot suprascrie comenzile deja publicate prin publicarea pe server a uneia acelasi nume;

- in cazul in care clientul incearca sa adauge o comanda cu un nume deja salvat in dictionar, serverul returneaza un mesaj de modificare si nu readauga comanda

Clientii pot solicita stergerea unei comenzi de pe server pe baza numelui acesteia;

- functionalite implementata.

Server-ul primeste fisierul pentru executia unei comenzi compuse identificata dupa
numele fisierului de intrare care trebuie sa coincida cu cel al comenzii de executat;

- numele comenzii si al fisierului trebuie sa corespunda. In caz contrar, serverul anunta clientul ca fisierul nu poate fi executat

Fisierul rezultat in urma executiei comenzii este trimis clientului care a initiat executia comenzii.

- in urma executarii, numele fisierului ce corespunde cu numele comenzi este retrimis de server , prin simularea explicata initial.
