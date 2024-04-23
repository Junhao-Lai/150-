
# Final Skeleton
#
# Hints/Reminders from Lab 3:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip = packet.find('ipv4')
#
# if ip.srcip == "1.1.1.1":
#     print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
# 
# To accept an OpenFlow Message telling a switch to accept packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should accept the packets out:
#
#        msg = of.ofp_flow_mod()
#        msg.match = of.ofp_match.from_packet(packet)
#        msg.idle_timeout = 30
#        msg.hard_timeout = 30
#
#        msg.actions.append(of.ofp_action_output(port = <PORT>))
#        msg.data = packet_in
#        self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
    """
    A Firewall object is created for each switch that connects.
    A Connection object for that switch is passed to the __init__ function.
    """
    def __init__ (self, connection):
        # Keep track of the connection to the switch so that we can
        # accept it messages!
        self.connection = connection

        # This binds our PacketIn event listener
        connection.addListeners(self)




    def do_final (self, packet, packet_in, port_on_switch, switch_id):
        # This is where you'll put your code. The following modifications have 
        # been made from Lab 3:
        #     - port_on_switch: represents the port that the packet was received on.
        #     - switch_id represents the id of the switch that received the packet.
        #            (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
        # You should use these to determine where a packet came from. To figure out where a packet 
        # is going, you can use the IP header information.

        def accept(port_num):
          msg = of.ofp_flow_mod()
          msg.match = of.ofp_match.from_packet(packet)
          msg.data = packet_in
          msg.priority = 1
          msg.idle_timeout = 30
          msg.hard_timeout = 30
          msg.buffer_id = packet_in.buffer_id
          msg.actions.append(of.ofp_action_output(port = port_num))
          self.connection.send(msg)

        ip  = packet.find('ipv4')
        icmp_packet = packet.find('icmp')
        arp_packet = packet.find('arp')


        # if arp_packet:
        #   return

        if ip:
          print("This is ip")
        elif icmp_packet:
          print("icmp_packet")
        elif arp_packet:
          print("this is arp")
        
        print("/////////////////////")
        if ip is None:
          msg = of.ofp_flow_mod() #define a openflow entry
          msg.match = of.ofp_match.from_packet(packet)
          msg.data = packet_in
          msg.idle_timeout = 30
          msg.hard_timeout = 30
          msg.buffer_id = packet_in.buffer_id
          msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD)) # ACTION FLOOD (accept the packet)
          self.connection.send(msg)
          return

        if ip: 
            print("This is the IP traffing \n")

            A = ["10.1.1.10","10.1.2.20","10.1.3.30","10.1.4.40"]
            B = ["10.2.5.50","10.2.6.60","10.2.7.70","10.2.8.80"]

            if switch_id == 1: #core switch
                print("Core switch!!\n")
                print(ip.srcip)
                print(ip.dstip)
                if ip.dstip == "10.3.9.90":
                  accept(10)
                elif ip.dstip == "108.24.31.112":
                  accept(6)
                elif ip.dstip == "106.44.82.103":
                  accept(7)  
                elif ip.srcip == "106.44.82.103":
                  print("from untrust dropped")
                  self.drop(packet,packet_in)

                elif ip.srcip == "108.24.31.112" and (ip.dstip in B): # add serveer later
                       print("from trust no send to B or server")
                       self.drop(packet,packet_in)

                elif (ip.srcip in A) and (ip.dstip in B):
                      print("A can't send to B")
                      self.drop(packet,packet_in)
  
              #  elif ip.dstip == "10.3.9.90":
              #       accept(10) 


                elif ip.dstip == "10.1.1.10" or ip.dstip == "10.1.2.20":
                  print("via s3 out from port 4\n")
                  accept(4)
                elif ip.dstip == "10.1.3.30" or ip.dstip == "10.1.4.40":
                  print("via s4\n")
                  accept(5)
                elif ip.dstip == "10.2.5.50" or ip.dstip == "10.2.6.60":
                  print("via s6\n")
                  accept(9)
                elif ip.dstip == "10.2.7.70" or ip.dstip == "10.2.8.80":
                  print("via s5\n")
                  accept(8)

              #  elif ip.dstip == "10.3.9.90":
              #       accept(10)

            elif switch_id == 2:
              # print("")
                print("Data center Switch")
                print(ip.srcip)
                print(ip.dstip)
               # if ip.srcip == "10.3.9.90":


                if ip.dstip == "10.3.9.90":
                    accept(9)
                elif ip.dstip == "108.24.31.112" or ip.dstip == "106.44.82.103" or ip.srcip == "108.24.31.112" or ip.srcip == "106.44": 
                  print("server to trust/untrust dropped || untrust/trust to server dropped")
                  self.drop(packet,packet_in)

    
            
            #    elif ip.srcip == ""

                else:
                    print("to core")
                    accept(3)

            elif switch_id == 3:
                #print("dongjing \n")

                print("Floor 1 Switch 1")
                print(ip.srcip)
                print(ip.dstip)
                if ip.dstip == "10.1.1.10":
                    accept(2)
                elif ip.dstip == "10.1.2.20":
                    accept(3)
                else:
                    accept(1)

            elif switch_id == 4:
                print("Floor 1 Switch 2\n")
                print(ip.srcip)
                print(ip.dstip)
                if ip.dstip == "10.1.3.30":
                    accept(2)
                elif ip.dstip == "10.1.4.40":
                    accept(3)
                else:
                    accept(1)

            elif switch_id == 5:
                print("Floor 2 Switch 2\n")
                print(ip.srcip)
                print(ip.dstip)
                if ip.dstip == "10.2.7.70":
                    accept(2)
                elif ip.dstip == "10.2.8.80":
                    accept(3)
                else:
                    accept(1)


            elif switch_id == 6:
                print("Floor 2 Switch 1\n")
                print(ip.srcip)
                print(ip.dstip)
                if ip.dstip == "10.2.5.50":
                    accept(2)
                elif ip.dstip == "10.2.6.60":
                    accept(3)
                else:
                    accept(1)
        else:
          msg = of.ofp_flow_mod() #define a openflow entry
          msg.match = of.ofp_match.from_packet(packet)
          msg.data = packet_in
          msg.idle_timeout = 30
          msg.hard_timeout = 30
          msg.buffer_id = packet_in.buffer_id
          msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD)) # ACTION FLOOD (accept the packet)
          self.connection.send(msg)
                    



    def drop(self, packet, packet_in):
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.idle_timeout = 30
      msg.hard_timeout = 30
      msg.buffer_id = packet_in.buffer_id
      self.connection.send(msg)




    print("Welcome Junhao Lai!!!\n")


                

    def _handle_PacketIn (self, event):
        """
        Handles packet in messages from the switch.
        """
        packet = event.parsed # This is the parsed packet data.
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        packet_in = event.ofp # The actual ofp_packet_in message.
        self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
    """
    Starts the component
    """
    def start_switch (event):
        log.debug("Controlling %s" % (event.connection,))
        Final(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
