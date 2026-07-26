import urllib.request
import datetime
import base64

def decode_base64_if_needed(text):
    # Mengecek apakah teks mentah dari internet sudah di-encode Base64 atau belum
    if "vless://" in text or "vmess://" in text or "trojan://" in text:
        return text
    try:
        return base64.b64decode(text).decode('utf-8')
    except Exception:
        return text

def main():
    print("Mulai menjalankan Scraper Sultan The Node Hunter...")
    
    # Daftar URL raw GitHub yang rajin update tiap beberapa menit/jam
    SOURCES = [
        "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/vless_configs.txt", 
        "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/vmess_configs.txt", 
        "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt", 
        "https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/protocols/vless.txt"
    ]
    
    all_nodes = set() # Pakai 'set' agar kalau ada node ganda, otomatis dihapus
    
    for url in SOURCES:
        try:
            print(f"[*] Menyerok dari: {url}")
            # Tarik data menggunakan urllib bawaan Python
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=15)
            raw_text = response.read().decode('utf-8')
            
            decoded_text = decode_base64_if_needed(raw_text)
            
            # Saring baris yang benar-benar link VPN saja
            for line in decoded_text.splitlines():
                line = line.strip()
                if line.startswith(('vless://', 'vmess://', 'trojan://', 'ss://')):
                    all_nodes.add(line)
        except Exception as e:
            print(f"[!] Gagal mengambil dari {url}: {e}")
            
    # Tambahkan penanda waktu (Watermark) bohongan agar kita tahu kapan bot terakhir update
    waktu_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    watermark = f"vless://sultan-uuid@1.1.1.1:443?type=ws&security=tls#🔥_Sultan_Update_{waktu_sekarang.replace(' ', '_')}"
    
    # --- KODE GABUNGAN LIMITASI ---
    # Ubah set menjadi list, lalu potong hanya mengambil 150 node pertama
    node_pilihan = list(all_nodes)[:150]
    
    # Gabungkan, pastikan watermark ada di paling atas saat di-import ke aplikasi
    final_nodes = [watermark] + node_pilihan
    final_text = "\n".join(final_nodes)
    
    # Wajib di-encode ke Base64 agar aplikasi seperti Sing-box/Xray bisa membaca URL-nya
    encoded_string = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
    
    # Timpa ke file sub.txt
    with open("sub.txt", "w") as file:
        file.write(encoded_string)
        
    print(f"Sukses! Berhasil membajak {len(node_pilihan)} node terpilih dari total {len(all_nodes)} tangkapan pada {waktu_sekarang}")

if __name__ == "__main__":
    main()
