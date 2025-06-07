# Wi-Fi Scanner Script 📡

This Python script is designed to scan for Wi-Fi networks in your vicinity on the Windows operating system and display their basic information.

---

## 🔍 What It Provides:

The script uses the `netsh wlan show networks` command to provide the following information:

* **Network Name (SSID):** The name of the Wi-Fi network.
* **Signal Quality:** The signal strength of the network (usually as a percentage).
* **Security Protocol:** The type of security the network uses (e.g., WPA2, WPA3, Open).

---

## 🚫 Limitations:

This simple scanner script cannot directly obtain certain information:

* **IP Address:** The internal or external IP addresses of surrounding networks cannot be learned through such scans due to security reasons.
* **Public/Private Status:** Whether a network is encrypted (security protocol) indicates if it's "private" or "open" (unencrypted). The script does not directly state "public" or "private."
* **Speed (Mbps):** While signal quality gives an idea of speed, the script does not directly show the network speed (Mbps).
* **Host:** The router hostnames of other networks cannot be obtained through this scan.

---

## 🚀 How to Use:

1.  **Save the Script:** Copy the Python code above and save it on your computer with a name like `wifi_scan.py`.

2.  **Open CMD as Administrator:**
    * Type `cmd` in the Windows search bar.
    * Right-click on the "Command Prompt" application that appears and select "Run as administrator."

3.  **Navigate to the Folder:** In CMD, go to the folder where you saved the `wifi_scan.py` file. For example, if you saved it to your desktop:
    ```bash
    cd C:\Users\YourUsername\Desktop
    ```
    (Replace `YourUsername` with your actual Windows username.)

4.  **Run the Script:**
    ```bash
    python wifi_scan.py
    ```

---

## 💻 Python Code:

```python
import subprocess
import re
import platform

def scan_wifi_windows():
    """Scans for Wi-Fi networks on Windows using the 'netsh wlan show networks' command."""
    networks = []
    try:
        # Scans Wi-Fi networks using the netsh command
        cmd_output = subprocess.check_output(['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'], encoding='utf-8', stderr=subprocess.PIPE)
        
        # Splits each network block
        # Parses output like:
        # SSID 1 : Network Name
        # SSID 2 : Another Network Name
        network_blocks = re.split(r'SSID \d+\s*:\s', cmd_output)[1:] # Skips the first empty element
        
        for block in network_blocks:
            ssid_match = re.search(r'SSID name\s*:\s(.+)', block)
            auth_match = re.search(r'Authentication\s*:\s(.+)', block)
            encryption_match = re.search(r'Encryption\s*:\s(.+)', block)
            signal_match = re.search(r'Signal\s*:\s(.+)', block)

            ssid = ssid_match.group(1).strip() if ssid_match else "Unknown"
            authentication = auth_match.group(1).strip() if auth_match else "Unknown"
            encryption = encryption_match.group(1).strip() if encryption_match else "Unknown"
            signal = signal_match.group(1).strip() if signal_match else "Unknown"

            # Determine security protocol
            security_protocol = f"{authentication}/{encryption}"
            if "Open" in authentication and "None" in encryption:
                security_protocol = "Open (Unencrypted)"
            elif "WPA2" in authentication:
                security_protocol = "WPA2"
            elif "WPA3" in authentication: # WPA3 support added
                security_protocol = "WPA3"
            elif "WEP" in authentication:
                security_protocol = "WEP"
            
            networks.append({
                "SSID": ssid,
                "Signal Quality": signal,
                "Security Protocol": security_protocol
            })
    except subprocess.CalledProcessError as e:
        print(f"Command error occurred: {e}")
        print(f"Error output: {e.stderr.decode('utf-8')}")
        print("Please ensure the command prompt (CMD) is run as administrator.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during Wi-Fi scan: {e}")
        return []
    return networks

def main():
    os_name = platform.system()
    print(f"Scanning Wi-Fi networks on {os_name}...\n")

    if os_name == "Windows":
        wifi_networks = scan_wifi_windows()
        if wifi_networks:
            for i, net in enumerate(wifi_networks):
                print(f"--- Network {i+1} ---")
                print(f"Network Name (SSID): {net['SSID']}")
                print(f"Signal Quality: {net['Signal Quality']}")
                print(f"Security Protocol: {net['Security Protocol']}")
                print("-" * 20)
        else:
            print("No Wi-Fi networks found nearby or scan failed.")
    else:
        print(f"This script is currently optimized for Windows only.")
        print(f"Different commands or libraries are required for '{os_name}' (e.g., 'nmcli' or 'iwlist' for Linux, 'airport -s' for macOS).")

if __name__ == "__main__":
    main()
```

---

## 💖 Support Us

If you like this project and wish to support its development, you can do so through the methods below:

<p align="center">
  <a href="mailto:ruhidjavadoff@gmail.com">
    <img src="https://img.shields.io/badge/Donate-Email_PayPal-blue?style=for-the-badge&logo=paypal" alt="Email PayPal">
  </a>
  <a href="https://ruhidjavadoff.site/donate/" target="_blank">
    <img src="https://img.shields.io/badge/Donate-Web_Site-green?style=for-the-badge&logo=donate" alt="Donate via Website">
  </a>
</p>

---

## 🌐 Follow Us

Stay updated on our projects and news by following us on social media!

<p align="center">
  <a href="https://ruhidjavadoff.site/followme/" target="_blank">
    <img src="https://img.shields.io/badge/Follow_Us-Social_Media-purple?style=for-the-badge&logo=rss" alt="Follow Us on Social Media">
  </a>
</p>

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## 🧑‍💻 Author

Ruhid Javadoff

---
