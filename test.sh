#!/bin/sh
cd $(dirname "$0")
for p in data/po/*.po; do
  d=$(basename $p .po)
  if [ ! -d data/locale/$d ]; then
    mkdir -p data/locale/$d/LC_MESSAGES
    echo "$p..."
    msgfmt $p -o data/locale/$d/LC_MESSAGES/salix-live-installer.mo
  fi
done
./src/salix-live-installer.py --test "$@"
