### Условие
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает у
сервера выполнение математической операции, параметры, которые вводятся с
клавиатуры. Сервер обрабатывает полученные данные и возвращает результат
клиенту. Варианты:

b. Решение квадратного уравнения.

Реализовать с помощью протокола TCP

### Используемый стэк
```
go version go1.22.5 darwin/arm64
```
Используются только базовые фреймворки и пакеты (`net`, `net\http`, `log` и т.д.)

### Запуск

Параметры запуска сервера:
```bash
go run task_2/server.go -p <port>
```
Параметры запуска клиента:
```bash
go run task_1/client.go -p <port> 
```
Клиент ожидает на вход три аргумента для уравнения (коэффициенты). Валидирует их на бэкенде и
находит решение через дискриминант. В случае провальной валидации сообщает об ошибке и ждет новый
ответ от пользователя. Сервер же постоянно слушает подключение и в горутине обрабатывает запросы
(т.е. одновременно может подключиться несколько клиентов), логируя ошибки и отправку сообщений.
Клиент может отключиться с помощью прописанной команды `exit`