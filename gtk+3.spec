Summary:	The Gimp Toolkit
Name:		gtk+3
Version:	3.10.4
Release:	1
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/gtk+/3.10/gtk+-%{version}.tar.xz
# Source0-md5:	88c8e2a88b8a3af32080f282af271a11
URL:		http://www.gtk.org/
BuildRequires:	atk-devel >= 1:2.10.0
BuildRequires:	at-spi2-atk-devel >= 2.10.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cairo-devel >= 1.12.0
BuildRequires:  colord-devel
BuildRequires:	cups-devel
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	gdk-pixbuf-devel >= 2.30.0
BuildRequires:	gettext-devel
BuildRequires:	glib-devel >= 1:2.38.0
# broken dep, --disable-schemas-compile ignored
BuildRequires:	glib-gio-gsettings
BuildRequires:	gobject-introspection-devel >= 1.38.0
BuildRequires:	gtk-doc
BuildRequires:	jasper-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
BuildRequires:	pango-devel >= 1:1.36.0
BuildRequires:	perl-base
BuildRequires:	pkg-config
BuildRequires:	shared-mime-info
BuildRequires:	xorg-libX11-devel
BuildRequires:	xorg-libXcomposite-devel
BuildRequires:	xorg-libXcursor-devel
BuildRequires:	xorg-libXext-devel
BuildRequires:	xorg-libXft-devel
BuildRequires:	xorg-libXi-devel
BuildRequires:	xorg-libXinerama-devel
BuildRequires:	xorg-libXrandr-devel
BuildRequires:	xorg-libXrender-devel
Requires(post,postun):	glib-gio-gsettings
Requires:	atk >= 1:2.10.0
Requires:	gdk-pixbuf >= 2.30.0
Requires:	glib-gio >= 1:2.38.0
Requires:	pango >= 1:1.36.0
Requires:	shared-mime-info
Suggests:	colord
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abivers		3.0.0

%description
GTK+, which stands for the Gimp ToolKit, is a library for creating
graphical user interfaces for the X Window System. It is designed to
be small, efficient, and flexible. GTK+ is written in C with a very
object-oriented approach.

%package devel
Summary:	GTK+ header files and development documentation
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and development documentation for the GTK+ libraries.

%package apidocs
Summary:	GTK+ API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
GTK+ API documentation.

%package update-icon-cache
Summary:	Utility to update icon cache used by GTK+ library
Group:		Applications/System

%description update-icon-cache
Utility to update icon cache used by GTK+ library.

%prep
%setup -qn gtk+-%{version}

%build
%{__libtoolize}
%{__gtkdocize}
%{__aclocal} -I m4macros
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--enable-introspection=yes	\
	--enable-packagekit=no		\
	--enable-x11-backend		\
	--enable-xcomposite		\
	--enable-xdamage		\
	--enable-xfixes			\
	--enable-xinerama		\
	--enable-xkb			\
	--enable-xrandr			\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/{modules,%{abivers}/{engines,theming-engines}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/%{abivers}/gtk.immodules

# shut up check-files (static modules and *.la for modules)
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/gtk-3.0/*/*/*.la

# remove unsupported locale scheme
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{az_IR,ca@valencia,crh,io,kg,my,ps}

# unpackaged
%{__rm} $RPM_BUILD_ROOT%{_bindir}/gtk3-demo*
%{__rm} $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas/org.gtk.{Demo,exampleapp}.gschema.xml

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/ldconfig
%update_gsettings_cache
umask 022
gtk-query-immodules-3.0 --update-cache ||:

%postun
/usr/sbin/ldconfig
if [ "$1" != "0" ]; then
    umask 022
    gtk-query-immodules-3.0 --update-cache ||:
else
    %update_gsettings_cache
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/gtk-launch
%attr(755,root,root) %{_bindir}/gtk-query-immodules-3.0
%attr(755,root,root) %{_bindir}/gtk3-widget-factory

%dir %{_libdir}/gtk-3.0
%attr(755,root,root) %ghost %{_libdir}/libgailutil-3.so.?
%attr(755,root,root) %ghost %{_libdir}/libgdk-3.so.?
%attr(755,root,root) %ghost %{_libdir}/libgtk-3.so.?
%attr(755,root,root) %{_libdir}/libgdk-3.so.*.*.*
%attr(755,root,root) %{_libdir}/libgtk-3.so.*.*.*
%attr(755,root,root) %{_libdir}/libgailutil-3.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%dir %{_libdir}/gtk-3.0/modules
%dir %{_libdir}/gtk-3.0/%{abivers}
%dir %{_libdir}/gtk-3.0/%{abivers}/engines
%dir %{_libdir}/gtk-3.0/%{abivers}/theming-engines
%dir %{_libdir}/gtk-3.0/%{abivers}/immodules
%dir %{_libdir}/gtk-3.0/%{abivers}/printbackends

%ghost %{_libdir}/gtk-3.0/%{abivers}/gtk.immodules

%attr(755,root,root) %{_libdir}/gtk-3.0/%{abivers}/printbackends/*.so
%attr(755,root,root) %{_libdir}/gtk-3.0/%{abivers}/immodules/im-*.so

%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/gtk-3.0/im-multipress.conf

%dir %{_datadir}/themes/Default/gtk-3.0
%dir %{_datadir}/themes/Emacs
%dir %{_datadir}/themes/Emacs/gtk-3.0
%dir %{_sysconfdir}/gtk-3.0
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.ColorChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.FileChooser.gschema.xml
%{_datadir}/themes/Default/gtk-3.0/gtk-keys.css
%{_datadir}/themes/Emacs/gtk-3.0/gtk-keys.css
%{_mandir}/man1/gtk-launch.1*
%{_mandir}/man1/gtk-query-immodules-3.0.1*

%files devel
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/gail-*
%{_includedir}/gtk-*
%{_aclocaldir}/*.m4
%{_datadir}/gtk-3.0
%{_pkgconfigdir}/*.pc
%{_datadir}/gir-1.0/*.gir

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gail-libgail-util3
%{_gtkdocdir}/gdk3
%{_gtkdocdir}/gtk3

%files update-icon-cache
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gtk-update-icon-cache
%{_mandir}/man1/gtk-update-icon-cache.1*

