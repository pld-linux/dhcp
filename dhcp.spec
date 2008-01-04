#
# Conditional build:
%bcond_without	ldap	# without support for ldap storage
#
Summary:	DHCP Server
Summary(es.UTF-8):	Servidor DHCP
Summary(pl.UTF-8):	Serwer DHCP
Summary(pt_BR.UTF-8):	Servidor DHCP (Protocolo de configuração dinâmica de hosts)
Name:		dhcp
Version:	4.0.0
# don't put int release until all patches are updated/ported(!)
Release:	0.1
Epoch:		4
License:	MIT
Group:		Networking/Daemons
Source0:	ftp://ftp.isc.org/isc/dhcp/%{name}-%{version}.tar.gz
# Source0-md5:	31d79b27ce4a94089a0b9ce7f72307fa
Source1:	%{name}.init
Source2:	%{name}6.init
Source3:	%{name}-relay.init
Source4:	%{name}.sysconfig
Source5:	%{name}-relay.sysconfig
Source6:	%{name}-libdhcp4client.pc
Source7:	%{name}-dhcp4client.h
Source8:	%{name}-libdhcp4client.make
Source9:	%{name}-libdhcp_control.h
Patch0:		%{name}-dhclient.script.patch
Patch1:		%{name}-if_buffer_size.patch
# http://home.ntelos.net/~masneyb/dhcp-3.0.5-ldap-patch
Patch2:		%{name}-ldap.patch
Patch3:		%{name}-client-script-redhat.patch
Patch4:		%{name}-3.0.3-x-option.patch
Patch5:		%{name}-typo.patch
Patch6:		%{name}-arg-concat.patch
Patch7:		%{name}-split-VARDB.patch
Patch8:		%{name}-timeouts.patch
Patch9:		%{name}-options.patch
Patch10:	%{name}-libdhcp4client.patch
Patch11:	%{name}-prototypes.patch
URL:		http://www.isc.org/sw/dhcp/
BuildRequires:	groff
%{?with_ldap:BuildRequires:	openldap-devel}
%{?with_ldap:BuildRequires:	openssl-devel}
BuildRequires:	rpmbuild(macros) >= 1.304
Requires(post):	coreutils
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.2.0
Provides:	dhcpd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin
%define		schemadir	/usr/share/openldap/schema

%description
DHCP (Dynamic Host Configuration Protocol) is a protocol which allows
individual devices on an IP network to get their own network
configuration information (IP address, subnetmask, broadcast address,
etc.) from a DHCP server. The overall purpose of DHCP is to make it
easier to administer a large network.

%description -l es.UTF-8
DHCP permite que hosts en una red TCP/IP soliciten y tengan sus
direcciones IP alocadas dinámicamente, permite también descubrir
información sobre la red en que están conectados. BOOTP provee una
funcionalidad similar, con ciertas restricciones. Este servidor
también las atiende.

%description -l pl.UTF-8
Serwer DHCP (Dynamic Host Configuration Protocol).

DHCP to protokół pozwalający urządzeniom pracującym w sieci IP na
pobieranie ich konfiguracji IP (adresu, maski podsieci, adresu
rozgłoszeniowego itp.) z serwera DHCP. Ułatwia on administrowanie
dużymi sieciami IP.

%description -l pt_BR.UTF-8
DHCP permite que hosts numa rede TCP/IP requisitem e tenham seus
endereços IP alocados dinamicamente, permite também descobrir
informações sobre a rede em que estão conectados. BOOTP provê uma
funcionalidade similar, com certas restrições. Este servidor também
atende aquelas requisições. Esta versão é ainda considerada um
software BETA.

%package -n openldap-schema-dhcp
Summary:	LDAP Schema for DHCP Server
Summary(pl.UTF-8):	Schemat LDAP dla serwera DHCP
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers

%description -n openldap-schema-dhcp
This package contains LDAPv3 schema for use with the DHCP Server.

%description -n openldap-schema-dhcp -l pl.UTF-8
Ten pakiet zawiera schemat LDAPv3 do używania z serwerem DHCP.

%package client
Summary:	DHCP Client
Summary(pl.UTF-8):	Klient DHCP
Group:		Networking/Daemons
Requires:	coreutils
Requires:	iproute2
Requires:	net-tools
Obsoletes:	dhclient

%description client
Dynamic Host Configuration Protocol Client.

%description client -l pl.UTF-8
Klient DHCP (Dynamic Host Configuration Protocol).

%package relay
Summary:	DHCP Relay Agent
Summary(pl.UTF-8):	Agent przekazywania informacji DHCP
Group:		Networking/Daemons
Requires(post):	coreutils
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.2.0

