%define name     systemimager
%define ver      2.9.4
%define rel      1
%define prefix   /usr
%define _build_all 1
%define _boot_flavor standard
# Set this to 1 to build only the boot rpm
# it can also be done in the .rpmmacros file
#define _build_only_boot 1
%{?_build_only_boot:%{expand: %%define _build_all 0}}


Summary: Software that automates Linux installs, software distribution, and production deployment.
Name: %name
Version: %ver
Release: %rel
Copyright: GPL
Group: Applications/System
Source: http://download.sourceforge.net/systemimager/%{name}-%{ver}.tar.bz2
BuildRoot: /tmp/%{name}-%{ver}-root
BuildArchitectures: noarch
Packager: dann frazier <dannf@dannf.org>
Docdir: %{prefix}/share/doc
URL: http://systemimager.org/
Distribution: System Installation Suite
Requires: rsync >= 2.4.6, syslinux >= 1.48, libappconfig-perl, dosfstools, /usr/bin/perl
AutoReqProv: no

%description
This is bogus and not used anywhere

%if %{_build_all}

%package server
Summary: Software that automates Linux installs, software distribution, and production deployment.
Version: %ver
Release: %rel
Copyright: GPL
Group: Applications/System
BuildRoot: /tmp/%{name}-%{ver}-root
Packager: dann frazier <dannf@dannf.org>
Docdir: %{prefix}/share/doc
URL: http://systemimager.org/
Distribution: System Installation Suite
Requires: rsync >= 2.4.6, systemimager-common = %{version}, perl-AppConfig, dosfstools, /sbin/chkconfig, perl, perl-XML-Simple
AutoReqProv: no

%description server
SystemImager is software that automates Linux installs, software 
distribution, and production deployment.  SystemImager makes it easy to
do installs, software distribution, content or data distribution, 
configuration changes, and operating system updates to your network of 
Linux machines. You can even update from one Linux release version to 
another!  It can also be used to ensure safe production deployments.  
By saving your current production image before updating to your new 
production image, you have a highly reliable contingency mechanism.  If
the new production enviroment is found to be flawed, simply roll-back 
to the last production image with a simple update command!  Some 
typical environments include: Internet server farms, database server 
farms, high performance clusters, computer labs, and corporate desktop
environments.

The server package contains those files needed to run a SystemImager
server.

%package common
Summary: Software that automates Linux installs, software distribution, and production deployment.
Version: %ver
Release: %rel
Copyright: GPL
Group: Applications/System
BuildRoot: /tmp/%{name}-%{ver}-root
Packager: dann frazier <dannf@dannf.org>
Docdir: %{prefix}/share/doc
URL: http://systemimager.org/
Distribution: System Installation Suite
Requires: perl
AutoReqProv: no

%description common
SystemImager is software that automates Linux installs, software 
distribution, and production deployment.  SystemImager makes it easy to
do installs, software distribution, content or data distribution, 
configuration changes, and operating system updates to your network of 
Linux machines. You can even update from one Linux release version to 
another!  It can also be used to ensure safe production deployments.  
By saving your current production image before updating to your new 
production image, you have a highly reliable contingency mechanism.  If
the new production enviroment is found to be flawed, simply roll-back 
to the last production image with a simple update command!  Some 
typical environments include: Internet server farms, database server 
farms, high performance clusters, computer labs, and corporate desktop
environments.

The common package contains files common to SystemImager clients 
and servers.

%package client
Summary: Software that automates Linux installs, software distribution, and production deployment.
Version: %ver
Release: %rel
Copyright: GPL
Group: Applications/System
BuildRoot: /tmp/%{name}-%{ver}-root
Packager: dann frazier <dannf@dannf.org>
Docdir: %{prefix}/share/doc
URL: http://systemimager.org/
Distribution: System Installation Suite
Requires: systemimager-common = %{version}, systemconfigurator, perl-AppConfig, rsync >= 2.4.6, perl
AutoReqProv: no

