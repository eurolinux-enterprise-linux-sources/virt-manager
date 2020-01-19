# -*- rpm-spec -*-


%define with_guestfs               0
%define stable_defaults            0
%define askpass_package            "openssh-askpass"
%define qemu_user                  "qemu"
%define libvirt_packages           "libvirt-daemon-kvm,libvirt-daemon-config-network"
%define kvm_packages               ""
%define preferred_distros          "fedora,rhel"
%define default_hvs                "qemu,xen"

%if 0%{?rhel}
%define preferred_distros          "rhel,fedora"
%define stable_defaults            1
%endif


# End local config


%define _version 1.4.1
%define _release 7


Name: virt-manager
Version: %{_version}
Release: %{_release}%{?dist}%{?extra_release}
%define verrel %{version}-%{release}

Summary: Desktop tool for managing virtual machines via libvirt
Group: Applications/Emulators
License: GPLv2+
BuildArch: noarch
URL: http://virt-manager.org/
Source0: http://virt-manager.org/download/sources/%{name}/%{name}-%{version}.tar.gz

Patch1: virt-manager-RHEL-only-virt-install-doc-remove-reference-to-physi.patch
Patch2: virt-manager-graphics-skip-authentication-only-for-VNC-with-liste.patch
Patch3: virt-manager-storage-Move-alloc-cap-validation-to-validate.patch
Patch4: virt-manager-Update-italian-translation-from-zanata.patch
Patch5: virt-manager-Fix-busted-italian-translation-again-bug-1433800.patch
Patch6: virt-manager-Update-some-translations.patch
Patch7: virt-manager-Fix-format-errors-in-it.po-and-ko.po.patch
Patch8: virt-manager-cli-Don-t-double-warn-when-skipping-disk-size-warnin.patch
Patch9: virt-manager-devicedisk-Raise-proper-error-on-invalid-source_volu.patch
Patch10: virt-manager-sshtunnels-Detect-listen-type-none-for-VNC-bz-144571.patch
Patch11: virt-manager-virtinst.cpu-don-t-validate-cpus-for-NUMA-cells.patch
Patch12: virt-manager-virtinst-introduce-support-for-maxMemory-element.patch
Patch13: virt-manager-virtinst-add-support-for-memory-device.patch
Patch14: virt-manager-interface-don-t-print-error-for-active-interface-wit.patch
Patch15: virt-manager-Reset-Guest.domain-to-None-on-domain-creation-error.patch
Patch16: virt-manager-guest-Don-t-repeatedly-overwrite-self.domain.patch
Patch17: virt-manager-guest-Only-use-define-start-logic-for-vz.patch
Patch18: virt-manager-virtinst.diskbackend-set-pool-after-creating-Storage.patch
Patch19: virt-manager-virtManager.connection-introduce-cb_add_new_pool.patch
Patch20: virt-manager-virt-install-add-support-for-SMM-feature.patch
Patch21: virt-manager-virt-install-add-support-for-loader-secure-attribute.patch
Patch22: virt-manager-virtinst-if-required-by-UEFI-enable-SMM-feature-and-.patch
Patch23: virt-manager-localization-update-Japanese-translations.patch
Patch24: virt-manager-virtinst-enable-secure-feature-together-with-smm-for.patch

Requires: virt-manager-common = %{verrel}
Requires: pygobject3
Requires: gtk3
Requires: libvirt-glib >= 0.0.9
Requires: dconf
Requires: dbus-x11

# The vte291 package is actually the latest vte with API version 2.91, while
# the vte3 package is effectively a compat package with API version 2.90.
# virt-manager works fine with either, so pull the latest bits so there's
# no ambiguity.
Requires: vte291

# For console widget
Requires: gtk-vnc2
Requires: spice-gtk3

%if 0%{?rhel} == 7
Requires: gnome-icon-theme
%endif


BuildRequires: intltool
BuildRequires: /usr/bin/pod2man
# For python, and python2 rpm macros
BuildRequires: python2-devel


%description
Virtual Machine Manager provides a graphical tool for administering virtual
machines for KVM, Xen, and LXC. Start, stop, add or remove virtual devices,
connect to a graphical or serial console, and see resource usage statistics
for existing VMs on local or remote machines. Uses libvirt as the backend
management API.


%package common
Summary: Common files used by the different Virtual Machine Manager interfaces
Group: Applications/Emulators

# This version not strictly required: virt-manager should work with older,
# however varying amounts of functionality will not be enabled.
Requires: libvirt-python >= 0.7.0
Requires: libxml2-python
Requires: python-requests
Requires: python-ipaddr
Requires: libosinfo >= 0.2.11
# Required for gobject-introspection infrastructure
Requires: pygobject3-base

%description common
Common files used by the different virt-manager interfaces, as well as
virt-install related tools.


%package -n virt-install
Summary: Utilities for installing virtual machines

Requires: virt-manager-common = %{verrel}
# For 'virsh console'
Requires: libvirt-client

Provides: virt-install
Provides: virt-clone
Provides: virt-xml
Obsoletes: python-virtinst

