import subprocess
import re
import platform

def scan_wifi_windows():
    """Windows'ta 'netsh wlan show networks' komutunu kullanarak Wi-Fi ağlarını tarar."""
    networks = []
    try:
        # netsh komutu ile Wi-Fi ağlarını tarar
        cmd_output = subprocess.check_output(['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'], encoding='utf-8', stderr=subprocess.PIPE)
        
        # Her bir ağ bloğunu ayırır
        # SSID 1 : Ağ Adı
        # SSID 2 : Diğer Ağ Adı
        # formatındaki çıktıları parse eder
        network_blocks = re.split(r'SSID \d+\s*:\s', cmd_output)[1:] # İlk boş elemanı atarız
        
        for block in network_blocks:
            ssid_match = re.search(r'SSID name\s*:\s(.+)', block)
            auth_match = re.search(r'Authentication\s*:\s(.+)', block)
            encryption_match = re.search(r'Encryption\s*:\s(.+)', block)
            signal_match = re.search(r'Signal\s*:\s(.+)', block)

            ssid = ssid_match.group(1).strip() if ssid_match else "Bilinmiyor"
            authentication = auth_match.group(1).strip() if auth_match else "Bilinmiyor"
            encryption = encryption_match.group(1).strip() if encryption_match else "Bilinmiyor"
            signal = signal_match.group(1).strip() if signal_match else "Bilinmiyor"

            # Güvenlik protokolunu belirle
            security_protocol = f"{authentication}/{encryption}"
            if "Open" in authentication and "None" in encryption:
                security_protocol = "Açık (Şifresiz)"
            elif "WPA2" in authentication:
                security_protocol = "WPA2"
            elif "WPA3" in authentication: # WPA3 desteği eklendi
                security_protocol = "WPA3"
            elif "WEP" in authentication:
                security_protocol = "WEP"
            
            networks.append({
                "SSID": ssid,
                "Sinyal Kalitesi": signal,
                "Güvenlik Protokolü": security_protocol
            })
    except subprocess.CalledProcessError as e:
        print(f"Komut hatası oluştu: {e}")
        print(f"Hata çıktısı: {e.stderr.decode('utf-8')}")
        print("Lütfen komut istemcisini (CMD) yönetici olarak çalıştırdığınızdan emin olun.")
        return []
    except Exception as e:
        print(f"Wi-Fi taraması sırasında beklenmeyen bir hata oluştu: {e}")
        return []
    return networks

def main():
    os_name = platform.system()
    print(f"{os_name} üzerinde Wi-Fi ağları taranıyor...\n")

    if os_name == "Windows":
        wifi_networks = scan_wifi_windows()
        if wifi_networks:
            for i, net in enumerate(wifi_networks):
                print(f"--- Ağ {i+1} ---")
                print(f"Ağ Adı (SSID): {net['SSID']}")
                print(f"Sinyal Kalitesi: {net['Sinyal Kalitesi']}")
                print(f"Güvenlik Protokolü: {net['Güvenlik Protokolü']}")
                print("-" * 20)
        else:
            print("Yakınlarda Wi-Fi ağı bulunamadı veya tarama başarısız oldu.")
    else:
        print(f"Bu script şu anda sadece Windows için optimize edilmiştir.")
        print(f"'{os_name}' için farklı komutlar veya kütüphaneler gereklidir (örn: Linux için 'nmcli' veya 'iwlist', macOS için 'airport -s').")

if __name__ == "__main__":
    main()

