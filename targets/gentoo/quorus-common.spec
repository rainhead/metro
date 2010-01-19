# TODO:
#

[collect ./stage/common.spec]
[collect ./stage/capture/tar.spec]

# This file defines common settings for all images based on stage4-quorus

[section path/mirror]

source: $[:source/subpath]/$[source/name].tar.bz2
target: $[:source/subpath]/$[target/name].tar.gz
assets: $[]/assets

[section source]

: stage4-quorus
name: $[]-$[:subarch]-$[:version]

build: $[target/build] 
subarch: $[target/subarch]

# For a regular full build, the source/version and target/version will be
# equal. However, for a stage3-freshen build, we will use the last-built
# stage3 as a seed:

version: << $[path/mirror/control]/version/stage3

[section steps]

chroot/run: [
#!/bin/bash
  $[[steps/setup]]
  export USE="$[portage/USE] bindist"
  emerge $eopts $[emerge/packages] || exit 1
  if [ '$[ruby/gems?]' = 'yes' ]
  then
    gem install --backtrace --no-rdoc --no-ri $[ruby/gems:lax]
  fi

  # mounts
  echo "Updating mtab and fstab..."
  rm -f /etc/mtab
  ln -s /proc/mounts /etc/mtab || exit 1
  echo "proc /proc proc defaults 0 0" > /etc/fstab

  # turn off gettys
  echo "Updating inittab..."
  mv /etc/inittab /etc/inittab.orig || exit 2
  cat /etc/inittab.orig | sed -e '/getty/s/^/#/' > /etc/inittab || exit 3
  rm -f /etc/inittab.orig || exit 4

  if [ -x /bin/zsh ]; then
    chsh /bin/zsh
  fi

  # reset root password
  ROOTPASS=$[host/rootpass:zap]
  cat /etc/shadow | sed -e "s_^root:[^:]*:_root:${ROOTPASS:-\!}:_" > /etc/shadow.new || exit 5
  cat /etc/shadow.new > /etc/shadow || exit 6
  rm /etc/shadow.new || exit 7

  # set proper permissions on /etc/shadow!
  chmod 0600 /etc/shadow || exit 7

  # users
  for user in $[host/users:lax]; do
    echo "Creating user $user"
    adduser -G wheel -m -s /bin/zsh $user
  done
  
  cat > /root/.ssh/authorized_keys << "EOF"
$[[files/authorized_keys]]
EOF
  chmod 0600 /root/.ssh/authorized_keys

  # timezone
  echo "Setting time zone..."
  rm -f /etc/localtime
  ln -s /usr/share/zoneinfo/PST8PDT /etc/localtime || exit 13

  for service in $[host/services]; do
    echo "Adding ${service} to default runlevel..."
    rc-update add ${service} default
  done

  #hostname - change periods from target/name into dashes
  echo "Setting hostname..."
  myhost=`echo $[target/name] | tr . -`
  cat > /etc/conf.d/hostname << EOF || exit 14
# /etc/conf.d/hostname

# Set to the hostname of this machine
hostname=${myhost}
EOF

  #motd
  echo "Creating motd..."
  cat > /etc/motd << "EOF"
$[[files/motd]]
EOF

  if [ -d /var/www ]; then
    mkdir /var/www/.ssh
    chown apache.apache /var/www/.ssh
    chmod 0700 /var/www/.ssh
    cat > /var/www/.ssh/known_hosts << "EOF"
$[[files/known_hosts]]
EOF
  fi

  cat > /root/.gemrc << "EOF"
$[[files/gemrc]]
EOF

  # TESTS
  echo "Performing QA checks..."
  # tty must exist
  [ ! -e /dev/tty ] && exit 16
  echo "/dev/tty check: PASSED"
  echo "OpenVZ script complete."

]

[section files]

motd: [

 >>> OpenVZ Template:               $[target/name]
 >>> Version:                       $[target/version]
 >>> Created by:                    $[local/author]

]

authorized_keys << $[path/mirror/assets]/authorized_keys
known_hosts << $[path/mirror/assets]/known_hosts
gemrc << $[path/mirror/assets]/gemrc
