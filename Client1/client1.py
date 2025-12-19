import socket

# Error Detection Methods Implementation

def calculate_parity_bit(data, parity_type='even'):
    """
    Calculate parity bit for the data.
    parity_type: 'even' or 'odd'
    Returns: '0' or '1'
    """
    binary_data = ''.join(format(ord(c), '08b') for c in data)
    count_ones = binary_data.count('1')
    
    if parity_type == 'even':
        return '0' if count_ones % 2 == 0 else '1'
    else:  # odd
        return '1' if count_ones % 2 == 0 else '0'

def calculate_2d_parity(data):
    """
    Calculate 2D Parity (Matrix Parity).
    Splits data into 8x8 matrix and calculates row and column parities.
    Returns: hex string of row and column parities
    """
    # Convert to binary
    binary_data = ''.join(format(ord(c), '08b') for c in data)
    
    # Pad to multiple of 8 bits
    while len(binary_data) % 8 != 0:
        binary_data += '0'
    
    # Create 8x8 matrix (or closest square)
    matrix_size = 8
    rows = []
    for i in range(0, len(binary_data), matrix_size):
        row = binary_data[i:i+matrix_size]
        if len(row) < matrix_size:
            row += '0' * (matrix_size - len(row))
        rows.append(row)
    
    # Pad rows to 8 rows
    while len(rows) < matrix_size:
        rows.append('0' * matrix_size)
    rows = rows[:matrix_size]  # Take first 8 rows
    
    # Calculate row parities
    row_parities = []
    for row in rows:
        count = row.count('1')
        row_parities.append('1' if count % 2 == 1 else '0')
    
    # Calculate column parities
    col_parities = []
    for col in range(matrix_size):
        count = sum(1 for row in rows if row[col] == '1')
        col_parities.append('1' if count % 2 == 1 else '0')
    
    # Combine row and column parities
    all_parities = ''.join(row_parities) + ''.join(col_parities)
    
    # Convert to hex
    parity_hex = hex(int(all_parities, 2))[2:].upper()
    return parity_hex

def calculate_crc(data, crc_type='CRC16'):
    """
    Calculate CRC (Cyclic Redundancy Check).
    crc_type: 'CRC8', 'CRC16', or 'CRC32'
    Returns: hex string of CRC value
    """
    import zlib
    
    data_bytes = data.encode('utf-8')
    
    if crc_type == 'CRC32':
        crc = zlib.crc32(data_bytes) & 0xFFFFFFFF
        return format(crc, '08X')
    elif crc_type == 'CRC16':
        # CRC-16-CCITT (polynomial 0x1021)
        crc = 0xFFFF
        poly = 0x1021
        for byte in data_bytes:
            crc ^= (byte << 8)
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
                crc &= 0xFFFF
        return format(crc, '04X')
    else:  # CRC8
        # CRC-8 (polynomial 0x07)
        crc = 0
        poly = 0x07
        for byte in data_bytes:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ poly
                else:
                    crc <<= 1
                crc &= 0xFF
        return format(crc, '02X')

def calculate_hamming_code(data):
    """
    Calculate Hamming Code for data.
    Uses Hamming(7,4) for every 4 bits.
    Returns: hex string of check bits
    """
    # Convert to binary
    binary_data = ''.join(format(ord(c), '08b') for c in data)
    
    # Process in 4-bit blocks
    hamming_bits = []
    
    for i in range(0, len(binary_data), 4):
        block = binary_data[i:i+4]
        if len(block) < 4:
            block += '0' * (4 - len(block))
        
        # Hamming(7,4): positions 1,2,3,4 are data, 5,6,7 are check bits
        d1, d2, d3, d4 = map(int, block)
        
        # Calculate check bits
        p1 = d1 ^ d2 ^ d4  # Parity for positions 1,2,4
        p2 = d1 ^ d3 ^ d4  # Parity for positions 1,3,4
        p3 = d2 ^ d3 ^ d4  # Parity for positions 2,3,4
        
        hamming_bits.extend([str(p1), str(p2), str(p3)])
    
    # Convert to hex
    hamming_str = ''.join(hamming_bits)
    # Pad to multiple of 4 bits
    while len(hamming_str) % 4 != 0:
        hamming_str += '0'
    
    hamming_hex = hex(int(hamming_str, 2))[2:].upper()
    return hamming_hex

def calculate_checksum(data):
    """
    Calculate Internet Checksum (IP Checksum).
    Returns: hex string of checksum
    """
    # Convert to bytes
    data_bytes = data.encode('utf-8')
    
    # Pad to even number of bytes
    if len(data_bytes) % 2 == 1:
        data_bytes += b'\x00'
    
    # Sum all 16-bit words
    checksum = 0
    for i in range(0, len(data_bytes), 2):
        word = (data_bytes[i] << 8) + data_bytes[i+1]
        checksum += word
    
    # Add carry bits
    while checksum >> 16:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    
    # One's complement
    checksum = ~checksum & 0xFFFF
    
    return format(checksum, '04X')

def generate_control_info(data, method):
    """
    Generate control information based on the selected method.
    """
    method_upper = method.upper()
    
    if method_upper == 'PARITY' or method_upper == 'PARITY_EVEN':
        return calculate_parity_bit(data, 'even')
    elif method_upper == 'PARITY_ODD':
        return calculate_parity_bit(data, 'odd')
    elif method_upper == '2D_PARITY' or method_upper == '2DPARITY':
        return calculate_2d_parity(data)
    elif method_upper.startswith('CRC'):
        crc_type = method_upper if method_upper in ['CRC8', 'CRC16', 'CRC32'] else 'CRC16'
        return calculate_crc(data, crc_type)
    elif method_upper == 'HAMMING':
        return calculate_hamming_code(data)
    elif method_upper == 'CHECKSUM' or method_upper == 'IP_CHECKSUM':
        return calculate_checksum(data)
    else:
        return calculate_crc(data, 'CRC16')  # Default

def main():
    # Server configuration
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 8000
    
    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to server
        print("Connecting to server...")
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connected to server!\n")
        
        # Get user input
        while True:
            data = input("Enter text to send: ")
            if '|' in data:
                print("Error: Character '|' is not allowed in the data. Please try again.")
            else:
                break
        
        # Select error detection method
        print("\nSelect error detection method:")
        print("1. Parity (Even)")
        print("2. Parity (Odd)")
        print("3. 2D Parity")
        print("4. CRC-8")
        print("5. CRC-16")
        print("6. CRC-32")
        print("7. Hamming Code")
        print("8. Internet Checksum")
        
        choice = input("Enter choice (1-8): ").strip()
        
        method_map = {
            '1': 'PARITY_EVEN',
            '2': 'PARITY_ODD',
            '3': '2D_PARITY',
            '4': 'CRC8',
            '5': 'CRC16',
            '6': 'CRC32',
            '7': 'HAMMING',
            '8': 'CHECKSUM'
        }
        
        method = method_map.get(choice, 'CRC16')
        
        # Generate control information
        control_info = generate_control_info(data, method)
        
        # Create packet: DATA|METHOD|CONTROL_INFORMATION
        packet = f"{data}|{method}|{control_info}"
        
        print(f"\nGenerated Packet: {packet}")
        print(f"Data: {data}")
        print(f"Method: {method}")
        print(f"Control Information: {control_info}\n")
        
        # Send packet to server
        client_socket.send(packet.encode('utf-8'))
        print("Packet sent to server!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()

