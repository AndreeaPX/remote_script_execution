import socket

def publish_script_list(client_socket, script_list):
    # Trimiterea comenzii de publicare a listei de script-uri catre server
    client_socket.send("PUBLISH_SCRIPTS".encode())

    # Trimiterea listei de script-uri catre server
    client_socket.send(",".join(script_list).encode())

    # Asteptarea confirmarii de la server
    response = client_socket.recv(1024).decode()
    print(response)

def preview_script_list(client_socket):
    # Trimiterea comenzii de previzualizare a listei de script-uri catre server
    client_socket.send("PREVIEW_SCRIPTS".encode())

    # Primirea listei de script-uri de la server
    script_list = client_socket.recv(1024).decode()

    # Afisarea listei de script-uri
    print("Lista de script-uri disponibile:")
    print(script_list)

def add_command(client_socket, command_text):
    # Trimiterea comenzii de add a unei comenzi catre server
    client_socket.send("ADD_COMMAND".encode())

    # Trimiterea textului comenzii catre server
    client_socket.send(command_text.encode())

    # Asteptarea confirmarii de la server
    response = client_socket.recv(1024).decode()
    if response == "Am modificat comanda cu acelasi nume.":
        print(response)
    else:
        print("Comanda a fost adaugata cu succes!")

def preview_commands(client_socket):
    # Trimiterea comenzii de previzualizare a listei de comenzi catre server
    client_socket.send("PREVIEW_COMMANDS".encode())

    # Primirea listei de comenzi de la server
    command_list = client_socket.recv(1024).decode()

    # Afisarea listei de comenzi
    print("Lista de comenzi adaugate:")
    print(command_list)

def execute_command(client_socket, input_file):
    # Trimiterea comenzii de executare a comenzii compuse catre server
    client_socket.send("EXECUTE".encode())

    # Trimiterea fisierului input catre server
    client_socket.send(input_file.encode())

    # Asteptarea rezultatului de la server
    result = client_socket.recv(1024).decode()
    print("Rezultatul comenzii compuse:")
    print(result)


def delete_command(client_socket, command_name):
    # Trimiterea comenzii de delete a unei comenzi catre server
    client_socket.send("DELETE_COMMAND".encode())

    # Trimiterea numelui comenzii catre server
    client_socket.send(command_name.encode())

    # Asteptarea raspunsului de la server
    response = client_socket.recv(1024).decode()
    print(response)

def exit_session(client_socket):
    # Trimiterea comenzii de exit a sesiunii catre server
    client_socket.send("EXIT".encode())
    client_socket.close()


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 1234))
    print("Conexiunea la server a fost realizata.")

    # Inregistrare client
    client_name = input("Introduceti numele de utilizator: ")
    client_socket.send(client_name.encode())

    while True:
        print("Comenzi disponibile:")
        print("1. Publica lista de script-uri")
        print("2. Previzualizeaza lista de script-uri")
        print("3. Adauga o comanda")
        print("4. Previzualizeaza comenzile")
        print("5. Executa comanda compusa")
        print("6. Sterge o comanda")
        print("7. Incheie sesiunea")

        choice = input("Introduceti numarul corespunzator comenzii solicitate: ")

        if choice == "1":
            script_list = input("Introduceti lista de script-uri (separate prin virgula): ").split(",")
            publish_script_list(client_socket, script_list)
        elif choice == "2":
            preview_script_list(client_socket)
        elif choice == "3":
            command_text = input("Introduceti textul comenzii: ")
            add_command(client_socket, command_text)
        elif choice == "4":
            preview_commands(client_socket)
        elif choice == "5":
            input_file = input("Introduceti fisierul de intrare: ")
            execute_command(client_socket, input_file)
        elif choice == "6":
            command_name = input("Introduceti numele comenzii de sters: ")
            delete_command(client_socket, command_name)
        elif choice == "7":
            exit_session(client_socket)
            break

start_client()