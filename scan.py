from Ip import *
from Ping import *
import sys
import argparse
#  testes
# ip = Ip("192.168.137.1/254")

# lista = ping_range_thread(ip.lista_de_ips)

# print( ip.ordenaListaIps( lista ) )

def main():
    print("#############################################")
    print("\n\nAnalisando ips... Aguarde um momento\n\n")
    print("#############################################\n\n")
        
    parser = argparse.ArgumentParser(description='range de ips')  # (1)
    parser.add_argument('--h')  #(2)     
    args = parser.parse_args() #(3)
    
    ip = Ip(str(args.h))
    lista = ping_range_thread( ip.lista_de_ips )

    
    for ip in  ip.ordenaListaIps( lista ):
        print("- {} online".format(ip))
    
if (__name__ == '__main__'):
    main()
    