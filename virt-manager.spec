# -*- rpm-spec -*-

%define _package virt-manager
%define _version 0.9.0
%define _release 29
%define virtinst_version 0.600.0-24

%define qemu_user                  "qemu"
%define preferred_distros          "rhel,fedora"
%define kvm_packages               "qemu-kvm"
%define libvirt_packages           "libvirt"
%define disable_unsupported_rhel   1

%define with_guestfs               0
%define with_spice                 1
%define with_tui                   0

%ifnarch %{ix86} x86_64
%define with_spice 0
%define default_graphics ""
%endif


# Compat for use of spec in multiple distros

%if 0%{?gconf_schema_prepare} == 0
%define gconf_schema_prepare() \
if [ "$1" -gt 1 ]; then \
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` \
    gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/%1.schemas > /dev/null || : \
fi \
%{nil}
%endif

%if 0%{?gconf_schema_upgrade} == 0
%define gconf_schema_upgrade() \
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` \
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/%1.schemas > /dev/null || : \
%{nil}
%endif

%if 0%{?gconf_schema_remove} == 0
%define gconf_schema_remove() \
if [ "$1" -eq 0 ]; then \
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` \
    gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/%1.schemas > /dev/null || : \
fi \
%{nil}
%endif


# End local config

# This macro is used for the continuous automated builds. It just
# allows an extra fragment based on the timestamp to be appended
# to the release. This distinguishes automated builds, from formal
# Fedora RPM builds
%define _extra_release %{?dist:%{dist}}%{!?dist:%{?extra_release:%{extra_release}}}

Name: %{_package}
Version: %{_version}
Release: %{_release}%{_extra_release}
%define verrel %{version}-%{release}

Summary: Virtual Machine Manager
Group: Applications/Emulators
License: GPLv2+
URL: http://virt-manager.org/
Source0: http://virt-manager.org/download/sources/%{name}/%{name}-%{version}.tar.gz
# Fix typo that broke net stats reporting (bz 726447)
Patch1: %{name}-fix-net-stats.patch
# Fix autodrawer on RHEL6, unbreaks opening console window (bz 727414)
Patch2: %{name}-rhel6-autodrawer.patch
# Fix 'Resize to VM' graphical option (bz 728541)
Patch3: %{name}-fix-resize-to-vm.patch
# More explicit python binary references (bz 708181)
Patch4: %{name}-explicit-python-bin.patch
# Fix launching 'create pool' dialog (bz 729226)
Patch5: %{name}-rhel6-gtk-fix.patch
# More SCSI option hiding (bz 727766)
Patch6: %{name}-more-scsi-hiding.patch
# Fix showing XML chars in VM name (bz 732371)
Patch7: %{name}-fix-xml-chars.patch
# Fix confusion when removing device with unapplied changes (bz 728845)
Patch8: %{name}-device-remove-confusion.patch
# Fix deleting guest with managed save data (bz 728155)
Patch9: %{name}-managed-save-delete.patch
# Fix error when adding default storage (bz 728497)
Patch10: %{name}-default-storage-error.patch
# Detect that RHEL6 qemu supports spice (bz 734693)
Patch11: %{name}-rhel-supports-spice.patch
# Properly fix crash when deleting a vm device (bz 728845)
Patch12: %{name}-device-removal-confusion2.patch
# Try harder to generate remote URI for localhost for p2p migration (bz 699953)
Patch13: %{name}-p2p-migrate-localhost-uri.patch
# Fix vm lookup race after vm creation (bz 731771)
Patch14: %{name}-create-vm-keyerror.patch
# Fix changing disk bus from virtio->ide (bz 769192, bz 741937)
Patch15: %{name}-fix-bus-change.patch
# Fix serial console stalls when showing lots of text (bz 747490)
Patch16: %{name}-fix-console-stalls.patch
# Fix connection drop if VM gets an error while shutting down (bz 742055)
Patch17: %{name}-dominfo-error-hangup.patch
# Make 'browse local' chooser allow entering a new path (bz 734529)
Patch18: %{name}-browse-local-path.patch
# Escape XML chars in vm description tooltip (bz 741158)
Patch19: %{name}-desc-xml-chars.patch
# Fix keyboard shortcuts when spice isn't focused (bz 733210)
Patch20: %{name}-spice-focus-fix.patch
# Hide unsupported serial types (bz 740775)
Patch21: %{name}-unsupported-serial.patch
# Warn about unapplied changes in customize dialog (bz 736270)
Patch22: %{name}-customize-feedback.patch
# Hide unsupported storage formats (bz 735766)
Patch23: %{name}-unsupported-storage-format.patch
# Fix scaling for spice (bz 750225)
Patch24: %{name}-spice-scaling.patch
# Don't allow a busted iface to break other iface details page (bz 786694)
Patch25: %{name}-iface-error-page.patch
# Option to change default storage format (bz 716673)
Patch26: %{name}-storage-format-option.patch
# Don't switch page every time lxc guest is updated (bz 796570)
Patch27: %{name}-lxc-page-switch.patch
# Don't blacklist disk device if we grab stats for shutdown guest (bz 796092)
Patch28: %{name}-disk-stats-race.patch
# Add QED to disk format list (bz 795323)
Patch29: %{name}-qed-format.patch
# Fix reopening a remote graphical console (bz 811316)
Patch30: %{name}-fix-console-reopen.patch
# Fix app crash when deleting multiple storage volumes (bz 803600)
Patch31: %{name}-delete-vol-crash.patch
# Actually fix graphics listen= addresses (bz 816279)
Patch32: %{name}-fix-listen-address.patch
Patch33: %{name}-Only-reboot-VM-if-it-had-an-install-phase.patch
Patch34: %{name}-match-usb-device-with-vendorID-productID-bus-device.patch
Patch35: %{name}-change-Mbps-to-MB-s-in-migration-dialog.patch
Patch36: %{name}-Make-deleting-storage-files-default.patch
Patch37: %{name}-details-Fix-changing-cirrus-QXL-for-active-VM-bz-928.patch
Patch38: %{name}-Top-level-windows-shouldn-t-be-visible-by-default.patch
Patch39: %{name}-details-the-bus-device-values-of-USB-device-is-decim.patch
Patch40: %{name}-Don-t-fail-on-selecting-network-without-IP.patch
Patch41: %{name}-addhardware-differentiate-duplicate-usb-devices-by-b.patch
Patch42: %{name}-Remove-address-when-changing-watchdog-models.patch
Patch43: %{name}-domain-add-pre-startup-signal-and-do-nodedevs-checki.patch
Patch44: %{name}-create-s-Gb-GB-for-storage-units.patch
Patch45: %{name}-Add-support-for-security-relabeling.patch
Patch46: %{name}-details-Always-show-toolbar-in-customize-dialog.patch
Patch47: %{name}-domain-Handle-PMSUSPENDED-status.patch
Patch48: %{name}-Update-some-help-descriptions.patch
Patch49: %{name}-virt-manager-add-support-for-gluster-storage-pools.patch
Patch50: %{name}-virt-manager-do-not-cause-a-trace-back-when-it-canno.patch
Patch51: %{name}-virt-manager-vmmCreateVolume-uses-the-correct-connec.patch
Patch52: %{name}-virt-manager-fix-char-device-source-mode.patch
Patch53: %{name}-add-new-spice-disable-usbredir-option-to-disable-aut.patch
Patch54: %{name}-error-use-helper-function-to-embed-customized-widget.patch
Patch55: %{name}-details-Add-auto-USB-redirection-support-in-console-.patch
Patch56: %{name}-virt-manager-Add-redirected-devices-details.patch
Patch57: %{name}-virt-manager-Learn-to-add-USB-redirection-devices.patch
Patch58: %{name}-AddHardware-Fix-checking-if-a-widget-is-sensitive.patch
Patch59: %{name}-console-A-few-tweaks-to-usbredir-code.patch
Patch60: %{name}-change-virt-manager-option-spice-disable-usbredir-to.patch
Patch61: %{name}-Properly-format-IPv6-addresses-for-spice.patch
Patch62: %{name}-Add-virtio-scsi-disk-bus-option.patch
Patch63: %{name}-prefs-Allow-changing-the-default-VM-CPU-mode-model-c.patch
Patch64: %{name}-virtManager-specify-missing-argument-in-a-call-to-_s.patch
Patch65: %{name}-xml-fix-xml-for-src-virt-manager.schemas.in.patch
Patch66: %{name}-ui-fix-alignment-of-Preferences-Feedback.patch
Patch67: %{name}-virt-manager-escape-host-string.patch
Patch68: %{name}-console-Handle-ipv6-addresses.patch
Patch69: %{name}-virt-manager-create-pool-Fix-description-of-Source-N.patch
Patch70: %{name}-ui-fix-alignment-of-Preferences-VM-Details.patch
Patch71: %{name}-virt-manager-prevent-events-while-the-storage-pool-m.patch
Patch72: %{name}-virt-manager-make-update-pool-blocking.patch
Patch73: %{name}-virt-manager-add-support-for-showing-panic-notifier-.patch
Patch74: %{name}-virt-manager-add-support-for-adding-panic-notifier-d.patch
Patch75: %{name}-create-whitelist-rhel7.patch
Patch76: %{name}-cli-Skip-gettext-setup-if-setting-locale-fails.patch
Patch77: %{name}-Use-correct-signal-and-callback-names-to-catch-cpu-t.patch
Patch78: %{name}-tunnels-do-not-close-unowned-fd.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# These two are just the oldest version tested
Requires: pygtk2 >= 1.99.12-6
Requires: gnome-python2-gconf >= 1.99.11-7
# This version not strictly required: virt-manager should work with older,
# however varying amounts of functionality will not be enabled.
Requires: libvirt-python >= 0.7.0
# Definitely does not work with earlier due to python API changes
Requires: dbus-python >= 0.61
Requires: dbus-x11
# Might work with earlier, but this is what we've tested
Requires: gnome-keyring >= 0.4.9
# Minimum we've tested with
# Although if you don't have this, comment it out and the app
# will work just fine - keyring functionality will simply be
# disabled
Requires: gnome-python2-gnomekeyring >= 2.15.4
# Minimum we've tested with
Requires: libxml2-python >= 2.6.23
# Absolutely require this version or later
Requires: python-virtinst >= %{virtinst_version}
# Required for loading the glade UI
Requires: pygtk2-libglade
# Earlier vte had broken python binding module
Requires: vte >= 0.12.2
# For online help
Requires: scrollkeeper
# For console widget
Requires: gtk-vnc-python >= 0.3.8
# For local authentication against PolicyKit
# Fedora 12 has no need for a client agent
%if 0%{?fedora} == 11
Requires: PolicyKit-authentication-agent
%endif
%if 0%{?fedora} >= 9 && 0%{?fedora} < 11
Requires: PolicyKit-gnome
%endif
%if %{with_spice}
Requires: spice-gtk-python
%endif
%if %{with_guestfs}
Requires: python-libguestfs
%endif

Obsoletes: virt-manager < 0.9.0-2
%if %{with_tui} == 0
Obsoletes: virt-manager-common <= %{verrel}
Conflicts: virt-manager-common > %{verrel}
%else
Requires: virt-manager-common = %{verrel}
%endif

BuildRequires: gettext
BuildRequires: scrollkeeper
BuildRequires: intltool
BuildRequires: GConf2

Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%if %{with_spice}
%define default_graphics "spice"
%endif

%description
Virtual Machine Manager provides a graphical tool for administering virtual
machines for KVM, Xen, and QEmu. Start, stop, add or remove virtual devices,
connect to a graphical or serial console, and see resource usage statistics
for existing VMs on local or remote machines. Uses libvirt as the backend
management API.

# TUI package setup
%if %{with_tui}
%package tui
Summary: Virtual Machine Manager text user interface
Group: Applications/Emulators

Requires: virt-manager-common = %{verrel}
Requires: python-newt_syrup
Requires: libuser-python
Requires: python-IPy

%description tui
An interactive text user interface for Virtual Machine Manager.

%package common
Summary: Common files used by the different Virtual Machine Manager interfaces
Group: Applications/Emulators

# This version not strictly required: virt-manager should work with older,
# however varying amounts of functionality will not be enabled.
Requires: libvirt-python >= 0.7.0
Requires: dbus-python
# Minimum we've tested with
Requires: libxml2-python >= 2.6.23
# Absolutely require this version or later
Requires: python-virtinst >= %{virtinst_version}

%description common
Common files used by the different Virtual Machine Manager interfaces.
%endif

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1
%patch65 -p1
%patch66 -p1
%patch67 -p1
%patch68 -p1
%patch69 -p1
%patch70 -p1
%patch71 -p1
%patch72 -p1
%patch73 -p1
%patch74 -p1
%patch75 -p1
%patch76 -p1
%patch77 -p1
%patch78 -p1

%build
%if %{qemu_user}
%define _qemu_user --with-qemu_user=%{qemu_user}
%endif

%if %{kvm_packages}
%define _kvm_packages --with-kvm-packages=%{kvm_packages}
%endif

%if %{preferred_distros}
%define _preferred_distros --with-preferred-distros=%{preferred_distros}
%endif

%if %{libvirt_packages}
%define _libvirt_packages --with-libvirt-package-names=%{libvirt_packages}
%endif

%if %{disable_unsupported_rhel}
%define _disable_unsupported_rhel --disable-unsupported-rhel-options
%endif

%if %{?default_graphics}
%define _default_graphics --with-default-graphics=%{default_graphics}
%endif

%if %{with_tui}
%define _tui_opt --with-tui
%else
%define _tui_opt --without-tui
%endif

%configure  %{?_tui_opt} \
            %{?_qemu_user} \
            %{?_kvm_packages} \
            %{?_libvirt_packages} \
            %{?_preferred_distros} \
            %{?_disable_unsupported_rhel} \
            %{?_default_graphics}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install  DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%gconf_schema_prepare %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database -q %{_datadir}/applications
%gconf_schema_upgrade %{name}

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database -q %{_datadir}/applications

%preun
%gconf_schema_remove %{name}

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%if %{with_tui}
%files
%else
%files -f %{name}.lang
%endif
%defattr(-,root,root,-)
%doc README COPYING COPYING-DOCS AUTHORS ChangeLog NEWS
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_bindir}/%{name}
%{_libexecdir}/%{name}-launch

%{_mandir}/man1/%{name}.1*

%if %{with_tui} == 0
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/virtManager/
%{_datadir}/%{name}/virtManager/*.py*
%endif

%{_datadir}/%{name}/*.glade
%{_datadir}/%{name}/%{name}.py*

%{_datadir}/%{name}/icons
%{_datadir}/icons/hicolor/*/apps/*

%{_datadir}/applications/%{name}.desktop
%{_datadir}/dbus-1/services/%{name}.service

%if %{with_tui}
%files common -f %{name}.lang
%defattr(-,root,root,-)
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/virtManager/

%{_datadir}/%{name}/virtManager/*.py*

%files tui
%defattr(-,root,root,-)

%{_bindir}/%{name}-tui
%{_datadir}/%{name}/%{name}-tui.py*

%{_datadir}/%{name}/virtManagerTui
%endif

%changelog
* Thu Feb 26 2015 Giuseppe Scrivano <gscrivan@redhat.com> - 0.9.0-29
- Use correct signal and callback names to catch cpu-threads property changes (rhbz#1190641)
- Fix crash caused by closing an unowned fd (rhbz#1174464)

* Wed Aug 06 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.9.0-28
- Add missing file for "Skip gettext setup if setting locale fails" (rhbz#1124387)

* Thu Jul 31 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.9.0-27
- Skip gettext setup if setting locale fails (rhbz#1124387)

* Thu Jun 05 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.9.0-26
- show RHEL7 in the OS list. (rhbz#1102345)

* Thu May 29 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.9.0-25
- virt-manager: pvpanic device support (rhbz#996517)

* Wed May 21 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.9.0-24
- virt-manager: make update pool blocking (rhbz#1091878)

* Mon May 19 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.9.0-23
- Prevent events while the storage pool model is accessed (rhbz#1091878)

* Fri May 09 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.9.0-22
- Fix alignment of Preferences/VM Details (rhbz#1094083)
- Fix description of "Source Name" in create-pool (rhbz#1094005)
- Handle ipv6 addresses (rhbz#870383)
- virt-manager: escape host string (rhbz#1094600)

* Tue May 06 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.9.0-21
- Fix error reporting (rhbz#1093980)
- Fix parser error when install virt-manager (rhbz#1093979)
- Fix Preferences/Feedback UI alignment (rhbz#1094083)

* Wed Apr 30 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.9.0-20
- virt-manager shows the right guest status when guest is pmsuspended (rhbz#1091292)
- Make consistent virt-manager's option "--profile=File" between manual page and help page. (rhbz#1069090)
- Virt-manager: Add Virtio SCSI disk option. (rhbz#1049781)
- Allow changing the default new VM CPU model. (rhbz#1046583)
- virt-manager supports native gluster fs (rhbz#1040172)
- virt-manager doesn't cause a python trace-back when it cannot open display (rhbz#1025706)
- AttributeError: 'NoneType' object has no attribute 'storagePoolLookupByName' (rhbz#927257)
- virt-manager doesn't set up TCP net console mode properly (rhbz#918451)
- virt-manager cannot open console through IPV6. (rhbz#870383)
- Support SPICE auto-redir in virt-manager (rhbz#807277)

* Thu Aug 01 2013 Martin Kletzander <mkletzan@redhat.com> - 0.9.0-19
- Fix changing cirrus->QXL for active VM (rhbz#985184)
- Top level windows shouldn't be visible by default (rhbz#990507)
- The bus, device values of USB device is decimal rather than hex (rhbz#820303)
- Don't fail on selecting network without IP (rhbz#869474)
- Differentiate duplicate usb devices by bus/addr (rhbz#820303)
- Remove address when changing watchdog models (rhbz#869206)
- Add 'pre-startup' signal and do nodedevs checking (rhbz#820303)
- Create: s/Gb/GB/ for storage units (rhbz#873142)
- Add support for security relabeling (rhbz#907399)
- Always show toolbar in customize dialog (rhbz#981628)

* Wed Dec 05 2012 Jiri Denemark <jdenemar@redhat.com> - 0.9.0-18
- Really apply patch for (rhbz#878946)

* Wed Dec 05 2012 Jiri Denemark <jdenemar@redhat.com> - 0.9.0-17
- Make deleting storage files default with added prompt (rhbz#878946)

* Mon Dec 03 2012 Jiri Denemark <jdenemar@redhat.com> - 0.9.0-16
- spec: Fix localupdate from noarch (rhbz#872611)

* Fri Oct 12 2012 Jiri Denemark <jdenemar@redhat.com> - 0.9.0-15
- Only reboot VM if it had an install phase (rhbz#824275)
- Match usb device with vendorID, productID, bus, device (rhbz#820303)
- Change Mbps to MB/s in migration dialog (rhbz#802639)

* Thu May 03 2012 Cole Robinson <crobinso@redhat.com> - 0.9.0-14
- Actually fix graphics listen= addresses (bz 816279)

* Wed May 02 2012 Cole Robinson <crobinso@redhat.com> - 0.9.0-13
- Fix graphical console for non localhost listen address (bz 816279)

* Wed Apr 25 2012 Cole Robinson <crobinso@redhat.com> - 0.9.0-12
- Fix reopening a remote graphical console (bz 811316)
- Fix app crash when deleting multiple storage volumes (bz 803600)

* Mon Apr 02 2012 Cole Robinson <crobinso@redhat.com> - 0.9.0-11
- Don't switch page every time lxc guest is updated (bz 796570)
- Don't blacklist disk device if we grab stats for shutdown guest (bz
  796092)
- Add QED to disk format list (bz 795323)

* Mon Feb 13 2012 Cole Robinson <crobinso@redhat.com> - 0.9.0-10
- Option to change default storage format (bz 716673)

* Thu Feb 09 2012 Cole Robinson <crobinso@redhat.com> - 0.9.0-9
- Fix scaling for spice (bz 750225)
- Don't allow a busted iface to break other iface details page (bz
  786694)

* Wed Feb 01 2012 Cole Robinson <crobinso@redhat.com> - 0.9.0-8
- Fix changing disk bus from virtio->ide (bz 769192, bz 741937)
- Fix serial console stalls when showing lots of text (bz 747490)
- Fix connection drop if VM gets an error while shutting down (bz
  742055)
- Make 'browse local' chooser allow entering a new path (bz 734529)
- Escape XML chars in vm description tooltip (bz 741158)
- Fix keyboard shortcuts when spice isn't focused (bz 733210)
- Hide unsupported serial types (bz 740775)
- Warn about unapplied changes in customize dialog (bz 736270)
- Hide unsupported storage formats (bz 735766)

* Thu Oct 13 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-7
- Detect that RHEL6 qemu supports spice (bz 734693)
- Properly fix crash when deleting a vm device (bz 728845)
- Try harder to generate remote URI for localhost for p2p migration (bz
  699953)
- Fix vm lookup race after vm creation (bz 731771)

* Tue Aug 30 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-6
- Fix 'Resize to VM' graphical option (bz 728541)
- More explicit python binary references (bz 708181)
- Fix launching 'create pool' dialog (bz 729226)
- More SCSI option hiding (bz 727766)
- Fix showing XML chars in VM name (bz 732371)
- Fix confusion when removing device with unapplied changes (bz 728845)
- Fix deleting guest with managed save data (bz 728155)
- Fix error when adding default storage (bz 728497)
- Disable unsupported RHEL6 options (bz 727766, bz 710337, bz 729590, bz
  717373)

* Tue Aug 02 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-5
- Fix autodrawer on RHEL6, unbreaks opening console window (bz 727414)
- Update icon cache after RPM install

* Mon Aug 01 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-4
- Manually define gconf macro if not found (bz 726325)

* Thu Jul 28 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-3
- Fix typo that broke net stats reporting (bz 726447)
- Add BuildRequires: GConf2 to fix package install (bz 726325)

* Wed Jul 27 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-2.el6
- Only depend on spice for arch=*86

* Tue Jul 26 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-1.el6
- Rebased to version 0.9.0
- Use a hiding toolbar for fullscreen mode
- Use libguestfs to show guest packagelist and more (Richard W.M. Jones)
- Basic 'New VM' wizard support for LXC guests
- Remote serial console access (with latest libvirt)
- Remote URL guest installs (with latest libvirt)
- Add Hardware: Support <filesystem> devices
- Add Hardware: Support <smartcard> devices (Marc-André Lureau)
- Enable direct interface selection for qemu/kvm (Gerhard Stenzel)
- Allow viewing and changing disk serial number

* Tue Apr 19 2011 Cole Robinson <crobinso@redhat.com> - 0.8.6-4.el6
- Fix device hotplug fallback attach (bz 692808)

* Wed Mar 09 2011 Cole Robinson <crobinso@redhat.com> - 0.8.6-3.el6
- Add ICH6 sound model (bz 680827)
- Don't error if shutting down a transient domain (bz 681113)
- Don't offer to create readonly file formats (673028)
- Improve wording if offering to reuse existing storage (bz 669741)
- Disallow changing format in 'customize' screen for new storage (bz 677255)

* Thu Feb 24 2011 Cole Robinson <crobinso@redhat.com> - 0.8.6-2
- Don't launch consoles on app startup (bz 670735)
- Fix connecting to VNC over unix socket (bz 651606)
- Fix changing 'Overview' settings (bz 673463)

* Fri Jan 14 2011 Cole Robinson <crobinso@redhat.com> - 0.8.6-1.el6
- Rebase to 0.8.6 (bz 658959)
- SPICE support (requires spice-gtk) (Marc-André Lureau)
- Option to configure CPU model
- Option to configure CPU topology
- Save and migration cancellation (Wen Congyang)
- Save and migration progress reporting
- Option to enable bios boot menu
- Option to configure direct kernel/initrd boot

* Wed Aug 11 2010 Chris Lalancette <clalance@redhat.com> - 0.8.4-8.el6
- Update translations (bz 575681)

* Wed Jul  7 2010 Cole Robinson <crobinso@redhat.com> - 0.8.4-7.el6
- Actually fix VNC auto keymap detection (bz 593333)

* Mon Jun 28 2010 Cole Robinson <crobinso@redhat.com> - 0.8.4-6.el6
- Reconnect to serial console on VM reboot (bz 604721)

* Mon Jun 21 2010 Cole Robinson <crobinso@redhat.com> - 0.8.4-5.el6
- Allow setting cpuset automatically from NUMA config (bz 604205)
- Update translations (bz 575681)
- Fix pool building for LVM/disk pools (bz 597519)

* Fri May 28 2010 Cole Robinson <crobinso@redhat.com> - 0.8.4-4.el6
- Allow changing disk cache mode (bz 594080)

* Tue May 18 2010 Cole Robinson <crobinso@redhat.com> - 0.8.4-3.el6
- Fix VNC reconnect error (bz 593326)
- Fix remote VNC connection with zsh (bz 593328)
- Fix VNC auto keymap detection (bz 593333)
- Fix New VM customize option with no storage (bz 593336)

* Thu May 13 2010 Cole Robinson <crobinso@redhat.com> - 0.8.4-2.el6
- Fix broken icon in UI (bz 577249)
- Only close connection on 'remote' error (bz 580613)
- Add pool refresh button (bz 580567)
- Managed save/restore support (bz 591625)
- Fix first run hypervisor detection (bz 591584)
- Don't allow shutdown or unpause while cloning (bz 577252)
- Offer to start default storage pool (bz 584672)
- Skip post-install restart if user destroys VM (bz 587703)
- Don't install outdated help docs (bz 588577)
- Warn about unsupported VCPU overcommit (bz 588655)
- Hide unsupported sound models (bz 588695)

* Wed Mar 24 2010 Cole Robinson <crobinso@redhat.com> - 0.8.4-1
- Rebase to 0.8.4
- 'Import' install option, to create a VM around an existing OS image
- Support multiple boot devices and boot order
- Watchdog device support
- Enable setting a human readable VM description.
- Option to manually specifying a bridge name, if bridge isn't detected

* Wed Jan 13 2010 Cole Robinson <crobinso@redhat.com> - 0.8.2-3.fc12
- Avoid use of HAL for device enumeration (bz 515734)

* Tue Jan 12 2010 Cole Robinson <crobinso@redhat.com> - 0.8.2-2.fc12
- Build with actual upstream tarball (not manually built dist)

* Mon Dec 14 2009 Cole Robinson <crobinso@redhat.com> - 0.8.2-1.fc12
- Update to 0.8.2 release
- Fix first virt-manager run on a new install
- Enable floppy media eject/connect

* Wed Dec 09 2009 Cole Robinson <crobinso@redhat.com> - 0.8.1-3.fc12
- Select manager row on right click, regressed with 0.8.1

* Sat Dec  5 2009 Cole Robinson <crobinso@redhat.com> - 0.8.1-2.fc12
- Set proper version Requires: for python-virtinst

* Thu Dec  3 2009 Cole Robinson <crobinso@redhat.com> - 0.8.1-1.fc12
- Update to release 0.8.1
- VM Migration wizard, exposing various migration options
- Enumerate CDROM and bridge devices on remote connections
- Support storage pool source enumeration for LVM, NFS, and SCSI

* Mon Oct 05 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-7.fc12
- More translations (bz 493795)
- Don't allow creating a volume without a name (bz 526111)
- Don't allow volume allocation > capacity (bz 526077)
- Add tooltips for toolbar buttons (bz 524083)

* Tue Sep 29 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-6.fc12
- Fix VCPU hotplug
- Remove access to outdated docs (bz 522823, bz 524805)
- Update VM state text in manager view (bz 526182)
- Update translations (bz 493795)

* Thu Sep 24 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-5.fc12
- Refresh host disk space in create wizard (bz 502777)
- Offer to fix disk permission issues (bz 517379)

* Thu Sep 17 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-4.fc12
- Don't close libvirt connection for non-fatal errors (bz 522168)
- Manager UI tweaks
- Generate better errors if disk/net stats polling fails

* Mon Sep 14 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-3.fc12
- Fix disk XML mangling via connect/eject cdrom (bz 516116)
- Fix delete button sensitivity (bz 518536)
- Fix populating text box from storage browser in 'New VM' (bz 517263)
- Fix a traceback in an 'Add Hardware' error path (bz 517286)

* Thu Aug 13 2009 Daniel P. Berrange <berrange@redhat.com> - 0.8.0-2.fc12
- Remove obsolete dep on policykit agent

* Tue Jul 28 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-1.fc12
- Update to release 0.8.0
- New 'Clone VM' Wizard
- Improved UI, including an overhaul of the main 'manager' view
- System tray icon for easy VM access (start, stop, view console/details)
- Wizard for adding serial, parallel, and video devices to existing VMs.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 21 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.0-5.fc12
- Fix 'opertaing' typo in 'New VM' dialog (#495128)
- Allow details window to resize again (#491683)
- Handle collecting username for vnc authentication (#499589)
- Actually handle arch config when creating a VM (#499145)
- Log libvirt capabilities at startup to aid debugging (#500337)

* Tue Apr 14 2009 Cole Robinson <crobinso@redhat.com> - 0.7.0-4.fc11
- More translation updates

* Thu Apr 09 2009 Cole Robinson <crobinso@redhat.com> - 0.7.0-3.fc11
- Fix incorrect max vcpu setting in New VM wizard (bz 490466)
- Fix some OK/Cancel button ordering issues (bz 490207)
- Use openAuth when duplicating a connection when deleting a VM
- Updated translations (bz 493795)

* Mon Mar 23 2009 Cole Robinson <crobinso@redhat.com> - 0.7.0-2.fc11
- Back compat fixes for connecting to older xen installations (bz 489885)
- Don't show harmless NoneType error when launching new VM details window

* Tue Mar 10 2009 Cole Robinson <crobinso@redhat.com> - 0.7.0-1.fc11
- Update to release 0.7.0
- Redesigned 'New Virtual Machine' wizard
- Option to remove storage when deleting a virtual machine.
- File browser for libvirt storage pools and volumes
- Physical device assignment (PCI, USB) for existing virtual machines.

* Wed Mar  4 2009 Cole Robinson <crobinso@redhat.com> - 0.6.1-4.fc11
- Update polish translation (bz 263301)
- Fix sending ctrl-alt-del to guest
- Fix cpu + mem stats options to remember preference.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  9 2009 Cole Robinson <crobinso@redhat.com> - 0.6.1-2
- Kill off consolehelper (PolicyKit is sufficient)

* Mon Jan 26 2009 Cole Robinson <crobinso@redhat.com> - 0.6.1-1
- Update to 0.6.1 release
- Disk and Network VM stats reporting
- VM Migration support
- Support adding sound devices to existing VMs
- Allow specifying device model when adding a network device to an existing VM

* Tue Jan 20 2009 Mark McLoughlin <markmc@redhat.com> - 0.6.0-7
- Add patch to ignore fix crash on force-poweroff with serial console (#470548)

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.0-6
- Rebuild for Python 2.6

* Mon Dec  1 2008 Cole Robinson <crobinso@redhat.com> - 0.6.0-5.fc10
- Fix spec for building on F9
- Update 'New VM' virt descriptions to be less black and white (bz 470563)

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.0-4
- Rebuild for Python 2.6

* Mon Oct 27 2008 Cole Robinson <crobinso@redhat.com> - 0.6.0-3.fc10
- Add dbus-x11 to Requires (bug 467886)
- Fedora translation updates (bug 467808)
- Don't add multiple sound devices if install fails
- Only popup volume path copy option on right click
- Fix a variable typo

* Tue Oct 14 2008 Cole Robinson <crobinso@redhat.com> - 0.6.0-2.fc10
- Add gnome-python2-gnome requirement.
- Allow seeing connection details if disconnected.
- Updated catalan translation.
- Update dutch translation.
- Update german translation. (bug 438136)
- Fix showing domain console when connecting to hypervisor.
- Update POTFILES to reflect reality (bug 466835)

* Wed Sep 10 2008 Cole Robinson <crobinso@redhat.com> - 0.6.0-1.fc10
- Update to 0.6.0 release
- Add libvirt storage management support
- Basic support for remote guest installation
- Merge VM console and details windows
- Poll avahi for libvirtd advertisement
- Hypervisor autoconnect option
- Add sound emulation when creating new guests

* Thu Apr  3 2008 Daniel P. Berrange <berrange@redhat.com> - 0.5.4-3.fc9
- Updated sr, de, fi, it, pl translations

* Thu Mar 13 2008 Daniel P. Berrange <berrange@redhat.com> - 0.5.4-2.fc9
- Don't run policykit checks when root (rhbz #436994)

* Mon Mar 10 2008 Daniel P. Berrange <berrange@redhat.com> - 0.5.4-1.fc9
- Update to 0.5.4 release

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5.3-2
- Autorebuild for GCC 4.3

* Thu Jan 10 2008 Daniel P. Berrange <berrange@redhat.com> - 0.5.3-1.fc9
- Update to 0.5.3 release

* Mon Oct 15 2007 Daniel P. Berrange <berrange@redhat.com> - 0.5.2-2.fc8
- Change TLS x509 credential name to sync with libvirt

* Thu Oct  4 2007 Daniel P. Berrange <berrange@redhat.com> - 0.5.2-1.fc8
- Update to 0.5.2 release
- No scrollbars for high res guest in low res host (rhbz 273181)
- Unable to remove network device (rhbz 242900)
- Fixed broken menu items (rhbz 307551)
- Require libvirt 0.3.3 to get CDROM change capability for Xen

* Tue Sep 25 2007 Daniel P. Berrange <berrange@redhat.com> - 0.5.1-1.fc8
- Updated to 0.5.1 release
- Open connections in background
- Make VNC connection retries more robust
- Allow changing of CDROM media on the fly
- Add PXE boot installation of HVM guests
- Allow tunnelling VNC over SSH

* Wed Aug 29 2007 Daniel P. Berrange <berrange@redhat.com> - 0.5.0-1.fc8
- Updated to 0.5.0 release
- Support for managing remote hosts
- Switch to use GTK-VNC for the guest console

* Fri Aug 24 2007 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-3.fc8
- Remove ExcludeArch since libvirt is now available

* Wed May  9 2007 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-2.fc7
- Refresh po file translations (bz 238369)
- Fixed removal of disk/network devices
- Fixed toolbar menu option state
- Fixed file dialogs & default widget states

* Mon Apr 16 2007 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-1.fc7
- Support for managing virtual networks
- Ability to attach guest to virtual networks
- Automatically set VNC keymap based on local keymap
- Support for disk & network device addition/removal

* Wed Mar 28 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.2-3.fc7
- Fix HVM check to allow KVM guests to be created (bz 233644)
- Fix default file size suggestion

* Tue Mar 27 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.2-2.fc7
- Ensure we own all directories we create (bz 233816)

* Tue Mar 20 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.2-1.fc7
- Added online help to all windows
- Bug fixes to virtual console popup, key grab & accelerator override

* Tue Mar 13 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.1-4.fc7
- Fixed thread locking to avoid deadlocks when a11y is enabled

* Fri Mar  2 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.1-3.fc7
- Fixed keyboard ungrab in VNC widget

* Tue Feb 20 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.1-2.fc7
- Only check for HVM on Xen hypervisor

* Tue Feb 20 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.1-1.fc7
- Added support for managing QEMU domains
- Automatically grab mouse pointer to workaround dual-cursor crazyness

* Wed Jan 31 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.0-2.fc7
- Added dep on desktop-file-utils for post/postun scripts

* Mon Jan 22 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.0-1.fc7
- Added support for managing inactive domains
- Require virt-inst >= 0.100.0 and libvirt >= 0.1.11 for ianctive
  domain management capabilities
- Add progress bars during VM creation stage
- Improved reliability of VNC console
- Updated translations again
- Added destroy option to menu bar to forceably kill a guest
- Visually differentiate allocated memory, from actual used memory on host
- Validate file magic when restoring a guest from a savd file
- Performance work on domain listing
- Allow creation of non-sparse files
- Fix backspace key in serial console

* Tue Dec 19 2006 Daniel P. Berrange <berrange@redhat.com> - 0.2.6-3.fc7
- Imported latest translations from Fedora i18n repository (bz 203783)
- Use 127.0.0.1 address for connecting to VNC console instead of
  localhost to avoid some issue with messed up /etc/hosts.
- Add selector for sparse or non-sparse file, defaulting to non-sparse.
  Add appropriate warnings and progress-bar text. (bz 218996)
- Disable memory ballooning & CPU hotplug for HVM guests (bz 214432)
- Updated memory-setting UI to include a hard upper limit for physical
  host RAM
- Added documentation on the page warning that setting virtual host RAM
  too high can exhaust the memory of the machine
- Handle errors when hostname resolution fails to avoid app exiting (bz 216975)

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.2.6-2.fc7
- rebuild for python 2.5

* Thu Nov  9 2006 Daniel P. Berrange <berrange@redhat.com> - 0.2.6-1.fc7
- Imported translations from Fedora i18n repository
- Make (most) scrollbar policies automatic
- Set busy cursor while creating new VMs
- Preference for controlling keygrab policy
- Preference for when to automatically open console (bz 211385)
- Re-try VNC connection attempt periodically in case VNC daemon
  hasn't finished starting up
- Added activation of URLs for about dialog (bz 210782)
- Improved error reporting when connecting to HV (bz 211229)
- Add command line args to open specific windows
- Don't skip para/full virt wizard step - instead gray out full
  virt option & tell user why
- Change 'physical' to 'logical' when refering to host CPUs
- Include hostname in titlebar
- Disable wizard sensitivity while creating VM

* Thu Oct 19 2006 Daniel P. Berrange <berrange@redhat.com> - 0.2.5-1.fc7
- Switch to use python-virtinst instead of python-xeninst due to 
  renaming of original package
- Disable keyboard accelerators when grabbing mouse to avoid things like
  Ctrl-W closing the local window, instead of remote window bz 210364
- Fix host memory reporting bz 211281
- Remove duplicate application menu entry bz 211230
- Fix duplicated mnemonics (bz 208408)
- Use blktap backed disks if available
- Use a drop down list to remember past URLs (bz 209479)
- Remove unused help button from preferences dialog (bz 209251)
- Fix exception when no VNC graphics is defined
- Force immediate refresh of VMs after creating a new one
- Improve error reporting if run on a kernel without Xen (bz 209122)
- More fixes to avoid stuck modifier keys on focus-out (bz 207949)

* Fri Sep 29 2006 Daniel P. Berrange <berrange@redhat.com> 0.2.3-2.fc6
- Fix segv in sparkline code when no data points are defined (bz  208185)
- Clamp CPU utilization between 0 & 100% just in case (bz 208185)

* Tue Sep 26 2006 Daniel Berrange <berrange@redhat.com> - 0.2.3-1.fc6
- Require xeninst >= 0.93.0 to fix block backed devices
- Skip para/fully-virt step when going back in wizard if not HVM host (bz 207409)
- Fix handling of modifier keys in VNC console so Alt key doesn't get stuck (bz 207949)
- Allow sticky modifier keys by pressing same key 3 times in row (enables Ctrl-Alt-F1
  by doing Ctrl Ctrl Ctrl  Alt-F1)
- Improved error handling during guest creation
- Log errors with python logging, instead of to stdout
- Remove unused buttons from main domain list window
- Switch out of full screen & release key grab when closing console
- Trim sparkline CPU history graph to 40 samples max
- Constraint VCPU adjuster to only allow upto guest's max VCPU count
- Show guest's max & current VCPU count in details page
- Fix rounding of disk sizes to avoid a 1.9 GB disk being rounded down to 1 GB
- Use raw block device path to CDROM not mount point for HVM guest (bz 206965)
- Fix visibility of file size spin box (bz 206186 part 2)
- Check for GTK failing to open X11 display (bz 205938)

* Fri Sep 15 2006 Daniel Berrange <berrange@redhat.com> - 0.2.2-1.fc6
- Fix event handling in create VM wizard (bz 206660 & 206186)
- Fix close button in about dialog (bz 205943)
- Refresh .pot files
- Turn on VNC scrollbars fulltime to avoid GTK window sizing issue
  which consistently resize too small.

* Mon Sep 11 2006 Daniel Berrange <berrange@redhat.com> - 0.2.1-3.fc6
- Added requires on pygtk2-libglade & librsvg2 (bz 205941 & 205942)
- Re-arrange to use console-helper to launch app
- Added 'dist' component to release number

* Wed Sep  6 2006 Jeremy Katz <katzj@redhat.com> - 0.2.1-2
- don't ghost pyo files (#205448)

* Mon Sep  4 2006 Daniel Berrange <berrange@redhat.com> - 0.2.1-1
- Updated to 0.2.1 tar.gz
- Added rules to install/uninstall gconf schemas in preun,post,pre
  scriptlets
- Updated URL for source to reflect new upstream download URL

* Thu Aug 24 2006 Jeremy Katz <katzj@redhat.com> - 0.2.0-3
- BR gettext

* Thu Aug 24 2006 Jeremy Katz <katzj@redhat.com> - 0.2.0-2
- only build on arches with virt

* Tue Aug 22 2006 Daniel Berrange <berrange@redhat.com> - 0.2.0-1
- Added wizard for creating virtual machines
- Added embedded serial console
- Added ability to take screenshots

* Mon Jul 24 2006 Daniel Berrange <berrange@redhat.com> - 0.1.5-2
- Prefix *.pyo files with 'ghost' macro
- Use fully qualified URL in Source  tag

* Thu Jul 20 2006 Daniel Berrange <berrange@redhat.com> - 0.1.5-1
- Update to new 0.1.5 release snapshot

* Thu Jul 20 2006 Daniel Berrange <berrange@redhat.com> - 0.1.4-1
- Update to new 0.1.4 release snapshot

* Mon Jul 17 2006 Daniel Berrange <berrange@redhat.com> - 0.1.3-1
- Fix License tag
- Updated for new release

* Wed Jun 28 2006 Daniel Berrange <berrange@redhat.com> - 0.1.2-3
- Added missing copyright headers on all .py files

* Wed Jun 28 2006 Daniel Berrange <berrange@redhat.com> - 0.1.2-2
- Added python-devel to BuildRequires

* Wed Jun 28 2006 Daniel Berrange <berrange@redhat.com> - 0.1.2-1
- Change URL to public location

* Fri Jun 16 2006 Daniel Berrange <berrange@redhat.com> - 0.1.0-1
- Added initial support for using VNC console

* Thu Apr 20 2006 Daniel Berrange <berrange@redhat.com> - 0.0.2-1
- Added DBus remote control service

* Wed Mar 29 2006 Daniel Berrange <berrange@redhat.com> - 0.0.1-1
- Initial RPM build
