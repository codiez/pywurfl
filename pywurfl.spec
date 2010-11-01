# TemplateVer:  0.4

%{?!python:%define python python}
%{?!pybasever:%{expand:%%define pybasever %(%{__python} -c "import sys ; print sys.version[:3]")}}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define origname pywurfl

Name:		%{origname}
Version:        7.1.0
Release:        1
Summary:        wurfl processing and query utilities

Group:          Development/Libraries
License:        LGPL
URL:		http://celljam.net/
Source0:	%{origname}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  %{python}-devel
Requires:       python-abi = %{pybasever}

# processing tools
Requires:       python-elementtree
Requires:       python-levenshtein

# ql
Requires:       pyparsing

%description
python tools for processing and querying wurfl.xml

%prep
%setup -n %{origname}-%{version} -q

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT --record=INSTALLED_FILES.tmp

# Ghost optimized 
sed 's/\(.*\.pyo\)/%ghost \1/' < INSTALLED_FILES.tmp > INSTALLED_FILES
find $RPM_BUILD_ROOT%{python_sitelib} -type d \
| sed "s|^$RPM_BUILD_ROOT|%dir |" >> INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root,-)
%doc doc/* LICENSE
%{_bindir}/*pyc
%{_bindir}/*pyo

%changelog
* Mon Mar 27 2006 Pau Aliagas <pau@newtral.org> 5.0.0a-1
- first rpm version

* Wed Apr 27 2006 Armand Lynch <lyncha@users.sourceforge.net>
- changed license to LGPL

* Sun Jun 4 2006 Armand Lynch <lyncha@users.sourceforge.net>
- updated version

* Sun Aug 3 2006 Armand Lynch <lyncha@users.sourceforge.net>
- updated version
- changed name to pywurfl

* Tue Sep 26 2006 Armand Lynch <lyncha@users.sourceforge.net>
- updated version

* Sat Feb 10 2007 Armand Lynch <lyncha@users.sourceforge.net>
- updated version

* Tue Jul 31 2007 Armand Lynch <lyncha@users.sourceforge.net>
- updated version

* Sun Apr 13 2008 Armand Lynch <lyncha@users.sourceforge.net>
- updated version

* Thu Apr 9 2009 Armand Lynch <lyncha@users.sourceforge.net> 6.4.1-1
- updated version

* Sat Mar 6 2010 Armand Lynch <lyncha@users.sourceforge.net> 7.0.0
- updated version

* Thu May 6 2010 Armand Lynch <lyncha@users.sourceforge.net> 7.1.0
- updated version

