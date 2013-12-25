%define		srcname	LibVNCServer
Summary:	LibVNCServer - a for easy implementation of VNC/RDP server
Summary(pl.UTF-8):	LibVNCServer - biblioteka do łatwego implementowania serwera VNC/RDP
Name:		libvncserver
Version:	0.9.9
Release:	6
Epoch:		0
License:	GPL v2
Group:		Libraries
Source0:	http://downloads.sourceforge.net/libvncserver/%{srcname}-%{version}.tar.gz
# Source0-md5:	70422169b122765693d2a294d13e3714
Patch0:		%{name}-linux.patch
Patch1:		format_string.patch
URL:		http://libvncserver.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gnutls-devel >= 2.4.0
BuildRequires:	libgcrypt-devel >= 1.4.0
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	zlib-devel
# not used (x11vnc moved to separate package)
#BuildRequires:	openssl-devel
# for noinst client_examples only
#BuildRequires:	SDL-devel
#BuildRequires:	ffmpeg-devel
Requires:	gnutls >= 2.4.0
Requires:	libgcrypt >= 1.4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibVNCServer makes writing a VNC server (or more correctly, a program
exporting a framebuffer via the Remote Frame Buffer protocol) easy.

It is based on OSXvnc, which in turn is based on the original Xvnc by
ORL, later AT&T research labs in UK.

It hides the programmer from the tedious task of managing clients and
compression schemata.

LibVNCServer was put together and is (actively ;-) maintained by
Johannes Schindelin <Johannes.Schindelin@gmx.de>.

%description -l pl.UTF-8
LibVNCServer ułatwia pisanie serwera VNC (lub, bardziej poprawnie,
programu eksportującego framebuffer poprzez protokół Remote Frame
Buffer).

Jest oparty na OSXvnc, który z kolei bazuje na oryginalnym Xvnc
napisanym przez ORL, a później AT&T.

Biblioteka ukrywa przed programistą nudne zadanie zarządzania
klientami i schematami kompresji.

LibVNCServer została poskładana i jest (aktywnie) utrzymywana przez
Johannesa Schindelina <Johannes.Schindelin@gmx.de>.

%package devel
Summary:	LibVNCServer header files
Summary(pl.UTF-8):	Pliki nagłówkowe LibVNCServer
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	gnutls-devel >= 2.4.0
Requires:	libgcrypt-devel >= 1.4.0
Requires:	libjpeg-devel
Requires:	zlib-devel

%description devel
LibVNCServer header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe LibVNCServer.

%package static
Summary:	Static LibVNCServer libraries
Summary(pl.UTF-8):	Statyczne biblioteki LibVNCServer
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static LibVNCServer libraries.

%description static -l pl.UTF-8
Statyczne biblioteki LibVNCServer.

%package progs
Summary:	Example programs that use LibVNCServer
Summary(pl.UTF-8):	Przykładowe programy wykorzystujące LibVNCServer
Group:		Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description progs
Example programs that use LibVNCServer.

%description progs -l pl.UTF-8
Przykładowe programy wykorzystujące LibVNCServer.

%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1
%patch1 -p1

install -d x11vnc/misc
touch x11vnc/Makefile.in x11vnc/misc/Makefile.in

awk 'BEGIN { f=1; } /# libtool.m4/ { f=0; } { if (f) { print $0; } }' acinclude.m4 > acinclude.m4.new
mv acinclude.m4.new acinclude.m4

sed -i -e '/AC_CONFIG_FILES.*x11vnc/d' configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--without-x11vnc
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# *.la not removed - *.pc don't contain Requires.private nor Libs.private

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libvncclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvncclient.so.0
%attr(755,root,root) %{_libdir}/libvncserver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvncserver.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/libvncserver-config
%attr(755,root,root) %{_libdir}/libvncclient.so
%attr(755,root,root) %{_libdir}/libvncserver.so
%{_libdir}/libvncclient.la
%{_libdir}/libvncserver.la
%{_includedir}/rfb
%{_pkgconfigdir}/libvncclient.pc
%{_pkgconfigdir}/libvncserver.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libvncclient.a
%{_libdir}/libvncserver.a

%files progs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/linuxvnc
