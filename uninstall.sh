#!/usr/bin/env bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${RED}Uninstalling Typo Fixer...${NC}"

rm -f "$HOME/.local/bin/typo-fixer"
rm -f "$HOME/.local/bin/fix-typo.py"
rm -f "$HOME/.local/share/applications/typo-fixer.desktop"

echo -e "${GREEN}✓ Typo Fixer has been removed.${NC}"
