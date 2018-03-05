from Ip import *
from Ping import *

ip = Ip("192.168.0.1/60")

if ( quiet_ping("192.168.0.1", 2000, 4) ):
    print("Online")
else :
    print("off line")
