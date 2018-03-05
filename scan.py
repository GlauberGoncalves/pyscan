from Ip import *
from Ping import *

ip = Ip("192.168.0.1/254")

lista = ping_range_thread(ip.lista_de_ips)

print( ip.ordenaListaIps( lista ) )
# ping_range(ip.lista_de_ips)

# if ( quiet_ping("192.168.0.1", 2000, 4) ):
#     print("Online")
# else :
#     print("off line")
