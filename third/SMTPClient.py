from socket import *
import base64

# Mail Content
subject = 'I love computer network'
contentType = 'text/plain'
msg = 'I love computer netword'
endMsg = '\r\n.\r\n'

mailServer = 'smtp.163.com'

fromAddress = "zhengyu4930@163.com"
toAddress = "949812478@qq.com"

username = base64.b64encode("zhengyu4930@163.com".encode('utf-8'))
password = base64.b64encode("tudoutudou4930".encode('utf-8'))

baseUsernmae = str(username, encoding="utf-8")
basePassword = str(password, encoding="utf-8")

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, 25))

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

helloCommand = 'HELO Alice\n'
clientSocket.send(helloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server')

clientSocket.sendall('AUTH LOGIN\r\n'.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if recv2[:3] != '334':
    print('334 reply not received from server')

clientSocket.sendall((baseUsernmae + '\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '334':
    print('334 reply not received from server')

clientSocket.sendall((basePassword + '\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '235':
    print('235 reply not received from server')

clientSocket.sendall(('MAIL FROM: <' + fromAddress + '>\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server')

clientSocket.sendall(('RCPT TO: <' + toAddress + '>\r\n').encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '250':
    print('250 reply not received from server')

clientSocket.send('DATA\r\n'.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '354':
    print('354 reply not received from server')

message = 'from:' + fromAddress + '\r\n'
message += 'to:' + toAddress + '\r\n'
message += 'subject:' + subject + '\r\n'
message += 'Content-Type:' + contentType + '\r\n'
message += '\r\n' + msg
clientSocket.sendall(message.encode())

clientSocket.sendall(endMsg.encode())
recv = clientSocket.recv(1024).decode()
print(recv)
if (recv[:3] != '250'):
    print('250 reply not received from server')

clientSocket.sendall('QUIT\r\n'.encode())

clientSocket.close()
