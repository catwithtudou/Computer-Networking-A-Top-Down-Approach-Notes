from socket import *

tcpSerPort = 8899
tcpSerSock = socket(AF_INET, SOCK_STREAM)

tcpSerSock.bind(('', tcpSerPort))
tcpSerSock.listen(5)

while True:
    print('Ready to serve ...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    message = tcpCliSock.recv(4096).decode()

    filename = message.split()[1].partition("//")[2].replace('/', '_')
    fileExist = "false"
    try:
        f = open(filename, "r")
        outputdata = f.readlines()
        fileExist = "true"
        print('File Exists!')

        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i].encode())
        print('Read from cache')

    except IOError:
        print('File Exist: ', fileExist)
        if fileExist == "false":
            print('Creating socket on proxyServer')
            proxy = socket(AF_INET, SOCK_STREAM)

            hostn = message.split()[1].partition("//")[2].partition("/")[0]
            print('Host name : ', hostn)
            try:
                # 连接到初始服务器80端口
                proxy.connect((hostn, 80))
                print('Socket connected to port 80 of the host')

                proxy.sendall(message.encode())
                recv = proxy.recv(4096)

                # 收到网页信息后返回至代理服务器
                tcpCliSock.sendall(recv)

                # 收到网页信息后创建文件
                tempFile = open("./" + filename, "w")
                tempFile.writelines(recv.decode().replace('\r\n', '\n'))
                tempFile.close()
            except:
                print('Illegal request')
        else:
            # 如果文件标志存在但并没有找到文件，则返回错误信息
            print('File Not Found ....')

    tcpCliSock.close()
