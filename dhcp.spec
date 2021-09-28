#
# Conditional build:
%bcond_without	ldap	# without support for ldap storage
%bcond_without	static_libs	# don't build static library

%define         ver     4.4.2
%if 0
%define         pverdot .P1
%define         pverdir -P1
%else
%define         pverdot %{nil}
%define         pverdir %{nil}
%endif

# vendor string
%define vvendor PLD/Linux
Summary:	DHCP Server
Summary(es.UTF-8):	Servidor DHCP
Summary(pl.UTF-8):	Serwer DHCP
Summary(pt_BR.UTF-8):	Servidor DHCP (Protocolo de configuração dinâmica de hosts)
Name:		dhcp
Version:	%{ver}%{pverdot}
Release:	1
Epoch:		4
License:	MIT
Group:		Networking/Daemons
Source0:	ftp://ftp.isc.org/isc/dhcp/%{ver}%{pverdir}/%{name}-%{ver}%{pverdir}.tar.gz
# Source0-md5:	2afdaf8498dc1edaf3012efdd589b3e1
Source1:	%{name}.init
Source2:	%{name}6.init
Source3:	%{name}-relay.init
Source4:	%{name}.sysconfig
Source5:	%{name}-relay.sysconfig
Source10:	%{name}.schema
Source11:	%{name}-README.ldap
Source12:	draft-ietf-dhc-ldap-schema-01.txt
Source13:	%{name}d-conf-to-ldap
Patch0:		%{name}-release-by-ifup.patch
Patch1:		%{name}-3.0.3-x-option.patch
Patch2:		%{name}-paths.patch
Patch3:		%{name}-timeouts.patch
Patch4:		%{name}-options.patch
Patch5:		%{name}-errwarn-message.patch
Patch6:		%{name}-memory.patch
Patch7:		%{name}-unicast-bootp.patch
Patch8:		%{name}-default-requested-options.patch
Patch9:		%{name}-manpages.patch
Patch10:	%{name}-extravars.patch
URL:		https://www.isc.org/dhcp/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	groff
%ifarch %{arm}
BuildRequires:	libatomic-devel
%endif
BuildRequires:	libtool
%{?with_ldap:BuildRequires:	openldap-devel}
%{?with_ldap:BuildRequires:	openssl-devel}
BuildRequires:	rpmbuild(macros) >= 1.304
Requires(post):	coreutils
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.2.0
Provides:	dhcpd
Obsoletes:	dhcpv6-server
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
BuildArch:	noarch

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
Suggests:	avahi-autoipd
Provides:	dhclient = %{epoch}:%{version}-%{release}
Obsoletes:	dhclient
Obsoletes:	dhcpv6-client
Obsoletes:	libdhcp4client
Obsoletes:	libdhcp4client-devel
Obsoletes:	libdhcp4client-static

%description client
Dynamic Host Configuration Protocol Client.

%description client -l pl.UTF-8
Klient DHCP (Dynamic Host Configuration Protocol).

%package client-dirs
Summary:	DHCP Client common dirs
Summary(pl.UTF-8):	Katalogi klienta DHCP
Group:		Networking/Daemons

%description client-dirs
Directories for scripts for dhcp-client.

%description client-dirs -l pl.UTF-8
Katalog przeznaczony na skrypty dla klienta dhcp.

%package relay
Summary:	DHCP Relay Agent
Summary(pl.UTF-8):	Agent przekazywania informacji DHCP
Group:		Networking/Daemons
Requires(post):	coreutils
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.2.0
Obsoletes:	dhcpv6-relay

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

%prep
%setup -q -n %{name}-%{ver}%{pverdir}
%patch0 -p1
# This patch is required for dhcdbd to function
# CHECK ME: adds -x (formerly -y):
#The -x argument enables extended option information to be created in the
#-s dhclient-script environment, which would allow applications running
#in that environment to handle options they do not know about in advance -
#this is a Red Hat extension to support dhcdbd and NetworkManager.
# however, fedora doesn't have this patch anymore, so can drop?
#%%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

