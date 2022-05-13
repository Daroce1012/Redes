from asyncio.windows_events import NULL
from  frame import Frame ,Hash,bin_hex,bin_dec,hex_bin,hex_dec,bin_hex_por_partes
import structs
import os
import shutil
from sys import stdin

host_list=[]
Devices=[]
sending = []
stopsend = []

def deteccion_errores(bin_str):

    data=bin_str[32:]

    datos_size=bin_dec(data[0:8])
    datos_verif_size=bin_dec(data[8:16])
    
    pos_final=(datos_size*8)+16
    datos=data[16:pos_final]
    datos_verif=data[pos_final:(datos_verif_size*8)+pos_final]
    hash_datos=Hash(bin_hex_por_partes(datos))

    return bin_dec(hash_datos)==bin_dec(datos_verif)


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
        send(string_list[2], string_list[3])
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


def send_frame(host,mac_destino,data):
    frame = None
    for i in host_list:
        if i.name == host:
            frame = Frame(i,mac_destino,data)
            send_f = frame.mac_destino + frame.mac_origen + frame.size + frame.size_dato_veri + frame.data + frame.dato_veri
            send(host,send_f)
            break
  

def mac (host ,address):
    for h in host_list:
        if(h.name == host):
           h.mac = address
     
#arreglar para switch y probar
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

    device_1.ports[int(port_1[1]) - 1] = device_2 #send del device 1
    device_2.ports[int(port_2[1]) - 1] = device_1 #send del device 2

    if device_1.value_send[int(port_1[1]) - 1] !=-1:
        device_1.send(device_1)
    elif device_2.value_send[int(port_1[1]) - 1] !=-1:
        device_2.send(device_2)

    for i in sending:
        if i.collision == "collision":
            i.time_to_send = -1
            sending.remove(i)
    return


def dfs_update_all(device): #restablece las propiedades de los dispositivos que son alcanzables desde device en todos las direcciones
    if isinstance(device, structs.Host):
        device.collision = ' '
        device.data_to_receive = []
    if isinstance(device, structs.Switch):
        device.data_to_receive = []
    for i in range(len(device.ports)):
        device.state_receive[i] = False
        device.value_receive = -1
        device.state_send = False
        device.value_send = -1
        if device.ports[i] != None :           
            dfs_update(device.ports[i])
        
#ponerlo funcional para el switch
def dfs_update(device):  #restablece las propiedades de los dispositivos que son alcanzables desde device en un solo sentido
    #device.value = -1
    if isinstance(device, structs.Host):
        device.collision = ' '
    for i in range(len(device.ports)):
        if device.ports[i] != None  and device.state_send[i]:
            device.state_send[i] = False
            device.value_send[i] = -1
            #device.states[i] = 'null'
            dfs_update(device.ports[i])
        else:
            #device.states[i] = 'null' 
            device.state_receive[i] = False
            if isinstance(device, structs.Host) or isinstance(device, structs.Switch):
                device.value_receive = -1
                device.data_to_receive = []
            

#arreglar para switch y probar
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
    if(device1.state_send[port]):
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
         """#voy a comparar las mac para saber si esta recibiendo de mi la pc a la que quiero enviar
            mac_receive = bin_hex(i.data_to_send[0:16]) #mac de la pc que recibe
            pc_receive = take_Host(mac_receive)  #pc que recibe
            if(len(pc_receive.data_to_receive)> 16) :#estoy aqui por eso tienes el error
                mac_send = bin_hex( pc_receive.data_to_receive[16:])
                for j in range(0,len (mac_send)):
                    if(i.mac[j] != mac_send[j]):
                        pass
                
          """
         i.time_to_send += 1
         if (i not in sending):
            temp = i.data_to_send[0]
               # if int(i.value) == -1 or i.value == temp: #todo lo que esta acontinuacion hasta el else iba dentro del if
            i.state_send[0] = True
            sending.append(i)
            i.value_send[0] = i.data_to_send.pop(0)
            i.collision = "ok"
            i.send(i)
                #else:                           #ya no hay colision xq los cables son duplex
                    #i.collision = "collision"
                    #i.time_to_send -= 1

    return


def data_txt(time):
    for item in host_list:
        if(item.data_to_receive!=None):
            h=open('host_data/'+item.name+'_data.txt','a+')
            _frame=item.data_to_receive
            mac_send=_frame[16:32]
            data=_frame[32:]
            if(deteccion_errores(data)):
                print(str(time) + ' ' + mac_send + ' ' + data)
                h.close()
            else:
                print(str(time) + ' ' + mac_send + ' ' + data + 'ERROR')
                h.close()

def writetxt(time):
        tempvalue = -1
        for device in Devices:
            s = open('devices/' + device.name + '.txt', 'a+')
            for i in range(len(device.ports)):
                if isinstance(device, structs.Host):
                    # tempvalue = str(device.value)
                    if (device.state_receive[i] and device.state_send[i]):
                        tempvalue = str(device.data_to_receive[len(device.data_to_receive) - 1])
                        tempvalue_1 = str(device.data_to_send[0])
                        print(str(time) + '  ' + device.name + '_' + str(i + 1) + '  ' + "receive:" + '  ' +
                              tempvalue + ' ' + "send:" + ' ' + tempvalue_1 + '  ' + device.collision,
                              file=s)
                    elif (device.state_send[i] and device.value_send != None):
                        tempvalue = device.value_send[0]
                        print(str(time) + '  ' + device.name + '_' + str(i + 1) + ' ' + "receive:" + '  ' +
                              "-1" + '  ' + "send" + '  ' + str(tempvalue) + '  ' + device.collision,
                              file=s)
                    elif (device.state_receive[i] and device.value_receive != None):
                        tempvalue = device.value_to_receive[0]
                        print(str(time) + '  s' + device.name + '_' + str(i + 1) + '  ' + "receive:" + '  ' +
                              str(tempvalue) + '  ' + "send" + ' ' + "-1" + '  ' + device.collision,
                              file=s)
                    else:
                        print(str(time) + '  s' + device.name + '_' + str(i + 1) + '  ' + "receive:" + '  ' +
                              "-1" + '  ' + "send" + ' ' + "-1" + ' ' + device.collision,
                              file=s)
                else:
                    if (device.state_receive[i]):
                        print(str(time) + '  ' + device.name + '_' + str(i + 1) + '  ' + "receive" + '  ' +
                              str(device.value_receive[i]) + ' ' + "send" + ' ' + "-1", file=s)
                    elif (device.state_send[i]):
                        print(
                            str(time) + '  ' + device.name + '_' + str(i + 1) + '  ' + "receive" + '  ' + "-1" + '  ' +
                            "send" + '  ' + str(device.value_send[i]), file=s)
                    else:
                        print(str(time) + '  ' + device.name + '_' + str(i + 1) + ' ' + "receive" + '  ' + "-1" + '  ' +
                              "send" + '-1', file=s)
            s.close()
            
def update_sending():
    for i in sending:
        i.state_send[0] = True
        i.value = i.data_to_send.pop(0)
        i.collision = "ok"
        i.send(i)


def update_value(delete):
    for i in sending:
        if (i not in delete):
            i.data_to_send.insert(0, i.value)
    for h in delete:
        h.value_send[0] = -1
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
                    data_txt(time)

        if(len(delete)>0):
           update_value(delete)
           if(len(sending)>0):
               update_sending()

        delete = []
        time += 1


main()
#bel este es el ultimo