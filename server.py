import socket
import threading

# Dictionar ce contine numele clientului si listele corespunzatoare de scripturi si comenzi
client_data = {}

def handle_client(client_socket):
    # Inregistrare si autentificare client
    client_name = client_socket.recv(1024).decode()
    #initializare dictionar
    client_data[client_socket] = {'name': client_name, 'scripts': [], 'commands': []}


    while True:
        # Primirea comenzii de la client
        command = client_socket.recv(1024).decode()

        if command == "PUBLISH_SCRIPTS":
            # Primirea listei de script-uri de la client - clientul nu poate modifica lista adaugata, dar o poate reface de la zero
            script_list = client_socket.recv(1024).decode().split(",")

            # Actualizarea listei de script-uri pentru clientul conectat
            client_data[client_socket]['scripts'] = script_list

            # Confirmarea clientului ca lista de script-uri a fost salvata
            client_socket.send("Lista de script-uri a fost salvata cu succes!".encode())

        elif command == "PREVIEW_SCRIPTS":
            # Permite clientului previzualizarea listei de scripturi pe care o poseda
            script_list = client_data[client_socket]['scripts']
            if len(script_list) == 0:
                client_socket.send("EMPTY".encode())
            else:
                client_socket.send(",".join(script_list).encode())

        elif command == "ADD_COMMAND":
            # Primirea comenzii adaugate de client
            command_text = client_socket.recv(1024).decode()

            # Verificare daca comanda exista deja in lista de comenzi
            existing_commands = client_data[client_socket]['commands']
            if command_text in existing_commands:
                client_socket.send("Am modificat comanda cu acelasi nume.".encode())
            else:
                # Adaugarea comenzii la lista clientului inregistrat
                existing_commands.append(command_text)
                client_data[client_socket]['commands'] = existing_commands
                # Confirmarea clientului ca o comanda a fost adaugata 
                client_socket.send("Comanda a fost adaugata cu succes!".encode())

        elif command == "DELETE_COMMAND":
            # Primirea numelui comenzii de la client
            command_name = client_socket.recv(1024).decode()

            # Verificarea daca comanda exista in lista clientului
            if command_name in client_data[client_socket]['commands']:
                # Stergerea comenzii din lista clientului
                client_data[client_socket]['commands'].remove(command_name)
                response = "Comanda a fost stearsa cu succes!"
            else:
                response = "Comanda nu exista in lista clientului."

            # Trimiterea raspunsului catre client
            client_socket.send(response.encode())

        elif command == "PREVIEW_COMMANDS":
            # Trimite clientului lista de comenzi
            command_list = client_data[client_socket]['commands']
            if len(command_list) == 0:
                client_socket.send("EMPTY".encode())
            else:
                client_socket.send(",".join(command_list).encode())

        elif command == "EXECUTE":
            # Verificare daca clientul are scripturi si comenzi salvate
            script_list = client_data[client_socket]['scripts']
            command_list = client_data[client_socket]['commands']

            if len(script_list) == 0 and len(command_list) == 0:
                # In cazul in care clientul nu are nici comenzi si nici scripturi
                client_socket.send("Listele scripturilor si ale comenzilor sunt goale.".encode())
            elif len(script_list) == 0:
                # In cazul in care lista scripturilor este goala
                client_socket.send("Nu exista scripturi de executat.".encode())
            elif len(command_list) == 0:
                # In cazul in care lista comenzilor este goala
                client_socket.send("Nu exista comenzi de executat.".encode())
            else:
                # Primirea fisierului de intrare
                input_file = client_socket.recv(1024).decode()

                # Verificare daca numele fisierului de intrare corespunde cu o comanda din lista clientului
                if input_file in command_list:
                    result = execute_command_sequence(script_list, input_file)
                    client_socket.send(result.encode())
                else:
                    #In cazul in care numele fisierului nu coincide cu numele comenzilor clientului
                    client_socket.send("Nu putem utiliza acest fisier.".encode())

        elif command == "EXIT":
            # Incheierea sesiunii cu clientul si eliminarea acestuia din dictionar
            client_socket.close()
            del client_data[client_socket]
            break

def execute_command_sequence(script_list, input_file):
    # Executarea comenzii compuse din nume comanda si nume fisier, care trebuie sa coincida
    result = None
    for script in script_list:
        # Executa script-ul si primeste rezultatul
        result = execute_script(script, input_file)
        input_file = result  # Iesirea script-ului curent devine intrarea pentru urmatorul script
    return result

def execute_script(script, input_file):
    # In acest exemplu, doar simulam executarea script-ului si returnam numele fisierului, dupa cum ne-a fost explicat de domnul profesor Nemedi
    output = f"Am executat scriptul cu numele : {script} - {input_file}"
    return output

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 1234))
    server_socket.listen(5)
    print("Serverul este pornit si poate asculta pana la 5 clienti.")
    while True:
        client_socket, address = server_socket.accept()
        print(f"Conexiune de la {address[0]}:{address[1]}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

start_server()