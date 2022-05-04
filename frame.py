from binhex import hexbin
import structs

class Frame:
    def __init__(self,host , mac_dest,data):#el data que recibe tiene que ser un string , el host que se recibe es un dispositivo
      d = Frame.hex_bin(data)
      self.mac_destino = mac_dest
      self.data = data
      self.mac_origen = self.Mac_Origen(host) 
      self.size = self.bin_dec(d[0:8])
      self.size_dato_veri = self.bin_dec(d[8:16])
      self.dato = d[16:16+self.size]
      self.dato_veri =d[16+self.size:16+self.size+self.size_dato_veri] 
      
      
    def Mac_Origen(host): #el host que recibe tiene que ser el dispositivo
        return  structs.Host(host).mac
    
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
        mac = Frame.hex_bin(mac_destino) 
        for i in mac:
            if i != '1':
                return False
        return True
    
    def size (d):
        a = d[0:8] #Primeros 8 bits

        return Frame.bin_dec(a)
    
    def veri_data (d):
        a = d[8:16] #Proximo 8 bits
        return Frame.bin_dec(a)