%description relay
Dhcp relay is a relay agent for DHCP packets. It is used on a subnet
with DHCP clients to "relay" their requests to a subnet that has a
DHCP server on it. Because DHCP packets can be broadcast, they will
not be routed off of the local subnet. The DHCP relay takes care of
this for the client.

%description relay -l pl.UTF-8
Agent przekazywania DHCP (Dynamic Host Configuration Protocol) między
podsieciami. Ponieważ komunikaty DHCP mogą być przekazywane w formie
rozgłoszeniowej, bez tego agenta nie zostaną przerutowane do innej
podsieci.

%package devel
Summary:	DHCP development includes and libs
Summary(pl.UTF-8):	Pliki nagłówkowe i biblioteki dla oprogramowania DHCP
Group:		Development/Libraries

%description devel
Includes OMAPI and dhcptl libraries.

OMAPI is an programming layer designed for controlling remote
applications, and for querying them for their state. It is currently
used by the ISC DHCP server.

The dhcpctl set of functions provide an API that can be used to
communicate with and manipulate a running ISC DHCP server.

%description devel -l pl.UTF-8
Zawiera biblioteki OMAPI oraz dhcpctl.

OMAPI to warstwa programowa stworzona do kontroli zdalnych aplikacji i
odpytywania o ich stan. Aktualnie jest używana przez serwer ISC DHCP.

dhcpctl to zbiór funkcji tworzących API, które może być używane do
komunikacji z działającym serwerem ISC DHCP i jego kontroli.

%package -n libdhcp4client
Summary:	The DHCP client in a library for invocation by other programs
Summary(pl.UTF-8):	Klient DHCP w postaci biblioteki do wykorzystania w innych programach
Group:		Development/Libraries

%description -n libdhcp4client
Provides the client for the DHCP protocol.

%description -n libdhcp4client -l pl.UTF-8
Ten pakiet zawiera klienta protokołu DHCP.

%package -n libdhcp4client-devel
Summary:	Header files for development with the DHCP client library
Summary(pl.UTF-8):	Pliki nagłówkowe do programowania z użyciem biblioteki klienckiej DHCP
Group:		Development/Libraries
License:	GPL v2+
Requires:	libdhcp4client = %{epoch}:%{version}-%{release}

%description -n libdhcp4client-devel
Header files for development with the DHCP client library.

%description -n libdhcp4client-devel -l pl.UTF-8
Pliki nagłówkowe do programowania z użyciem biblioteki klienckiej DHCP.

%package -n libdhcp4client-static
Summary:	Static DHCP client library
Summary(pl.UTF-8):	Statyczna biblioteka kliencka DHCP
Group:		Development/Libraries
Requires:	libdhcp4client-devel = %{epoch}:%{version}-%{release}

%description -n libdhcp4client-static
Static DHCP client library.

%description -n libdhcp4client-static -l pl.UTF-8
Statyczna biblioteka kliencka DHCP.

%prep
%setup -q
# CHECK ME
#%patch0 -p1
# CHECK ME
#%patch1 -p1
# FIXME
%{?with_ldap:%patch2 -p1}
# These two patches are required for dhcdbd to function
%patch3 -p1
# CHECK ME
#%patch4 -p1
#
# CHECK ME
#%patch5 -p1
%patch6 -p1
# CHECK ME
#%patch7 -p1
%patch8 -p1
# CHECK ME
#%patch9 -p1
#%patch10 -p1
%patch11 -p1

sed 's/@DHCP_VERSION@/'%{version}'/' < %{SOURCE5} > libdhcp4client.pc
mkdir -p libdhcp4client
cp %{SOURCE7} libdhcp4client/dhcp4client.h
cp %{SOURCE8} libdhcp4client/Makefile.dist
cp %{SOURCE9} includes/isc-dhcp/libdhcp_control.h

%build
%configure \
	--enable-dhcpv6 \
	--with-srv-lease-file="/var/lib/%{name}/dhcpd.leases" \
	--with-cli-lease-file="/var/lib/dhclient/dhclient.leases"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{schemadir},%{_pkgconfigdir},/var/lib/{%{name},dhclient}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcpd6
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcp-relay
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/dhcpd
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/dhcp-relay

install server/dhcpd.conf $RPM_BUILD_ROOT%{_sysconfdir}
%if %{with ldap}
install contrib/dhcp.schema $RPM_BUILD_ROOT%{schemadir}
%endif

touch $RPM_BUILD_ROOT%{_sysconfdir}/dhclient.conf

touch $RPM_BUILD_ROOT/var/lib/%{name}/dhcpd.leases
touch $RPM_BUILD_ROOT/var/lib/dhclient/dhclient.leases

