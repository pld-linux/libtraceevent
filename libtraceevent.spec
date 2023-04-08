#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	Linux kernel trace event library
Name:		libtraceevent
Version:	1.7.2
Release:	1
License:	GPL v2/LGPL
Group:		Libraries
Source0:	https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git/snapshot/%{name}-%{version}.tar.gz
# Source0-md5:	5a8cd771ab709e7a7eb793555c7e570f
URL:		https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux kernel trace event library.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q

%build
%{__make} \
	CFLAGS="%{rpmcflags}" \
	prefix=%{_prefix} \
	libdir=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=%{_prefix} \
	libdir=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/%{name}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}.so.1
%dir %{_libdir}/traceevent
%dir %{_libdir}/traceevent/plugins
%attr(755,root,root) %{_libdir}/traceevent/plugins/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%{_includedir}/traceevent
%{_pkgconfigdir}/%{name}.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/%{name}.a
%endif
