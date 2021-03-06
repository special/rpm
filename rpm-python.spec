# build against xz?
%bcond_without xz
# build against python
%bcond_without python
# sqlite backend is pretty useless
%bcond_with sqlite
# just for giggles, option to build with internal Berkeley DB
%bcond_with int_bdb

%define rpmhome /usr/lib/rpm

%define rpmver 4.9.1.2


Summary: The RPM package management system
Name: rpm-python
Version: 4.9.1.2
Release: 18
BuildRequires: python-devel
# This includes the Source0 => END_OF_INCLUDE_IN_PYTHON_SPEC lines from the main spec file
%{expand:%(sed -n -e '/^Source0:/,/^##END_OF_INCLUDE_IN_PYTHON_SPEC##/p' <%_sourcedir/rpm.spec)}
Source100: rpm.spec
Requires: coreutils
Requires: db4-utils
Requires: popt >= 1.10.2.1
Requires: curl
Requires: rpm = %{version}
BuildRequires: db4-devel


# XXX generally assumed to be installed but make it explicit as rpm
# is a bit special...
BuildRequires: %{_vendor}-rpm-config
BuildRequires: gawk
BuildRequires: elfutils-devel >= 0.112
BuildRequires: elfutils-libelf-devel
BuildRequires: readline-devel zlib-devel
BuildRequires: nss-devel
# The popt version here just documents an older known-good version
BuildRequires: popt-devel >= 1.10.2
BuildRequires: file-devel
BuildRequires: gettext-devel
BuildRequires: ncurses-devel
BuildRequires: bzip2-devel >= 0.9.0c-2
BuildRequires: lua-devel >= 5.1
BuildRequires: libcap-devel
BuildRequires: xz-devel >= 4.999.8
BuildRequires: cvs


%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages. Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%prep
# This includes the %%prep section from the main spec file
%{expand:%(sed -n -e '/^%%prep/,/^%%install/p' <%_sourcedir/rpm.spec | sed -e '1d' -e '$d')}
%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR="$RPM_BUILD_ROOT" install
find "%{buildroot}" -not -type d -and -not -path %{buildroot}%{_libdir}/python%{py_ver}/site-packages/rpm/\* -print0 | xargs -0 rm
pushd $RPM_BUILD_ROOT/%py_sitedir/rpm
rm -f _rpmmodule.a _rpmmodule.la
python %py_libdir/py_compile.py *.py
python -O %py_libdir/py_compile.py *.py
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/python*

