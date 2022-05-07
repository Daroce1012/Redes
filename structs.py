from pickle import FALSE


class Device: #estructura general que engloba a todos los dispositivos
    def __init__(self,name,PortsNumber):
        self.name=name                        # nombre del dispositivo
        self.state_send=[False]*PortsNumber   # representa el estado de envio en cada uno de los puertos
        self.state_recive=[False]*PortsNumber # representa el estado de recepcion en cada uno de los puerto
        self.ports=[None]*PortsNumber         # representa a cada uno de los puertos
        self.value_send=[-1]*PortsNumber      # informacion que se esta enviando por el puertp
        self.value_recive = [-1]*PortsNumber  # informacion que se esta reciviendo por el puerto


        # este metodo send de los dispositivos hace un recorrido en profundidad por los puertos
        # se llama a partir de un dispositivo q este enviando
        # asigna el valor en canal a todos los otros dispositivos que se alcancen, asignandole ademas el estado por puerto a cada uno

    def send(self, device):
        temp = self.value
        self.value = device.value
        for i in range(len(self.ports)):
            if (self.ports[i] != None):
                if (self.ports[i] == device):
                    if device.value != -1 and isinstance(self, Host) and self.states[0] == "send" and device.value != temp:
                        self.collision = "collision"
                        self.data_to_send.insert(0,temp)
                    self.states[i] = "recive"

                else:
                    self.states[i] = "send"
                    if (self.ports[i].value != self.value):
                        self.ports[i].send(self)


class Host(Device):  # estructura host o computer 
    def __init__(self,name):
        super().__init__(name,1)
        self.time_to_send = -1 # tiempo de envio de datos
        self.data_to_send=  [] # datos que faltan por enviar
        self.data_to_recive=[] # datos recividos hasta el momento
        self.collision=' '     # representa si hubo una colision en el puerto
        self.mac = None        # direccion mac del dispositivo
         

class Hub(Device):
    def __init__(self,name,PortsNumber):
        super().__init__(name,PortsNumber)


class Switch(Device):
     def __init__(self,name,PortsNumber):
        super().__init__(name,PortsNumber)
        self.mac_conect = [[]]
        

