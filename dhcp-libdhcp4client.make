#
# Makefile.dist for libdhcp4client
#
# We get the libdhcp4client library from the patched ISC source code.  We
# rebuild key C files with -DLIBDHCP to turn on the library features we
# need.  Normal build results in standard ISC code (i.e., not LIBDHCP
# stuff enabled).  We then link together a static library and a shared
# library with the new resulting objects.
#
# Copyright (C) 2006, 2007  Red Hat, Inc. All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A * PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Jason Vas Dias
#                    David Cantrell <dcantrell@redhat.com>
#

# What version of ISC DHCP is this?
VER   = $(shell grep DHCP_VERSION ../../includes/version.h | head -1 | cut -d '"' -f 2 | cut -d 'V' -f 2 | cut -d '-' -f 1)

PROGS = libdhcp4client.a libdhcp4client-$(VER).so.0

# NOTE: The ordering of these file lists is important!  We are using the
# whole program optimization features of gcc, so the order matters here.

# Source files shared by all objects
COMMON_SRCS = client_clparse.c client_dhclient.c common_alloc.c common_bpf.c \
              common_comapi.c common_conflex.c common_discover.c \
              common_dispatch.c common_dns.c common_ethernet.c \
              common_execute.c common_inet.c common_lpf.c common_memory.c \
              common_options.c common_packet.c common_parse.c common_print.c \
              common_socket.c common_tables.c common_tr.c common_tree.c \
              dst_dst_api.c dst_base64.c dst_hmac_link.c dst_md5_dgst.c \
              omapip_alloc.c omapip_array.c omapip_auth.c omapip_buffer.c \
              omapip_connection.c omapip_convert.c omapip_dispatch.c \
              omapip_errwarn.c omapip_handle.c omapip_hash.c \
              omapip_listener.c omapip_mrtrace.c omapip_result.c \
              omapip_support.c omapip_toisc.c omapip_trace.c

# Source files for libdhcp4client.o
CLIENT_SRCS = common_ctrace.c common_dlpi.c common_nit.c common_upf.c \
              dst_dst_support.c dst_prandom.c omapip_generic.c \
              omapip_message.c omapip_protocol.c

# Source files for libres.o (minires)
MINIRES_SRCS = minires_ns_date.c minires_ns_name.c minires_ns_parse.c \
               minires_ns_samedomain.c minires_ns_sign.c minires_ns_verify.c \
               minires_res_comp.c minires_res_findzonecut.c \
               minires_res_init.c minires_res_mkquery.c \
               minires_res_mkupdate.c minires_res_query.c minires_res_send.c \
               minires_res_sendsigned.c minires_res_update.c

# ISC dhcp headers we need to copy to /usr/include/dhcp4client
DHCP_HEADERS = dhcpd.h cdefs.h osdep.h arpa/nameser.h minires/minires.h \
               site.h cf/linux.h dhcp.h statement.h tree.h inet.h dhctoken.h \
               omapip/omapip_p.h failover.h ctrace.h minires/resolv.h \
               minires/res_update.h omapip/convert.h omapip/hash.h \
               omapip/trace.h

HDRS = dhcp4client.h
SRCS = $(COMMON_SRCS) $(CLIENT_SRCS)
OBJS = $(SRCS:.c=.o)

INCLUDES = -I$(TOP) -I$(TOP)/includes -I$(TOP)/dst -I.
CFLAGS   = $(DEBUG) $(PREDEFINES) $(INCLUDES) $(COPTS) \
           -DCLIENT_PATH=${CLIENT_PATH} -DLIBDHCP -DUSE_MD5

all: $(PROGS)

install: all
	install -p -m 0755 -D libdhcp4client-$(VER).so.0 $(DESTDIR)$(LIBDIR)/libdhcp4client-$(VER).so.0
	ln -sf libdhcp4client-$(VER).so.0 $(DESTDIR)/$(LIBDIR)/libdhcp4client.so
	install -p -m 0644 -D libdhcp4client.a $(DESTDIR)$(LIBDIR)/libdhcp4client.a
	install -p -m 0644 -D dhcp4client.h $(DESTDIR)$(INCDIR)/dhcp4client/dhcp4client.h
	for hdr in $(DHCP_HEADERS) ; do \
		install -p -m 0644 -D $(TOP)/includes/$${hdr} $(DESTDIR)$(INCDIR)/dhcp4client/$${hdr} ; \
	done

depend:
	$(MKDEP) $(INCLUDES) $(PREDEFINES) $(SRCS)

clean:
	-rm -f $(OBJS)

realclean: clean
	-rm -f $(PROG) *~ #*

distclean: realclean
	-rm -f Makefile

# This isn't the cleanest way to set up links, but I prefer this so I don't
# need object targets for each subdirectory.  The idea is simple.  Since
# libdhcp4client is a linked together wad of objects from across the source
# tree, we change / to _ when linking source files here.  Follow this example:
#
# We need to use client/dhclient.c, so we make this link:
#     rm -f client_dhclient.c
#     ln -s $(TOP)/client/dhclient.c client_dhclient.c
#
# Simple.  Given the way the ISC build system works, this is the easiest to
# maintain and least invasive.
#
# David Cantrell <dcantrell@redhat.com>
links:
	@for target in $(SRCS); do \
		source="`echo $$target | sed -e 's|_|/|'`"; \
		if [ ! -b $$target ]; then \
			rm -f $$target; \
		fi; \
		ln -s $(TOP)/$$source $$target; \
	done; \
	for hdr in $(HDRS); do \
		if [ ! -b $$hdr ]; then \
			rm -f $$hdr; \
		fi; \
		ln -s $(TOP)/libdhcp4client/$$hdr $$hdr; \
	done

# minires is difficult to build because it overrides things in common and dst,
# so we just link with the already built libres.a since we need it all anyway
libres.a:
	if [ ! -f ../minires/$@ ]; then \
		$(MAKE) -C ../minires; \
	fi; \
	ln ../minires/libres.a .; \
	$(AR) x libres.a

# Create the libraries
# minires/res_query.o contains an undefined symbol __h_errno_set, is not
# used by any dhcp code, and is optimized out by the linker when producing
# the dhclient executable or a shared library
libdhcp4client.a: $(OBJS) libres.a
	$(AR) crus $@ $(OBJS) `$(AR) t libres.a | grep -v res_query.o`

libdhcp4client-$(VER).so.0: $(OBJS) libres.a
	$(CC) -shared -o $@ -Wl,-soname,$@ $(OBJS) `$(AR) t libres.a | grep -v res_query.o`

# Dependencies (semi-automatically-generated)
