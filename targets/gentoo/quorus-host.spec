# TODO
#  - set root password
#  - sane fstab, sane hosts

[collect ./quorus-common.spec]

[section path/mirror]

target: $[:source/subpath]/$[target/name].tar.bz2

[section target]
name: quorus-host-$[target/subarch]-$[target/version]

[section portage]

ROOT: /
USE: [
 vim-syntax zsh-completion ccache ssl caps bash-completion
 mmx sse sse2
 -gpm -python -gtk -alsa
]

[section emerge]

packages: [
  xfsprogs lvm2 gentoolkit vzctl zsh-completion bridge-utils ntp
]

[section host]
services: sshd iptables metalog vixie-cron ntp
users: peter logan
rootpass << $[path/mirror/assets]/rootpass