%description -n virt-install
Package includes several command line utilities, including virt-install
(build and install new VMs) and virt-clone (clone an existing virtual
machine).


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

%build
%if %{qemu_user}
%define _qemu_user --qemu-user=%{qemu_user}
%endif

%if %{kvm_packages}
%define _kvm_packages --kvm-package-names=%{kvm_packages}
%endif

%if %{preferred_distros}
%define _preferred_distros --preferred-distros=%{preferred_distros}
%endif

%if %{libvirt_packages}
%define _libvirt_packages --libvirt-package-names=%{libvirt_packages}
%endif

%if %{askpass_package}
%define _askpass_package --askpass-package-names=%{askpass_package}
%endif

%if %{stable_defaults}
%define _stable_defaults --stable-defaults
%endif

%if %{default_hvs}
%define _default_hvs --default-hvs %{default_hvs}
%endif

python setup.py configure \
    %{?_qemu_user} \
    %{?_kvm_packages} \
    %{?_libvirt_packages} \
    %{?_askpass_package} \
    %{?_preferred_distros} \
    %{?_stable_defaults} \
    %{?_default_hvs}


%install
python setup.py \
    --no-update-icon-cache --no-compile-schemas \
    install -O1 --root=$RPM_BUILD_ROOT
%find_lang %{name}

# Replace '#!/usr/bin/env python2' with '#!/usr/bin/python2'
# The format is ideal for upstream, but not a distro. See:
# https://fedoraproject.org/wiki/Features/SystemPythonExecutablesUseSystemPython
for f in $(find %{buildroot} -type f -executable -print); do
    sed -i "1 s|^#!/usr/bin/env python2|#!%{__python2}|" $f || :
done

# The conversion script was only added to virt-manager after several
# Fedora cycles of using gsettings. Installing it now could convert old data
# and wipe out recent settings.
rm %{buildroot}%{_datadir}/GConf/gsettings/org.virt-manager.virt-manager.convert


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%doc README.md COPYING NEWS.md
%{_bindir}/%{name}

%{_mandir}/man1/%{name}.1*

