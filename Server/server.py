import socket
import random
import threading

# Error Injection Methods Implementation

def bit_flip(data):
    """Flip a random bit in the binary representation of the data."""
    if not data:
        return data
    
    # Convert to binary
    binary_list = []
    for char in data:
        binary_list.extend(list(format(ord(char), '08b')))
    
    # Flip a random bit
    if binary_list:
        flip_index = random.randint(0, len(binary_list) - 1)
        binary_list[flip_index] = '1' if binary_list[flip_index] == '0' else '0'
    
    # Convert back to string
    result = []
    for i in range(0, len(binary_list), 8):
        byte_bits = binary_list[i:i+8]
        if len(byte_bits) == 8:
            char_code = int(''.join(byte_bits), 2)
            result.append(chr(char_code))
    
    return ''.join(result)

def character_substitution(data):
    """Replace a random character with another random character."""
    if not data:
        return data
    
    index = random.randint(0, len(data) - 1)
    # Replace with random printable ASCII character
    new_char = chr(random.randint(32, 126))
    return data[:index] + new_char + data[index+1:]

def character_deletion(data):
    """Remove a random character from the data."""
    if not data:
        return data
    
    index = random.randint(0, len(data) - 1)
    return data[:index] + data[index+1:]

def character_insertion(data):
    """Insert a random character into the middle of the data."""
    if not data:
        return chr(random.randint(32, 126))
    
    index = random.randint(0, len(data))
    new_char = chr(random.randint(32, 126))
    return data[:index] + new_char + data[index:]

def character_swapping(data):
    """Swap two adjacent characters."""
    if len(data) < 2:
        return data
    
    index = random.randint(0, len(data) - 2)
    chars = list(data)
    chars[index], chars[index + 1] = chars[index + 1], chars[index]
    return ''.join(chars)

def multiple_bit_flips(data):
    """Flip multiple random bits."""
    if not data:
        return data
    
    # Convert to binary
    binary_list = []
    for char in data:
        binary_list.extend(list(format(ord(char), '08b')))
    
    # Flip 2-5 random bits
    num_flips = random.randint(2, min(5, len(binary_list)))
    flip_indices = random.sample(range(len(binary_list)), num_flips)
    
    for idx in flip_indices:
        binary_list[idx] = '1' if binary_list[idx] == '0' else '0'
    
    # Convert back to string
    result = []
    for i in range(0, len(binary_list), 8):
        byte_bits = binary_list[i:i+8]
        if len(byte_bits) == 8:
            char_code = int(''.join(byte_bits), 2)
            result.append(chr(char_code))
    
    return ''.join(result)

def burst_error(data):
    """Corrupt a sequence of 3-8 consecutive characters."""
    if len(data) < 3:
        return data
    
    burst_length = random.randint(3, min(8, len(data)))
    start_index = random.randint(0, len(data) - burst_length)
    
    # Corrupt the burst by replacing with random characters
    corrupted = list(data)
    for i in range(start_index, start_index + burst_length):
        corrupted[i] = chr(random.randint(32, 126))
    
    return ''.join(corrupted)

def inject_error(data, error_method=None):
    """
    Inject error into data using the specified method.
    If method is None, randomly selects one.
    """
    methods = [
        bit_flip,
        character_substitution,
        character_deletion,
        character_insertion,
        character_swapping,
        multiple_bit_flips,
        burst_error
    ]
    
    if error_method is None:
        method = random.choice(methods)
    else:
        method_map = {
            'bit_flip': bit_flip,
            'substitution': character_substitution,
            'deletion': character_deletion,
            'insertion': character_insertion,
            'swapping': character_swapping,
            'multiple_flips': multiple_bit_flips,
            'burst': burst_error
        }
        method = method_map.get(error_method.lower(), random.choice(methods))
    
    return method(data)

