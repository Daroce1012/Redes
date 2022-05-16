from  frame import Hash,bin_hex,bin_dec,hex_bin,hex_dec,bin_hex_por_partes
from main import take_Host

class Device:                                  # estructura general que engloba a todos los dispositivos
    def __init__(self,name,PortsNumber):
        self.name=name                         # nombre del dispositivo
        self.state_send=[False]*PortsNumber    # representa el estado de envio en cada uno de los puertos
        self.state_receive=[False]*PortsNumber # representa el estado de recepcion en cada uno de los puerto
        self.ports=[None]*PortsNumber          # representa a cada uno de los puertos
        self.value_send=[-1]*PortsNumber       # informacion que se esta enviando por el puerto
        self.value_receive = [-1]*PortsNumber  # informacion que se esta reciviendo por el puerto

        # este metodo send de los dispositivos hace un recorrido en profundidad por los puertos,asigna el valor en canal a todos los otros dispositivos que se alcancen
        # se llama a partir de un dispositivo q este enviando que sera device
        # asignandole ademas el estado por puerto a cada uno,  self es quien recive la informacion 
    def send(self, device): 
        temp = '-1'                                                     # valor que recibio va a recibir self
        # self.value = device.value
        for i in range(len(device.ports)):                              # Buscando el valor a enviar, buscando el cable de envio
             if (device.ports[i] != None and device.ports[i] == self):
                   temp = device.value_send[i]                          # Valor que se le va a enviar al destino


        for i in range(len(self.ports)):
            if (self.ports[i] != None):

                if (self.ports[i] == device):       # me busco en los puertos del que quiero enviales la informacion,i representa el puerto de self
                    self.state_receive[i] = True    # cable que recibe en el self ,actualizando el estado
                    
                    if(isinstance(self, Host) and self.value_receive[i] !=-1 and self.ports[i].state_receive and self.value_receive[i] != temp ):
                        self.self.collision = "collision"
                        # como solucionar esta colision hablo de esto belsai  
                        # ver recuperacion de los bits perdidos   
                    self.value_receive[i] = temp    # actualizo el valor a recibir
                    if(isinstance(self, Host) or isinstance(self, Switch)):
                        self.data_to_receive.append(temp)    

                else: # el resto de los puertos envian mi valor en caso de que sea un host , pero si es un switch , ya eso cambia
                    brodcast = True
                    mac_dest_bin = None
                    puerto = None                                       # puerto del switch que va a enviar la inf del switch
                   # table = False
                    if(isinstance(self, Switch)):
                        if(len(self.data_to_receive)>31):               # registrar la mac origen y el puerto
                            mac_orig_bin = self.data_to_receive[16:32]  # proximos 16 bits mac origen
                            self.table.append([mac_orig_bin,i])         # registro la informacion en table mac, puerto
                        
                        if(len(self.data_to_receive)>15):               # busca el puerto que va a recibir
                            mac_dest_bin = self.data_to_receive[0:16]   # primeros 16 bits mac destino
                            temp = take_Host(bin_hex(mac_dest_bin))     # temp != None implica que existe un destino en especifico
                            if mac_dest_bin != "1111111111111111" and temp !=None:
                                for i in self.table:                    # Buscar si el host en la table del switch   
                                    if (i[0])[0] == mac_dest_bin:
                                        brodcast = False
                                        puerto = (i[0])[1]         

                    if(self is not device):
                        self.state_send[i] = True                   # actualiza el estado
                        self.value_send[i] = str(temp)              # agregarle al resto de los puertos , los puertos se van recorriendo por el for de arriba y aqui se le pone el value
                    else:
                        temp = self.value_send[i]

                    if brodcast:                                        # enviar a todos los conectados a el
                        puerto = i

                    next_self = self.ports[puerto]                   # dispositivo alcanzable desde self , i puerto de self que lo conecta a este dipositivo
                    value_next = 0
                    for j in range(0, len(next_self.ports)):         # buscando el valor que tiene el otro dispositivo en receive
                        if next_self.ports[j] == self:               # j puerto que conecta al dispositivo con self
                            value_next = next_self.value_receive[j]  # guardo el valor que esta reciviendo a partir de self

                    if(value_next != temp):            # si el dispositvo al que se llega a traves de self no esta actualizado
                        self.ports[puerto].send(self)  # expandir a self       
                    """"        
                    if brodcast:
                        puerto = i    
                    next_self = self.ports[puerto]                       # dispositivo alcanzable desde self , i puerto de self que lo conecta a este dipositivo
                    value_next = 0
                    for j in range(0, len(next_self.ports)):        # buscando el valor que tiene el otro dispositivo en receive
                        if next_self.ports[j] == self:               # j puerto que conecta al dispositivo con self
                            value_next = next_self.value_receive[j] 
                    """


class Host(Device):             # estructura host
    def __init__(self,name):
        super().__init__(name,1)
        self.time_to_send = -1  # tiempo de envio de datos
        self.data_to_send=  []  # datos que faltan por enviar
        self.data_to_receive=[] # datos recibidos hasta el momento
        self.collision=' '      # representa si hubo una colision en el puerto
        self.mac = None         # direccion mac del dispositivo
         

class Hub(Device):
    def __init__(self,name,PortsNumber):
        super().__init__(name,PortsNumber)


class Switch(Device):
     def __init__(self,name,PortsNumber):
        super().__init__(name,PortsNumber)
        self.table = [[]]  # tabla lista de mac y puertos
        self.data_to_receive=[]  # frame
        self.frame_stop = []     # guarda los frame que tiene en stop
        