%description client
SystemImager is software that automates Linux installs, software
distribution, and production deployment.  SystemImager makes it easy to
do installs, software distribution, content or data distribution,
configuration changes, and operating system updates to your network of
Linux machines. You can even update from one Linux release version to
another!  It can also be used to ensure safe production deployments.
By saving your current production image before updating to your new
production image, you have a highly reliable contingency mechanism.  If
the new production enviroment is found to be flawed, simply roll-back
to the last production image with a simple update command!  Some
typical environments include: Internet server farms, database server
farms, high performance clusters, computer labs, and corporate desktop
environments.

The client package contains the files needed on a machine for it to
be imaged by a SystemImager server.

%endif

%package %{_build_arch}boot-%{_boot_flavor}
Summary: Software that automates Linux installs, software distribution, and production deployment.
Version: %ver
Release: %rel
Copyright: GPL
Group: Applications/System
BuildRoot: /tmp/%{name}-%{ver}-root
Packager: dann frazier <dannf@dannf.org>
Docdir: %{prefix}/share/doc
URL: http://systemimager.org/
Distribution: System Installation Suite
Obsoletes: systemimager-%{_build_arch}boot
Requires: systemimager-server >= %{version}
AutoReqProv: no

%description %{_build_arch}boot-%{_boot_flavor}
SystemImager is software that automates Linux installs, software 
distribution, and production deployment.  SystemImager makes it easy to
do installs, software distribution, content or data distribution, 
configuration changes, and operating system updates to your network of 
Linux machines. You can even update from one Linux release version to 
another!  It can also be used to ensure safe production deployments.  
By saving your current production image before updating to your new 
production image, you have a highly reliable contingency mechanism.  If
the new production enviroment is found to be flawed, simply roll-back 
to the last production image with a simple update command!  Some 
typical environments include: Internet server farms, database server 
farms, high performance clusters, computer labs, and corporate desktop
environments.

The %{_build_arch}boot package provides specific kernel, ramdisk, and fs utilities
to boot and install %{_build_arch} Linux machines during the SystemImager autoinstall
process.

%changelog
* Sun Oct 27 2002 dann frazier <dannf@dannf.org> 2.9.4-1
- new upstream release

* Thu Oct 13 2002 dann frazier <dannf@dannf.org> 2.9.3-2
- added code to migrate users to rsync stubs

* Thu Oct 02 2002 dann frazier <dannf@dannf.org> 2.9.3-1
- new upstream release

* Thu Sep 19 2002 Sean Dague <sean@dague.net> 2.9.1-1
- Added \%if \%{_build_all} stanzas to make building easier.

* Tue Feb  5 2002 Sean Dague <sean@dague.net> 2.1.1-1
- Added section 5 manpages
- removed syslinux requirement, as it isn't need for ia64

* Mon Jan 14 2002 Sean Dague <sean@dague.net> 2.1.0-1
- Set Macro to build $ARCHboot packages propperly
- Targetted rpms for noarch target (dannf@dannf.org)
- Synced up file listing

* Wed Dec  5 2001 Sean Dague <sean@dague.net> 2.0.1-1
- Update SystemImager version
- Changed prefix to /usr
- Made seperate i386boot package

* Mon Nov  5 2001 Sean Dague <sean@dague.net> 2.0.0-4
- Added build section for true SRPM ability

* Mon Oct  28 2001 Sean Dague <sean@dague.net> 2.0.0-3
- Added common package

* Sat Oct 20 2001  Sean Dague <sean@dague.net> 2.0.0-2
- Recombined client and server into one spec file

* Thu Oct 18 2001 Sean Dague <sean@dague.net> 2.0.0-1
- Initial build
- Based on work by Ken Segura <ksegura@5o7.org>

%prep
%setup -q

make -j11 get_source

# Only build everything if on x86, this helps with PPC build issues
%if %{_build_all}
%build
cd $RPM_BUILD_DIR/%{name}-%{version}/
make all