%{_datadir}/%{name}/ui/*.ui
%{_datadir}/%{name}/virt-manager
%{_datadir}/%{name}/virtManager

%{_datadir}/%{name}/icons
%{_datadir}/icons/hicolor/*/apps/*

%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/glib-2.0/schemas/org.virt-manager.virt-manager.gschema.xml


%files common -f %{name}.lang
%dir %{_datadir}/%{name}

%{_datadir}/%{name}/virtcli
%exclude %{_datadir}/%{name}/virtconv
%{_datadir}/%{name}/virtinst


%files -n virt-install
%{_mandir}/man1/virt-install.1*
%{_mandir}/man1/virt-clone.1*
%exclude %{_mandir}/man1/virt-convert.1*
%{_mandir}/man1/virt-xml.1*

%{_datadir}/%{name}/virt-install
%{_datadir}/%{name}/virt-clone
%exclude %{_datadir}/%{name}/virt-convert
%{_datadir}/%{name}/virt-xml

%{_bindir}/virt-install
%{_bindir}/virt-clone
%exclude %{_bindir}/virt-convert
%{_bindir}/virt-xml


%changelog
* Thu Jun 08 2017 Pavel Hrdina <phrdina@redhat.com> - 1.4.1-7
- virtinst: enable secure feature together with smm for UEFI (rhbz#1387479)

* Mon Jun 05 2017 Pavel Hrdina <phrdina@redhat.com> - 1.4.1-6
- virt-install: add support for SMM feature (rhbz#1387479)
- virt-install: add support for loader secure attribute (rhbz#1387479)
- virtinst: if required by UEFI enable SMM feature and set q35 machine type (rhbz#1387479)
- localization: update Japanese translations (rhbz#1375044)

* Wed May 24 2017 Pavel Hrdina <phrdina@redhat.com> - 1.4.1-5
- Reset Guest.domain to None on domain creation error (rhbz#1441902)
- guest: Don't repeatedly overwrite self.domain (rhbz#1441902)
- guest: Only use define+start logic for vz (rhbz#1441902)
- virtinst.diskbackend: set pool after creating StorageVolume (rhbz#1450311)
- virtManager.connection: introduce cb_add_new_pool (rhbz#1435064)

* Tue May 16 2017 Pavel Hrdina <phrdina@redhat.com> - 1.4.1-4
- virtinst.cpu: don't validate "cpus" for NUMA cells (rhbz#1281526)
- virtinst: introduce support for <maxMemory> element (rhbz#1281526)
- virtinst: add support for memory device (rhbz#1281526)
- interface: don't print error for active interface without an IP address (rhbz#1449509)

* Wed May 03 2017 Pavel Hrdina <phrdina@redhat.com> - 1.4.1-3
- cli: Don't double warn when skipping disk size warning (rhbz#1433239)
- devicedisk: Raise proper error on invalid source_volume (rhbz#1445198)
- sshtunnels: Detect listen type=none for VNC (rhbz#1445714)

* Thu Apr 20 2017 Pavel Hrdina <phrdina@redhat.com> - 1.4.1-2
- graphics: skip authentication only for VNC with listen type none (rhbz#1434551)
- storage: Move alloc/cap validation to validate() (rhbz#1433239)
- Update italian translation from zanata (rhbz#1435806)
- Fix busted italian translation, again (bug 1433800) (rhbz#1435806)
- Update some translations (rhbz#1435806)
- Fix format errors in it.po and ko.po (rhbz#1435806)

* Fri Mar 10 2017 Pavel Hrdina <phrdina@redhat.com> - 1.4.1-1
- rebased to latest upstream version 1.4.1 (rhbz#1422472)
- virtManager.clone: don't generate default clone_path for some storage pools (rhbz#1420190)
- virtinst.diskbackend: unify how we get disk type (rhbz#1420187)
- virtManager/interface: detect whether IP address comes from DHCP server (rhbz#1410722)
- virtManager/viewers: fix connection to remote SPICE with password (rhbz#1401790)
- man: virt-install: keymap is valid for spice graphics as well (rhbz#1399091)
- virtinst/cli: set default value for disk sparse to "yes" (rhbz#1392990)
- virtManager/addhardware: get supported disk bus types from libvirt (rhbz#1387218)
- domain: Use libvirt.VIR_DOMAIN_OPEN_GRAPHICS_SKIPAUTH (rhbz#1379581)
- virt-manager: don't autostart other connection if --show-* was specified (rhbz#1377244)
- ui/snapshots: add a tooltip for refresh button (rhbz#1375452)
- virt-install: fix --wait=0 to behave like --noautoconsole (rhbz#1371781)
- domain: add support to rename domain with nvram vars file (rhbz#1368922)
- man/virt-install: remove -c as short for --connect (rhbz#1366241)
- console: set unavailable page while closing details window (rhbz#1365367)
- virt-clone: add support to clone nvram VARS (rhbz#1243335)

* Wed Sep 07 2016 Pavel Hrdina <phrdina@redhat.com> - 1.4.0-2
- translation: mark some strings to be translated (rhbz#1271152)
- translation: fix usage of translate function (rhbz#1271152)
- Add complete translations for supported languages (rhbz#1282276)

* Mon Jun 20 2016 Pavel Hrdina <phrdina@redhat.com> - 1.4.0-1
- rebased to latest upstream version 1.4.0 (rhbz#1296550)
- virt-manager: connect with openGraphicsFD (rhbz#1341453)
- ui: remove "Restore Saved Machine..." from File menu of Connection Details (rhbz#1340356)
- virt-install: add a new guest feature GIC for ARM guests (rhbz#1334857)
- virt-manager: fix --show-domain-creator to not depend on manager window (rhbz#1331707)
- man: virt-manager: properly indent --spice-disable-auto-usbredir (rhbz#1331633)
- virtinst: add virtio device model and accel3d attribute (rhbz#1326589)
- addhardware: don't remove QXL if VNC graphics are configured (rhbz#1326544)
- urlfetcher: Fix rawhide URL detection (rhbz#1321719)
- virt-install: concatenate all extra-args argument (rhbz#1315941)
- create: report an error if storage doesn't exists for import installation (rhbz#1305210)
- console: fix checkbox to save password if it was loaded from keyring (rhbz#1302175)
- connection: fix detection that libvirtd is stopped (rhbz#1297303)
- localization: mark several strings as translatable (rhbz#1271152)
- create: skip continue-install restart if user destroys VM (rhbz#1235238)
- cli: add --graphics listen=socket support (rhbz#1044570)

* Thu Apr 07 2016 Pavel Hrdina <phrdina@redhat.com> - 1.3.2-1
- rebased to latest upstream version 1.3.2 (rhbz#1296550)
- create: Drop explicit kickstart UI (rhbz#1086577)
- virt-manager: revive cli dbus API (rhbz#1162815)
- cli: Have '--input tablet' default to bus=usb (rhbz#1232087)
- storage: Fix updating UI when volume deleted (rhbz#1233531)
- ui: improve pause/resume tooltip (rhbz#1238618)
- virt-install: don't report missing console in extra-args for ppc64 (rhbz#1247434)
- details: Use devicedisk path lookup for source_pool (rhbz#1257469)
- virtinst.connection: detect RHEL system also for session connection (rhbz#1258691)
- man: virt-install: fix a typo in examples (rhbz#1263900)
- virt-install: report warning for cpuset=auto on non-NUMA host (rhbz#1263903)
- virt-install: always enable pae for xen hvm 64bit guest (rhbz#1267160)
- urlfetcher: Recognize RHEL Atomic Host ISOs (rhbz#1268001)
- storage: remove attempt counter from disk allocation thread (rhbz#1270277)
- virt-install: use correct path for linux and initrd for SLES on ppc64 (rhbz#1270430)
- virt-clone: remove socket path for unix channel (rhbz#1270696)
- man: fix cdrom section in virt-install man (rhbz#1290314)

* Wed Sep 30 2015 Pavel Hrdina <phrdina@redhat.com> - 1.2.1-8
- Localization: fix some wrong translations (rhbz#1228094)

* Tue Sep 22 2015 Pavel Hrdina <phrdina@redhat.com> - 1.2.1-7
- Add complete translations for supported languages (rhbz#1228094)

* Wed Aug 19 2015 Pavel Hrdina <phrdina@redhat.com> - 1.2.1-6
- addhardware: Fix USB host device listing (rhbz#1254115)

* Tue Aug 11 2015 Pavel Hrdina <phrdina@redhat.com> - 1.2.1-5
- details: don't display error if machine is missing in XML (rhbz#1238981)
- hostdev: add an address element for USB host devs if necessary (rhbz#1230611)
- virtinst: fix two undefined variable warnings (rhbz#1230611)
- Revert "create: customize: Hide bus=virtio-scsi" (rhbz#1206097)
- scsi-storage: unify SCSI storage code and logic (rhbz#1206097)
- virt-install: report an error for pxe install without network (rhbz#1250382)
- addstorage: remove _check_ideal_path (rhbz#1232599)

* Wed Jul 22 2015 Pavel Hrdina <phrdina@redhat.com> - 1.2.1-4
- virtManager/create: update capsinfo sooner in set_conn_state (rhbz#1244566)
- support: enable hv_time since qemu-kvm 1.5.3 from RHEL (rhbz#1083537)

* Fri Jul 17 2015 Pavel Hrdina <phrdina@redhat.com> - 1.2.1-3
- Fix adding iscsi pools (bz 1231558) (rhbz#1235987)
- virt-xml: refactor the handling of --define and --update (rhbz#1192875)
- virtinst.cpu: fix copy host cpu definition (rhbz#1240938)
- refactor detection of guest type capabilities (rhbz#1215692)
- capabilities: detect ACPI and APIC capabilites properly (rhbz#1215692)
- virtinst.support: enable hv_time support since qemu-kvm (rhbz#1083537)

* Mon Jun 22 2015 Pavel Hrdina <phrdina@redhat.com> - 1.2.1-2
- spec: fix rpm's to contain virt-xml - rebase related (rhbz#1197254)

* Mon Jun 22 2015 Pavel Hrdina <phrdina@redhat.com> - 1.2.1-1
- rebased to latest upstream version 1.2.1 (rhbz#1197254)
- clone: do not use a '/' separator when using a disk file under / (rhbz#1210564)
- spec: we don't need to depend on qemu-kvm (rhbz#1046651)
- doc: make --sparse documentation in man page consistent (rhbz#1210572)

* Tue May 26 2015 Pavel Hrdina <phrdina@redhat.com> - 1.2.0-4
- man: virt-xml: Fix example (rhbz#1222983)
- create: verify HYPER-V support after customization (rhbz#1185253)

* Fri May 15 2015 Giuseppe Scrivano <gscrivan@redhat.com> - 1.2.0-3
- Fix --show-host-summary (rhbz#1220322)
- Fix listing of VMs on hosts with old libvirt (rhbz#1219629)
- Fix delete of VMs which have disks with type volume (rhbz#1219427)
- Fix USB Redirection type shortcut key (rhbz#1172108)
- Show correctly the start mode for running network interfaces (rhbz#1154480)

* Thu May 7 2015 Giuseppe Scrivano <gscrivan@redhat.com> - 1.2.0-2
- Fix exception when the address is not an IP (rhbz#1219023)

* Wed May 6 2015 Giuseppe Scrivano <gscrivan@redhat.com> - 1.2.0-1
- Allow to clone guest with custom path via virt-manager (rhbz#1183495)
- Allow to open guest console after input incorrect passwd (rhbz#1165990)
- virt-manager shows correctly the domain processor page (rhbz#1167600)
- Shortcut keys on hardware page take effect (rhbz#1172108)
- virt-clone can clone guest with disk type volume (rhbz#1177099)
- virt-manager can create a new guest on a remote xen host (rhbz#1177113)
- virt-manager can show the right state of guest on a remote XEN server (rhbz#1177207)
- virt-manager does not show the new added hot-plug devices immediately (rhbz#1179138)
- Can create Ubuntu guest on rhel7 host (rhbz#1179652)
- Fixed misleading "restart your domain" message (rhbz#1180559)
- Windows 2008 R2 or Win7 SP1 smp guest booting hang with hv_t (rhbz#1185253)
- Fixed wrong boot options example in virt-xml manual (rhbz#1192768)
- Fixed virt-install rpm missing dependency on pygobject3-base (rhbz#1195860)
- Possibility to use persistent reservation on FC disks created via KVM (rhbz#1200356)
- virt-install: auto-add usb controller(s) for usbredir (rhbz#1204895)
- Using virt-clone on a qcow2 image doesn't behave differently (rhbz#1207729)
- The progress bar shows correctly when set output disk under /root (rhbz#1210265)
- virt-clone deals correctly with --file path under / (rhbz#1210564)
- Make manual doc and error message similar about 'sparse' usage (rhbz#1210572)
- Handle virt-rhelsaX.Y machine types (rhbz#1212021)
- Do not keep showing error message after first failed attempt to add a device (rhbz#1213202)
- Show the serial console when no graphical screen is configured (rhbz#1213911)
- Better support for Ipv6 addresses (rhbz#1217302)
- Use the VM name to name disks (rhbz#1218278)
- aarch64 support (rhbz#1197254)

* Tue May 5 2015 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-14
- Allow to clone guest with custom path via virt-manager (rhbz#1183495)
- Allow to open guest console after input incorrect passwd (rhbz#1165990)
- virt-manager shows correctly the domain processor page (rhbz#1167600)
- Shortcut keys on hardware page take effect (rhbz#1172108)
- virt-clone can clone guest with disk type volume (rhbz#1177099)
- virt-manager can create a new guest on a remote xen host (rhbz#1177113)
- virt-manager can show the right state of guest on a remot (rhbz#1177207)
- virt-manager does not show the new added hot-plug devices immediately (rhbz#1179138)
- Can create Ubuntu guest on rhel7 host (rhbz#1179652)
- Fixed misleading "restart your domain" message (rhbz#1180559)
- Windows 2008 R2 or Win7 SP1 smp guest booting hang with hv_t (rhbz#1185253)
- Fixed wrong boot options example in virt-xml manual (rhbz#1192768)
- Fixed virt-install rpm missing dependency on pygobject3-base (rhbz#1195860)
- Possibility to use persistent reservation on FC disks created via KVM (rhbz#1200356)
- virt-install: auto-add usb controller(s) for usbredir (rhbz#1204895)
- Using virt-clone on a qcow2 image doesn't behave differently (rhbz#1207729)
- The progress bar shows correctly when set output disk under /root (rhbz#1210265)
- virt-clone deals correctly with --file path under / (rhbz#1210564)
- Make manual doc and error message similar about 'sparse' usage (rhbz#1210572)
- Handle virt-rhelsaX.Y machine types (rhbz#1212021)
- Do not keep showing error message after first failed attempt to add a device (rhbz#1213202)
- Show the serial console when no graphical screen is configured (rhbz#1213911)
- Better support for Ipv6 addresses (rhbz#1217302)
- Use the VM name to name disks (rhbz#1218278)
- aarch64 support (rhbz#1197254)

* Sun May 3 2015 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-13
- PPC64LE support (rhbz#1209844)

* Sat Jan 10 2015 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-12
- Enable inspection only if the add_libvirt_dom function is present (rhbz#1138203)

* Fri Jan 9 2015 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-11
- Limit number of default usb redirdevs to 2 (rhbz#1175447)

* Tue Dec 9 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-10
- Fix add bridge (rhbz#1172028)

* Tue Dec 2 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-9
- Fix video model switch (rhbz#1169295)

* Fri Nov 21 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-8
- Display correctly IPv6 addresses (rhbz#1094631)

* Tue Nov 18 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-7
- Install virt-xml (rhbz#1159401)
- Quit immediately if the wrong id is passed to -show* functions (rhbz#1164691)
- Add virtio26 alias to --os-variant (rhbz#1162800)
- do not show MAC address when not set (rhbz#1164123)

* Mon Nov 10 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-6
- Add dependency on libosinfo to virt-manager-common (rhbz#1159401)

* Fri Oct 31 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-5
- Fix delete for disk type='volume'. (rhbz#1146869)
- Handle correctly a SPICE auth error. (rhbz#1152981)

* Wed Oct 08 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-4
- show disk info for guest with disk type volume (rhbz#1146869)
- depend on dconf and dbus-x11 (rhbz#1146982)
- OVMF support (rhbz#1111986)
- depend on gnome-icon-theme (rhbz#1146612)

* Tue Sep 23 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-3
- Improve UI responsiveness on a high latency connection (rhbz#607735)

* Tue Sep 16 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-2
- Use libosinfo for improved OS metadata (rhbz#1055588)
- Add "ich9-intel-hda" to the sound device list (rhbz#1140937)

* Mon Sep 08 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 1.1.0-1
- Rebase to 1.1.0 (bz #1055588)
- The rebase also fixes these bugs:
    rhbz#1138190, rhbz#1130105, rhbz#1130077, rhbz#1122059,
    rhbz#1098040, rhbz#1093762, rhbz#1092786, rhbz#1091666,
    rhbz#1091331, rhbz#1087689, rhbz#1083461, rhbz#1048054,
    rhbz#1047875, rhbz#1047874, rhbz#1047725, rhbz#1027576,
    rhbz#948525, rhbz#607735

* Mon Mar 24 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.10.0-20
- Remove CD/DVDROM example from the documentation (bz #1072610)

* Thu Mar 20 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.10.0-19
- Not propose to install from CD/DVD in RHEL7 (bz #1072610)
- Disable add filesystem passthrough for RHEL7 qemu (bz #1077172)

* Fri Feb 28 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.10.0-18
- Fix virtio-scsi disk addressing (bz #1036716)

* Thu Feb 20 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.10.0-17
- files: drop virt-image and virt-convert (bz #1061913)

* Mon Feb 10 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.10.0-16
- doc: reintroduce --force in man pages (bz #1060571)

* Fri Feb 07 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.10.0-15
- cli: drop --prompt from --help output (bz #1060571)

* Wed Feb 05 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.10.0-14
- inhibit --prompt for cli tools (bz #1060571)
- Don't use SCSI or USB disks with stable_defaults (bz #1058808)

* Wed Jan 22 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.10.0-13
- include proper patch for "Rename hide_unsupported_rhel_options to stable_defaults and clean-up its usage" (bz #908616)

* Tue Jan 21 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.10.0-12
- update translations (bz #1030385)
- Rename hide_unsupported_rhel_options to stable_defaults and clean-up its usage (bz #908616)
- osdict: Mark RHEL 7 as supported (bz #1053074)

* Wed Jan 15 2014 Giuseppe Scrivano <gscrivan@redhat.com> - 0.10.0-11
- doc: state correctly the number of possible values for --network= (bz #1049041)

* Fri Jan 10 2014 Martin Kletzander <mkletzan@redhat.com> - 0.10.0-10
- addhw: Fix FS UI for non-qemu (bz #1039829)
- virt-manager: vmmCreateVolume uses the correct connection (bz #1043150)
- virt-manager: use DISPLAY in the error message only when it is set (bz #1038496)
- virt-install: Support --network source, source_mode, target (bz #1049041)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.10.0-9
- Mass rebuild 2013-12-27

* Mon Dec 09 2013 Martin Kletzander <mkletzan@redhat.com> - 0.10.0-8
- capabilities: correctly parse "cpus" in the host NUMA topology (bz #1032320)
- console: Fix console_active() logic (bz #947020)
- virt-manager: Yet more fixes for DISPLAY unset error (bz #1038496)

* Fri Nov 08 2013 Martin Kletzander <mkletzan@redhat.com> - 0.10.0-7
- Add file with the patch for rhbz#1021789

* Thu Nov 07 2013 Martin Kletzander <mkletzan@redhat.com> - 0.10.0-6
- LVM: Show warning when allocation==0 and allocation != capacity (bz #1021789)

* Wed Oct 30 2013 Martin Kletzander <mkletzan@redhat.com> - 0.10.0-5
- virtinst: allow EGD RNG devices to have both bind and connect sources (bz #1001773)
- virt-install: EGD RNG devs need a host to connect to if backend_mode=bind (bz #1001773)
- virt-manager: fix adding EGD RNG devices in UDP mode (bz #1001773)
- virt-manager: show correctly EGD RNG devices information (bz #1001773)

* Thu Oct 10 2013 Martin Kletzander <mkletzan@redhat.com> - 0.10.0-4
- Add support for multifunction address parameter (bz #956700)
- Automatically add multifunction address parameter when needed (bz #956700)
- Fix addresses in manual (bz #956700)
- Fix automatic search for multifunction parameter (bz #956700)
- virtinst: add support for virtio-rng devices (bz #1001773)
- virt-install: add support for virtio-rng devices (bz #1001773)
- virtManager: add GUI elements for showing RNG devices (bz #1001773)
- virtManager: add GUI elements for adding a RNG device (bz #1001773)
- virt-install: accept a single argument form for RNG devices (bz #1001773)
- cli: rng devices accepts options also when the short form is used (bz #1001773)
- tests: move the storage pool under /dev (bz #1014338)
- Fix tests on f20, /dev/loop0 isn't available (bz #1014338)

* Mon Sep 02 2013 Martin Kletzander <mkletzan@redhat.com> - 0.10.0-3
- Fix UUID generation according to RFC 4122 (bz #963161)
- Handle storage formats properly (bz #907289)
- virt-manager: do not delete tabs while destroying the details window (bz #985291)
- change virt-manager option spice-disable-usbredir to spice-disable-auto-usbredir (bz #923567)

* Fri Aug 09 2013 Martin Kletzander <mkletzan@redhat.com> - 0.10.0-2
- virt-install: Make default graphics configurable (bz #912615)
- Use proper disk targets (bz #968878)
- inspection: Check can_set_row_none before setting icon to None (bz #979979)
- virt-manager: Fix self.config (bz #907289)
- add new "spice-disable-usbredir" option to disable autoredir feature (bz #923567)
- error: use helper function to embed customized widget into dialog (bz #923567)
- details: Add auto USB redirection support in console viewer (bz #923567)

* Wed Jun 19 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-1
- Rebased to version 0.10.0
- Fix screenshots (bz #969410)
- Add Fedora 19 osdict option (bz #950230)
- Fix loading libguestfs OS icons (bz #905238)
- Make packagekit search cancellable (bz #973777)
- Fix freeze on guest shutdown if serial console connected (bz #967968)

* Mon May 27 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-0.5.gitde1695b2
- Fix default graphics, should be spice+qxl (bz #965864)
- Check for libvirt default network package on first run (bz #950329)
- Fix changing VM cirrus->QXL (bz #928882)

* Wed May 15 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-0.4.gitb68faac8
- Drop bogus packagekit check for avahi-tools (bz #963472)

* Wed May 15 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-0.3.gitb68faac8
- Fix error creating QEMU guests (bz #962569)

* Thu May 09 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-0.2.gitb68faac8
- Fix dep on vte3 (bz #958945)
- Fix dep on virt-manager-common (bz #958730)
- Fix crash when installing from ISO media (bz #958641)
- Fix poor error reporting with unknown CLI option (bz #958730)

* Mon Apr 29 2013 Cole Robinson <crobinso@redhat.com> - 0.10.0-0.1.gitd3f9bc8e
- Update to git snapshot for next release

* Mon Apr 01 2013 Cole Robinson <crobinso@redhat.com> - 0.9.5-1
- Rebased to version 0.9.5
- Enable adding virtio-scsi disks (Chen Hanxiao) (bz 887584)
- Support security auto-relabel setting (Martin Kletzander)
- Support disk iotune settings (David Shane Holden)
- Support 'reset' as a reboot option (John Doyle)
- Don't pull in non-native qemu packages on first run (bz 924469)
- Don't create LVM volumes with alloc=0, it doesn't work (bz 872162)
- Fix storage browser hang on KDE (bz 880781)
- Fix package installation on KDE (bz 882024)

* Fri Mar 01 2013 Cole Robinson <crobinso@redhat.com> - 0.9.4-5
- Add explicit dep on pod2man (bz #914562)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Cole Robinson <crobinso@redhat.com> - 0.9.4-4
- Use correct KVM package names on first run (bz #873878)
- network: fix parsing ip blocks with prefix= (bz #872814)
- Don't recommend all of libvirt, just the kvm bits (bz #872246)

* Tue Oct 30 2012 Cole Robinson <crobinso@redhat.com> - 0.9.4-3
- Fix first run packagekit interaction (bz #870851)
- Fix another backtrace if guest is pmsuspended (bz #871237)

* Wed Oct 24 2012 Cole Robinson <crobinso@redhat.com> - 0.9.4-2
- Fix KVM package install on app first run
- Fix listing domain with 'suspended' state (bz #850954)
- Fix 'browse local' behavior when choosing directory (bz #855335)
- Fix libgnome-keyring dep (bz #811921)

* Sun Jul 29 2012 Cole Robinson <crobinso@redhat.com> - 0.9.4-1
- Rebased to version 0.9.4
- Fix VNC keygrab issues (bz 840240)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Cole Robinson <crobinso@redhat.com> - 0.9.3-1
- Rebased to version 0.9.3
- Convert to gtkbuilder: UI can now be editted with modern glade tool
- virt-manager no longer runs on RHEL5, but can manage a remote RHEL5
  host
- Option to configure spapr net and disk devices for pseries (Li Zhang)
- Offer to install openssh-askpass if we need it (bz 754484)
- Don't leave defunct SSH processes around (bz 757892)
- Offer to start libvirtd after install (bz 791152)
- Fix crash when deleting storage volumes (bz 805950)
- Show serial device PTY path again (bz 811760)
- Fix possible crash when rebooting fails (bz 813119)
- Offer to discard state if restore fails (bz 837236)

* Wed Jun 06 2012 Cole Robinson <crobinso@redhat.com> - 0.9.1-4
- Fix connecting to console with specific listen address
- Fix regression that dropped spice dependency (bz 819270)

* Wed Apr 25 2012 Cole Robinson <crobinso@redhat.com> - 0.9.1-3
- Actually make spice the default (bz 757874)
- Only depend on spice on arch it is available (bz 811030)
- Depend on libgnome-keyring (bz 811921)

* Mon Feb 13 2012 Cole Robinson <crobinso@redhat.com> - 0.9.1-2
- Fix error reporting for failed remote connections (bz 787011)
- Fix setting window title when VNC mouse is grabbed (bz 788443)
- Advertise VDI format in disk details (bz 761300)
- Don't let an unavailable host hang the app (bz 766769)
- Don't overwrite existing create dialog when reshowing (bz 754152)
- Improve tooltip for 'force console shortcuts' (bz 788448)

* Wed Feb 01 2012 Cole Robinson <crobinso@redhat.com> - 0.9.1-1
- Rebased to version 0.9.1
- Support for adding usb redirection devices (Marc-André Lureau)
- Option to switch usb controller to support usb2.0 (Marc-André Lureau)
- Option to specify machine type for non-x86 guests (Li Zhang)
- Support for filesystem device type and write policy (Deepak C Shetty)
- Many bug fixes!

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-8
- Fix crashes when deleting a VM (bz 749263)

* Tue Sep 27 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-7
- Fix 'Resize to VM' graphical option (bz 738806)
- Fix deleting guest with managed save data
- Fix error when adding default storage
- Don't flush XML cache on every tick
- Use labels for non-editable network info fields (bz 738751)
- Properly update icon cache (bz 733836)

* Tue Aug 02 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-6
- Fix python-newt_syrup dep

* Mon Aug 01 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-5
- Don't have a hard dep on libguestfs (bz 726364)
- Depend on needed python-newt_syrup version

* Thu Jul 28 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-4
- Fix typo that broke net stats reporting

* Wed Jul 27 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-3
- Add BuildRequires: GConf2 to fix pre scriplet error

* Tue Jul 26 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-2
- Fix virtinst dep

* Tue Jul 26 2011 Cole Robinson <crobinso@redhat.com> - 0.9.0-1.fc17
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

* Thu Apr 28 2011 Cole Robinson <crobinso@redhat.com> - 0.8.7-5.fc16
- Stop netcf errors from flooding logs (bz 676920)
- Bump default mem for new guests to 1GB so F15 installs work (bz
  700480)

* Tue Apr 19 2011 Cole Robinson <crobinso@redhat.com> - 0.8.7-4.fc16
- Fix spice RPM dependency (bz 697729)

* Thu Apr 07 2011 Cole Robinson <crobinso@redhat.com> - 0.8.7-3.fc16
- Fix broken cs.po which crashed gettext
- Fix offline attach fallback if hotplug fails
- Offer to attach spicevmc if switching to spice

* Thu Mar 31 2011 Cole Robinson <crobinso@redhat.com> - 0.8.7-2.fc16
- Fix using spice as default graphics type
- Fix lockup as non-root (bz 692570)

* Mon Mar 28 2011 Cole Robinson <crobinso@redhat.com> - 0.8.7-1.fc16
- Rebased to version 0.8.7
- Allow renaming an offline VM
- Spice password support (Marc-André Lureau)
- Allow editting NIC <virtualport> settings (Gerhard Stenzel)
- Allow enabling/disabling individual CPU features
- Allow easily changing graphics type between VNC/SPICE for existing VM
- Allow easily changing network source device for existing VM

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Cole Robinson <crobinso@redhat.com> - 0.8.6-1.fc15
- Update to 0.8.6
- SPICE support (requires spice-gtk) (Marc-André Lureau)
- Option to configure CPU model
- Option to configure CPU topology
- Save and migration cancellation (Wen Congyang)
- Save and migration progress reporting
- Option to enable bios boot menu
- Option to configure direct kernel/initrd boot

* Wed Aug 25 2010 Cole Robinson <crobinso@redhat.com> - 0.8.5-1.fc15
- Update to 0.8.5
- Improved save/restore support
- Option to view and change disk cache mode
- Configurable VNC keygrab sequence (Michal Novotny)

* Mon Aug  2 2010 David Malcolm <dmalcolm@redhat.com> - 0.8.4-3.fc15
- fix python 2.7 incompatibility (bz 620216)

* Thu May 27 2010 Cole Robinson <crobinso@redhat.com> - 0.8.4-2.fc14
- Only close connection on specific remote errors
- Fix weird border in manager UI (bz 583728)
- Fix broken icons
- Cancel post-install reboot if VM is forced off
- Fix traceback if customizing a livecd install (bz 583712)
- Add pool refresh button
- Properly autodetect VNC keymap (bz 586201)
- Fix traceback when reconnecting to remote VNC console (bz 588254)
- Fix remote VNC connection with zsh as default shell

* Wed Mar 24 2010 Cole Robinson <crobinso@redhat.com> - 0.8.4-1.fc14
- Update to version 0.8.4
- 'Import' install option, to create a VM around an existing OS image
- Support multiple boot devices and boot order
- Watchdog device support
- Enable setting a human readable VM description.
- Option to manually specifying a bridge name, if bridge isn't detected

* Mon Mar 22 2010 Cole Robinson <crobinso@redhat.com> - 0.8.3-2.fc14
- Fix using a manual 'default' pool (bz 557020)
- Don't force grab focus when app is run (bz 548430)
- Check packagekit for KVM and libvirtd (bz 513494)
- Fake a reboot implementation if libvirt doesn't support it (bz 532216)
- Mark some strings as translatable (bz 572645)

* Mon Feb  8 2010 Cole Robinson <crobinso@redhat.com> - 0.8.3-1.fc13
- Update to 0.8.3 release
- Manage network interfaces: start, stop, view, provision bridges, bonds, etc.
- Option to 'customize VM before install'.

* Tue Jan 12 2010 Cole Robinson <crobinso@redhat.com> - 0.8.2-2.fc13
- Build with actual upstream tarball (not manually built dist)

* Mon Dec 14 2009 Cole Robinson <crobinso@redhat.com> - 0.8.2-1.fc13
- Update to 0.8.2 release
- Fix first virt-manager run on a new install
- Enable floppy media eject/connect

* Wed Dec 09 2009 Cole Robinson <crobinso@redhat.com> - 0.8.1-3.fc13
- Select manager row on right click, regressed with 0.8.1

* Sat Dec  5 2009 Cole Robinson <crobinso@redhat.com> - 0.8.1-2.fc13
- Set proper version Requires: for python-virtinst

* Thu Dec  3 2009 Cole Robinson <crobinso@redhat.com> - 0.8.1-1.fc13
- Update to release 0.8.1
- VM Migration wizard, exposing various migration options
- Enumerate CDROM and bridge devices on remote connections
- Support storage pool source enumeration for LVM, NFS, and SCSI

* Mon Oct 05 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-8.fc13
- Don't allow creating a volume without a name (bz 526111)
- Don't allow volume allocation > capacity (bz 526077)
- Add tooltips for toolbar buttons (bz 524083)

* Mon Oct 05 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-7.fc13
- More translations (bz 493795)

* Tue Sep 29 2009 Cole Robinson <crobinso@redhat.com> - 0.8.0-6.fc13
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
