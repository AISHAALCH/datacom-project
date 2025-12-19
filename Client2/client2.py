import socket

# Import error detection methods (same as Client 1)
def calculate_parity_bit(data, parity_type='even'):
    """Calculate parity bit for the data."""
    binary_data = ''.join(format(ord(c), '08b') for c in data)
    count_ones = binary_data.count('1')
    
    if parity_type == 'even':
        return '0' if count_ones % 2 == 0 else '1'
    else:  # odd
        return '1' if count_ones % 2 == 0 else '0'

def calculate_2d_parity(data):
    """Calculate 2D Parity (Matrix Parity)."""
    binary_data = ''.join(format(ord(c), '08b') for c in data)
    
    while len(binary_data) % 8 != 0:
        binary_data += '0'
    
    matrix_size = 8
    rows = []
    for i in range(0, len(binary_data), matrix_size):
        row = binary_data[i:i+matrix_size]
        if len(row) < matrix_size:
            row += '0' * (matrix_size - len(row))
        rows.append(row)
    
    while len(rows) < matrix_size:
        rows.append('0' * matrix_size)
    rows = rows[:matrix_size]
    
    row_parities = []
    for row in rows:
        count = row.count('1')
        row_parities.append('1' if count % 2 == 1 else '0')
    
    col_parities = []
    for col in range(matrix_size):
        count = sum(1 for row in rows if row[col] == '1')
        col_parities.append('1' if count % 2 == 1 else '0')
    
    all_parities = ''.join(row_parities) + ''.join(col_parities)
    parity_hex = hex(int(all_parities, 2))[2:].upper()
    return parity_hex

def calculate_crc(data, crc_type='CRC16'):
    """Calculate CRC (Cyclic Redundancy Check)."""
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
    """Calculate Hamming Code for data."""
    binary_data = ''.join(format(ord(c), '08b') for c in data)
    
    hamming_bits = []
    
    for i in range(0, len(binary_data), 4):
        block = binary_data[i:i+4]
        if len(block) < 4:
            block += '0' * (4 - len(block))
        
        d1, d2, d3, d4 = map(int, block)
        
        p1 = d1 ^ d2 ^ d4
        p2 = d1 ^ d3 ^ d4
        p3 = d2 ^ d3 ^ d4
        
        hamming_bits.extend([str(p1), str(p2), str(p3)])
    
    hamming_str = ''.join(hamming_bits)
    while len(hamming_str) % 4 != 0:
        hamming_str += '0'
    
    hamming_hex = hex(int(hamming_str, 2))[2:].upper()
    return hamming_hex

def calculate_checksum(data):
    """Calculate Internet Checksum (IP Checksum)."""
    data_bytes = data.encode('utf-8')
    
    if len(data_bytes) % 2 == 1:
        data_bytes += b'\x00'
    
    checksum = 0
    for i in range(0, len(data_bytes), 2):
        word = (data_bytes[i] << 8) + data_bytes[i+1]
        checksum += word
    
    while checksum >> 16:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    
    checksum = ~checksum & 0xFFFF
    
    return format(checksum, '04X')

def recalculate_control_info(data, method):
    """Recalculate control information based on the method."""
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
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 8001  # Port where server waits for Client 2
    
    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to server
        print("Connecting to server (port 8001)...")
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print("Connected to server!")
        print("Waiting for corrupted packet...\n")
        
        # Receive packet from server
        packet = client_socket.recv(8192).decode('utf-8')
        
        # Parse packet: DATA|METHOD|CONTROL_INFORMATION
        parts = packet.split('|')
        if len(parts) != 3:
            print("Error: Invalid packet format!")
            return
        
        received_data, method, received_control = parts
        
        # Recalculate control information
        computed_control = recalculate_control_info(received_data, method)
        
        # Compare
        status = "DATA CORRECT" if computed_control.upper() == received_control.upper() else "DATA CORRUPTED"
        
        # Display results
        print("=" * 60)
        print("ERROR DETECTION RESULTS")
        print("=" * 60)
        print(f"Received Data      : {received_data}")
        print(f"Method             : {method}")
        print(f"Sent Check Bits    : {received_control}")
        print(f"Computed Check Bits: {computed_control}")
        print(f"Status             : {status}")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("\nConnection closed.")

if __name__ == "__main__":
    main()

