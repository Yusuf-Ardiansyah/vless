import urllib.request
import datetime
import base64
import socket
import json
import urllib.parse
import concurrent.futures

def decode_base64_if_needed(text):
    # Mengecek apakah teks mentah dari internet sudah di-encode Base64 atau belum
    if "vless://" in text or "vmess://" in text or "trojan://" in text:
        return text
    try:
        return base64.b64decode(text).decode('utf-8')
    except Exception:
        return text

def get_host_port(link):
    """Mengekstrak Host (IP/Domain) dan Port dari link VLESS/VMESS/TROJAN"""
    try:
        if link.startswith("vmess://"):
            # vmess:// formatnya adalah base64 JSON
            b64_data = link[8:]
            # Perbaiki padding base64 jika kurang
            b64_data += "=" * ((4 - len(b64_data) % 4) % 4)
            config = json.loads(base64.b64decode(b64_data).decode('utf-8'))
            return config.get('add'), int(config.get('port'))
        
        elif link.startswith(("vless://", "trojan://")):
            # Format umum: vless://uuid@host:port?params#name
            parsed = urllib.parse.urlparse(link)
            netloc = parsed.netloc
            if "@" in netloc:
                netloc = netloc.split("@")[1]
            host_port = netloc.split(":")
            if len(host_port) >= 2:
                return host_port[0], int(host_port[1])
    except Exception:
        pass
    return None, None

def check_node_alive(link):
    """Mengecek apakah node hidup menggunakan TCP Ping (Timeout 3 detik)"""
    host, port = get_host_port(link)
    
    # Jika gagal ekstrak host/port (format aneh), buang saja
    if not host or not port:
        return None 
    
    try:
        # Mengetuk pintu server (TCP Connection)
        with socket.create_connection((host, port), timeout=3.0):
            return link # Sukses! Pintu terbuka, node HIDUP
    except Exception:
        return None # Gagal! Timeout/Connection Refused, node MATI

def main():
    print("🚀 Mulai menjalankan Scraper Sultan The Node Hunter...")
    
    # Daftar URL raw GitHub
    SOURCES = [
        "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/vless_configs.txt", 
        "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/vmess_configs.txt", 
        "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt", 
        "https://raw.githubusercontent.com/Delta-Kronecker/V2ray-Config/main/config/protocols/vless.txt"
    ]
    
    all_nodes = set()
    
    for url in SOURCES:
        try:
            print(f"[*] Menyerok dari: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=15)
            raw_text = response.read().decode('utf-8')
            
            decoded_text = decode_base64_if_needed(raw_text)
            
            for line in decoded_text.splitlines():
                line = line.strip()
                if line.startswith(('vless://', 'vmess://', 'trojan://')):
                    all_nodes.add(line)
        except Exception as e:
            print(f"[!] Gagal mengambil dari {url}: {e}")
            
    print(f"\n🔍 Total {len(all_nodes)} node mentah didapatkan. Memulai seleksi alam (TCP Ping)...")
    
    alive_nodes = []
    
    # 🔥 FITUR SULTAN: MULTI-THREADING (Mengecek 20 node sekaligus agar super cepat)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(check_node_alive, all_nodes)
        for res in results:
            if res is not None:
                alive_nodes.append(res)
                
    print(f"✅ Seleksi selesai! Sisa {len(alive_nodes)} node tangguh yang MASIH HIDUP.")

    # Watermark Sultan
    waktu_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    watermark = f"vless://sultan-uuid@1.1.1.1:443?type=ws&security=tls#🔥_Sultan_Update_{waktu_sekarang.replace(' ', '_')}"
    
    # Ambil 150 node pertama dari list yang SUDAH PASTI HIDUP
    node_pilihan = alive_nodes[:150]
    
    final_nodes = [watermark] + node_pilihan
    final_text = "\n".join(final_nodes)
    
    encoded_string = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
    
    with open("sub.txt", "w") as file:
        file.write(encoded_string)
        
    print(f"🎉 SUKSES! {len(node_pilihan)} node premium siap digunakan pada {waktu_sekarang}")

if __name__ == "__main__":
    main()
