from lib2to3.pygram import pattern_symbols


class Device: #estructura general que engloba a todos los dispositivos
    def __init__(self,name,PortsNumber):
        self.name=name                         # nombre del dispositivo
        self.state_send=[False]*PortsNumber    # representa el estado de envio en cada uno de los puertos
        self.state_receive=[False]*PortsNumber # representa el estado de recepcion en cada uno de los puerto
        self.ports=[None]*PortsNumber          # representa a cada uno de los puertos
        self.value_send=[-1]*PortsNumber       # informacion que se esta enviando por el puerto
        self.value_receive = [-1]*PortsNumber  # informacion que se esta reciviendo por el puerto


        # este metodo send de los dispositivos hace un recorrido en profundidad por los puertos
        # se llama a partir de un dispositivo q este enviando
        # asigna el valor en canal a todos los otros dispositivos que se alcancen, asignandole ademas el estado por puerto a cada uno

    def send(self, device):
        temp = -1
        # self.value = device.value
        for i in range(len(device.ports)): #Buscando el valor a enviar
             if (device.ports[i] != None and device.ports[i] == self):
                   temp = device.value_send[i] #Valor que se le va a enviar al destino

        for i in range(len(self.ports)):
            if (self.ports[i] != None):
                if (self.ports[i] == device):       # me busco en los puesrtos del que quiero enviales la informacion

                    self.state_receive[i] = True    # actualizando el estado
                    
                    if(isinstance(self, Host) and self.value_receive[i] !=-1 and self.ports[i].state_receive and self.value_receive[i] != temp ):
                        self.self.collision = "collision"
                        #como solucionar esta colision hablo de esto belsai     
                                    
                    self.value_receive[i] = temp    # actualizo el valor a recibir

                    #if device.value != -1 and isinstance(self, Host) and self.state_send[0] == True and device.value != temp:
                        #self.collision = "collision"
                        #self.data_to_send.insert(0,temp)
                    #self.state_receive[i] = True  
                      
                else: # el resto de los puertos envian mi valor en caso de que sea un host , pero si es un switch , ya eso cambia
                  
                    if(isinstance(self, Switch)):
                        pass

                    else:
                       self.state_send[i] = True  #actualiza el estado
                       self.value_send[i] = temp  # agregarle al resto de los puertos , los puertos se van recorriendo por el for de arriba y aqui se le pone el value
                       
                       next_self = self.ports[i] #dispositivo alcanzable desde self , i puerto de self que envia a este dipositivo
                       value_next = 0
                       for j in range(0, len(next_self.ports)):
                           if next_self.ports[j] == self:
                               value_next = next_self.value_receive[j]

                       if(value_next != temp): #si el dispositvo al que se llega a traves de self no esta actualizado
                            self.ports[i].send(self)
                    """self.state_send[i] = True
                    if (self.ports[i].value != self.value):
                        self.ports[i].send(self)
                    """

class Host(Device):  # estructura host o computer 
    def __init__(self,name):
        super().__init__(name,1)
        self.time_to_send = -1  # tiempo de envio de datos
        self.data_to_send=  []  # datos que faltan por enviar
        self.data_to_receive=[] # datos recividos hasta el momento
        self.collision=' '      # representa si hubo una colision en el puerto
        self.mac = None         # direccion mac del dispositivo
         

class Hub(Device):
    def __init__(self,name,PortsNumber):
        super().__init__(name,PortsNumber)


class Switch(Device):
     def __init__(self,name,PortsNumber):
        super().__init__(name,PortsNumber)
        self.mac_conect = [[]]
        

