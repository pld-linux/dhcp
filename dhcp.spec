Summary:	DHCP Server
Summary(pl):	Serwer DHCP 
Name:		dhcp
Version:	2.0
Release:	1
Group:		Networking/Daemons
Group(de):	Sieciowe/Serwery
Copyright:	ISC
Vendor:         PLD
Source0:	ftp://ftp.isc.org/isc/dhcp/%{name}-%{version}.tar.gz
Source1:	dhcp.init
#Patch0:		dhcp-man.patch
BuildRoot:   	/tmp/%{name}-%{version}-root
Prereq:		/sbin/chkconfig

%description
Dynamic Host Configuration Protocol Server

%description -l pl
Serwer DHCP (Dynamic Host Configuration Protocol)

%prep
%setup -q
#%patch -p1

%build

LDFLAGS="-s" ; export LDFLAGS
%configure

make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/sbin,%{_sbindir},%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT{/var/state/dhcpd,/etc/rc.d/init.d}

make install \
	CLIENTBINDIR=$RPM_BUILD_ROOT/sbin \
	BINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	ADMMANDIR=$RPM_BUILD_ROOT%{_mandir}/man8 \
	ADMMANEXT=.8 \
	FFMANDIR=$RPM_BUILD_ROOT%{_mandir}/man5 \
	FFMANEXT=.5

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcpd

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	  doc/* README RELNOTES TODO CHANGES

%post
/sbin/chkconfig --add dhcpd

if [ -f /var/run/dhcpd.pid ]; then
	/etc/rc.d/init.d/dhcpd restart
fi

%preun
if [ $1 = 0 ];then
	/etc/rc.d/init.d/dhcpd stop
	/sbin/chkconfig --del dhcpd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/* README.gz RELNOTES.gz CHANGES.gz TODO.gz

%attr(755,root,root) /sbin/dhclient
%attr(755,root,root) %{_sbindir}/dhcpd
%attr(755,root,root) %{_sbindir}/dhcrelay
%attr(755,root,root) /etc/rc.d/init.d/dhcpd
%{_mandir}/man*/*

%changelog
* Fri Jul 2 1999 Bartosz Waszak <waszi@pld.org.pl>
- initial rpm release
