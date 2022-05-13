from http.client import REQUEST_ENTITY_TOO_LARGE
import json
from re import S
import socket
import time
from _thread import *
from unicodedata import name
from urllib import request

HOST = '192.168.0.12' # 나의 주소
PORT = 9988 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
 
server_socket.listen()

client_socket, addr = server_socket.accept()

print('Connected by', addr)

date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime(time.time()))\

while True:

    message = "HTTP/1.1{}\r\nDate: {}\r\nServer: Mac\r\nContent-Length: {}\r\nkeep-Alive: timeout=10, max100\r\nConnection: Keep-Alive\r\nContent-Type: json\r\n\r\n{}"

    data = client_socket.recv(1024)
    if not data:
        break
    
    print(data
    )
    request = data.decode().split("\r\n")

        
    try :
        order = request[-1].split(" ",3)
        order[1] != "Gundam"
        unit_name = order[0] + " " + order[1]
    except Exception as e: 
        resp =  " 400"
        body = "BAD REQUEST"
        message = message.format(resp,date,len(body),body)
        client_socket.sendall(message.encode())
        continue

    with open('data.json') as f :
            file = json.load(f)

    

    # GET Method
    if request[0] == 'get' :
        #데이터 비교
        for unit in file['UNIT'] :
            check = 0
            if unit_name == unit['NAME']: 
                check = 1
                resp =  " 200"
                message = message.format(resp,date,len(str(unit)),str(unit))   
                client_socket.sendall(message.encode())
                break

        else:
            resp = " 404"
            errmes = "NOT FOUND(GET ERROR)"
            message = message.format(resp,date,len(errmes),(errmes))         
            client_socket.sendall(message.encode())
            continue

    # POST Method (create)
    elif request[0] == 'post' :

        try :
            unit_name = request[-1]
        except :
            resp = " 400"
            errmes = "BAD REQUEST(POST ERROR)"
            message = message.format(resp,date,len(str(errmes)),str(errmes))         
            client_socket.sendall(message.encode())
            continue
        
        
        for unit in file['UNIT'] :
            if unit['NAME'] == unit_name : 
                check = 1
                resp = " 400"
                errmes = "BAD REQUEST(POST ERROR)\r\nIt's already exist"
                message = message.format(resp,date,len(str(errmes)),str(errmes))
                client_socket.sendall(message.encode())
                

            else: check=0
           
        if check == 0 :
            newObj = {
                "NAME": unit_name,
                "MODEL": "",
                "PILOT": "",
                "TEAM": ""
            }

            file['UNIT'].append(newObj)
                
            with open('data.json','w') as f :
                json.dump(file,f,indent=2)
                        
            resp = " 201"
            message = message.format(resp,date,len(str(newObj)),str(newObj))  
            client_socket.sendall(message.encode())



    # HEAD Method
    elif request[0] == 'head' : 
        
        for unit in file['UNIT'] :
            check = 0
            if unit_name == unit['NAME']: 
                check = 1
                resp =  " 200"
                body = ""
                message = message.format(resp,date,len(str(body)),str(body))
                client_socket.sendall(message.encode())
                break

        else:
            resp = " 404"
            errmes = "NOT FOUND(GET ERROR)"
            message = message.format(resp,date,len(errmes),(errmes))         
            client_socket.sendall(message.encode())
            continue


    # PUT Method (update)
    elif request[0] == 'put' :

        try :
            category = order[2]
            value = order[3]
        except:
            resp = " 400"
            errmes = "BAD REQUEST(PUT ERROR)"
            message = message.format(resp,date,len(str(errmes)),str(errmes))
            client_socket.sendall(message.encode())

            print(category +" " + value)

        for i,unit in enumerate(file['UNIT']) : 
            if unit_name == unit['NAME'] :
                
                if category == 'MODEL' :
                    file['UNIT'][i]['MODEL'] = str(value)
                    resp =  " 200"
                    break
                    
                elif category == 'PILOT' :
                    file['UNIT'][i]['PILOT'] = str(value)
                    resp =  " 200"
                    break

                elif category == 'TEAM' :
                    file['UNIT'][i]['TEAM'] = str(value)
                    resp =  " 200"
                    break                 


        with open('data.json','w') as f :
            json.dump(file,f,indent=2)
        message = message.format(resp,date,len(str(unit)),str(unit))     
        client_socket.sendall(message.encode())

    else :
        resp = "400"
        errmes = "BAD REQUEST\r\nCheck Your Method"
        message = message.format(resp,date,len(str(errmes)),str(errmes))  
        client_socket.sendall(message.encode())


    



# 소켓을 닫습니다.
client_socket.close()
server_socket.close()