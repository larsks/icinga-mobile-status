Name:		icinga-mobile-status
Version:	20100415.2
Release:	1%{?dist}
Summary:	Simple status output for mobile devices.

Group:		Optional
License:	GPL
Source0:	%{name}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Prereq:		icinga

Buildarch:	noarch

%description
Simple status output for mobile devices.

%prep
%setup -q -n %{name}

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT/usr/share/icinga/cgi
install -d -m 755 $RPM_BUILD_ROOT/usr/share/icinga/templates

install -m 755 mobile.cgi $RPM_BUILD_ROOT/usr/share/icinga/cgi/mobile.cgi
install -m 444 mobile.html $RPM_BUILD_ROOT/usr/share/icinga/templates/mobile.html

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)

/usr/share/icinga/cgi/mobile.cgi
/usr/share/icinga/templates/mobile.html

