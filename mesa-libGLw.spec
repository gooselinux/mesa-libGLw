# Bit of a kludge to get libGLw built independently of Mesa.
# Joyfully stolen from the mesa-6.5 spec file.

Summary: Xt / Motif OpenGL widgets
Name: mesa-libGLw
Version: 6.5.1
Release: 10%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.mesa3d.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0: http://dl.sourceforge.net/sourceforge/mesa3d/MesaLib-%{version}.tar.bz2
Patch0: mesa-6.5-build-config.patch
Patch1: mesa-6.5.1-libGLw.patch

BuildRequires: libXt-devel
BuildRequires: libGL-devel
BuildRequires: openmotif-devel

Provides: libGLw
# libGLw used to be in Mesa package in RHL 6.x, 7.[0-2], RHEL 2.1
Obsoletes: Mesa <= 3.4.2-10
# libGLw moved to XFree86-libs for RHL 7.3, 8, 9, FC1, RHEL 3
Obsoletes: XFree86-libs < 4.3.0-127
# libGLw moved to xorg-x11-libs FC[2-4], RHEL4
Obsoletes: xorg-x11-libs < 6.8.2-38

%description
Mesa libGLw runtime library.

%package devel
Summary: Mesa libGLw development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libGL-devel
Requires: openmotif-devel
Provides: libGLw-devel

%description devel
Mesa libGLw development package.

#-- prep -------------------------------------------------------------
%prep
%setup -q -n Mesa-%{version}

%patch0 -p0 -b .build-config
%patch1 -p1 -b .motif

# WARNING: The following files are copyright "Mark J. Kilgard" under the GLUT
# license and are not free software (but redistributable), so we remove them.
rm include/GL/uglglutshapes.h

#-- Build ------------------------------------------------------------
%build

make OPT_FLAGS="$RPM_OPT_FLAGS" LIB_DIR=%{_lib} linux

#-- Install ----------------------------------------------------------
%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL_DIR=$RPM_BUILD_ROOT%{_prefix} LIB_DIR=%{_lib}

#-- Clean ------------------------------------------------------------
%clean
rm -rf $RPM_BUILD_ROOT

#-- Check ------------------------------------------------------------
%check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc src/glw/README
%{_libdir}/libGLw.so.1
%{_libdir}/libGLw.so.1.0.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/libGLw.so
%{_includedir}/GL/GLwDrawA.h
%{_includedir}/GL/GLwDrawAP.h
%{_includedir}/GL/GLwMDrawA.h
%{_includedir}/GL/GLwMDrawAP.h

%changelog
* Wed Aug 10 2011 Dave Airlie <airlied@redhat.com> 6.5.1-10
- initial EL6 import + change to using openmotif to build against.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.5.1-6
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6.5.1-5
- Autorebuild for GCC 4.3

* Fri Oct 12 2007 Matthias Clasen <mclasen@redhat.com> - 6.5.1-4
- Fix spec file syntax issues  (#330331)

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 6.5.1-3
- Rebuild for build id

* Wed Jan 24 2007 Adam Jackson <ajax@redhat.com> 6.5.1-2
- Minor spec fixes (#210798)

* Fri Sep 29 2006 Adam Jackson <ajackson@redhat.com> 6.5.1-1
- lib64 fixes and cleanups from Patrice Dumas (#188974)

* Tue Sep 19 2006 Adam Jackson <ajackson@redhat.com> 6.5.1-0.2
- Use 6.5.1 release tarball.  Drop patches and build scripts that are no
  longer necessary.

* Tue Sep 19 2006 Adam Jackson <ajackson@redhat.com> 6.5.1-0.1
- Move revision back up to 6.5.1 for upgrade path from FC5.  Misc other
  spec fixes as per bug #188974 comment 30.

* Mon Sep 18 2006 Adam Jackson <ajackson@redhat.com> 1.0-4
- Rename back to mesa-libGLw as per bug #188974.

* Wed Aug 30 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-3
- Fix package for x86_64

* Tue Aug 29 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.0-2
- Fix package to depend on lesstif-devel
- -devel now Requires libGL-devel
- use name var in -devel Requires
- actually use RPM_OPT_FLAGS
- symlink devel libs, not copy (except for .*.*.*)

* Fri Aug  7 2006 Adam Jackson <ajackson@redhat.com> 1.0-1
- Split libGLw out from Mesa.
