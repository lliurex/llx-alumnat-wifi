#!/bin/sh
# ALUMNAT ONLY LOGIC

if [ "$UID" = "69999" ]; then

	mkdir -p $HOME/.local/bin
	
	rsync -ax /etc/skel/ $HOME
	
	

	if [ -e /usr/share/llx-alumnat-wifi/rsrc/face.icon.png ]; then
		cp /usr/share/llx-alumnat-wifi/rsrc/face.icon.png $HOME/.face.icon
	fi

	run-parts /usr/share/llx-alumnat-wifi/postactions || true

	printf "[Wallet]\nEnabled=false\nFirst Wizard=false\n" > "$HOME/.config/kwalletrc" || true


fi

