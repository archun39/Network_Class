
import socket


# 서버의 주소입니다. hostname 또는 ip address를 사용할 수 있습니다.
HOST = '192.168.0.12'  
# 서버에서 지정해 놓은 포트 번호입니다. 
PORT = 9988      


# 소켓 객체를 생성합니다. 
# 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.  
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 지정한 HOST와 PORT를 사용하여 서버에 접속합니다. 
client_socket.connect((HOST, PORT))

while True : 
    message = "{}\r\nHTTP/1.1\r\nHost: 127.0.0.1\r\nUser-Agent: M1PRO\r\nAccept: json ,spplication/xhtml+xml\r\nAccept-Language: kr\r\nContent-Length: {}\r\nKeep-Alive: 50\r\nConnection: keep-alive\r\n\r\n{}"
    request = input(">> Method : ")

    if request == 'end' :
        break
        
    elif request == 'exit' :
        break

    elif request == 'get' :
        data = input("GET : ")
        message = message.format(request,len(data),data)
        


    elif request == 'post' :
        data = input("POST : ")
        message = message.format(request,len(data),data)
        

    elif request == 'put' : 
        data = input("PUT : ")
        message = message.format(request,len(data),data)
        
    
    elif request == 'head' :
        data = input("HEAD : ")
        message = message.format(request,len(data),data)
        

    else :
        print("400(BAD REQUEST)")
        continue

    client_socket.sendall(message.encode())

    data = client_socket.recv(1024)
   
    print(data)
    
    


# 소켓을 닫습니다.
client_socket.close()