import hid
from datetime import datetime

# Replace these with your device's actual vendor and product IDs
# Zuoya GMK87 default IDs
VENDOR_ID = 0x320f
PRODUCT_ID = 0x5055

def send_data(device, data):
    # Ensure to send the report ID as the first byte if needed
    # Some HID devices do not require it.
    # For this device, we'll use 0x00 as the report ID
    device.write([0x00] + data)

def update_time(device):
    now = datetime.now()
    
    print("update_time - Initiate transaction")
    data1 = [0x04, 0x01] + [0x00] * 62
    send_data(device, data1)

    print("update_time - Building data set with current time and settings")
    data2 = [
        0x04, 0x53, 0x06, 0x06, 0x30, 0x00, 0x00, 0x00, 0x00, 0x12, 
        0x03, 0x01, 0x00, 0x01, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00,
    ]

    # Time data
    print("update_time - Current time:", now)
    data2[30:37] = [
        now.year - 2000,
        now.month,
        now.day,
        now.weekday(), 
        now.hour,
        now.minute,
        now.second
    ]

    # Additional configuration settings (example values - adjust as needed)
    # These are placeholder values - you should replace them with actual configuration
    # parameters for your specific device
    data2[37:45] = [
        0x01,  # Configuration flag 1
        0x02,  # Configuration flag 2
        0x03,  # Configuration value 1
        0x04,  # Configuration value 2
        0x05,  # Configuration value 3
        0x06,  # Configuration value 4
        0x07,  # Configuration value 5
        0x08,  # Configuration value 6
    ]

    # Ensure that data2 is exactly 64 bytes long
    data2 += [0x00] * (64 - len(data2))
    send_data(device, data2)
    
    # Finalize configuration
    print("update_time - Finalize transaction")
    data3 = [0x04, 0x02] + [0x00] * 62
    send_data(device, data3)

def main():
    try:
        print("Opening device...")
        device = hid.device()
        device.open(VENDOR_ID, PRODUCT_ID)
        print("Device opened.")
        print("Updating time...")
        update_time(device)
        print("Time update command sent.")
    except Exception as e:
        print(f"Unable to open device: {e}")
    finally:
        if 'device' in locals() and device:
            device.close()

if __name__ == "__main__":
    main()


