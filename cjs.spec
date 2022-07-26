%global glib2_version 2.58.0
%global gobject_introspection_version 1.61.2
%global gtk3_version 3.20
%global mozjs78_version 78.12.0-1

Name:          cjs
Epoch:         1
Version:       5.4.1
Release:       2
Summary:       Javascript Bindings for Cinnamon

License:       MIT and (MPLv1.1 or GPLv2+ or LGPLv2+)
# The following files contain code from Mozilla which
# is triple licensed under MPL1.1/LGPLv2+/GPLv2+:
# The console module (modules/console.c)
# Stack printer (gjs/stack.c)
URL:           https://github.com/linuxmint/%{name}
Source0:       %{url}/archive/%{version}/%{name}-%{version}.tar.gz

ExcludeArch:   %{ix86}

BuildRequires: dbus-daemon
BuildRequires: gcc-c++
BuildRequires: meson
BuildRequires: pkgconfig(cairo-gobject)
BuildRequires: pkgconfig(dbus-glib-1)
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gobject-introspection-1.0) >= %{gobject_introspection_version}
BuildRequires: pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires: pkgconfig(mozjs-78) >= %{mozjs78_version}
BuildRequires: pkgconfig(readline)
BuildRequires: pkgconfig(sysprof-capture-4)
# Required for checks
%ifnarch s390 s390x
BuildRequires: dbus-x11
BuildRequires: xorg-x11-server-Xvfb
%endif

Requires: glib2%{?_isa} >= %{glib2_version}
Requires: gobject-introspection%{?_isa} >= %{gobject_introspection_version}
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: mozjs78%{?_isa} >= %{mozjs78_version}

%description
Cjs allows using Cinnamon libraries from Javascript. It's based on the
Spidermonkey Javascript engine from Mozilla and the GObject introspection
framework.


%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{?epoch}:%{version}-%{release}

%description devel
Files for development with %{name}.


%package tests
Summary: Tests for the cjs package
Requires: %{name}%{?_isa} = %{?epoch}:%{version}-%{release}

%description tests
The cjs-tests package contains tests that can be used to verify
the functionality of the installed cjs package.


%prep
%autosetup -p1


%build
%meson --libexecdir=%{_libexecdir}/cjs/
%meson_build


%install
%meson_install


%check
%ifnarch s390 s390x aarch64
xvfb-run -a /usr/bin/meson test -C %{_vpath_builddir} \
 --num-processes %{_smp_build_ncpus} --print-errorlogs
%endif


%files
%doc NEWS README.md
%license COPYING
%{_bindir}/cjs
%{_bindir}/cjs-console
%{_libdir}/*.so.*
%{_libdir}/cjs/


%files devel
%doc examples/*
%{_includedir}/cjs-1.0/
%{_libdir}/pkgconfig/cjs-*1.0.pc
%{_libdir}/*.so
%{_datadir}/cjs-1.0/


%files tests
%{_libexecdir}/cjs/
%{_datadir}/installed-tests/
%{_datadir}/glib-2.0/schemas/org.cinnamon.CjsTest.gschema.xml


%changelog
* Mon Jul 25 2022 Wenlong Ding <wenlong.ding@turbolinux.com.cn> - 1:5.4.1-2
- Change spec file to disable check in aarch64

* Thu Jul 21 2022 Wenlong Ding <wenlong.ding@turbolinux.com.cn> - 1:5.4.1-1
- Initial Packaging
