# EBUP - Extensible Binary User Protocol

---

## 📖 English Documentation

### Overview

**EBUP** (Extensible Binary User Protocol) is a lightweight, UDP-based network communication protocol designed for peer-to-peer communication between systems over a network. It provides features such as system discovery, acknowledgment queries, priority messaging, and automatic packet handling using threading.

**No External Dependencies**: EBUP is a dependency-free protocol that uses only Python's standard library (socket, json, threading, time). No external packages are required.

### Key Features

- **UDP-Based Communication**: Uses UDP sockets for fast, connectionless communication
- **Automatic Discovery**: Broadcast-based discovery to find other EBUP systems on the network
- **Acknowledgment System**: Check if remote systems are available and measure latency
- **Priority Messaging**: Send messages with priority flag for immediate attention
- **Threaded Listener**: Runs a background listener thread to continuously receive incoming packets
- **Address Book**: Maintains a record of discovered systems with metadata
- **Packet Structure**: Standardized JSON-based packet format with starter/end bits for validation

### Class: EBUProtocol

#### Constructor
```python
EBUProtocol(systemID=None, systemPort=defaultPort)
```
- **systemID**: Unique identifier for this system (defaults to local IP)
- **systemPort**: UDP port to listen on (default: 1302)

Initializes the EBUP interface, binds to the specified port, and starts the listener thread.

#### Key Methods

**`sendPocket(destination, data, priority=False)`**
- Sends a packet to a destination system
- `destination`: IP address of the target system
- `data`: Message content (dict or any data type)
- `priority`: If True, marks the message as priority

**`isAvailable(destination, timeout=3)`**
- Checks if a remote system is available and responsive
- Returns True if available, False on timeout
- Measures and displays latency in milliseconds

**`discovery(timeout)`**
- Broadcasts a discovery signal to find all EBUP systems on the network
- Waits for responses within the specified timeout (seconds)
- Returns a list of discovered system IPs

**`updateAddressBook(answers)`**
- Adds discovered systems to the address book
- Records IP address and creation timestamp

**`getLocalIP()` (Static Method)**
- Automatically detects the local IP address
- Fallback to localhost (127.0.0.1) if detection fails

### Packet Structure

Packets are structured as JSON arrays:
```
[starterBit, senderID, destinationID, payload, enderBit]
```

### Message Types

- **ack_query**: Acknowledgment check request
- **ack_affirmative**: Acknowledgment confirmation
- **discovery**: Discovery broadcast message
- **discovery_here**: Discovery response
- **msg**: Regular message
- **msgInfo**: Message status information

### Default Configuration

- Default Port: 1302
- Starter Bit: "EBUP-S-v1"
- Ender Bit: "EBUP-E-v1"

### Example Usage

```python
from ebup import EBUProtocol

# Create EBUP interface
ebup = EBUProtocol()

# Check if a system is available
ebup.isAvailable("192.168.1.100", timeout=3)

# Discover systems on network
discovered_systems = ebup.discovery(timeout=5)

# Send a message
ebup.sendPocket("192.168.1.100", {"data": "Hello!"})

# Send a priority message
ebup.sendPocket("192.168.1.100", "Urgent message", priority=True)
```

---

## 📖 Türkçe Dokumentasyon

### Genel Bakış

**EBUP** (Ether-Based UDP Protocol), ağ üstündeki sistemler arasında eş-seviyesi (peer-to-peer) iletişim sağlamak için tasarlanmış hafif, UDP tabanlı bir protokoldür. Sistem keşfi, onay sorguları, öncelikli mesajlaşma ve threading kullanarak otomatik paket işleme gibi özellikler sunar.
**Dış Kütüphane Bağımlılığı Yok**: EBUP, yalnızca Python'ın standart kütüphanelerini (socket, json, threading, time) kullanan, tamamen bağımlılıktan bağımsız bir protokoldür. Herhangi bir harici paket kurulumuna gerek yoktur.
### Temel Özellikler

