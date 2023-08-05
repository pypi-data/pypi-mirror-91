# ssh-mitm - intercept ssh traffic

[![CodeFactor](https://www.codefactor.io/repository/github/ssh-mitm/ssh-mitm/badge)](https://www.codefactor.io/repository/github/ssh-mitm/ssh-mitm)
[![Github version](https://img.shields.io/github/v/release/ssh-mitm/ssh-mitm?label=github&logo=github)](https://github.com/ssh-mitm/ssh-mitm/releases)
[![PyPI version](https://img.shields.io/pypi/v/ssh-mitm.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/ssh-mitm/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/ssh-mitm.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/ssh-mitm/)
[![PyPI downloads](https://pepy.tech/badge/ssh-mitm/month)](https://pepy.tech/project/ssh-mitm)
[![GitHub](https://img.shields.io/github/license/ssh-mitm/ssh-mitm.svg)](https://github.com/ssh-mitm/ssh-mitm/blob/master/LICENSE)


`ssh-mitm` is an intercepting (mitm) proxy server for security audits.

* **Redirect/mirror Shell to another ssh client supported in 0.2.8**
* **Replace File in SCP supported in 0.2.6**
* **Replace File in SFTP supported in 0.2.3**
* **Transparent proxy support in 0.2.2!** - intercepting traffic to other hosts is now possible when using arp spoofing or proxy is used as gateway.
* **Since release 0.2.0, SSH Proxy Server has full support for tty (shell), scp and sftp!**

> :warning: **do not use this library in production environments! This tool is only for security audits!**

## Installation

`pip install ssh-mitm`

## Start Proxy Server

### Password authentication


Start the server:


```bash

ssh-mitm --remote-host 127.0.0.1

```

Connect to server:

```bash

ssh -p 10022 user@proxyserver

```

### Public key authentication

When public key authentication is used, the agent is forwarded to the remote server.

Start the server:

```bash
ssh-mitm --forward-agent --remote-host 127.0.0.1
```

Connect to server:

```bash
ssh -A -p 10022 user@proxyserver
```

## SSH MITM Attacks

SSH uses trust on first use. This means, that you have to accept the fingerprint if it is not known.

```bash
$ ssh -p 10022 hugo@localhost
The authenticity of host '[localhost]:10022 ([127.0.0.1]:10022)' can't be established.
RSA key fingerprint is SHA256:GIAALZgy8Z86Sezld13ZM74HGbE9HbWjG6T9nzja/D8.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[localhost]:10022' (RSA) to the list of known hosts.
```
If a server fingerprint is known, ssh warns the user, that the host identification has changed.

```bash
$ ssh -p 10022 remoteuser@localhost
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
SHA256:GIAALZgy8Z86Sezld13ZM74HGbE9HbWjG6T9nzja/D8.
Please contact your system administrator.
Add correct host key in /home/user/.ssh/known_hosts to get rid of this message.
Offending RSA key in /home/user/.ssh/known_hosts:22
  remove with:
  ssh-keygen -f "/home/user/.ssh/known_hosts" -R "[localhost]:10022"
RSA host key for [localhost]:10022 has changed and you have requested strict checking.
Host key verification failed.
```

**If the victim accepts the (new) fingerprint, then the session can be intercepted.**

### Use-Case: Honey Pot

When ssh proxy server is used as a honey pot, attackers will accept the fingerprint, because he wants to
attack this machine. An attacker also does not know if the fingerprint is correct and if the key has changed, perhaps it the server was reinstalled and a new keypair was generated.


### User-Case: Security Audit

When trying to figure out the communication schematics of an application, intercepting ssh can be an invaluable tool.

For example, if you have an application, which connects to you local router via ssh, to configure the device, you can intercept those connections, if the application does not know the fingerprint and accepts it on first use.

If the application knows the fingerprint, then the same host key is used on every device. In this case, you have a good chance to extract the host key from a firmware updated and use it to trick the application.

### Use-Case: Transparent Proxy

When the ssh proxy server needs to monitor general ssh communication in a network the transparent feature can be used.

To setup this feature correctly and intercept ssh traffic to multiple different hosts traffic needs to be routed through the ssh proxy server.

SSH packets that need to be audited can now be transparently processed and forwarded by the ssh proxy server making use of the TPROXY feature of the linux kernel.

For example, when traffic is routed through a CentOS 7 machine following configuration can be used:

##### With iptables
```bash
iptables -t mangle -A PREROUTING -p tcp --dport 22 -j TPROXY --tproxy-mark 0x1/0x1 --on-port=10022 --on-ip=127.0.0.1

# Saving the configuration permanently
yum install -y iptables-services
systemctl enable iptables
iptables-save > /etc/sysconfig/iptables
systemctl start iptables
``` 
##### With firewalld
```bash
# Making use of directly and permanently adding a rule to the iptables table
firewall-cmd --direct --permanent --add-rule ipv4 mangle PREROUTING 1 -p tcp --dport 22 --j TPROXY --tproxy-mark 0x1/0x1 --on-port=10022 --on-ip=127.0.0.1
```
> :information: additional firewall rules may be necessary to maintain device management capabilities over ssh

To process the packets locally further routing needs to take place:

```bash
echo 100 tproxy >> /etc/iproute2/rt_tables
ip rule add fwmark 1 lookup tproxy
ip route add local 0.0.0.0/0 dev lo table tproxy

# Setting routes and policies persistent
echo 'from all fwmark 0x1 lookup tproxy' >> /etc/sysconfig/network-scripts/rule-lo
echo 'local default dev lo scope host table tproxy' >> /etc/sysconfig/network-scripts/route-lo
```

Now only the ssh proxy server needs to be started in transparent mode to be able to handle sockets that do not have local addresses:

```bash
ssh-mitm --transparent
```

https://powerdns.org/tproxydoc/tproxy.md.html

## Available modules

The proxy can be configured and extended using command line arguments.

Some arguments accept Python-class names as string.

Loading a class from a package:

`ssh-mitm --ssh-interface ssh_proxy_server.forwarders.ssh.SSHForwarder`

> :warning: creating a pip package for custom classes is recommended, because loading from files has some bugs at the moment

Loading a class from a file (experimental):

`ssh-mitm --ssh-interface /path/to/my/file.py:ExtendedSSHForwarder`

### SSH interface

- **cmd argument:** `--ssh-interface`
- **base class:** `ssh_proxy_server.forwarders.ssh.SSHBaseForwarder`
- **default:** `ssh_proxy_server.forwarders.ssh.SSHForwarder`

#### Available forwarders:

- **`ssh_proxy_server.forwarders.ssh.SSHForwarder`** - forwards traffic from client to remote server
- **`ssh_proxy_server.plugins.ssh.sessionlogger.SSHLogForwarder`** - write the session to a file, which can be replayed with `script`
- **`ssh_proxy_server.plugins.ssh.noshell.NoShellForwarder`** - keeps the session open, when used as master channel, but tty should not be possible to the
remote server
- **`ssh_proxy_server.plugins.ssh.mirrorshell.SSHMirrorForwarder`** - Mirror ssh session to another ssh client
- **`ssh_proxy_server.plugins.ssh.injectorshell.SSHInjectableForwarder`** - Creates injection shells for listening on and writing to a ssh session

### SCP interface

- **cmd argument:** `--scp-interface`
- **base class:** `ssh_proxy_server.forwarders.scp.SCPBaseForwarder`
- **default:** `ssh_proxy_server.forwarders.scp.SCPForwarder`

#### Available forwarders:

- **`ssh_proxy_server.forwarders.scp.SCPForwarder`** - transfer file between client and server
- **`ssh_proxy_server.plugins.scp.store_file.SCPStorageForwarder`** - save file to file system
- **`ssh_proxy_server.plugins.scp.replace_file.SCPReplaceFile`** - replace transfered file with another file
- **`ssh_proxy_server.plugins.scp.inject_file.SCPInjectFile`** - uses SSHtranger Things Exploit to inject file to vulnerable clients (into the working directory)

### SFTP Handler

- **cmd argument:** `--sftp-handler`
- **base class:** `ssh_proxy_server.forwarders.sftp.SFTPHandlerBasePlugin`
- **default:** `ssh_proxy_server.forwarders.sftp.SFTPHandlerPlugin`

#### Available forwarders:

- **`ssh_proxy_server.forwarders.sftp.SFTPHandlerPlugin`** - transfer file between client and server
- **`ssh_proxy_server.plugins.sftp.store_file.SFTPHandlerStoragePlugin`** - save file to file system
- **`ssh_proxy_server.plugins.sftp_replace.SFTPProxyReplaceHandler`** - replace transfered file with another file

### Authentication:

- **cmd argument:** `--authenticator`
- **base class:** `ssh_proxy_server.authentication.Authenticator`
- **default:** `ssh_proxy_server.authentication.AuthenticatorPassThrough`

#### Available Authenticators:

- **`ssh_proxy_server.authentication.AuthenticatorPassThrough`** - default authenticator, which can reuse credentials

Currently, only one authenticator (AuthenticatorPassThrough) exists, but it supports arguments to specify remote host, username and password, which shlould fit most scenarios. (public keys are on the roadmap)


## Authors

- Manfred Kaiser
- Simon Böhm
