# CipherSherlock Git Repository

Here are the files needed to create a Git repository for your tool CipherSherlock.

```
CipherSherlock/            # root folder
├── .gitignore            # files to ignore
├── README.md             # project overview and usage
├── requirements.txt      # Python dependencies
└── CipherSherlock.py     # main script
```

---

## .gitignore

```
__pycache__/
*.pyc
.env
venv/
*.log
```

## requirements.txt

```
tqdm==4.65.0
```

## README.md

```markdown
# CipherSherlock 🔍

CipherSherlock is a powerful command-line decoder and CTF reverse engineering tool. Designed to help ethical hackers, students, and cybersecurity enthusiasts unravel multiple layers of encoded data, it's your best partner in uncovering hidden flags like `HTB{...}` or `rootCTF{...}`.

## ✨ Features

- Auto-detect encoding formats like Base64, Hex, Binary, ROT13
- Decode recursively across multiple layers
- Match or auto-detect CTF flag formats
- Includes a `--random` decoding mode to try mixed combinations
- Progress bars and clean terminal output

---

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Nikhilkaware36/CipherSherlock.git
   cd CipherSherlock
   ```
2. (Optional) Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependency:
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Commands & Usage

### Basic decoding with a flag format
```bash
python3 CipherSherlock.py -i "<encoded_string>" -f "rootCTF{}"
```

### Auto-detect flag (no `-f` required)
```bash
python3 CipherSherlock.py -i "<encoded_string>"
```

### Try random mixed decoding modes
```bash
python3 CipherSherlock.py -i "<encoded_string>" -f "rootCTF{}" -r
```

### Get help & all options
```bash
python3 CipherSherlock.py -h
```

---

## 🧩 Command-line Options
    
    | Option / Flag       | Description                                                 |
    |---------------------|-------------------------------------------------------------|
    | `-i`, `--input`      | (Required) Provide the encoded input string                 |
    | `-f`, `--flag-format`| (Optional) Define your expected flag format (e.g., `HTB{}`) |
    | `-r`, `--random`     | Try random decoding combinations                            |
    | `-h`, `--help`       | Show help message                                           |

---

## 🐞 Troubleshooting

    - If `tqdm` is missing, install it with:
      ```bash
      pip install tqdm
      ```
    - Use `-r` to brute-force uncommon encoding patterns.
    - Always double-check input for extra characters or formatting errors.
- Report bugs/issues on GitHub:
  [CipherSherlock Issues](https://github.com/Nikhilkaware36/CipherSherlock/issues)

---

## 📜 License

MIT License

---

## 👨‍💻 Author

Created and maintained by [Nikhilkaware36](https://github.com/Nikhilkaware36)
```

