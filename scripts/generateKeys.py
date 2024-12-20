import os

def generate_key(size):
    return os.urandom(size)

dev_eui = generate_key(8)
app_eui = generate_key(8)
app_key = generate_key(16)

print("For node config")
print("uint8_t devEui[] = {", ', '.join(f"0x{x:02X}" for x in dev_eui), "};")
print("uint8_t appEui[] = {", ', '.join(f"0x{x:02X}" for x in app_eui), "};")
print("uint8_t appKey[] = {", ', '.join(f"0x{x:02X}" for x in app_key), "};")
print("For server config")
print(''.join(f"{x:02x}" for x in dev_eui))
print(''.join(f"{x:02x}" for x in app_eui))
print(''.join(f"{x:02x}" for x in app_key))