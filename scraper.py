import datetime
import base64

def main():
    print("Mulai menjalankan Scraper Sultan...")
    
    # 1. Mendapatkan waktu saat ini
    waktu_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. Dummy node (format vless bohongan untuk tes)
    dummy_node = f"vless://sultan-uuid@1.1.1.1:443?type=ws&security=tls#Node_Update_{waktu_sekarang}"
    
    # 3. Encode ke Base64 (Format standar sub)
    encoded_bytes = base64.b64encode(dummy_node.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    
    # 4. Tulis (overwrite) ke file sub.txt
    with open("sub.txt", "w") as file:
        file.write(encoded_string)
        
    print(f"Sukses mengupdate sub.txt pada {waktu_sekarang}")

if __name__ == "__main__":
    main()
