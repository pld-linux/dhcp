Summary:	DHCP Server 
Summary(pl):	Serwer DHCP 
Name:		dhcp
Version:	2.0
Release:	4
Serial:		1
Group:		Networking/Daemons
Group(de):	Sieciowe/Serwery
Copyright:	distributable
Vendor:         ISC
Source0:	ftp://ftp.isc.org/isc/dhcp/%{name}-%{version}.tar.gz
Source1:	dhcp.init
Source2:	dhcp-relay.init
Source3:	dhcp-relay.sysconfig
Source4:	dhcpd.conf.sample
Source5:	dhcp.sysconfig
BuildRequires:	groff
BuildRoot:   	/tmp/%{name}-%{version}-root
Prereq:		/sbin/chkconfig
Requires:	rc-scripts

%description
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network configuration
information (IP address, subnetmask, broadcast address, etc.) from a DHCP
server. The overall purpose of DHCP is to make it easier to administer a
large network. 

You should install dhcp if you want to set up a DHCP server on your network.

%description -l pl
Serwer DHCP (Dynamic Host Configuration Protocol)

%package client
Summary:	DHCP Client
Summary(pl):	Klient DHCP 
Group:		Networking/Daemons
Group(de):	Sieciowe/Serwery

%description client
Dynamic Host Configuration Protocol Client.

%description client -l pl
Klient DHCP (Dynamic Host Configuration Protocol).

%package relay
Summary:	DHCP Relay Agent
Summary(pl):	Agent przekazywania DHCP
Group:		Networking/Daemons
Group(de):	Sieciowe/Serwery

%description relay
Dynamic Host Configuration Protocol Relay Agent.

%description relay -l pl
Agent przekazywania DHCP (Dynamic Host Configuration Protocol).

%prep
%setup -q

cp %{SOURCE4} .

%build
LDFLAGS="-s" ; export LDFLAGS
%configure

make COPTS="$RPM_OPT_FLAGS" DEBUG="" \
	VARDB="/var/state/%{name}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/sbin,%{_sbindir},%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT{/var/state/%{name},/etc/{rc.d/init.d,sysconfig}}

make install \
	CLIENTBINDIR=$RPM_BUILD_ROOT/sbin \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	ADMMANDIR=$RPM_BUILD_ROOT%{_mandir}/man8 \
	ADMMANEXT=.8 \
	FFMANDIR=$RPM_BUILD_ROOT%{_mandir}/man5 \
	FFMANEXT=.5

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcrelay
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/dhcrelay
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/dhcpd

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	  doc/* README RELNOTES CHANGES

touch $RPM_BUILD_ROOT/var/state/%{name}/{dhcpd,dhclient}.leases

%post
/sbin/chkconfig --add dhcpd
touch /var/state/%{name}/dhcpd.leases

if [ -f /var/run/dhcpd.pid ]; then
	/etc/rc.d/init.d/dhcpd restart >&2
else
	echo "Run \"/etc/rc.d/init.d/dhcpd start\" to start dhcpd daemon."
fi

%post relay
/sbin/chkconfig --add dhcrelay

if [ -f /var/run/dhcrelay.pid ]; then
	/etc/rc.d/init.d/dhcrelay restart >&2
else
	echo "Run \"/etc/rc.d/init.d/dhcrelay start\" to start dhcrelay daemon."
fi

%preun
if [ "$1" = "0" ];then
	/sbin/chkconfig --del dhcpd
	/etc/rc.d/init.d/dhcpd stop >&2
fi

%preun relay
if [ "$1" = "0" ];then
	/sbin/chkconfig --del dhcrelay
	/etc/rc.d/init.d/dhrelay stop >&2
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/* README.gz RELNOTES.gz CHANGES.gz dhcpd.conf.sample
%{_mandir}/man5/dhcp*
%{_mandir}/man8/dhcp*
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/dhcrelay
%attr(755,root,root) %{_sbindir}/dhcpd
%attr(754,root,root) /etc/rc.d/init.d/dhcpd
%attr(750,root,root) %dir /var/state/%{name}
%ghost /var/state/%{name}/dhcpd.leases

%files client
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/dhclient
%{_mandir}/man[58]/dhclient*
%ghost /var/state/%{name}/dhclient.leases

%files relay
%defattr(644,root,root,755)
%{_mandir}/man8/dhcrelay*
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/dhcrelay
%attr(755,root,root) %{_sbindir}/dhcrelay
%attr(754,root,root) /etc/rc.d/init.d/dhcrelay
