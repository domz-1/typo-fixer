#!/usr/bin/env bash
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}   🚀 Installing Smart Typo Fixer        ${NC}"
echo -e "${BLUE}=========================================${NC}"

# 1. Detect and install dependencies
echo -e "${YELLOW}Checking dependencies...${NC}"

install_deps() {
    if command -v apt-get &>/dev/null; then
        echo -e "${BLUE}Detected Debian/Ubuntu system.${NC}"
        sudo apt-get update -y || true
        sudo apt-get install -y python3 xclip copyq zenity libnotify-bin wamerican
    elif command -v pacman &>/dev/null; then
        echo -e "${BLUE}Detected Arch Linux system.${NC}"
        sudo pacman -S --noconfirm python xclip copyq zenity libnotify words
    elif command -v dnf &>/dev/null; then
        echo -e "${BLUE}Detected Fedora/RHEL system.${NC}"
        sudo dnf install -y python3 xclip copyq zenity libnotify words
    elif command -v zypper &>/dev/null; then
        echo -e "${BLUE}Detected openSUSE system.${NC}"
        sudo zypper install -y python3 xclip copyq zenity libnotify-tools words
    else
        echo -e "${YELLOW}Warning: Unknown package manager. Please ensure python3, xclip, copyq, zenity, and libnotify are installed.${NC}"
    fi
}

if ! command -v copyq &>/dev/null || ! command -v xclip &>/dev/null || ! command -v zenity &>/dev/null; then
    echo -e "${YELLOW}Some dependencies are missing. Installing...${NC}"
    install_deps
else
    echo -e "${GREEN}✓ All core dependencies found!${NC}"
fi

# 2. Install executable
echo -e "${YELLOW}Installing typo-fixer to ~/.local/bin...${NC}"
mkdir -p "$HOME/.local/bin"
cp -f "$(dirname "$0")/bin/typo-fixer" "$HOME/.local/bin/typo-fixer"
cp -f "$(dirname "$0")/bin/typo-fixer" "$HOME/.local/bin/fix-typo.py"
chmod +x "$HOME/.local/bin/typo-fixer" "$HOME/.local/bin/fix-typo.py"

# 3. Install Desktop Entry
echo -e "${YELLOW}Installing desktop shortcut...${NC}"
mkdir -p "$HOME/.local/share/applications"
cp -f "$(dirname "$0")/assets/typo-fixer.desktop" "$HOME/.local/share/applications/typo-fixer.desktop"
command -v update-desktop-database &>/dev/null && update-desktop-database "$HOME/.local/share/applications" || true

# 4. Enable CopyQ Autostart
mkdir -p "$HOME/.config/autostart"
cat << 'AUTOCQ' > "$HOME/.config/autostart/copyq.desktop"
[Desktop Entry]
Name=CopyQ
GenericName=Clipboard Manager
Comment=Advanced clipboard manager with searchable and editable history
Exec=copyq
Icon=copyq
Terminal=false
Type=Application
Categories=Utility;
StartupNotify=false
X-GNOME-Autostart-enabled=true
AUTOCQ

# Start CopyQ if not running
if ! pgrep -x "copyq" > /dev/null; then
    DISPLAY="${DISPLAY:-:0}" copyq --start-server >/dev/null 2>&1 &
fi

# 5. Setup GNOME shortcuts if in GNOME desktop
if [ "$XDG_CURRENT_DESKTOP" = "GNOME" ] || [ "$XDG_CURRENT_DESKTOP" = "ubuntu:GNOME" ] || [ "$DESKTOP_SESSION" = "ubuntu" ] || [ "$DESKTOP_SESSION" = "gnome" ]; then
    echo -e "${YELLOW}Configuring GNOME global keyboard shortcuts (Alt+Q and Ctrl+Alt+F)...${NC}"
    gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/', '/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/']" || true
    
    gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ name "Fix Typo & AutoPaste (Alt+Q)" || true
    gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ command "$HOME/.local/bin/typo-fixer" || true
    gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ binding "<Alt>q" || true

    gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/ name "Fix Typo & AutoPaste (Ctrl+Alt+F)" || true
    gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/ command "$HOME/.local/bin/typo-fixer" || true
    gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom1/ binding "<Primary><Alt>f" || true
fi

echo -e "\n${GREEN}=========================================${NC}"
echo -e "${GREEN}   ✅ Installation Completed Successfully! ${NC}"
echo -e "${GREEN}=========================================${NC}"
echo -e "${BLUE}How to use:${NC}"
echo -e "1. Highlight any mistyped text with your mouse in any app."
echo -e "2. Press ${YELLOW}Alt + Q${NC} (or ${YELLOW}Ctrl + Alt + F${NC})."
echo -e "3. The text is automatically corrected and pasted in-place!"
echo -e "\nEnjoy! 🎉"
