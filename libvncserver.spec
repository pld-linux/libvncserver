%define		_packname	LibVNCServer
Summary:	A library to make writing a vnc server easy
Name:		libvncserver
Version:	0.6
Release:	1
Epoch:		0
License:	GPL
Group:		Libraries
URL:		http://libvncserver.sourceforge.net/
Source0:	http://dl.sf.net/libvncserver/%{_packname}-%{version}.tar.gz
# Source0-md5:	b6ef0d29a1247a4dbb1b5bbc6bab6458
BuildRequires:	libjpeg-devel
BuildRequires:	zlib-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	XFree86-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibVNCServer makes writing a VNC server (or more correctly, a program
exporting a framebuffer via the Remote Frame Buffer protocol) easy.

It is based on OSXvnc, which in turn is based on the original Xvnc by
ORL, later AT&T research labs in UK.

It hides the programmer from the tedious task of managing clients and
compression schemata.

LibVNCServer was put together and is (actively ;-) maintained by
Johannes Schindelin <Johannes.Schindelin@gmx.de>

%prep
%setup -q -n %{_packname}-%{version}


%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_includedir}/rfb
%{_includedir}/rfb/*
%{_libdir}/*.a
