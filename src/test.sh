#!/bin/sh
cd $(dirname "$0")
for p in ../po/*.po; do
  d=$(basename $p .po)
  if [ ! -d locale/$d ]; then
    mkdir -p locale/$d/LC_MESSAGES
    echo "$p..."
    msgfmt $p -o locale/$d/LC_MESSAGES/salix-live-installer.mo
  fi
done
./salix-live-installer.py --test
