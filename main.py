from asyncio.windows_events import NULL
from frame import Frame, bin_hex
import structs
import os
import shutil
from sys import stdin

host_list=[]
Devices=[]
sending = []
stopsend = []
#stopframe = []

def read_Script(name):
    with open(name,"r") as archivo:
        for linea in archivo:
            parse(linea)

def parse(string_list):
    if(string_list[1]=="create"):
        create(string_list)
    elif (string_list[1] == "mac"):
        mac(int(string_list[0]), string_list[2])    
    elif(string_list[1]=="connect"):
        connect(int(string_list[0]),string_list[2],string_list[3])
    elif(string_list[1]=="disconnect"):
        disconnect(int(string_list[0]),string_list[2])
    elif (string_list[1] == "send"):
        send(int(string_list[0]), string_list[2], string_list[3])
    elif (string_list[1] == "send_frame"):
        send_frame(string_list[2], string_list[3],string_list[4])   
        
def create(linea_list):
    if(len(linea_list)==4):
        create_host(int(linea_list[0]), linea_list[3])
    elif linea_list[2] == "switch":
        create_switch(int(linea_list[0]), linea_list[3], int(linea_list[4]))
    else:
        create_hub(int(linea_list[0]), linea_list[3], int(linea_list[4]))

def create_hub(time,name,puertos):
    hub_=structs.Hub(name, puertos)
    Devices.append(hub_)

def create_host(time,name):
    host_=structs.Host(name)
    host_list.append(host_)
    Devices.append(host_)

def create_switch(time,name,puertos):
    switch_=structs.Hub(name, puertos)
    Devices.append(switch_)


def send(host,data):
    for i in Devices:
        if(i.name == host):
            i.data_to_send = [x for x in data]
            if i not in  stopsend :
                stopsend.append(i)

    return


#Modificar esto que no sirve
def send_frame(host,mac_destino,data):
    frame = None
    for i in host_list:
        if i.name == host:
            frame = Frame(i,mac_destino,data)
            send_f = frame.mac_destino + frame.mac_origen + frame.data
            send(host,send_f)
            break
  #  if frame != None:
   #     stopframe.append(frame)




def dfs(device):  #restablece las propiedades de los dispositivos que son alcanzables desde device
    device.value = -1
    if isinstance(device, structs.Host):
        device.collision = ' '
    for i in range(len(device.ports)):
        if device.ports[i] != None and device.states[i] != 'null':
            device.states[i] = 'null'
            dfs(device.ports[i])


def mac (host ,address):
    for h in host_list:
        if(h.name == host):
           h.mac = address
     

def connect(time,port1,port2):
    port_1=port1.split('_')
    port_2=port2.split('_')
    device_1 = None
    device_2 = None
    temp = 0
    for j in Devices:
        if(j.name==port_1[0]):
            device_1=j
        elif(j.name==port_2[0]):
            device_2=j

    device_1.ports[int(port_1[1]) - 1] = device_2
    device_2.ports[int(port_2[1]) - 1] = device_1

    if device_1.value !=-1:
        device_1.send(device_1)
    elif device_2.value !=-1:
        device_2.send(device_2)

    for i in sending:
        if i.collision == "collision":
            i.time_to_send = -1
            sending.remove(i)
    return

def dfs_update(device):  #restablece las propiedades de los dispositivos que son alcanzables desde device
    device.value = -1
    if isinstance(device, structs.Host):
        device.collision = ' '
    for i in range(len(device.ports)):
        if device.ports[i] != None and device.states[i] != 'null':
            device.states[i] = 'null'
            dfs_update(device.ports[i])
        else:
            device.states[i] = 'null'

def disconnect(time,port):
    
    port = port.split('_')
    device_name = port[0]
    port = int(port[1]) - 1

    device1 = None
    device2 = None

    # buscando al dispositivo que contiene al puerto que se envio en la instruccion desconectar
    for j in Devices:
       if (j.name == device_name):
           device1 = j

    device2 = device1.ports[port]

    # buscando al primer dispositivo en los puertos del segundo
    for i in range(len(device2.ports)):
        if device2.ports[i] is not None and device2.ports[i] == device1:
            device2.ports[i] = None

    device1.ports[port] = None
    if(device1.states[port] == "send"):
       dfs_update(device2)

    else:
     dfs_update(device1)

    return

