%define api %(echo %{version} |cut -d. -f1)
%define major %api

%define qtminor %(echo %{version} |cut -d. -f2)
%define qtsubminor %(echo %{version} |cut -d. -f3)
%define beta %nil

%define qtwebsockets %mklibname qt%{api}websockets %{major}
%define qtwebsocketsd %mklibname qt%{api}websockets -d
%define qtwebsockets_p_d %mklibname qt%{api}websockets-private -d

%define _qt5_prefix %{_libdir}/qt%{api}

Name:		qt5-qtwebsockets
Version:	5.6.0
%if "%{beta}" != ""
Release:	1.%{beta}.1
%define qttarballdir qtwebsockets-opensource-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
%else
Release:	1
%define qttarballdir qtwebsockets-opensource-src-%{version}
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
Summary:	Qt GUI toolkit
Group:		Development/KDE and Qt
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		http://www.qt.io
BuildRequires:	qmake5 >= %{version}
BuildRequires:	pkgconfig(Qt5Core) >= %{version}
BuildRequires:	pkgconfig(Qt5Network) >= %{version}
BuildRequires:	pkgconfig(Qt5Test) >= %{version}

%description
QtWebSockets is a pure Qt implementation of WebSockets - both client and
server.
It is implemented as a Qt add-on module, that can easily be embedded into
existing Qt projects. It has no other dependencies than Qt.

#------------------------------------------------------------------------------

%package -n	%{qtwebsockets}
Summary:	Qt%{api} Component Library
Group:		System/Libraries

%description -n %{qtwebsockets}
Qt%{api} Component Library.

QtWebSockets is a pure Qt implementation of WebSockets - both client and
server.

%files -n %{qtwebsockets}
%{_qt5_libdir}/libQt5WebSockets.so.%{major}*

#------------------------------------------------------------------------------

%package -n	%{qtwebsocketsd}
Summary:	Devel files needed to build apps based on QtWebSockets
Group:		Development/KDE and Qt
Requires:	%{qtwebsockets} = %version

%description -n %{qtwebsocketsd}
Devel files needed to build apps based on QtWebSockets.

%files -n %{qtwebsocketsd}
%{_qt5_libdir}/libQt5WebSockets.prl
%{_qt5_libdir}/libQt5WebSockets.so
%{_qt5_libdir}/pkgconfig/Qt5WebSockets.pc
%{_qt5_includedir}/QtWebSockets
%exclude %{_qt5_includedir}/QtWebSockets/%{version}
%{_qt5_libdir}/cmake/*
%{_qt5_prefix}/mkspecs/modules/*.pri
%{_qt5_exampledir}/*

#------------------------------------------------------------------------------

%package -n	%{qtwebsockets_p_d}
Summary:	Devel files needed to build apps based on QtWebSockets
Group:		Development/KDE and Qt
Requires:	%{qtwebsocketsd} = %version
Provides:	qt5-qtwebsockets-private-devel = %version

%description -n %{qtwebsockets_p_d}
Devel files needed to build apps based on QtWebSockets.

%files -n %{qtwebsockets_p_d}
%{_qt5_includedir}/QtWebSockets/%{version}

#------------------------------------------------------------------------------

%prep
%setup -q -n %qttarballdir

%build
%qmake_qt5

%make
#------------------------------------------------------------------------------

%install
%makeinstall_std INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

install -d %{buildroot}/%{_qt5_docdir}

# .la and .a files, die, die, die.
rm -f %{buildroot}%{_qt5_libdir}/lib*.la
rm -f %{buildroot}%{_qt5_libdir}/lib*.a