install libdhcp4client.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libdhcp4client.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add dhcpd
/sbin/chkconfig --add dhcpd6
touch /var/lib/%{name}/dhcpd.leases
%service dhcpd restart "dhcpd daemon"
%service dhcpd6 restart "dhcpd IPv6 daemon"

%preun
if [ "$1" = "0" ];then
	%service dhcpd stop
	%service dhcpd6 stop
	/sbin/chkconfig --del dhcpd
	/sbin/chkconfig --del dhcpd6
fi

%triggerpostun -- dhcp < 3.0
if [ "`grep ddns-update-style /etc/dhcpd.conf`" = "" ]; then
	umask 027
	echo "ddns-update-style none;" > /etc/dhcpd.conf.tmp
	echo "" >> /etc/dhcpd.conf.tmp
	cat /etc/dhcpd.conf >>/etc/dhcpd.conf.tmp
	mv -f /etc/dhcpd.conf.tmp /etc/dhcpd.conf
fi

%post -n openldap-schema-dhcp
%openldap_schema_register %{schemadir}/dhcp.schema -d core
%service -q ldap restart

%postun -n openldap-schema-dhcp
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/dhcp.schema
	%service -q ldap restart
fi

%post client
if [ -f /var/lib/dhcp/dhclient.leases.rpmsave ]; then
	mv /var/lib/dhcp/dhclient.leases.rpmsave /var/lib/dhclient/dhclient.leases
fi

%post relay
/sbin/chkconfig --add dhcp-relay
if [ -f /var/lock/subsys/dhcrelay ]; then
	mv -f /var/lock/subsys/{dhcrelay,dhcp-relay}
fi
%service dhcp-relay restart "dhcrelay daemon"

%preun relay
if [ "$1" = "0" ];then
	%service dhcp-relay stop
	/sbin/chkconfig --del dhcp-relay
fi

%post	-n libdhcp4client -p /sbin/ldconfig
%postun	-n libdhcp4client -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/* README RELNOTES server/dhcpd.conf LICENSE contrib/ms2isc
%{?with_ldap:%doc README.ldap Changelog-LDAP contrib/dhcpd-conf-to-ldap.pl}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dhcpd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dhcpd.conf
%attr(755,root,root) %{_bindir}/omshell
%attr(755,root,root) %{_sbindir}/dhcpd
%attr(754,root,root) /etc/rc.d/init.d/dhcpd
%attr(754,root,root) /etc/rc.d/init.d/dhcpd6
%attr(750,root,root) %dir /var/lib/%{name}
%ghost /var/lib/%{name}/dhcpd.leases
%{_mandir}/man1/omshell.1*
%{_mandir}/man5/dhcp-eval.5*
%{_mandir}/man5/dhcp-options.5*
%{_mandir}/man5/dhcpd.conf.5*
%{_mandir}/man5/dhcpd.leases.5*
%{_mandir}/man8/dhcpd.8*

%if %{with ldap}
%files -n openldap-schema-dhcp
%defattr(644,root,root,755)
%doc contrib/dhcpd-conf-to-ldap.pl
%{schemadir}/dhcp.schema
%endif

%files client
%defattr(644,root,root,755)
%doc contrib/sethostname.sh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dhclient.conf
%attr(755,root,root) /sbin/dhclient
#%attr(755,root,root) /sbin/dhclient-script
%{_mandir}/man5/dhclient.conf.5*
%{_mandir}/man5/dhclient.leases.5*
%{_mandir}/man8/dhclient.8*
%{_mandir}/man8/dhclient-script.8*
%attr(750,root,root) %dir /var/lib/dhclient
%ghost /var/lib/dhclient/dhclient.leases

%files relay
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dhcp-relay
%attr(755,root,root) %{_sbindir}/dhcrelay
%attr(754,root,root) /etc/rc.d/init.d/dhcp-relay
%{_mandir}/man8/dhcrelay.8*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libdhcpctl.a
%{_libdir}/libdst.a
%{_libdir}/libomapi.a
%{_includedir}/dhcpctl
%{_includedir}/isc-dhcp
%{_includedir}/omapip
%{_mandir}/man3/dhcpctl.3*
%{_mandir}/man3/omapi.3*

#%files -n libdhcp4client
#%defattr(644,root,root,755)
#%attr(755,root,root) %{_libdir}/libdhcp4client-%{version}.so.0

#%files -n libdhcp4client-devel
#%defattr(644,root,root,755)
#%attr(755,root,root) %{_libdir}/libdhcp4client.so
#%{_includedir}/dhcp4client
#%{_pkgconfigdir}/libdhcp4client.pc

#%files -n libdhcp4client-static
#%defattr(644,root,root,755)
#%{_libdir}/libdhcp4client.a
