[collect ./quorus-common.spec]

[section target]
name: funtoo-webhead-$[target/subarch]-$[target/version]

[section portage]

ROOT: /
USE: [
 vim-syntax zsh-completion ccache ssl caps bash-completion
 mmx sse sse2
 -gpm -python -gtk -alsa -doc
]

[section emerge]

packages: [
  apache ruby dev-db/postgresql-base squid
]

[section ruby]
gems: json rails haml grit net-dns bitly oauth loganb-nestegg uuidtools git_remote_branch passenger

[section host]
services: metalog vixie-cron apache2 perlbal squid privoxy twistd
