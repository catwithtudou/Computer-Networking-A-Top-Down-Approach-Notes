from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
# prepare a server socket
serverSocket.bind(('', 6789))  # 将TCP欢迎套接字绑定到指定端口号
serverSocket.listen(1)  # 最大连接数为1

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()  # 接收到客户端连接请求后,建立新的TCP连接套接字
    try:
        message = connectionSocket.recv(1024)  # 获取了客户端发送的报文
        filename = message.split()[1] # 获取文件名称
        f = open(filename[1:])
        outputdata = f.read();
        # Send one HTTP header line into socket
        header = ' HTTP/1.1 200 OK\n' \
                 'Connection: close\n' \
                 'Content-Type: text/html\n' \
                 'Content-Length: %d\n\n' % (len(outputdata))
        connectionSocket.send(header.encode())  # 发送响应报文

        # Send the content of the requested file to the client
        for i in range(0,len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
    except IOError:
        #  Send response message for file not found
        header = 'HTTP/1.1. 404 Found'  # 返回404
        connectionSocket.send(header.encode())

        # close client socket
        connectionSocket.close()
serverSocket.close()
