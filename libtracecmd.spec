#
# Conditional build:
%bcond_without	apidocs		# asciidoc documentation
%bcond_with	static_libs	# static library (unlikely to be useful)
#
Summary:	Library for creating and reading trace-cmd data files
Summary(pl.UTF-8):	Biblioteka do tworzenia i odczytu plików danych trace-cmd
Name:		libtracecmd
Version:	1.4.0
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git/snapshot/trace-cmd-%{name}-%{version}.tar.gz
# Source0-md5:	ca43732c21031ff310cc8107461fb7ed
URL:		https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git/
%{?with_apidocs:BuildRequires:	asciidoc}
BuildRequires:	libtraceevent-devel >= 1.5
BuildRequires:	libtracefs-devel >= 1.6
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel >= 1.4.0
Requires:	libtraceevent >= 1.5
Requires:	libtracefs >= 1.6
Requires:	zstd >= 1.4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library for creating and reading trace-cmd data files.

%description -l pl.UTF-8
Biblioteka do tworzenia i odczytu plików danych trace-cmd.

%package devel
Summary:	Header files for libtracecmd library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libtracecmd
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libtracefs-devel >= 1.6

%description devel
Header files for libtracecmd library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libtracecmd.

%package static
Summary:	Static libtracecmd library
Summary(pl.UTF-8):	Statyczna biblioteka libtracecmd
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libtracecmd library.

%description static -l pl.UTF-8
Statyczna biblioteka libtracecmd.

%package apidocs
Summary:	API documentation for libtracecmd in HTML format
Summary(pl.UTF-8):	Dokumentacja API biblioteki libtracecmd w formacie HTML
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libtracecmd in HTML format.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libtracecmd w formacie HTML.

%prep
%setup -q -n trace-cmd-%{name}-%{version}

%build
CFLAGS="%{rpmcflags}" \
CPPFLAGS="%{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} libs %{?with_static_libs:libtracecmd.a} \
	CC="%{__cc}" \
	VERBOSE=1 \
	prefix=%{_prefix} \
	libdir_relative=%{_lib}

%if %{with apidocs}
%{__make} doc \
	V=1
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install_libs \
	prefix=%{_prefix} \
	libdir_relative=%{_lib} \
	DESTDIR=$RPM_BUILD_ROOT \
	VERBOSE=1

%if %{with static_libs}
install -p build/lib/trace-cmd/libtracecmd.a $RPM_BUILD_ROOT%{_libdir}
%endif

%if %{with apidocs}
%{__make} install_doc \
	prefix=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT
%endif

# remove trace-cmd docs
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/man{1,5}
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/trace-cmd

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_libdir}/libtracecmd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtracecmd.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtracecmd.so
%{_includedir}/trace-cmd
%{_pkgconfigdir}/libtracecmd.pc
%if %{with apidocs}
%{_mandir}/man3/libtracecmd.3*
%{_mandir}/man3/tracecmd_*.3*
%endif

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtracecmd.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/libtracecmd-doc
%endif
