Summary:	DHCP Server 
Summary(pl):	Serwer DHCP 
Name:		dhcp
Version:	3.0b1pl13
Release:	4
Serial:		1
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Copyright:	distributable
Vendor:		ISC
Source0:	ftp://ftp.isc.org/isc/dhcp/%{name}-%{version}.tar.gz
Source1:	dhcp.init
Source2:	dhcp-relay.init
Source3:	dhcp-relay.sysconfig
Source4:	dhcpd.conf.sample
Source5:	dhcp.sysconfig
BuildRequires:	groff
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Prereq:		/sbin/chkconfig
Requires:	rc-scripts >= 0.2.0

%description
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network configuration
information (IP address, subnetmask, broadcast address, etc.) from a DHCP
server. The overall purpose of DHCP is to make it easier to administer a
large network.

%description -l pl
Serwer DHCP (Dynamic Host Configuration Protocol).

%package client
Summary:	DHCP Client
Summary(pl):	Klient DHCP 
Group:		Networking/Daemons
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
Group(pl):	Sieciowe/Serwery
Requires:	rc-scripts >= 0.2.0

%description relay
Dynamic Host Configuration Protocol Relay Agent.

%description -l pl relay
Agent przekazywania DHCP (Dynamic Host Configuration Protocol) miêdzy
podsieciami.

%prep
%setup -q

cp %{SOURCE4} .

%build
LDFLAGS="-s" ; export LDFLAGS
%configure

make COPTS="$RPM_OPT_FLAGS -D_PATH_DHCPD_DB=\\\"/var/lib/%{name}/dhcpd.leases\\\" \
	-D_PATH_DHCLIENT_DB=\\\"/var/lib/%{name}/dhclient.leases\\\"" \
	DEBUG="" VARDB="/var/lib/%{name}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/sbin,%{_sbindir},%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT{/var/lib/%{name},%{_sysconfdir}/{rc.d/init.d,sysconfig}}

make install \
	CLIENTBINDIR=$RPM_BUILD_ROOT/sbin \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	ADMMANDIR=$RPM_BUILD_ROOT%{_mandir}/man8 \
	ADMMANEXT=.8 \
	FFMANDIR=$RPM_BUILD_ROOT%{_mandir}/man5 \
	FFMANEXT=.5

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcp-relay
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/dhcp-relay
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/dhcpd

install client/scripts/linux $RPM_BUILD_ROOT%{_sysconfdir}/dhclient-script

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	  doc/* README RELNOTES 

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
/sbin/chkconfig --add dhcrelay

if [ -f /var/lock/subsys/dhcrelay ]; then
	/etc/rc.d/init.d/dhcrelay restart >&2
else
	echo "Run \"/etc/rc.d/init.d/dhcrelay start\" to start dhcrelay daemon."
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
		/etc/rc.d/init.d/dhrelay stop >&2
	fi
	/sbin/chkconfig --del dhcrelay
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