def take_Host(mac):
    for i in host_list:
        if(i.mac == mac) :
            return i
    return None

def to_sendig():
    if len(stopsend)> 0 :
        for i in stopsend:
            mac_recive = bin_hex(i.data_to_send[0:16])
            pc_recive = take_Host(mac_recive)
            if(len(pc_recive.data_to_recive)> ) #estoy aqui por eso tienes el error

            
            if (i not in sending):
                i.time_to_send += 1
                temp = i.data_to_send[0]
               # if int(i.value) == -1 or i.value == temp: todo lo que esta acontinuacion hasta el else iba dentro del if 
                i.states[0] = i.states[0]+"send"
                sending.append(i)
                i.value = i.data_to_send.pop(0)
                i.collision = "ok"
                i.send(i)
                #else:                           #ya no hay colision xq los cables son duplex
                    #i.collision = "collision"
                    #i.time_to_send -= 1

    return

"""def to_sending_frame():
    if len(stopframe)>0:
        for i in stopframe:
            host = i.host_origen
            if(host not in sending):
              pass
    pass
"""
    


def writetxt(time):
    for device in Devices:
            s = open('devices/' + device.name + '.txt', 'a+')
            for i in range(len(device.ports)):
                if isinstance(device, structs.Host):
                    tempvalue = str(device.value)
                    if(device.collision == "collision"):
                            tempvalue = device.data_to_send[0]
                    print(str(time) + '  ' + device.name + '_' + str(i + 1) + '  ' + device.states[i] + '  ' + (
                     tempvalue if device.states[i] != 'null' else ' ') + '  ' + device.collision,
                          file=s)
                else:
                    print(str(time) + '  ' + device.name + '_' + str(i + 1) + '  ' + device.states[i] + '  ' + (
                    str(device.value) if device.states[i] != 'null' else ' '), file=s)
            s.close()


def update_sending():
    for i in sending:
        i.states[0] = "send"
        i.value = i.data_to_send.pop(0)
        i.collision = "ok"
        i.send(i)


def update_value(delete):
    for i in sending:
        if (i not in delete):
            i.data_to_send.insert(0, i.value)
    for h in delete:
        h.value = -1
        h.time_to_send = -1
        dfs_update(h)
        sending.remove(h)


def main():
    global signal_time
    global writing_intervals  # cada vez q transcurra este valor en ms se escribira en el txt correspondiente de cada dispositivo

    config = open('config.txt', 'r')

    signal_time = int(config.readline(-1))
    writing_intervals = int(config.readline(-1))
    config.close()

    time = 0
    f = open('script.txt', 'r')

    try:
        shutil.rmtree('devices')
        os.mkdir('devices')
    except:
        pass
    lines = [line.split() for line in f]
    f.close()
    delete = []
    while (len(lines) or len(stopsend)):  # el programa se mantiene corriendo mientras quede una linea por leer o un bit de informacion que enviar
        while (len(lines) and int(lines[0][0]) == time):  # se leen todas las instrucciones del instante de tiempo actual
            instruction = lines.pop(0)
            parse(instruction)
        if len(stopsend)>0:
            to_sendig()

        if (time % writing_intervals == 0):
            writetxt(time)

        for device in sending:  # cuando un dispositivo envia un bit de info y lo mantiene en el canal durante un intervalo de signalTime sale de la cola de los q estan enviando
            if int(device.time_to_send) == (int(signal_time)-1):
                delete.append(device) #quitar de sending
                if len(device.data_to_send) == 0:  # ademas, si ya no tiene mas bits q enviar sale de la cola de los q quieren enviar
                    stopsend.remove(device)

        if(len(delete)>0):
           update_value(delete)
           if(len(sending)>0):
               update_sending()

        delete = []
        time += 1


main()

