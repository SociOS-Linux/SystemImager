#!/bin/sh
#
# "SystemImager"
#
#  Copyright (C) 2000 Brian Elliott Finley 
#                     <brian@bgsw.net>
#  Copyright (C) 2002-2003 Bald Guy Software
#                          <brian@bgsw.net>
#
#  Copyright (C) 2017-2018 Olivier Lahaye
#                     <olivier.lahaye@cea.fr>
#   $Id$
#
#   See http://www.iana.org/assignments/bootp-dhcp-parameters for details
#   on custom options (new_option_NNN) as viewed below. -BEF-
#   
#   option-100  ->  IMAGESERVER (depricated -> actually reserved for "printer name")
#   option-140  ->  IMAGESERVER
#   option-141  ->  LOG_SERVER_PORT
#   option-142  ->  SSH_DOWNLOAD_URL
#   option-143  ->  FLAMETHROWER_DIRECTORY_PORTBASE
#   option-144  ->  TMPFS_STAGING
#   option-208  ->  SSH_DOWNLOAD_URL (deprecated)
#                   disabled by JRT 2006-10-11
#                   see dhclient.conf for commentary

# systemimager-load-dhcpopts will read /tmp/dhclient.$DEVICE.dhcpopts and update
# /tmp/variables.txt accordingly. (priority is givent to local.cfg, then cmdline,
# then DHCP at last)

. /lib/systemimager-lib.sh # Load /tmp/variables.txt and some macros
logdebug "==== systemimager-load-dhcpopts ===="

DEVICE=$1

if test -r /tmp/dhclient.$DEVICE.dhcpopts # ISC Client
then
	loginfo "ISC dhcp client detected"
	loginfo "Reading values that are not already set (cmdline, ...)"
	source /tmp/dhclient.$DEVICE.dhcpopt

	[ -z "$HOSTNAME" ] || [ "$HOSTNAME" == "localhost" ] || [ "$HOSTNAME" == "(none)" ] && [ -n "$new_host_name" ] && HOSTNAME="$new_host_name" && loginfo "Got HOSTNAME=$new_host_name"
	[ -z "$DOMAINNAME" ] && [ -n "$new_domain_name" ] && DOMAINNAME="$new_domain_name" && loginfo "Got DOMAINNAME=$new_domain_name"


	################################################################################
	#
	# Originally we assumed the DHCP server was the imageserver, then we started
	# using option-100 (turns out option-100 is reserved for "printer name"),
	# now we use option-140 (reserved for "private use").  The following 
	# funkification is for backwards compatibility with servers using older 
	# dhcp.conf files. -BEF-
	#
	if [ -z "$IMAGESERVER" ]; then
	    if [ -n "$new_option_140" ]; then
        	IMAGESERVER=$new_option_140
		loginfo "Got IMAGESERVER=${new_option_140} (from option-140)"
	    elif [ -n "$new_option_100" ]; then
	        IMAGESERVER=$new_option_100
        	logwarn "Got IMAGESERVER=${new_option_100} (from option-100. VERY DEPRECATED!)"
	    elif [ -n "$new_dhcp_server_identifier" ]; then
        	IMAGESERVER=$new_dhcp_server_identifier
		logwarn "Got IMAGESERVER=${new_dhcp_server_identifier} (used DHCP server as IMAGESERVER: VERY DEPRECATED!)"
	    fi
	fi

	[ -z "$LOG_SERVER" ] && [ -n "$new_log_servers" ] && LOG_SERVER="$new_log_servers" && loginfo "Got LOG_SERVER=${new_log_servers}"
	[ -z "$LOG_SERVER_PORT" ] && [ -n "$new_option_141" ] && LOG_SERVER_PORT="$new_option_141" && loginfo "Got LOG_SERVER_PORT=${new_option_141}"
                                                        
	[ -z "$IPADDR" ] && [ -n "$new_ip_address" ] && IPADDR="$new_ip_address" && loginfo "Got IPADDR=${new_ip_address}"
	[ -z "$NETMASK" ] && [ -n "$new_subnet_mask" ] && NETMASK="$new_subnet_mask" && loginfo "Got NETMASK=${new_subnet_mask}"
	[ -z "$NETWORK" ] && [ -n "$new_network_number" ] && NETWORK="$new_network_number" && loginfo "Got NETWORK=${new_network_number}"
	[ -z "$BROADCAST" ] && [ -n "$new_broadcast_address" ] && BROADCAST="$new_broadcast_address" && loginfo "Got BROADCAST=${new_broadcast_address}"
	[ -z "$FLAMETHROWER_DIRECTORY_PORTBASE" ] && [ -n "$new_option_143" ] && FLAMETHROWER_DIRECTORY_PORTBASE="$new_option_143" && loginfo "Got FLAMETHROWER_DIRECTORY_PORTBASE=${new_option_143}"
	[ -z "$TMPFS_STAGING" ] && [ -n "$new_option_144" ] && TMPFS_STAGING="$new_option_144" && loginfo "Got TMPFS_STAGING=${new_option_144}"
	[ -z "$GATEWAY" ] && [ -n "$new_routers" ] && GATEWAY="$new_routers" && loginfo "Got GATEWAY=${new_routers}"
	[ -z "$GATEWAY_DEV" ] && [ -n "$DEVICE" ] && GATEWAYDEV="$DEVICE" && loginfo "Got GATEWAYDEV=${DEVICE}"

                                                        
	################################################################################
	#
	# Originally we used option-208 here, but pxelinux started using it too, so 
	# we switched to using option-142.
	#
	[ -z "$SSH_DOWNLOAD_URL" ] && [ -n "$new_option_142" ] && SSH_DOWNLOAD_URL="$new_option_142" && loginfo "Got SSH_DOWNLOAD_URL=${new_option_142}"

	loginfo "Finished reading DHCP lease informations."

