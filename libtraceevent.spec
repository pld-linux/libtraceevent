#
# Conditional build:
%bcond_without	apidocs		# asciidoc documentation
%bcond_without	static_libs	# static libraries
#
Summary:	Linux kernel trace event library
Summary(pl.UTF-8):	Biblioteka do śledzenia zdarzeń jądra Linuksa
Name:		libtraceevent
Version:	1.7.3
Release:	1
License:	GPL v2/LGPL v2.1
Group:		Libraries
Source0:	https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git/snapshot/%{name}-%{version}.tar.gz
# Source0-md5:	5616c52896da1198f531e5612f35e2ca
URL:		https://git.kernel.org/pub/scm/libs/libtrace/libtraceevent.git
%{?with_apidocs:BuildRequires:	asciidoc}
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux kernel trace event library.

%description -l pl.UTF-8
Biblioteka do śledzenia zdarzeń jądra Linuksa.

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

%package apidocs
Summary:	API documentation for libtraceevent in HTML format
Summary(pl.UTF-8):	Dokumentacja API biblioteki libtraceevent w formacie HTML
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libtraceevent in HTML format.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libtraceevent w formacie HTML.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	VERBOSE=1 \
	prefix=%{_prefix} \
	libdir_relative=%{_lib}

%if %{with apidocs}
%{__make} doc \
	V=1
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=%{_prefix} \
	libdir_relative=%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT \
	VERBOSE=1

%if %{with apidocs}
%{__make} doc-install \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT \
	V=1
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libtraceevent.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtraceevent.so.1
%dir %{_libdir}/traceevent
%dir %{_libdir}/traceevent/plugins
%attr(755,root,root) %{_libdir}/traceevent/plugins/*.so

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtraceevent.so
%{_includedir}/traceevent
%{_pkgconfigdir}/libtraceevent.pc
%if %{with apidocs}
%{_mandir}/man3/kbuffer_*.3*
%{_mandir}/man3/libtraceevent.3*
%{_mandir}/man3/tep_*.3*
%{_mandir}/man3/trace_seq_*.3*
%endif

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtraceevent.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/libtraceevent-doc
%endif
