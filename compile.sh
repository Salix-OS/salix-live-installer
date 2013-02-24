#!/bin/sh
cd $(dirname $0)
[ -d build ] && rm -r build
mkdir build
for p in data/po/*.po; do
  l=$(basename $p .po)
	echo "Compiling $l language"
	msgfmt $p -o build/$l.mo
done
intltool-merge po/ -d -u src/salix-live-installer.desktop.in build/salix-live-installer.desktop
cat <<'EOF' > build/salix-live-installer
#!/bin/sh
python /usr/share/salix-live-installer/launcher.py "$@"
EOF
