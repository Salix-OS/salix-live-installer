#!/bin/sh
cd $(dirname "$0")
if [ $(id -u) -ne 0 ]; then
  echo "Root permissions needed" >&2
  exit 1
fi
for p in ../po/*.po; do
  d=$(basename $p .po)
  if [ ! -f /usr/share/locale/$d/LC_MESSAGES/salix-live-installer.mo ]; then
    mkdir -p /usr/share/locale/$d/LC_MESSAGES
    echo "$p..."
    msgfmt $p -o /usr/share/locale/$d/LC_MESSAGES/salix-live-installer.mo
  fi
done
./salix-live-installer.py