# Copy in documentation and example scripts for LDAP patch to dhcpd
cp -a %{SOURCE11} README.ldap
cp -a %{SOURCE12} doc
cp -a %{SOURCE13} contrib

# Replace @PRODUCTNAME@
%{__sed} -i -e 's|@PRODUCTNAME@|%{vvendor}|g' common/dhcp-options.5
%{__sed} -i -e 's|@PRODUCTNAME@|%{vvendor}|g' configure.ac

# Update paths in all man pages
for page in client/dhclient.conf.5 client/dhclient.leases.5 client/dhclient-script.8 client/dhclient.8; do
	%{__sed} -i -e 's|CLIENTBINDIR|/sbin|g' \
			-e 's|RUNDIR|%{_localstatedir}/run|g' \
			-e 's|DBDIR|%{_localstatedir}/db/dhclient|g' \
			-e 's|ETCDIR|%{_sysconfdir}|g' $page
done

for page in server/dhcpd.conf.5 server/dhcpd.leases.5 server/dhcpd.8; do
	%{__sed} -i -e 's|CLIENTBINDIR|/sbin|g' \
				-e 's|RUNDIR|%{_localstatedir}/run|g' \
				-e 's|DBDIR|%{_localstatedir}/db/dhcpd|g' \
				-e 's|ETCDIR|%{_sysconfdir}|g' $page
done

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CFLAGS="%{rpmcflags} -fPIC -D_GNU_SOURCE=1"
%configure \
%ifarch %{arm}
	LIBS="-latomic" \
%endif
	%{!?with_static_libs:--disable-static} \
	--enable-dhcpv6 \
	--with-srv-lease-file=/var/lib/dhcpd/dhcpd.leases \
	--with-cli-lease-file=/var/lib/dhclient/dhclient.leases \
	--with-srv-pid-file=/var/run/dhcpd.pid \
	--with-cli-pid-file=/var/run/dhclient.pid \
	--with-relay-pid-file=/var/run/dhcrelay.pid \
	--with%{!?with_ldap:out}-ldap
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig,dhclient-enter-hooks.d,dhclient-exit-hooks.d},%{_pkgconfigdir},/var/lib/{dhcpd,dhclient}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcpd6
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcp-relay
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/dhcpd
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/dhcp-relay

install client/scripts/linux $RPM_BUILD_ROOT/sbin/dhclient-script

install server/dhcpd.conf.example $RPM_BUILD_ROOT%{_sysconfdir}/dhcpd.conf
install doc/examples/dhcpd-dhcpv6.conf $RPM_BUILD_ROOT%{_sysconfdir}/dhcpd6.conf

%if %{with ldap}
install -d $RPM_BUILD_ROOT%{schemadir}
install %{SOURCE10} $RPM_BUILD_ROOT%{schemadir}
%endif

:> $RPM_BUILD_ROOT%{_sysconfdir}/dhclient.conf

touch $RPM_BUILD_ROOT/var/lib/dhcpd/dhcpd.leases
touch $RPM_BUILD_ROOT/var/lib/dhclient/dhclient.leases

touch $RPM_BUILD_ROOT/var/lib/dhcpd/dhcpd6.leases
touch $RPM_BUILD_ROOT/var/lib/dhclient/dhclient6.leases

