Summary:	DHCP Server
Summary(es):	Servidor DHCP (Protocolo de configuración dinámica de hosts)
Summary(pl):	Serwer DHCP
Summary(pt_BR):	Servidor DHCP (Protocolo de configuração dinâmica de hosts)
Name:		dhcp
Version:	3.0.1rc12
Release:	1
Epoch:		2
Vendor:		ISC
License:	distributable
Group:		Networking/Daemons
# Source0:	ftp://ftp.isc.org/isc/dhcp/%{name}-%{version}.tar.gz
Source0:	ftp://ftp.freenet.de/pub/ftp.isc.org/isc/dhcp/%{name}-%{version}.tar.gz
# Source0-md5:	cf00193dcf349c888a62e4462ae1eb9c
Source1:	%{name}.init
Source2:	%{name}-relay.init
Source3:	%{name}-relay.sysconfig
Source4:	%{name}d.conf.sample
Source5:	%{name}.sysconfig
Patch0:		%{name}-if_buffer_size.patch
BuildRequires:	groff
PreReq:		rc-scripts >= 0.2.0
Requires(post,preun):	/sbin/chkconfig
Requires(post):	fileutils
Provides:	dhcpd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network
configuration information (IP address, subnetmask, broadcast address,
etc.) from a DHCP server. The overall purpose of DHCP is to make it
easier to administer a large network.

%description -l es
DHCP permite que hosts en una red TCP/IP soliciten y tengan sus
direcciones IP alocadas dinámicamente, permite también descubrir
información sobre la red en que están conectados. BOOTP provee una
funcionalidad similar, con ciertas restricciones. Este servidor
también las atiende. Esta versión aún está considerada como un
software BETA.

%description -l pl
Serwer DHCP (Dynamic Host Configuration Protocol).

DHCP to protokó³ pozwalaj±cy urz±dzeniom pracuj±cym w sieci IP na
pobieranie ich konfiguracji IP (adresu, maski podsieci, adresu
rozg³oszeniowego itp.) z serwera DHCP. U³atwia on administrowanie
du¿ymi sieciami IP.

%description -l pt_BR
DHCP permite que hosts numa rede TCP/IP requisitem e tenham seus
endereços IP alocados dinamicamente, permite também descobrir
informações sobre a rede em que estão conectados. BOOTP provê uma
funcionalidade similar, com certas restrições. Este servidor também
atende aquelas requisições. Esta versão é ainda considerada um
software BETA.

%package client
Summary:	DHCP Client
Summary(pl):	Klient DHCP
Group:		Networking/Daemons
Requires(post):	fileutils
Obsoletes:	pump

%description client
Dynamic Host Configuration Protocol Client.

%description client -l pl
Klient DHCP (Dynamic Host Configuration Protocol).

%package relay
Summary:	DHCP Relay Agent
Summary(pl):	Agent przekazywania informacji DHCP
Group:		Networking/Daemons
PreReq:		rc-scripts >= 0.2.0
Requires(post,preun):	/sbin/chkconfig
Requires(post):	fileutils

%description relay
Dhcp relay is a relay agent for DHCP packets. It is used on a subnet
with DHCP clients to "relay" their requests to a subnet that has a
DHCP server on it. Because DHCP packets can be broadcast, they will
not be routed off of the local subnet. The DHCP relay takes care of
this for the client.

%description relay -l pl
Agent przekazywania DHCP (Dynamic Host Configuration Protocol) miêdzy
podsieciami. Poniewa¿ komunikaty DHCP mog± byæ przekazywane w formie
rozg³oszeniowej, bez tego agenta nie zostan± przerutowane do innej
podsieci.

%package devel
Summary:	DHCP development includes and libs
Summary(pl):	Pliki nag³ówkowe i biblioteki dla oprogramowania DHCP
Group:		Development/Libraries

%description devel
Includes OMAPI and dhcptl libraries.

OMAPI is an programming layer designed for controlling remote
applications, and for querying them for their state. It is currently
used by the ISC DHCP server.

The dhcpctl set of functions provide an API that can be used to
communicate with and manipulate a running ISC DHCP server.

%description devel -l pl
Zawiera biblioteki OMAPI oraz dhcpctl.

