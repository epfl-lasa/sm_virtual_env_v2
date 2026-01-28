HOME = "127.0.0.1"

# Fixed motion capture system
FIXED_MOCAP_IP_LOCAL = "192.168.131.103"
FIXED_MOCAP_IP_REMOTE_HANDS = "192.168.131.102"
FIXED_MOCAP_IP_REMOTE_FEET = "192.168.131.101"

# when receives data from hand interfaces, this UDP info is used to send data to another script
UDP_IP = HOME
UDP_PORT_HANDS = 5005
UDP_PORT_FEET = 5007

# in case of using the pedal interface
PEDAL_IP_LOCAL = "10.42.0.1"
PEDAL_IP_REMOTE = None # not used for now!
PEDAL_IP_LOCAL_PORT = 5009

# when receives data from foot interfaces, this UDP info is used to send data to another script
FEET_UDP_IP = HOME
FEET_UDP_PORT = 5025