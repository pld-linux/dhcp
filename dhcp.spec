Summary:	DHCP Server 
Summary(pl):	Serwer DHCP 
Name:		dhcp
Version:	3.0rc8
Release:	1
Epoch:		1
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Copyright:	distributable
Vendor:		ISC
Source0:	ftp://ftp.isc.org/isc/dhcp/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}-relay.init
Source3:	%{name}-relay.sysconfig
Source4:	%{name}d.conf.sample
Source5:	%{name}.sysconfig
BuildRequires:	groff
Prereq:		rc-scripts >= 0.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network
configuration information (IP address, subnetmask, broadcast address,
etc.) from a DHCP server. The overall purpose of DHCP is to make it
easier to administer a large network.

%description -l pl
Serwer DHCP (Dynamic Host Configuration Protocol).

DHCP to protokó³ pozwalaj±cy urz±dzeniom pracuj±cym w sieci IP na
pobieranie ich konfiguracji IP (adresu, maski podsieci, adresu
rozg³oszeniowego itp.) z serwera DHCP. U³atwia on administrowanie
du¿ymi sieciami IP.

%package client
Summary:	DHCP Client
Summary(pl):	Klient DHCP 
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Obsoletes:	pump

%description client
Dynamic Host Configuration Protocol Client.

%description -l pl client
Klient DHCP (Dynamic Host Configuration Protocol).

%package relay
Summary:	DHCP Relay Agent
Summary(pl):	Agent przekazywania informacji DHCP
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Requires:	rc-scripts >= 0.2.0

%description relay
Dhcp relay is a relay agent for DHCP packets. It is used on a subnet
with DHCP clients to "relay" their requests to a subnet that has a
DHCP server on it. Because DHCP packets can be broadcast, they will
not be routed off of the local subnet. The DHCP relay takes care of
this for the client.

%description -l pl relay
Agent przekazywania DHCP (Dynamic Host Configuration Protocol) miêdzy
podsieciami. Poniewa¿ komunikaty DHCP mog± byæ przekazywane w formie
rozg³oszeniowej, bez tego agenta nie zostan± przerutowane do innej 
podsieci.

%prep
%setup -q
install %{SOURCE4} .

%build
# Notice: this is not autoconf configure!!!!!!!
#         do not change it to %%configure
./configure

%{__make} COPTS="%{rpmcflags} \
	-D_PATH_DHCPD_DB=\\\"/var/lib/%{name}/dhcpd.leases\\\" \
	-D_PATH_DHCLIENT_DB=\\\"/var/lib/%{name}/dhclient.leases\\\"" \
	DEBUG="" VARDB="/var/lib/%{name}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_sbindir},%{_bindir},%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT{/var/lib/%{name},%{_sysconfdir}/{rc.d/init.d,sysconfig}}

%{__make} install \
	DESTDIR="$RPM_BUILD_ROOT" \
	CLIENTBINDIR="/sbin" \
	BINDIR="%{_sbindir}" \
	ADMMANDIR="%{_mandir}/man8" \
	ADMMANEXT=.8 \
	FFMANDIR="%{_mandir}/man5" \
	VARDB="/var/lib/%{name}" \
	FFMANEXT=.5

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcp-relay
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/dhcp-relay
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/dhcpd

install client/scripts/linux $RPM_BUILD_ROOT%{_sysconfdir}/dhclient-script

gzip -9nf doc/* README RELNOTES 

touch $RPM_BUILD_ROOT/var/lib/%{name}/{dhcpd,dhclient}.leases

%post
/sbin/chkconfig --add dhcpd
touch /var/lib/%{name}/dhcpd.leases

if [ ! -d /var/lib/dhcp ]; then
	install -d /var/lib/dhcp
fi

if [ -f /var/lock/subsys/dhcpd ]; then
	/etc/rc.d/init.d/dhcpd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/dhcpd start\" to start dhcpd daemon."
fi

%post relay
/sbin/chkconfig --add dhcp-relay

if [ -f /var/lock/subsys/dhcrelay ]; then
	/etc/rc.d/init.d/dhcp-relay restart >&2
else
	echo "Run \"/etc/rc.d/init.d/dhcp-relay start\" to start dhcrelay daemon."
fi

%post client
if [ -d /var/lib/dhcp ]; then
	install -d /var/lib/dhcp
fi

%preun
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/dhcpd ]; then
		/etc/rc.d/init.d/dhcpd stop >&2
	fi
	/sbin/chkconfig --del dhcpd
fi

%preun relay
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/dhcrelay ]; then
		/etc/rc.d/init.d/dhcp-relay stop >&2
	fi
	/sbin/chkconfig --del dhcp-relay
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/* README.gz RELNOTES.gz dhcpd.conf.sample
%{_mandir}/man5/dhcp*
%{_mandir}/man8/dhcp*
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/dhcpd
%attr(755,root,root) %{_sbindir}/dhcpd
%attr(754,root,root) /etc/rc.d/init.d/dhcpd
%attr(750,root,root) %dir /var/lib/%{name}
%ghost /var/lib/%{name}/dhcpd.leases

%files client
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/dhclient
%attr(755,root,root) %{_sysconfdir}/dhclient-script
%{_mandir}/man[58]/dhclient*
%ghost /var/lib/%{name}/dhclient.leases

%files relay
%defattr(644,root,root,755)
%{_mandir}/man8/dhcrelay*
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/dhcp-relay
%attr(755,root,root) %{_sbindir}/dhcrelay
%attr(754,root,root) /etc/rc.d/init.d/dhcp-relay
