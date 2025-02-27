# Работа приложения (клиентскаая часть)

- Клиент подключается по сокету localhost:12345
- Пользователь вводит свой никнейм
- Клиент запускает поток для прослушивания сервера
- Клиент прослушивает ввод строк от пользователя и отправляет их на сервер
- Клиент читает сообщение и выводит его в консоль, клиент может получить и своё сообщение

# Стек реализации

- Язык: Python
- Библиотека: socket, threading
- Протокол: TCP

# Запуск
- Запустить сервер
- Запустить несколько клиентов в разных терминалах
- Придумать никнейм и начать общение

# Код клиента
```py
import socket
import threading

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'Никнейм?':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Произошла ошибка!")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

nickname = input("Введите свой никнейм: ")

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
```