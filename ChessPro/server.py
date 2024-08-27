import socket
import threading
import json
global game_state
HOST = ''
PORT = 65432

game_state = {
    "turn_step": 0,
    "blue_pieces": ['hero1', 'hero2', 'hero3', 'pawn', 'pawn'],
    "blue_locations":[(0, 0), (1, 0), (2,0), (3, 0), (4, 0)],
    "red_pieces": ['hero1', 'hero2', 'hero3', 'pawn', 'pawn'],
    "red_locations": [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4)],
    "move_history": []
}

def handle_client(conn, addr, clients):
    print(f"Connected to {addr}")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                print(f"Client {addr} disconnected")
                break

            print(f"Message from {addr}: {data}")
            command = json.loads(data)
            process_command(command, clients)
            
            for client in clients:
                if client != conn:
                    try:
                        client.send(json.dumps(game_state).encode())
                    except BrokenPipeError:
                        print(f"Error sending data to client {client.getpeername()}")
                        clients.remove(client)
    except ConnectionResetError:
        print(f"ConnectionResetError with {addr}")
    finally:
        conn.close()
        clients.remove(conn)
        print(f"Connection with {addr} closed")

def process_command(command, clients):
    print(f"Command received: {command}")

    if command["action"] == "move":
        piece = command["piece"]
        start = command["start"]
        end = command["end"]

        if piece in game_state["blue_pieces"]:
            index = game_state["blue_pieces"].index(piece)
            game_state["blue_locations"][index] = end
            if end in game_state["red_locations"]:
                red_index = game_state["red_locations"].index(end)
                game_state["red_pieces"].pop(red_index)
                game_state["red_locations"].pop(red_index)
        elif piece in game_state["red_pieces"]:
            index = game_state["red_pieces"].index(piece)
            game_state["red_locations"][index] = end
            if end in game_state["blue_locations"]:
                blue_index = game_state["blue_locations"].index(end)
                game_state["blue_pieces"].pop(blue_index)
                game_state["blue_locations"].pop(blue_index)

        game_state["turn_step"] = 1 - game_state["turn_step"]
        game_state["move_history"].append(f"{piece} moved from {start} to {end}")

        print(f"Game state updated: {game_state}")


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server started...")
        clients = []
        while True:
            conn, addr = s.accept()
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr, clients)).start()

if __name__ == "__main__":
    start_server()
