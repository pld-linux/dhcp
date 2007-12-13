/* libdhcp_control.h
 *
 * DHCP client control API for libdhcp, a minimal interface to the
 * ISC dhcp IPv4 client libdhcp4client library,
 * and to the dhcpv6 DHCPv6 client libdhcp6client library.
 *
 * Each DHCP client library must include this file to be controlled
 * by libdhcp.
 *
 * Copyright (C) 2006  Red Hat, Inc. All rights reserved.
 *
 * This copyrighted material is made available to anyone wishing to use,
 * modify, copy, or redistribute it subject to the terms and conditions of
 * the GNU General Public License v.2, or (at your option) any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY expressed or implied, including the implied warranties of
 * MERCHANTABILITY or FITNESS FOR A * PARTICULAR PURPOSE.  See the GNU General
 * Public License for more details.  You should have received a copy of the
 * GNU General Public License along with this program; if not, write to the
 * Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
 * 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
 * source code or documentation are not subject to the GNU General Public
 * License and may only be used or replicated with the express permission of
 * Red Hat, Inc.
 *
 * Red Hat Author(s): Jason Vas Dias
 *                    David Cantrell <dcantrell@redhat.com>
 */

#ifndef LIBDHCP_CONTROL_H
#define LIBDHCP_CONTROL_H

#include <stdarg.h>
#include <stdint.h>

#define  LOG_FATAL 8

typedef enum dhcp_state_e {
    /* DHCPv4 client states
     * third callback arg will be a 'struct client_state *'
     */
    DHC4_NBI,     /* failed: no broadcast interfaces found              */
    DHC4_PREINIT, /* configuration started - bring the interface "UP"   */
    DHC4_BOUND,   /* lease obtained                                     */
    DHC4_RENEW,   /* lease renewed                                      */
    DHC4_REBOOT,  /* have valid lease, but now obtained a different one */
    DHC4_REBIND,  /* new, different lease                               */
    DHC4_STOP,    /* remove old lease                                   */
    DHC4_MEDIUM,  /* media selection begun                              */
    DHC4_TIMEOUT, /* timed out contacting DHCP server                   */
    DHC4_FAIL,    /* all attempts to contact server timed out, sleeping */
    DHC4_EXPIRE,  /* lease has expired, renewing                        */
    DHC4_RELEASE, /* releasing lease                                    */

    /* This state raised by both clients: */
    DHC_TIMEDOUT, /* libdhcp_control timeout has been exceeded          */

    /* DHCPv6 client states:    */
    DHC6_BOUND,   /* new lease obtained             - arg is optinfo *  */
    DHC6_REBIND,  /* existing expired lease rebound - arg is optinfo *  */
    DHC6_RELEASE  /* existing lease expired         - arg is dhcp6_iaidaddr*/
} DHCP_State;

struct libdhcp_control_s;

/* ala syslog(3): LOG_EMERG=0 - LOG_DEBUG=7 (+ LOG_FATAL=8 : finished -> 1) */
typedef int (*LIBDHCP_Error_Handler) (struct libdhcp_control_s *ctl,
                                      int priority, const char *fmt,
                                      va_list ap);

/* The DHCP clients will call the users' callback on important state change
 * events, with the second arg set to the client DHCP_State, and the third
 * arg set to a client specific pointer as described below. */
typedef int (*LIBDHCP_Callback) (struct libdhcp_control_s *control,
                                 enum dhcp_state_e, void*);

typedef struct libdhcp_control_s {
    /* the DHCP clients' main loop calls this on state changes */
    LIBDHCP_Callback callback;

    /* LIBDHCP_Capability bits to enable */
    uint16_t capability;

    /* set to one to make clients exit their main loop */
    uint8_t finished;

    /* set to one to decline the lease (DHCPv4 only) */
    uint8_t decline;

    /* (timeout+now) == time after which clients MUST return */
    time_t timeout;

    /* clients set this to time(0) on entering main loop */
    time_t now;

    /* user data pointer */
    void *arg;
    LIBDHCP_Error_Handler eh;
} LIBDHCP_Control;

/* DHCP client "capabilities" */
typedef enum libdhcp_capability_e {
    /* use / do not use persistent lease database files */
    DHCP_USE_LEASE_DATABASE = 1,

    /* use / do not use pid file */
    DHCP_USE_PID_FILE = 2,

    /*
     * DHCPv6 supports these capabilities in process, 
     * while the DHCPv4 client will fork and exec the dhclient-script to
     * implement them if these bits are set - otherwise, if no bits are set,
     * the callback is called and the script is not run.
     */
    /* configure interfaces UP/DOWN as required */
    DHCP_CONFIGURE_INTERFACES = 4,

    /* configure interface addresses as required */
    DHCP_CONFIGURE_ADDRESSES = 8,

    /* configure routes as required */
    DHCP_CONFIGURE_ROUTES = 16,

    /* configure resolv.conf as required */
    DHCP_CONFIGURE_RESOLVER = 32,

    /* DHCPv6 only: */
    /* configure radvd.conf & restart radvd as required */
    DHCP_CONFIGURE_RADVD = 64,
} LIBDHCP_Capability;

#endif
