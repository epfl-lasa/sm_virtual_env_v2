# Copyright © 2018 Naturalpoint
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# OptiTrack NatNet direct depacketization sample for Python 3.x
#
# Uses the Python NatNetClient.py library to establish a connection (by creating a NatNetClient),
# and receive data via a NatNet connection and decode it using the NatNetClient library.

from NatNetPythonClient.NatNetClient import *
import sys
import time
import socket
import threading
import queue

from defs_udp import *

queue = queue.Queue()


def handle_exit(signum, frame):
    print("\nExecution stopped by user.")
    exit(0)


def receive_new_frame(data_dict):
    order_list = [
        "frameNumber",
        "markerSetCount",
        "unlabeledMarkersCount",
        "rigidBodyCount",
        "skeletonCount",
        "labeledMarkerCount",
        "timecode",
        "timecodeSub",
        "timestamp",
        "isRecording",
        "trackedModelsChanged",
    ]
    dump_args = False
    if dump_args == True:
        out_string = "    "
        for key in data_dict:
            out_string += key + "="
            if key in data_dict:
                out_string += data_dict[key] + " "
            out_string += "/"
        print(out_string)


def udp_client(queue):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        while True:
            if not queue.empty():
                message = queue.get()
                client_socket.sendto(message.encode(), (UDP_IP, UDP_PORT_FEET))


def receive_rigid_body_frame(new_id, position, rotation):
    queue.put(f"{new_id}:{position}:{rotation}")


def my_parse_args(arg_list, args_dict):
    # set up base values
    arg_list_len = len(arg_list)
    if arg_list_len > 1:
        args_dict["serverAddress"] = arg_list[1]
        if arg_list_len > 2:
            args_dict["clientAddress"] = arg_list[2]
        if arg_list_len > 3:
            if len(arg_list[3]):
                args_dict["use_multicast"] = True
                if arg_list[3][0].upper() == "U":
                    args_dict["use_multicast"] = False
    return args_dict


if __name__ == "__main__":

    client_thread = threading.Thread(target=udp_client, args=(queue,), daemon=True)
    client_thread.start()

    optionsDict = {}
    optionsDict["clientAddress"] = FIXED_MOCAP_IP_LOCAL
    optionsDict["serverAddress"] = FIXED_MOCAP_IP_REMOTE_FEET
    optionsDict["use_multicast"] = False

    optionsDict = my_parse_args(sys.argv, optionsDict)

    streaming_client = NatNetClient()
    streaming_client.set_client_address(optionsDict["clientAddress"])
    streaming_client.set_server_address(optionsDict["serverAddress"])
    streaming_client.set_use_multicast(optionsDict["use_multicast"])
    streaming_client.new_frame_listener = receive_new_frame
    streaming_client.rigid_body_listener = receive_rigid_body_frame

    if not streaming_client.run():
        print("ERROR: Could not start streaming client.")
        try:
            sys.exit(1)
        except SystemExit:
            print("...")
        finally:
            print("Exiting...")

    is_looping = True

    time.sleep(1)

    if streaming_client.connected() is False:
        print("ERROR: Could not connect properly. Check that Motive streaming is on.")
        try:
            sys.exit(2)
        except SystemExit:
            print("...")
        finally:
            print("Exiting...")

    while is_looping:
        time.sleep(1.0 / 120.0)

    client_thread.join()
