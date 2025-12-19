Data Transmission with Error Detection Methods
===============================================

HOW TO RUN THE PROJECT
----------------------

This project requires 3 terminal windows. Start them in this order:

1. Start the Server:
   cd Server
   python server.py

2. Start Client 2 (Receiver):
   cd Client2
   python client2.py

3. Start Client 1 (Data Sender):
   cd Client1
   python client1.py

IMPORTANT: Start in this order - Server first, then Client 2, then Client 1.

PROJECT STRUCTURE
-----------------

Client1/client1.py  - Data sender with error detection methods
Server/server.py    - Data corruptor with error injection methods
Client2/client2.py  - Receiver with error detection and reporting

ERROR DETECTION METHODS (Client 1)
----------------------------------
1. Parity (Even)
2. Parity (Odd)
3. 2D Parity
4. CRC-8
5. CRC-16
6. CRC-32
7. Hamming Code
8. Internet Checksum

ERROR INJECTION METHODS (Server)
--------------------------------
1. Bit Flip
2. Character Substitution
3. Character Deletion
4. Character Insertion
5. Character Swapping
6. Multiple Bit Flips
7. Burst Error
8. Random (Auto)

PACKET FORMAT
-------------
DATA|METHOD|CONTROL_INFORMATION

Example: HELLO|CRC16|87AF

REQUIREMENTS
-----------
- Python 3.x
- No external dependencies (uses only standard library)