%else
%build
cd $RPM_BUILD_DIR/%{name}-%{version}/
make binaries

%endif

%if %{_build_all}

%install
cd $RPM_BUILD_DIR/%{name}-%{version}/
make install_server_all DESTDIR=/tmp/%{name}-%{ver}-root PREFIX=%prefix
make install_client_all DESTDIR=/tmp/%{name}-%{ver}-root PREFIX=%prefix
%else

%install
cd $RPM_BUILD_DIR/%{name}-%{version}/
make install_binaries DESTDIR=/tmp/%{name}-%{ver}-root PREFIX=%prefix

%endif

%clean
#cd $RPM_BUILD_DIR/%{name}-%{version}/
#make distclean
#rm -rf $RPM_BUILD_ROOT

%if %{_build_all}

%pre server
# /etc/systemimager/rsyncd.conf is now generated from stubs stored
# in /etc/systemimager/rsync_stubs.  if upgrading from an early
# version, we need to create stub files for all image entries
if [ -f /etc/systemimager/rsyncd.conf -a \
    ! -d /etc/systemimager/rsync_stubs ]; then
    echo "You appear to be upgrading from a pre-rsync stubs release."
    echo "/etc/systemimager/rsyncd.conf is now auto-generated from stub"
    echo "files stored in /etc/systemimager/rsync_stubs."
    echo "Backing up /etc/systemimager/rsyncd.conf to:"
    echo -n "  /etc/systemimager/rsyncd.conf-before-rsync-stubs... "
    mv /etc/systemimager/rsyncd.conf \
      /etc/systemimager/rsyncd.conf-before-rsync-stubs

    ## leave an extra copy around so the postinst knows to make stub files from it
    cp /etc/systemimager/rsyncd.conf-before-rsync-stubs \
      /etc/systemimager/rsyncd.conf-before-rsync-stubs.tmp
    echo "done."
fi    


%post server
# First we check for rsync service under xinetd and get rid of it
# also note the use of DURING_INSTALL, which is used to
# support using this package in Image building without affecting
# processes running on the parrent
if [[ -a /etc/xinetd.d/rsync ]]; then
    mv /etc/xinetd.d/rsync /etc/xinetd.d/rsync.presis~
    `pidof xinetd > /dev/null`
    if [[ $? == 0 ]]; then
        if [ -z $DURING_INSTALL ]; then
            /etc/init.d/xinetd restart
        fi
    fi
fi

# If we are upgrading from a pre-rsync-stubs release, the preinst script
# will have left behind a copy of the old rsyncd.conf file.  we need to parse
# it and make stubs files for each image.

# This assumes that this file has been managed by systemimager, and
# that there is nothing besides images entries that need to be carried
# forward.

in_image_section=0
current_image=""
if [ -f /etc/systemimager/rsyncd.conf-before-rsync-stubs.tmp ]; then
    echo "Migrating image entries from existing /etc/systemimager/rsyncd.conf to"
    echo "individual files in the /etc/systemimager/rsync_stubs/ directory..."
    while read line; do
	## Ignore all lines until we get to the image section
	if [ $in_image_section -eq 0 ]; then
	    echo $line | grep -q "^# only image entries below this line"
	    if [ $? -eq 0 ]; then
		in_image_section=1
	    fi
	else
	    echo $line | grep -q "^\[.*]$"
	    if [ $? -eq 0 ]; then
		current_image=$(echo $line | sed 's/^\[//' | sed 's/\]$//')
		echo -e "\tMigrating entry for $current_image"
		if [ -e "/etc/systemimager/rsync_stubs/40$current_image" ]; then
		    echo -e "\t/etc/systemimager/rsync_stubs/40$current_image already exists."
		    echo -e "\tI'm not going to overwrite it with the value from"
		    echo -e "\t/etc/systemimager/rsyncd.conf-before-rsync-stubs.tmp"
		    current_image=""
		fi
	    fi
	    if [ "$current_image" != "" ]; then
		echo "$line" >> /etc/systemimager/rsync_stubs/40$current_image
	    fi
	fi
    done < /etc/systemimager/rsyncd.conf-before-rsync-stubs.tmp
    rm -f /etc/systemimager/rsyncd.conf-before-rsync-stubs.tmp
    echo "Migration complete - please make sure to migrate any configuration you have"
    echo "    made in /etc/systemimager/rsyncd.conf outside of the image section."
