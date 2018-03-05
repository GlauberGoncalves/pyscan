import socket

class MyStats:
    thisIP   = "0.0.0.0"
    pktsSent = 0
    pktsRcvd = 0
    minTime  = 999999999
    maxTime  = 0
    totTime  = 0
    avrgTime = 0
    fracLoss = 1.0

#=============================================================================#
def do_one(myStats, destIP, hostname, timeout, mySeqNumber, packet_size, quiet = False):
    """
    Returns either the delay (in ms) or None on timeout.
    """
    delay = None

    try: # One could use UDP here, but it's obscure
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    except socket.error as e:
        print("failed. (socket error: '%s')" % e.args[1])
        raise # raise the original error

    my_ID = os.getpid() & 0xFFFF

    sentTime = send_one_ping(mySocket, destIP, my_ID, mySeqNumber, packet_size)
    if sentTime == None:
        mySocket.close()
        return delay

    myStats.pktsSent += 1

    recvTime, dataSize, iphSrcIP, icmpSeqNumber, iphTTL = receive_one_ping(mySocket, my_ID, timeout)

    mySocket.close()

    if recvTime:
        delay = (recvTime-sentTime)*1000
        if not quiet:
            print("%d bytes from %s: icmp_seq=%d ttl=%d time=%d ms" % (
                dataSize, socket.inet_ntoa(struct.pack("!I", iphSrcIP)), icmpSeqNumber, iphTTL, delay)
            )
        myStats.pktsRcvd += 1
        myStats.totTime += delay
        if myStats.minTime > delay:
            myStats.minTime = delay
        if myStats.maxTime < delay:
            myStats.maxTime = delay
    else:
        delay = None
        # print("Request timed out.")

    return delay

#=============================================================================#
def quiet_ping(hostname, timeout, count,
               packet_size, path_finder):
    """
    Same as verbose_ping, but the results are returned as tuple
    """
        
    myStats = MyStats() # Reset the stats
    mySeqNumber = 0 # Starting value

    try:
        destIP = socket.gethostbyname(hostname)
    except socket.gaierror as e:
        return False

    myStats.thisIP = destIP

    # This will send packet that we dont care about 0.5 seconds before it starts
    # acrutally pinging. This is needed in big MAN/LAN networks where you sometimes
    # loose the first packet. (while the switches find the way... :/ )
    if path_finder:
        fakeStats = MyStats()
        do_one(fakeStats, destIP, hostname, timeout,
                        mySeqNumber, packet_size, quiet=True)
        time.sleep(0.5)

    for i in range(count):
        delay = do_one(myStats, destIP, hostname, timeout,
                        mySeqNumber, packet_size, quiet=True)

        if delay == None:
            delay = 0

        mySeqNumber += 1

        # Pause for the remainder of the MAX_SLEEP period (if applicable)
        # if (MAX_SLEEP > delay):
        #     time.sleep((MAX_SLEEP - delay)/1000)

    if myStats.pktsSent > 0:
        myStats.fracLoss = (myStats.pktsSent - myStats.pktsRcvd)/myStats.pktsSent
    if myStats.pktsRcvd > 0:
        myStats.avrgTime = myStats.totTime / myStats.pktsRcvd

    # return tuple(max_rtt, min_rtt, avrg_rtt, percent_lost)
    # return myStats.maxTime, myStats.minTime, myStats.avrgTime, myStats.fracLoss
    if(myStats.maxTime):
        print("ip {} online".format(hostname))
    return myStats.maxTime

print(quiet_ping("192.168.0.1",2000, 2))