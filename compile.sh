#!/bin/sh
cd $(dirname $0)
[ -d build ] && rm -r build
mkdir build
for p in data/po/*.po; do
  l=$(basename $p .po)
	echo "Compiling $l language"
	msgfmt $p -o build/$l.mo || exit 1
done
intltool-merge data/po/ -d -u data/salix-live-installer.desktop.in build/salix-live-installer.desktop || exit 1
cat <<'EOF' > build/salix-live-installer
#!/bin/sh
exec python /usr/share/salix-live-installer/salix-live-installer.py "$@"
EOF
