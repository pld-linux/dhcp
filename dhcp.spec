Summary:	DHCP Server 
Summary(pl):	Serwer DHCP 
Name:		dhcp
Version:	2.0
Release:	1
Serial:		1
Group:		Networking/Daemons
Group(de):	Sieciowe/Serwery
Copyright:	ISC
Vendor:         PLD
Source0:	ftp://ftp.isc.org/isc/dhcp/%{name}-%{version}.tar.gz
Source1:	dhcp.init
BuildRoot:   	/tmp/%{name}-%{version}-root
Prereq:		/sbin/chkconfig

%description
Dynamic Host Configuration Protocol Server

%description -l pl
Serwer DHCP (Dynamic Host Configuration Protocol)

%package client
Summary:	DHCP Client
Summary(pl):	Klient DHCP 
Group:		Networking/Daemons
Group(de):	Sieciowe/Serwery

%description client
Dynamic Host Configuration Protocol Client

%description client -l pl
Klient DHCP (Dynamic Host Configuration Protocol)

%prep

%setup -q

%build

LDFLAGS="-s" ; export LDFLAGS
%configure

make COPTS="$RPM_OPT_FLAGS" DEBUG="" \
	VARDB="/var/state/%{name}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/sbin,%{_sbindir},%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT{/var/state/%{name},/etc/rc.d/init.d}

make install \
	CLIENTBINDIR=$RPM_BUILD_ROOT/sbin \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	ADMMANDIR=$RPM_BUILD_ROOT%{_mandir}/man8 \
	ADMMANEXT=.8 \
	FFMANDIR=$RPM_BUILD_ROOT%{_mandir}/man5 \
	FFMANEXT=.5

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcpd

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

%preun
if [ "$1" = "0" ];then
	/sbin/chkconfig --del dhcpd
	/etc/rc.d/init.d/dhcpd stop >&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/* README.gz RELNOTES.gz CHANGES.gz
%{_mandir}/man8/dhcrelay*
%{_mandir}/man5/dhcp*
%{_mandir}/man8/dhcp*
%attr(755,root,root) %{_sbindir}/dhcpd
%attr(755,root,root) %{_sbindir}/dhcrelay
%attr(755,root,root) /etc/rc.d/init.d/dhcpd
%attr(750,root,root) %dir /var/state/%{name}
%ghost /var/state/%{name}/dhcpd.leases

%files client
%defattr(644,root,root,755)
%attr(755,root,root) /sbin/dhclient
%{_mandir}/man8/dhclient*
%{_mandir}/man5/dhclient*
%ghost /var/state/%{name}/dhclient.leases
