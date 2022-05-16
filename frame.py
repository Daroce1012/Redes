import structs

def Hash(hex_str):
       count=0
       hash_var=0
       while(count<len(hex_str)):
            actual_byte=hex_str[count:count+2]
            hash_var=hash_var + hex_dec(actual_byte)
            count=count + 2
       dec_bin=bin(hash_var)[2:]
       return dec_bin

def Mac_Origen(host): #el host que recibe tiene que ser el dispositivo
        return  hex_bin(structs.Host(host).mac)
    
def bin_hex(exp_bin):
        hexstr=f'{int(exp_bin,2):X}'
        return hexstr
        

def hex_bin(exp_hex):
        binstr="{0:08b}".format(int(exp_hex,16))
        return binstr

def hex_dec(exp_hex):
        return int(exp_hex,16)

def bin_dec(exp_bin):
        return int(exp_bin,2)
    
def Is_to_all(mac_destino):
        mac = hex_bin(mac_destino) 
        for i in mac:
            if i != '1':
                return False
        return True
    
def size (d):
        a = d[0:8] #Primeros 8 bits

        return bin_dec(a)
    
def veri_data (d):
     a = d[8:16] #Proximo 8 bits
     return bin_dec(a)   

def bin_hex_por_partes(bin_str):

    count=0
    bin_hex_var=""
    while(count<len(bin_str)):
        actual=bin_str[count:count+8]
        bin_hex_var=bin_hex_var+bin_hex("".join(actual))
        count=count+8
    return bin_hex_var

class Frame:
    def __init__(self,host , mac_dest,data):#el data que recibe tiene que ser un string , el host que se recibe es un dispositivo
      d = hex_bin(data)
      self.host_origen = host
      self.data = d
      self.mac_destino = hex_bin(mac_dest)
      self.mac_origen = Mac_Origen(host) 
      self.size = bin(len(data)/2)[2:]                # cant de byts en binario que representa el tamnno en byts de los datos
      self.dato_veri = Hash(data)   
      self.size_dato_veri = bin(self.dato_veri/8)[2:] # cant de byts en binario que representa el tamnno en byts de los datos 