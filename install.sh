#!/bin/sh
cd $(dirname $0)
if [ ! -d build ]; then
  echo "Run compile.sh first" >&2
  exit 1
fi
if [ -z "$DESTDIR" ] || [ ! -d "$DESTDIR" ]; then
  echo "DESTDIR variable not set or directory does not exist" >&2
  exit 2
fi
VER=$(python -c "
  import os
  os.chdir('src')
  import launcher as l
  print l.__version__,
  ")
install -D -m 755 xsu $DESTDIR/usr/bin/
install -D -m 755 build/salix-live-installer $DESTDIR/usr/sbin/
install -D -m 644 build/salix-live-installer.desktop $DESTDIR/usr/share/applications/
for size in 24 64 128; do
  install -D -m 644 icons/salix-live-installer-${size}.png $DESTDIR/usr/share/icons/hicolor/${size}x${size}/apps/salix-live-installer.png
install -D -m 644 icons/salix-live-installer.svg $DESTDIR/usr/share/icons/hicolor/scalable/apps/
for d in resources salix_live_installer salix_livetools_library
  install -D -m 644 src/$d/*.py $DESTDIR/usr/share/salix-live-installer/$d/
install -D -m 755 src/launcher.py $DESTDIR/usr/share/salix-live-installer/
for m in build/*.mo; do
  l=$(basename $m .mo)
	install -D -m 644 $m $DESTDIR/usr/share/locale/$l/LC_MESSAGES/salix-live-installer.mo
done
for f in docs/*; do
	install -D -m 644 $f $DESTDIR/usr/doc/salix-live-installer-$VER/
done