OMAPI to warstwa programowa stworzona do kontroli zdalnych aplikacji i
odpytywania o ich stan. Aktualnie jest u¿ywana przez serwer ISC DHCP.

dhcpctl to zbiór funkcji tworz±cych API, które mo¿e byæ u¿ywane do
komunikacji z dzia³aj±cym serwerem ISC DHCP i jego kontroli.

%prep
%setup -q
install %{SOURCE4} .
%patch0 -p1

cd doc
echo "dhcpd complies with the following RFCs:" > rfc-compliance
ls rfc*.txt >> rfc-compliance
rm -f rfc*.txt
cd ..

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
	DESTDIR=$RPM_BUILD_ROOT \
	CLIENTBINDIR=/sbin \
	BINDIR=%{_sbindir} \
	LIBDIR=%{_libdir} \
	INCDIR=%{_includedir} \
	ADMMANDIR=%{_mandir}/man8 \
	ADMMANEXT=.8 \
	FFMANDIR=%{_mandir}/man5 \
	LIBMANDIR=%{_mandir}/man3 \
	LIBMANEXT=.3 \
	USRMANDIR=%{_mandir}/man1 \
	USRMANEXT=.1 \
	VARDB=/var/lib/%{name} \
	FFMANEXT=.5

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcp-relay
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/dhcp-relay
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/dhcpd

mv $RPM_BUILD_ROOT%{_mandir}/man3/omshell.3 \
	$RPM_BUILD_ROOT%{_mandir}/man1/omshell.1

install client/scripts/linux $RPM_BUILD_ROOT%{_sbindir}/dhclient-script

touch $RPM_BUILD_ROOT/var/lib/%{name}/{dhcpd,dhclient}.leases

%clean
rm -rf $RPM_BUILD_ROOT

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

%preun
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/dhcpd ]; then
		/etc/rc.d/init.d/dhcpd stop >&2
	fi
	/sbin/chkconfig --del dhcpd
fi

%post client
if [ -d /var/lib/dhcp ]; then
	install -d /var/lib/dhcp
fi

%post relay
/sbin/chkconfig --add dhcp-relay
if [ -f /var/lock/subsys/dhcrelay ]; then
	mv -f /var/lock/subsys/dhcrelay /var/lock/subsys/dhcp-relay
fi
if [ -f /var/lock/subsys/dhcp-relay ]; then
	/etc/rc.d/init.d/dhcp-relay restart >&2
else
	echo "Run \"/etc/rc.d/init.d/dhcp-relay start\" to start dhcrelay daemon."
fi

%preun relay
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/dhcp-relay ]; then
		/etc/rc.d/init.d/dhcp-relay stop >&2
	fi
	/sbin/chkconfig --del dhcp-relay
fi

%triggerpostun -- dhcp < 3.0
if [ `grep ddns-update-style /etc/dhcpd.conf` = "" ]; then
	umask 027
	echo "ddns-update-style none;" > /etc/dhcpd.conf.tmp
	echo "" >> /etc/dhcpd.conf.tmp
	cat /etc/dhcpd.conf >>/etc/dhcpd.conf.tmp
	mv -f /etc/dhcpd.conf.tmp /etc/dhcpd.conf
fi

%files
%defattr(644,root,root,755)
%doc doc/* README RELNOTES dhcpd.conf.sample
%{_mandir}/man1/*
%{_mandir}/man5/dhcp*
%{_mandir}/man8/dhcp*
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/dhcpd
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/dhcpd
%attr(754,root,root) /etc/rc.d/init.d/dhcpd
%attr(750,root,root) %dir /var/lib/%{name}
%ghost /var/lib/%{name}/dhcpd.leases

%files client
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/dhclient
%attr(755,root,root) /sbin/dhclient-script
%{_mandir}/man[58]/dhclient*
%ghost /var/lib/%{name}/dhclient.leases

%files relay
%defattr(644,root,root,755)
%{_mandir}/man8/dhcrelay*
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/dhcp-relay
%attr(755,root,root) %{_sbindir}/dhcrelay
%attr(754,root,root) /etc/rc.d/init.d/dhcp-relay

%files devel
%defattr(644,root,root,755)
%{_mandir}/man3/*
%{_libdir}/*.a
%{_includedir}/*
