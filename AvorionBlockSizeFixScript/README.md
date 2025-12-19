# Avorion Block Size Fix Script

A small Python utility that fixes block size in Avorion files caused by block size requirements.

This script scans a file, detects block dimensions (axis) that are below the defined threshold (usually '0.011', can be configured directly in the file), and snaps them to their intended values, preventing build errors, warnings, and invalid block sizes in-game.

---

## 🔧 What This Script Does

- Reads an Avorion XML file
- Detects block size (axis) values affected by minimum block size requeriments
- Rounds/snaps values to the nearest valid size
- Preserves the original file by creating a backup
- Writes a corrected file compatible with Avorion

---

## 📂 Supported Files

- Avorion ship/station/etc files (`.xml`)
- Works on any avorion files, downloaded from workshop (copy the file to your folder to be on the safe side), or from your creations.

---

## 🧪 Why This Is Needed

Some designers created files for Avorion Workshop that are no longer supported due to new requirements on minimum axis size for all blocks:
- 0.00000001
- 0.00999999

These values will:
- Make the file unable to be loaded on a server that imposes minimum size limits
- Prevent resizing blocks
- Cause warnings or making the file unable to be imported

This script fixes those values safely and automatically.

---

## ▶️ How to Use

### 1️⃣ Requirements

- Python 3 or newer
- No external libraries required
  
### 2️⃣ Run the Script

- Place the script in the same folder as the .xml file.
- Open a Command window (search for cmd on Windows)
- Navigate to the folder where the script is and run:
- python avorion_block_fix.py your_file.xml

---

## 💾 Backup Behavior

- The original file is never overwritten
- A Backup/ folder is created automatically
- The original ship file is moved there before writing the fixed version, as well the script, after finishing execution, leaving the folder almost identical as in the beggining.

This ensures your original data is always safe.

---

## 🛠️ Customization

If needed, you can adjust the minimum acceptable axis size of the script, directly inside the script.

Open the file with a text editor like notepad or notepad++ and change the line `MIN_SIZE = 0.___`

---

## ⚠️ Notes

- Always test the fixed ship in a test galaxy first
- Creative does not have size restrictions, use a normal galaxy with infinite credits/resources enabled.
- This script does not modify save games
- Use at your own risk

---

## 📜 License

MIT License

You are free to use, modify, and redistribute this script.

---

## 🙏 Credits
- ChatGPT for doing the borring stuff. **When creating with AI, you are responsible for checking the code, testing and assuring the quality of the work.**
- Developed to solve Avorion block size issues encountered by the community
