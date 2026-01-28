# Virtual Environment for the Multi-Limb Coordination Study
Project: [4-arms manipulation through supernumerary robotic manipulation: a study of multi-limb coordination](https://www.epfl.ch/labs/lasa/4hands/) 

## Requirements
Make sure you have **Python 3.12** installed. The following Python packages are required:
- [PyGame](https://www.pygame.org/)
- [NumPy](https://numpy.org/)
- [imageio](https://imageio.readthedocs.io/)
- [SciPy](https://www.scipy.org/)

Additionally, you need a local network, using a switch, with ideally three computers. Two of these should run Microsoft Windows. Each Windows machine should have an OptiTrack V120 Trio connected.

On these Windows machines, you should install the Motive software, which receives data from the OptiTrack cameras and transmits it over the network. You can configure the IP addresses and other network settings directly within the Motive software.

The third computer acts as the client: it receives the motion capture data from the two Windows machines and uses it to control objects in the virtual environment.

You can find the defined IP addresses and ports used in this project in the file: motive/defs_udp.py.
