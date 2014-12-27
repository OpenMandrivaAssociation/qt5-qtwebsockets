%define api 5
%define major %api

%define qtminor 4
%define qtsubminor 0

%define qtversion %{api}.%{qtminor}.%{qtsubminor}

%define qtwebsockets %mklibname qt%{api}websockets %{major}
%define qtwebsocketsd %mklibname qt%{api}websockets -d
%define qtwebsockets_p_d %mklibname qt%{api}websockets-private -d

%define qttarballdir qtwebsockets-opensource-src-%{qtversion}
%define _qt5_prefix %{_libdir}/qt%{api}

Name:		qt5-qtwebsockets
Version:	%{qtversion}
Release:	1
Summary:	Qt GUI toolkit
Group:		Development/KDE and Qt
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		http://www.qt.io
Source0:	http://download.qt.io/official_releases/qt/%{api}.%{qtminor}/%{version}/submodules/%{qttarballdir}.tar.xz
BuildRequires:	qt5-qtbase-devel = %{version}
BuildRequires:	pkgconfig(Qt5Core) = %{version}

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
%exclude %{_qt5_includedir}/QtWebSockets/%qtversion
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
%{_qt5_includedir}/QtWebSockets/%qtversion

#------------------------------------------------------------------------------

%prep
%setup -q -n %qttarballdir

%build
%qmake_qt5

%make
#------------------------------------------------------------------------------

%install
%makeinstall_std INSTALL_ROOT=%{buildroot}

install -d %{buildroot}/%{_qt5_docdir}

# .la and .a files, die, die, die.
rm -f %{buildroot}%{_qt5_libdir}/lib*.la
rm -f %{buildroot}%{_qt5_libdir}/lib*.a