fi
## END make stubs from pre-stub /etc/systemimager/rsyncd.conf file

/usr/sbin/mkrsyncd_conf

if [[ -a /usr/lib/lsb/install_initd ]]; then
    /usr/lib/lsb/install_initrd /etc/init.d/systemimager
fi

if [[ -a /sbin/chkconfig ]]; then
    /sbin/chkconfig --del systemimager
fi

%preun server
/etc/init.d/systemimager stop

if [[ -a /usr/lib/lsb/remove_initd ]]; then
    /usr/lib/lsb/remove_initd /etc/init.d/systemimager
fi

if [[ -a /sbin/chkconfig ]]; then
    /sbin/chkconfig --del systemimager
fi

if [[ -a /etc/xinetd.d/rsync.presis~ ]]; then
    mv /etc/xinetd.d/rsync.presis~ /etc/xinetd.d/rsync
    `pidof xinetd > /dev/null`
    if [[ $? == 0 ]]; then
        /etc/init.d/xinetd restart
    fi
fi


%files common
%defattr(-, root, root)
%prefix/bin/lsimage
%prefix/share/man/man8/lsimage*
%prefix/share/man/man5/autoinstall*
%dir %prefix/lib/systemimager
%prefix/lib/systemimager/perl/SystemImager/Common.pm
%prefix/lib/systemimager/perl/SystemImager/Config.pm

%files server
%defattr(-, root, root)
%doc CHANGE.LOG COPYING CREDITS README VERSION
%doc doc/manual/systemimager* doc/manual/html doc/manual/examples
%doc doc/autoinstall* doc/local.cfg
%dir /var/log/systemimager
%dir /var/lib/systemimager/images
%dir /var/lib/systemimager/scripts
%dir /var/lib/systemimager/overrides
%dir /etc/systemimager
%config /etc/systemimager/pxelinux.cfg/*
%config(noreplace) /etc/systemimager/rsync_stubs/*
%config(noreplace) /etc/systemimager/systemimager.conf
/etc/init.d/systemimager
/etc/init.d/netboot*
/var/lib/systemimager/images/*
%prefix/sbin/addclients
%prefix/sbin/cpimage
%prefix/sbin/getimage
%prefix/sbin/mk*
%prefix/sbin/mvimage
%prefix/sbin/netbootmond
%prefix/sbin/pushupdate
%prefix/sbin/rmimage
%prefix/bin/mkautoinstall*
%prefix/lib/systemimager/perl/SystemImager/Server.pm
%prefix/share/man/man5/systemimager*
%prefix/share/man/man8/addclients*
%prefix/share/man/man8/cpimage*
%prefix/share/man/man8/getimage*
%prefix/share/man/man8/install_si*
%prefix/share/man/man8/mk*
%prefix/share/man/man8/mvimage*
%prefix/share/man/man8/rmimage*

%files client
%defattr(-, root, root)
%doc CHANGE.LOG COPYING CREDITS README VERSION
%dir /etc/systemimager
%config /etc/systemimager/updateclient.local.exclude
%config /etc/systemimager/client.conf
%prefix/sbin/updateclient
%prefix/sbin/prepareclient
%prefix/share/man/man8/updateclient*
%prefix/share/man/man8/prepareclient*

%endif

%files %{_build_arch}boot-%{_boot_flavor}
%defattr(-, root, root)
%dir %prefix/share/systemimager/boot/%{_build_arch}
%prefix/share/systemimager/boot/%{_build_arch}/*

