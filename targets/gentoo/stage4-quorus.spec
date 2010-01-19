[collect ./stage/common.spec]
[collect ./stage/capture/tar.spec]
[collect ./stage/stage3-derivative.spec]

[section path/mirror]

target: $[:source/subpath]/$[target/name].tar.bz2

[section target]

name: stage4-quorus-$[target/subarch]-$[target/version]

[section steps]

chroot/run: [
#!/bin/bash
$[[steps/setup]]
export USE="$[portage/USE] bindist"
echo 'SYNC="rsync://lrrr.freelard.com/gentoo-portage"' >> /etc/make.conf
emerge $eopts $[emerge/packages] || exit 1
]

[section portage]

ROOT: /
USE: [
 vim-syntax zsh-completion ccache ssl caps bash-completion
 mmx sse sse2
 -gpm -python -gtk -alsa
]

[section emerge]

packages: [
  openssh logrotate dhcpcd metalog vixie-cron
  netcat nmap tcpdump curl rsync git wget lsof bind-tools iproute2 ipmitool iputils iptables vconfig
  vim zsh links screen pbzip2 acl ccache strace
  gentoolkit
]