- **UDP Tabanlı İletişim**: Hızlı, bağlantısız iletişim için UDP soketleri kullanır
- **Otomatik Keşif**: Ağ üstündeki diğer EBUP sistemlerini bulmak için broadcast tabanlı keşif
- **Onay Sistemi**: Uzak sistemlerin müsait olup olmadığını kontrol eder ve gecikme süresini ölçer
- **Öncelikli Mesajlaşma**: Acil dikkat gerektiren mesajları önceli olarak gönderebilir
- **Arkaplan Dinleyicisi**: Gelen paketleri sürekli olarak almak için arka planda çalışan bir iş parçacığı
- **Adres Defteri**: Keşfedilen sistemlerin kaydını metaveri ile birlikte tutar
- **Paket Yapısı**: Doğrulama için başlangıç/bitiş bitleri ile standardlaştırılmış JSON tabanlı paket formatı

### Sınıf: EBUProtocol

#### Yapıcı (Constructor)
```python
EBUProtocol(systemID=None, systemPort=defaultPort)
```
- **systemID**: Bu sistem için benzersiz tanımlayıcı (varsayılan: yerel IP)
- **systemPort**: Dinlenecek UDP portu (varsayılan: 1302)

EBUP arayüzünü başlatır, belirtilen porta bağlanır ve dinleyici iş parçacığını başlatır.

#### Temel Yöntemler

**`sendPocket(destination, data, priority=False)`**
- Hedef sisteme bir paket gönderir
- `destination`: Hedef sistemin IP adresi
- `data`: Mesaj içeriği (dict veya herhangi bir veri türü)
- `priority`: True ise mesajı öncelikli olarak işaretler

**`isAvailable(destination, timeout=3)`**
- Uzak bir sistemin müsait olup olmadığını ve yanıt verip vermediğini kontrol eder
- Müsaitse True, zaman aşımında False döndürür
- Gecikme süresini milisaniye cinsinden ölçer ve gösterir

**`discovery(timeout)`**
- Ağ üstündeki tüm EBUP sistemlerini bulmak için keşif sinyali yayınlar
- Belirtilen zaman aşımı süresi içinde (saniye) yanıtları bekler
- Keşfedilen sistem IP adreslerinin bir listesini döndürür

**`updateAddressBook(answers)`**
- Keşfedilen sistemleri adres defterine ekler
- IP adresi ve oluşturma zamanını kaydeder

**`getLocalIP()` (Statik Yöntem)**
- Yerel IP adresini otomatik olarak algılar
- Algılama başarısız olursa localhost'a (127.0.0.1) geri döner

### Paket Yapısı

Paketler JSON dizileri olarak yapılandırılır:
```
[starterBit, senderID, destinationID, payload, enderBit]
```

### Mesaj Türleri

- **ack_query**: Onay kontrol isteği
- **ack_affirmative**: Onay onaylaması
- **discovery**: Keşif yayın mesajı
- **discovery_here**: Keşif yanıtı
- **msg**: Normal mesaj
- **msgInfo**: Mesaj durum bilgisi

### Varsayılan Yapılandırma

- Varsayılan Port: 1302
- Başlangıç Biti: "EBUP-S-v1"
- Bitiş Biti: "EBUP-E-v1"

### Kullanım Örneği

```python
from ebup import EBUProtocol

# EBUP arayüzü oluştur
ebup = EBUProtocol()

# Bir sistemin müsait olup olmadığını kontrol et
ebup.isAvailable("192.168.1.100", timeout=3)

# Ağ üstünde sistemleri keşfet
discovered_systems = ebup.discovery(timeout=5)

# Mesaj gönder
ebup.sendPocket("192.168.1.100", {"data": "Merhaba!"})

# Öncelikli mesaj gönder
ebup.sendPocket("192.168.1.100", "Acil mesaj", priority=True)
```

---

## 📋 Teknik Detaylar / Technical Details

### Buffer Mechanism / Tampon Mekanizması
- Gelen yanıtlar ve keşif cevapları buffer listesinde saklanır
- Asenkron işlem için sistem tarafından kontrol edilir

### Threading / İş Parçacığı
- Dinleyici daemon thread'i arka planda çalışır
- Ana programı engellemeyen bağımsız ağ kontrolü sağlar

### Error Handling / Hata Yönetimi
- Port bağlama hatasını yakalar ve bunu kullanan başka bir işlemi bildiriyor
- IP algılamada başarısız olursa 127.0.0.1'e geri döner