def handle_client1(client1_socket, client2_socket):
    """Handle communication from Client 1 and forward to Client 2."""
    try:
        # Receive packet from Client 1
        packet = client1_socket.recv(8192).decode('utf-8')
        print(f"Received from Client 1: {packet}")
        
        # Parse packet: DATA|METHOD|CONTROL_INFORMATION
        parts = packet.split('|')
        if len(parts) != 3:
            print("Invalid packet format!")
            return
        
        data, method, control_info = parts
        print(f"Original Data: {data}")
        print(f"Method: {method}")
        print(f"Control Info: {control_info}")
        
        # Inject error
        print("\nSelect error injection method:")
        print("1. Bit Flip")
        print("2. Character Substitution")
        print("3. Character Deletion")
        print("4. Character Insertion")
        print("5. Character Swapping")
        print("6. Multiple Bit Flips")
        print("7. Burst Error")
        print("8. Random (Auto)")
        
        choice = input("Enter choice (1-8, default 8): ").strip() or '8'
        
        error_method_map = {
            '1': 'bit_flip',
            '2': 'substitution',
            '3': 'deletion',
            '4': 'insertion',
            '5': 'swapping',
            '6': 'multiple_flips',
            '7': 'burst',
            '8': None
        }
        
        selected_error = error_method_map.get(choice, None)
        corrupted_data = inject_error(data, selected_error)
        
        print(f"\nCorrupted Data: {corrupted_data}")
        
        # Create corrupted packet: DATA|METHOD|CONTROL_INFORMATION
        corrupted_packet = f"{corrupted_data}|{method}|{control_info}"
        
        # Forward to Client 2
        if client2_socket:
            client2_socket.send(corrupted_packet.encode('utf-8'))
            print(f"Forwarded to Client 2: {corrupted_packet}")
        else:
            print("Client 2 not connected!")
            
    except Exception as e:
        print(f"Error handling Client 1: {e}")
    finally:
        client1_socket.close()

client2_socket = None
client2_lock = threading.Lock()

def wait_for_client2():
    """Wait for Client 2 to connect in a separate thread."""
    global client2_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", 8001))
    server_socket.listen(5)
    
    while True:
        try:
            print("Waiting for Client 2 to connect on port 8001...")
            sock, addr = server_socket.accept()
            with client2_lock:
                global client2_socket
                if client2_socket:
                    client2_socket.close()
                client2_socket = sock
            print(f"Client 2 connected from {addr}")
        except Exception as e:
            print(f"Error accepting Client 2: {e}")
            break

def main():
    global client2_socket
    SERVER_IP = "127.0.0.1"
    CLIENT1_PORT = 8000  # Port for Client 1
    CLIENT2_PORT = 8001  # Port for Client 2
    
    # Socket for Client 1
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_IP, CLIENT1_PORT))
    server_socket.listen(5)
    
    print("=" * 50)
    print("Data Corruptor Server")
    print("=" * 50)
    print(f"Listening for Client 1 on port {CLIENT1_PORT}...")
    print(f"Listening for Client 2 on port {CLIENT2_PORT}...")
    print("=" * 50)
    print("NOTE: Start Client 2 first, then Client 1")
    print("=" * 50)
    
    # Start thread to wait for Client 2
    client2_thread = threading.Thread(target=wait_for_client2, daemon=True)
    client2_thread.start()
    
    while True:
        try:
            # Accept Client 1 connection
            print(f"\nWaiting for Client 1 on port {CLIENT1_PORT}...")
            client1_socket, addr = server_socket.accept()
            print(f"Client 1 connected from {addr}")
            
            # Wait a bit for Client 2 if not connected
            if client2_socket is None:
                print("Warning: Client 2 not connected yet. Waiting...")
                import time
                for i in range(10):  # Wait up to 10 seconds
                    time.sleep(1)
                    with client2_lock:
                        if client2_socket:
                            break
                    print(".", end="", flush=True)
                print()
            
            # Handle Client 1 in a thread
            with client2_lock:
                current_client2 = client2_socket
            thread = threading.Thread(
                target=handle_client1,
                args=(client1_socket, current_client2)
            )
            thread.start()
            
        except KeyboardInterrupt:
            print("\nShutting down server...")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    server_socket.close()
    with client2_lock:
        if client2_socket:
            client2_socket.close()

if __name__ == "__main__":
    main()

