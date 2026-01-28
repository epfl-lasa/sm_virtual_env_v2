# Virtual Environment for the Multi-Limb Coordination Study
Project: [4-arms manipulation through supernumerary robotic manipulation: a study of multi-limb coordination](https://www.epfl.ch/labs/lasa/4hands/) 

## Requirements
Make sure you have **Python 3.12** installed. The following Python packages are required:
- [PyGame](https://www.pygame.org/)
- [NumPy](https://numpy.org/)
- [imageio](https://imageio.readthedocs.io/)
- [SciPy](https://www.scipy.org/)

Additionally, you need a local network, using a switch, with ideally three computers. Two of these should run Microsoft Windows. Each Windows machine should have an OptiTrack V120 Trio connected. The last PC in this project, is running Ubuntu, a GNU/Linux operating system.

On these Windows machines, you should install the Motive software, which receives data from the OptiTrack cameras and transmits it over the network. You can configure the IP addresses and other network settings directly within the Motive software.

The third computer acts as the client: it receives the motion capture data from the two Windows machines and uses it to control objects in the virtual environment.

You can find the defined IP addresses and ports used in this project in the file: motive/defs_udp.py.


## Attention 
The `NatNetPythonClient` is used to read data remotely from the Motive software.  
It is distributed under the following license: [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0).

## Set-up
First, define **marker sets** for each OptiTrack machine:  

- **Two marker sets** for tracking the **feet**  
- **Two marker sets** for tracking the **hands**  

In the Motive software, assign the following IDs to each marker set for mapping (this will be used in the third PC to get the values):

```python
INTERFACES = [
    {"name": "left_hand", "udp_id": 1},
    {"name": "right_hand", "udp_id": 2},
    {"name": "left_foot", "udp_id": 3},
    {"name": "right_foot", "udp_id": 4}
]
```

After setting up the marker sets, verify their quality in the Motive software. You can adjust their poses, calibrate them, and make other necessary refinements to ensure accurate tracking.

Next, on the third PC, ensure it is connected to the OptiTrack systems. You can test the connection using the `ping` command to verify network communication.

## Running the Scripts

Now, open **three terminals** and run the following scripts:

```bash
python motive/interface_motive_feet.py
python motive/interface_motive_hands.py
python main.py
```

## Logs
All log data is saved in the `logs` directory, created using `ensure_dir("logs")` in the `main.py`.  

