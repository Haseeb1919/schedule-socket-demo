import socket
import threading
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind(ADDR)
except socket.error as e:
    print(str(e))

server.listen()

print(f"[STARTING] server is starting...")
print(f"[LISTENING] Server is listening on {SERVER}")

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if not msg_length:
            break

        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)
        
        if msg == "turn on":
            device_state = "on"
            response = "DEVICE IS ON"
            print(f"[{addr}] Device is now ON")
        elif msg == "turn off":
            device_state = "off"
            response = "DEVICE IS OFF"
            print(f"[{addr}] Device is now OFF")
        elif msg == "quit":
            print(f"[{addr}] Client is quitting...")
            break
        else:
            print(f"[{addr}] Unknown command: {msg}")
        
        conn.send(("Device state is now: " + device_state).encode(FORMAT))
    
    print(f"[{addr}] Connection closed.")
    conn.close()

def start():
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

start()
