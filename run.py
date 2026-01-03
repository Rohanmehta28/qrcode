import uvicorn
import socket

def get_ip_address():
    try:
        # Connect to an external server (doesn't actually send data) to get the local IP used for routing
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    ip = get_ip_address()
    port = 8000
    
    print("\n" + "="*60)
    print(f"🚀  SERVER STARTING")
    print("="*60)
    print(f"To test on your mobile phone, ensure it's on the same WiFi.")
    print(f"Then access the API at:")
    print(f"\n    http://{ip}:{port}/docs\n")
    print("="*60 + "\n")
    
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
