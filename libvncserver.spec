#
# Conditional build:
%bcond_with	openssl	# use OpenSSL instead of GnuTLS

Summary:	LibVNCServer - a for easy implementation of VNC/RDP server
Summary(pl.UTF-8):	LibVNCServer - biblioteka do łatwego implementowania serwera VNC/RDP
Name:		libvncserver
Version:	0.9.11
Release:	3
License:	GPL v2
Group:		Libraries
#Source0Download: https://github.com/LibVNC/libvncserver/releases
Source0:	https://github.com/LibVNC/libvncserver/archive/LibVNCServer-%{version}.tar.gz
# Source0-md5:	7f06104d5c009813e95142932c4ddb06
Patch0:		%{name}-linux.patch
Patch1:		%{name}-noLlibdir.patch
URL:		https://github.com/LibVNC/libvncserver/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{!?with_openssl:BuildRequires:	gnutls-devel >= 2.4.0}
BuildRequires:	libgcrypt-devel >= 1.4.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	libva-devel >= 1.2.0
BuildRequires:	libva-x11-devel >= 1.2.0
%{?with_openssl:BuildRequires:	openssl-devel}
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	systemd-devel >= 1:209
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXdamage-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	zlib-devel
# for noinst client_examples only
#BuildRequires:	SDL-devel
#BuildRequires:	gtk+2-devel >= 2.0
# for vnc2mpg example
#BuildRequires:	ffmpeg-devel || lame-libs-devel
%{!?with_openssl:Requires:	gnutls >= 2.4.0}
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
Requires:	%{name} = %{version}-%{release}
%{!?with_openssl:Requires:	gnutls-devel >= 2.4.0}
Requires:	libgcrypt-devel >= 1.4.0
Requires:	libjpeg-devel
Requires:	libpng-devel
%{?with_openssl:Requires:	openssl-devel}
Requires:	zlib-devel

%description devel
LibVNCServer header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe LibVNCServer.

%package static
Summary:	Static LibVNCServer libraries
Summary(pl.UTF-8):	Statyczne biblioteki LibVNCServer
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LibVNCServer libraries.

%description static -l pl.UTF-8
Statyczne biblioteki LibVNCServer.

%prep
%setup -q -n libvncserver-LibVNCServer-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_openssl:--without-gnutls} \
	%{!?with_openssl:--without-ssl}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvnc*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_libdir}/libvncclient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvncclient.so.1
%attr(755,root,root) %{_libdir}/libvncserver.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvncserver.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/libvncserver-config
%attr(755,root,root) %{_libdir}/libvncclient.so
%attr(755,root,root) %{_libdir}/libvncserver.so
%{_includedir}/rfb
%{_pkgconfigdir}/libvncclient.pc
%{_pkgconfigdir}/libvncserver.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libvncclient.a
%{_libdir}/libvncserver.a