elif test -r /tmp/leaseinfo.$DEVICE.dhcp.ipv4
then
	# OPTION_XYZ merchanism understood from https://github.com/openSUSE/wicked/blob/master/src/leaseinfo.c
	# understood options names (declared in /etc/wickedd/dhcp4.xml) are made uppercase and prefixed with OPTION_
	# "." and "/" are translated to "_"
	# Options received from dhcp server that are not defined in /etc/wickedd/dhcp4.xml are named "UNKNOWN_<option number>"
	loginfo "wickedd-dhcp client detected."
	loginfo "Reading values that are not already set (cmdline, ...)"
	source /tmp/leaseinfo.$DEVICE.dhcp.ipv4
	[ -z "$HOSTNAME" ] && logwarn "Failed to get hostname from DHCP! (will try to get it from DNS or scripts/host file later)"
	[ -z "$DOMAINNAME" ] && [ -n "$DNSDOMAINNAME" ] && DOMAINNAME="$DNSDOMAINNAME" && loginfo "Got DOMAINNAME=$DNSDOMAINNAME"

	if [ -z "$IMAGESERVER" ]; then
	    if [ -n "$OPTION_IMAGE_SERVER" ]; then
        	IMAGESERVER=$OPTION_IMAGE_SERVER
		loginfo "Got IMAGESERVER=${OPTION_IMAGE_SERVER} (from option-140)"
	    elif [ -n "$UNKNOWN_100" ]; then
        	IMAGESERVER=$UNKNOWN_100
		logwarn "Got IMAGESERVER=${UNKNOWN_100} (from option-100: DEPRECATED!)"
	    elif [ -n "$BOOTSERVERNAME" ]; then
        	IMAGESERVER=$BOOTSERVERNAME
		loginfo "Got IMAGESERVER=${BOOTSERVERNAME} (used boot server as IMAGESERVER)"
	    elif [ -n "$BOOTSERVERADDR" ]; then
        	IMAGESERVER=$BOOTSERVERADDR
		loginfo "Got IMAGESERVER=${BOOTSERVERADDR} (used boot server as IMAGESERVER)"
	    elif [ -n "$SERVERID" ]; then
        	IMAGESERVER=$SERVERID
		logwarn "Got IMAGESERVER=${SERVERID} (used DHCP server as IMAGESERVER: VERY DEPRECATED!)"
	    fi
	fi


	[ -z "$LOG_SERVER" ] && [ -n "$LOGSERVER" ] && LOG_SERVER="$LOGSERVER" && loginfo "Got LOG_SERVER=${LOGSERVER}"
	[ -z "$LOG_SERVER_PORT" ] && [ -n "$OPTION_LOG_SERVER_PORT" ] && LOG_SERVER_PORT="$OPTION_LOG_SERVER_PORT" && loginfo "Got LOG_SERVER_PORT=${OPTION_LOG_SERVER_PORT}"
                                                        
	if test -n "$IPADDR"
	then
		IPADDR=${IPADDR%%/*} # Remove mask
	else
		shellout "Failed to get an IP address from DHCP."
	fi
	[ -z "$NETMASK" ] && shellout "Failed to get NETMASK from DHCP."
	[ -z "$NETWORK" ] && shellout "Failed to get NETWORK from DHCP."
	[ -z "$BROADCAST" ] && logwarn "Failed to get BROADCAST address from DHCP."
	[ -z "$FLAMETHROWER_DIRECTORY_PORTBASE" ] && [ -n "$OPTION_FLAMETHROWER_DIRECTORY_PORTBASE" ] && FLAMETHROWER_DIRECTORY_PORTBASE="$OPTION_FLAMETHROWER_DIRECTORY_PORTBASE" && loginfo "Got FLAMETHROWER_DIRECTORY_PORTBASE=${OPTION_FLAMETHROWER_DIRECTORY_PORTBASE}"
	[ -z "$TMPFS_STAGING" ] && [ -n "$OPTION_TMPFS_STAGING" ] && TMPFS_STAGING="$OPTION_TMPFS_STAGING" && loginfo "Got TMPFS_STAGING=${OPTION_TMPFS_STAGING}"
	[ -z "$GATEWAY" ] && [ -n "$GATEWAYS" ] && GATEWAY="${GATEWAYS%% *}" && loginfo "Got GATEWAY=${GATEWAY} (from GATEWAYS=${GATEWAYS})"
	[ -z "$GATEWAY_DEV" ] && [ -n "$DEVICE" ] && GATEWAYDEV="$DEVICE" && loginfo "Got GATEWAYDEV=${DEVICE}"
	[ -z "$SSH_DOWNLOAD_URL" ] && [ -n "$OPTION_SSH_DOWNLOAD_URL" ] && SSH_DOWNLOAD_URL="$OPTION_SSH_DOWNLOAD_URL" && loginfo "Got SSH_DOWNLOAD_URL=${OPTION_SSH_DOWNLOAD_URL}"

	loginfo "Finished reading DHCP lease informations."
else
	logerror "No DHCP_OPTIONS found in /tmp! systemd-networkd which is not yet supported?"
	shellout "Failed to read DHCP options!"
fi

# Save variables to /tmp/variables.txt
write_variables

### END SystemImager loading network config ###
