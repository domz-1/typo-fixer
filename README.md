# 🚀 Smart Typo Fixer & Auto-Corrector for Linux

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Linux%20(X11%20%26%20GNOME)-orange.svg)]()
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)]()
[![Languages](https://img.shields.io/badge/Supports-English%20%7C%20Arabic-purple.svg)]()

A blazing-fast, system-wide smart typo and spelling fixer for Linux. Highlight any mistyped text anywhere (browser, editor, terminal, chat apps), press **`Alt + Q`**, and it instantly corrects spelling, grammar, and accidental keyboard layout mistypes (e.g. typing Arabic with English layout or vice-versa), then **automatically replaces the text in-place** without even needing `Ctrl + V`!

---

## ✨ Key Features

- ⚡ **Instant In-Place Auto-Paste:** Select your broken text, hit `Alt + Q`, and watch it get replaced in 0.05s.
- 🌐 **Accidental Keyboard Layout Detection:**
  - Typed **`اثممخ`** while your keyboard was set to Arabic? It automatically converts and corrects to **`Hello`**.
  - Typed **`sghl ugd;l`** while your keyboard was in English? It converts to **`سلام عليكم`**.
- 🎯 **High-Precision Multi-Engine Correction:**
  - Fast local dictionary fuzzy matching (`/usr/share/dict/words` + common typo maps).
  - Neural grammar and spell checking via LanguageTool.
  - Offline local AI fallback via Ollama (Gemma 3 / Qwen).
- 🔠 **Smart Capitalization & Punctuation:** Automatically fixes leading capitals and trailing punctuation (`?`, `.`).
- 🔔 **Desktop Notifications & Visual Feedback:** Shows beautiful instant notifications displaying the *Before* and *After*.
- 🖥️ **GUI Input Dialog Fallback:** If triggered without selecting text, it opens a clean GUI box (Zenity) so you can type or paste manually.

---

## 📸 Real-World Examples

| What You Mistyped | What Typo Fixer Auto-Corrects & Pastes |
| :--- | :--- |
| `اثممخ` (Arabic layout by mistake) | ➔ **`Hello`** |
| `اثممخ اخص شقث غخع` | ➔ **`Hello how are you?`** |
| `sghl ugd;l` (English layout by mistake) | ➔ **`سلام عليكم`** |
| `i wnat to mkae coroect for my speieng` | ➔ **`I want to make correct for my spelling`** |
| `can you help me bc idk what to do` | ➔ **`Can you help me because I don't know what to do?`** |

---

## 📦 Dependencies

Typo Fixer depends on standard Linux utilities available across all distributions:

| Dependency | Purpose |
| :--- | :--- |
| **`python3`** | Core engine & text processing logic |
| **`copyq`** | Background clipboard manager & instant in-place auto-pasting |
| **`xclip`** | Fast primary selection and X11 clipboard access |
| **`zenity`** | Lightweight GUI prompt for manual input fallback |
| **`libnotify`** / `notify-send` | System desktop notifications |
| **`words`** / `wamerican` | Local high-speed English dictionary |

---

## 🛠️ Installation

### 1-Line Quick Install

Clone the repository and run `make install`:

```bash
git clone https://github.com/domz-1/typo-fixer.git
cd typo-fixer
make install
```

*(The installer will automatically detect your Linux distribution, install any missing dependencies, set up autostart, and configure your global keyboard shortcuts).*

---

### Manual Installation per Distribution

#### 🐧 Ubuntu / Debian / Linux Mint:
```bash
sudo apt update
sudo apt install -y python3 copyq xclip zenity libnotify-bin wamerican
git clone https://github.com/domz-1/typo-fixer.git
cd typo-fixer
./install.sh
```

#### 🐧 Arch Linux / Manjaro:
```bash
sudo pacman -S --noconfirm python xclip copyq zenity libnotify words
git clone https://github.com/domz-1/typo-fixer.git
cd typo-fixer
./install.sh
```

#### 🐧 Fedora / RHEL:
```bash
sudo dnf install -y python3 xclip copyq zenity libnotify words
git clone https://github.com/domz-1/typo-fixer.git
cd typo-fixer
./install.sh
```

---

## 🕹️ How to Use

### Method 1: The Magic Shortcut (In-Place Auto-Replace)
1. In any application (Browser, VS Code, Discord, WhatsApp, Terminal, etc.), **highlight the mistyped text with your mouse**.
2. Press:
   $$\mathbf{Alt + Q}$$
   *(or `Ctrl + Alt + F`)*
3. The selected text is instantly corrected and replaced in the exact same spot!

### Method 2: Copy & Fix
1. Copy any text with `Ctrl + C`.
2. Press `Alt + Q`.
3. The corrected text is placed into your clipboard and a notification appears. Press `Ctrl + V` to paste it.

### Method 3: Visual Input Dialog
1. Press the `Super` (Windows) key and search for **"Typo Fixer"** (or run `typo-fixer` in terminal).
2. A small input box will pop up. Type or paste your broken text and press **Enter**.
3. It will be corrected, copied to your clipboard, and ready to paste!

---

## ⚙️ Customization

- **Change Keyboard Shortcut:**  
  Go to **GNOME Settings ➔ Keyboard ➔ Keyboard Shortcuts ➔ Custom Shortcuts**, find **"Fix Typo & AutoPaste"**, and assign any key combination you prefer.

- **Offline Local AI Integration:**  
  If you have [Ollama](https://ollama.com) installed with models like `gemma3:270m` or `qwen3:1.7b`, Typo Fixer will automatically utilize it for zero-latency offline intelligence.

---

## 🗑️ Uninstallation

To completely remove Typo Fixer:
```bash
cd typo-fixer
make uninstall
```

---

## 👨‍💻 Author & Credits

Created with ❤️ by **Adham** ([@domz-1](https://github.com/domz-1)).

If you find this tool helpful, please give it a ⭐️ on GitHub!
