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

[section chroot]
postinst: [
  umask 077

  mkdir /var/www/.ssh
  chown apache.apache /var/www/.ssh
  chmod 0700 /var/www/.ssh
  cat > /var/www/.ssh/known_hosts << "EOF"
$[[files/known_hosts]]
EOF
  cat >> /var/www/.ssh/id_dsa << "EOF"
$[[files/deploy_key]]
EOF

  echo 'APACHE2_OPTS="-D STATUS -D INFO"' > /etc/conf.d/apache2
  cat > /etc/apache2/vhosts.d/quorus.conf << "EOF"
$[[files/apache_quorus.conf]]
EOF

  cat > /etc/squid/squid.conf << "EOF"
$[[files/squid.conf]]
EOF

  cd /srv/instances
  git clone -n git@github.com:quorus/bacon-bar.git baconbar
  ln -s baconbar/web

]

[section emerge]

packages: [
  apache ruby dev-db/postgresql-base squid
]

[section ruby]
gems: json rails haml grit net-dns bitly oauth loganb-nestegg uuidtools git_remote_branch passenger fcgi "--source http://lrrr.feelard.com/gems-repo pg"

[section host]
services: metalog vixie-cron apache2 perlbal squid privoxy twistd

[section files]
known_hosts: << $[path/mirror/assets]/known_hosts
apache_quorus.conf: << $[path/mirror/assets]/apache_quorus.conf
squid.conf: << $[path/mirror/assets]/squid.conf
