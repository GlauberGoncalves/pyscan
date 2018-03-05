import string
from operator import itemgetter, attrgetter

class Ip:    
    def __init__(self, range_ip):
        self.ip = range_ip
        self.lista_de_ips = []

        self.geraListaDeIps()


    def geraListaDeIps(self):
        faixas = self.ip.split(".")
        if( faixas[3].find("/") > 0 ):
            aux    = faixas[3].split("/")
            inicio = int( aux[0] )
            fim    = int( aux[1] )

            prefixo_ip = "{}.{}.{}.".format(faixas[0], faixas[1], faixas[2])
            self.lista_de_ips = [(prefixo_ip + str(i)) for i in range(inicio, fim + 1)]
        else:
            self.lista_de_ips = ["{}.{}.{}.{}".format(faixas[0],faixas[1],faixas[2],faixas[3])]
    
    def ordenaListaIps(self, lista_ips):
        lista_ordenada = []
        aux = []
        
        for ip in lista_ips:
            aux.append( [ip, ( int( ip.split(".")[3] ) ) ] )

        lista_ordenada = sorted(aux, key=itemgetter(1))
        # print( lista_ordenada )
        return [ ip[0] for ip in lista_ordenada ]
        # return [ ip[0] for ip in lista_ordenada)]



            