%if %{with static_libs}
# HACK: strip doesn't like .a inside .a
install -d stripworkdir
cd stripworkdir
for a in $RPM_BUILD_ROOT%{_libdir}/*.a; do
	archives=$(ar t $a | grep '\.a$' || :)
	[ "$archives" ] || continue

	# hope we don't have to recurse here
	for ar in $archives; do
		rm -f *.o *.a
		ar x $a $ar
		ar x $ar
		ar d $a $ar
		ar cr $a *.o
	done
done
cd -
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch /var/lib/dhcpd/dhcpd.leases
touch /var/lib/dhcpd/dhcpd6.leases
/sbin/chkconfig --add dhcpd
%service dhcpd restart "dhcpd daemon"
/sbin/chkconfig --add dhcpd6
%service dhcpd6 restart "dhcpd IPv6 daemon"

%preun
if [ "$1" = "0" ];then
	%service dhcpd stop
	/sbin/chkconfig --del dhcpd
	%service dhcpd6 stop
	/sbin/chkconfig --del dhcpd6
fi

%triggerpostun -- dhcp < 3.0
if ! grep -q ddns-update-style /etc/dhcpd.conf; then
	%{__sed} -i -e '1iddns-update-style none;' /etc/dhcpd.conf
fi

%post -n openldap-schema-dhcp
%openldap_schema_register %{schemadir}/dhcp.schema -d core
%service -q ldap restart

%postun -n openldap-schema-dhcp
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/dhcp.schema
	%service -q ldap restart
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

%triggerun client -- %{name}-client < 4:4.0.2-2
if [ -f /etc/dhclient-enter-hooks ] ; then
	mv /etc/dhclient-enter-hooks /etc/dhclient-enter-hooks.d/
fi
if [ -f /etc/dhclient-exit-hooks ] ; then
	mv /etc/dhclient-exit-hooks /etc/dhclient-exit-hooks.d/
fi

%files
%defattr(644,root,root,755)
%doc doc/* README RELNOTES server/dhcpd.conf.example LICENSE
%doc contrib/ms2isc %{?with_ldap:contrib/dhcpd-conf-to-ldap README.ldap}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dhcpd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dhcpd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dhcpd6.conf
%attr(755,root,root) %{_bindir}/omshell
%attr(755,root,root) %{_sbindir}/dhcpd
%attr(754,root,root) /etc/rc.d/init.d/dhcpd
%attr(754,root,root) /etc/rc.d/init.d/dhcpd6
%attr(750,root,root) %dir /var/lib/dhcpd
%ghost /var/lib/dhcpd/dhcpd.leases
%ghost /var/lib/dhcpd/dhcpd6.leases
%{_mandir}/man1/omshell.1*
%{_mandir}/man5/dhcp-eval.5*
%{_mandir}/man5/dhcp-options.5*
%{_mandir}/man5/dhcpd.conf.5*
%{_mandir}/man5/dhcpd.leases.5*
%{_mandir}/man8/dhcpd.8*

%files client
%defattr(644,root,root,755)
%doc contrib/sethostname.sh client/dhclient.conf.example
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dhclient.conf
%attr(755,root,root) /sbin/dhclient
%attr(755,root,root) /sbin/dhclient-script
%{_mandir}/man5/dhclient.conf.5*
%{_mandir}/man5/dhclient.leases.5*
%{_mandir}/man8/dhclient.8*
%{_mandir}/man8/dhclient-script.8*
%dir %attr(750,root,root) /var/lib/dhclient
%ghost /var/lib/dhclient/dhclient.leases
%ghost /var/lib/dhclient/dhclient6.leases

%files client-dirs
%defattr(644,root,root,755)
%dir %{_sysconfdir}/dhclient-enter-hooks.d
%dir %{_sysconfdir}/dhclient-exit-hooks.d

%files relay
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dhcp-relay
%attr(755,root,root) %{_sbindir}/dhcrelay
%attr(754,root,root) /etc/rc.d/init.d/dhcp-relay
%{_mandir}/man8/dhcrelay.8*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libdhcp.a
%{_libdir}/libdhcpctl.a
%{_libdir}/libomapi.a
%{_includedir}/dhcpctl
%{_includedir}/omapip
%{_mandir}/man3/dhcpctl.3*
%{_mandir}/man3/omapi.3*

%if %{with ldap}
%files -n openldap-schema-dhcp
%defattr(644,root,root,755)
%{schemadir}/dhcp.schema
%endif
