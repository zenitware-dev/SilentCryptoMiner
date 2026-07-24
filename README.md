<img width="1488" height="1124" alt="image" src="https://github.com/user-attachments/assets/d6d5869c-3480-4c94-a1d1-80aafd267e34" />
### Information

SilentCryptoMiner is an open source, silent crypto miner. The readme will detail features of the project. For precompiled builds, check the release page.


### Donations

If this project has served you well or been useful for resarching, please feel free to donate:

 - XMR: Present


Features
-----------------------

 - Hidden CPU Mining + GPU Mining with selective miner inclusion

 - Written on C/C++

 - Loader your files in Runtime (u need write raw link for archive.zip, with password in loaderlink.txt (format link,pass .zip legacy password encoding))

 - Start only after reboot pc (increase detects) 
 
 - GUI Builder (RU / EN Language)

 - Split Mining (To split the mining, you must specify a mining percentage (1–99) in the second configuration file; the default is 50/50.)

 - Remote Update Feature, Update your miners from the panel itself
 
 - Configurable miner selection (include CPU, GPU, or both)

- SSL support

- Watchdog to detect the miner process and restart if not running  

- "Process watch" to pause mining if certain processes are detected running
    
- On the fly configurations, to update when needed

- Windows Defender C: drive exclusion (automatic when running as administrator)

Installation
------------
**Requirements:**

python -m pip install --upgrade pip
python -m pip install PySide6 PyInstaller pyaes

### Create Builder
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "MyApp" --icon "icon.ico" --add-data "icon.ico:." "main.py"

Builder creating in dist

### Test settings
You can copy settings from builder windows and start default xmrig.exe with settings https://github.com/xmrig/xmrig/releases/download/v6.26.0/xmrig-6.26.0-windows-x64.zip (if u test gpu need download cuda.dll https://github.com/xmrig/xmrig-cuda)

### Issues
If you notice a bug or any other issue that isn't installation, please feel free to find me at t.me/liberty_support, or open an issue on github.

# Disclaimer

This software ("SilentCryptoMiner") is designed solely for lawful use on networks and devices for which the user has obtained explicit, prior authorization from the network owner, system administrator, or device owner. Use of the Miner on any network, system, or hardware without such authorization may violate computer fraud and abuse laws. Through use of this project for illegal uses, you acknowledge you are taking this demonstration of mining malware in the wild and using it for your own gain. By using this software, you indemnify, defend, and hold harmless the developer, distributor, and any affiliated parties from and against any and all claims, damages, losses, liabilities, costs, and expenses (including reasonable attorneys’ fees) arising out of or related to your unauthorized use of the Miner
