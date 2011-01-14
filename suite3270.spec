Summary:	IBM 3270 terminal emulator
Summary(pl.UTF-8):	Emulator terminala IBM 3270
Name:		suite3270
Version:	3.3.11ga6
Release:	1
License:	MIT-like
Group:		Applications/Terminal
Source0:	http://x3270.bgp.nu/download/%{name}-%{version}-src.tgz
# Source0-md5:	01d6d3809a457e6f6bd3731642e0c02d
URL:		http://x3270.bgp.nu/
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	tcl-devel >= 8.4
BuildRequires:	xorg-app-bdftopcf
BuildRequires:	xorg-app-mkfontdir
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXaw-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-proto-xproto-devel
BuildRequires:	xorg-util-imake
Requires(post,postun):	fontpostinst
# better separate x3270 (the rest doesn't depend on X)
Obsoletes:	x3270
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
x3270 is an IBM 3270 terminal emulator. It runs over a TELNET
connection, emulating either an IBM 3279 (color) or 3278 (monochrome).
It supports:
 - The full TN3270E protocol
 - SSL/TLS (via the OpenSSL library) for encrypted sessions
 - APL2 characters
 - Non-English character sets, including Russian, Turkish, Hebrew and
   DBCS Chinese and Japanese
 - IND$FILE file transfer
 - NVT mode (emulating a color xterm)
 - A pop-up keypad for 3270-specific keys
 - A scrollbar
 - Printer session integration
 - Extensive debugging and scripting facilities

It does not yet support graphics.

x3270 is available in several different forms:
 - x3270 is for use on a graphics display
 - c3270 is a curses-based version for use on a dumb terminal (e.g., a
   serial terminal or a Linux console)
 - s3270 is a displayless version for writing screen-scraping scripts
 - tcl3270 is similar to s3270, but integrated with Tcl
 - pr3287 is for printer emulation

%description -l pl.UTF-8
x3270 to emulator terminala IBM 3270. Działa po połączeniu TELNET,
emulując terminal IBM 3279 (kolorowy) lub 3278 (monochromatyczny).
Obsługuje:
 - pełny protokół TN3270E
 - SSL/TLS (poprzez bibliotekę OpenSSL) do szyfrowanych sesji
 - znaki APL2
 - różne zestawy znaków, włącznie z rosyjskim, tureckim, hebrajskim
   oraz chińskim i japońskim DBCS
 - przesyłanie plików IND$FILE
 - tryb NVT (emulację terminala kolorowego)
 - wyskakujący keypad do klawiszy specyficznych dla 3270
 - pasek przewijania
 - integrację sesji drukarki
 - śledzenie i skrypty.

Nie obsługuje jeszcze grafiki.

x3270 jest dostępny w kilku różnych postaciach:
 - x3270 do używania na ekranie graficznym
 - c3270 to wersja oparta o curses do używania na prostym terminalu
   (np. terminalu szeregowym lub konsoli linuksowej)
 - s3270 to wersja niewyświetlająca, do pisania skryptów
 - tcl3270 to wersja podobna do s3270, ale zintegrowana z Tcl-em
 - pr3287 do emulacji drukarki.

%prep
%setup -q -c

%build
export ac_cv_lib_nsl_gethostbyname=no
CPPFLAGS="-I/usr/include/ncurses"
cd c3270-3.3
%configure
%{__make}
cd ../pr3287-3.3
%configure
%{__make}
cd ../s3270-3.3
%configure
%{__make}
cd ../tcl3270-3.3
%configure
%{__make}
cd ../x3270-3.3
%configure \
	--with-fontdir=%{_fontsdir}/misc
%{__make} \
	CDEBUGFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 -C c3270-3.3 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -j1 -C pr3287-3.3 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -j1 -C s3270-3.3 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -j1 -C tcl3270-3.3 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -j1 -C x3270-3.3 install \
	DESTDIR=$RPM_BUILD_ROOT \
	BINDIR=%{_bindir}

rm -rf doc
install -d doc/{c3270,pr3287,s3270,tcl3270,x3270}
cp -a c3270-3.3/{LICENSE,README,html} doc/c3270
cp -a pr3287-3.3/{LICENSE,README,html} doc/pr3287
cp -a s3270-3.3/{LICENSE,README,Examples,html} doc/s3270
cp -a tcl3270-3.3/{LICENSE,README,Examples,html} doc/tcl3270
cp -a x3270-3.3/{LICENSE,README*,Examples,html} doc/x3270

%clean
rm -rf $RPM_BUILD_ROOT

%post
fontpostinst misc

%postun
fontpostinst misc

%files
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_bindir}/c3270
%attr(755,root,root) %{_bindir}/pr3287
%attr(755,root,root) %{_bindir}/s3270
%attr(755,root,root) %{_bindir}/tcl3270
%attr(755,root,root) %{_bindir}/x3270
%attr(755,root,root) %{_bindir}/x3270if
%dir %{_sysconfdir}/x3270
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/x3270/ibm_hosts
%{_fontsdir}/misc/3270*.pcf.gz
