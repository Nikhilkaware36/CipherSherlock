import base64
import codecs
import re
import argparse
from tqdm import tqdm

# ANSI color codes
RED = "\033[1;31m"
RESET = "\033[0m"

BANNER = f"""
{RED}██╗      ██████╗  ██████╗██╗  ██╗███████╗██████╗ 
██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║     ██║   ██║██║     █████╔╝ █████╗  ██████╔╝
██║     ██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
███████╗╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║
╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{RESET}

{RED}     CipherSherlock by Nikhilkaware36 (GitHub){RESET}
"""

def detect_encoding(data: str):
    """Detect possible encodings"""
    detections = []
    try:
        base64.b64decode(data)
        detections.append("Base64")
    except Exception:
        pass

    try:
        int(data, 16)
        if len(data) % 2 == 0:
            detections.append("Hex")
    except Exception:
        pass

    try:
        codecs.decode(data, 'rot_13')
        detections.append("ROT13")
    except Exception:
        pass

    if re.fullmatch(r'[01]+', data):
        detections.append("Binary")

    return detections


def decode_data(data: str, method: str):
    """Decode using specified method"""
    try:
        if method == "Base64":
            return base64.b64decode(data).decode('utf-8', errors='ignore')
        elif method == "Hex":
            return bytes.fromhex(data).decode('utf-8', errors='ignore')
        elif method == "ROT13":
            return codecs.decode(data, 'rot_13')
        elif method == "Binary":
            chars = [chr(int(data[i:i+8], 2)) for i in range(0, len(data), 8)]
            return ''.join(chars)
    except Exception:
        return "[!] Decoding failed"


def flag_found(decoded: str, flag_format: str):
    """Check if decoded data matches flag format"""
    pattern = flag_format.replace('{', '\\{').replace('}', '\\}').replace('...', '.*')
    return bool(re.search(pattern, decoded))


def auto_detect_flag(decoded: str):
    """Automatically detect flag-like format"""
    flag_patterns = [
        r'([A-Za-z0-9_]+{.*})',    # Common flags
        r'[A-Za-z0-9_]+{.*}',       # Flags like HTB{...}
    ]

    for pattern in flag_patterns:
        match = re.search(pattern, decoded)
        if match:
            return match.group(0)
    return None


def process_layers(raw_data, flag_format=None):
    """Process multiple encoding layers"""
    print(BANNER)
    layer = 1
    current_data = raw_data
    flag_found_output = False
    layer_output = []
    seen_data = set()

    with tqdm(total=100, desc="Decrypting...", unit="%", ncols=100) as pbar:
        while True:
            methods = detect_encoding(current_data)
            if not methods:
                print(f"⚠️ No more known encodings detected at layer {layer}.")
                break

            method = methods[0]
            print(f"\n🧐 **Layer {layer}: Detected** {method}")
            decoded = decode_data(current_data, method)
            print(f"   🔓 **Decoded**: {decoded}")

            flag_match = False
            if flag_format and flag_found(decoded, flag_format):
                print(f"   🎯 **Flag pattern** '{flag_format}' found!")
                flag_found_output = True
                flag_match = True

            if not flag_match:
                auto_flag = auto_detect_flag(decoded)
                if auto_flag:
                    print(f"   🎯 **Auto-detected Flag**: {auto_flag}")
                    flag_found_output = True

            layer_output.append({
                "layer": layer,
                "method": method,
                "decoded": decoded,
                "flag_match": flag_match or bool(auto_flag)
            })

            if decoded == current_data or decoded in seen_data:
                print(f"⚠️ **No change after decoding** at layer {layer}. Stopping.")
                break

            seen_data.add(decoded)
            current_data = decoded
            layer += 1

            pbar.update(1)

        return layer_output, flag_found_output


def main():
    print(BANNER)  # Show banner on any run
    parser = argparse.ArgumentParser(description='🔍 CipherSherlock - Format Detector and Recursive Decoder')
    parser.add_argument('-i', '--input', type=str, required=True, help='Encoded input string')
    parser.add_argument('-f', '--flag-format', type=str, help='Flag format e.g., HTB{...} or rootCTF{}')
    parser.add_argument('-r', '--random', action='store_true', help='Try multiple mixed encodings for flag detection')
    args = parser.parse_args()

    print(f"🔍 **Input String**: {args.input}")
    print("=" * 50)

    try:
        raw_data = args.input.strip()
        layer_output, flag_found_output = process_layers(raw_data, args.flag_format)

        if flag_found_output:
            print("\n🎯 **FLAG FOUND!** 🎯")
            for entry in layer_output:
                if entry['flag_match']:
                    print(f"📝 **Layer {entry['layer']}**")
                    print(f"   ➡️ **Method**: {entry['method']}")
                    print(f"   🔓 **Decoded**: {entry['decoded']}")
                    print("=" * 50)
        else:
            print("\n🚨 **No Flag Found!** 🚨")
            print("=" * 50)
            print(f"   ➡️ Total Layers Processed: {len(layer_output)}")
            print("=" * 50)
            print("💡 **Reason:** The flag format was not found after processing all layers.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    print(BANNER)  # Show banner before any error/output
    main()
