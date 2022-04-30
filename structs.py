class Device: #estructura general que engloba a todos los dispositivos
    def __init__(self,name,PortsNumber):
        self.name=name
        self.states=["null"]*PortsNumber #representa el estado de cada uno de los puertos
        self.ports=[None]*PortsNumber # representa a cada uno de los puertos
        self.value=-1 #informacion que se esta transmitiendo o reciviendo en el canal


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
        self.time_to_send = -1
        self.data_to_send=[]
        self.collision=' '


class Hub(Device):
    def __init__(self,name,PortsNumber):
        super().__init__(name,PortsNumber)




