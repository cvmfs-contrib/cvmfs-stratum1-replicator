Name:		cvmfs-stratum1-replicator
Version:	0.3
# The release_prefix macro is used in the OBS prjconf, don't change its name
%define release_prefix 1
Release:	%{release_prefix}%{?dist}
Summary:	Snapshot services for the CVMFS Stratum-1

Group:		Applications/System
License:	Apache 2.0
URL:		https://github.com/bbockelm/cvmfs-stratum1-replicator

# To generate tarball:
# git archive --format=tgz --prefix=%{name}-%{version}/ v%{version} > %{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz

%{?systemd_requires}
BuildRequires: systemd
BuildArch:      noarch

Requires:	cvmfs-server

%description
A set of systemd-based unit files and generators for synchronizing repositories
on a CVMFS Stratum-1 server.

%prep
%setup -q

%build

%install

install -d $RPM_BUILD_ROOT/%{_unitdir}
install -d $RPM_BUILD_ROOT/usr/lib/systemd/system-generators
install -d $RPM_BUILD_ROOT/usr/bin
install -m 0644 cvmfs-snapshot.service $RPM_BUILD_ROOT%{_unitdir}/cvmfs-snapshot.service
install -m 0644 cvmfs-snapshot@.service $RPM_BUILD_ROOT%{_unitdir}/cvmfs-snapshot@.service
install -m 0644 cvmfs-snapshot@.timer $RPM_BUILD_ROOT%{_unitdir}/cvmfs-snapshot@.timer
install -m 0755 cvmfs-snapshot-generator $RPM_BUILD_ROOT/usr/lib/systemd/system-generators/cvmfs-snapshot-generator
install -m 0755 see-cvmfs-snapshot $RPM_BUILD_ROOT/usr/bin/see-cvmfs-snapshot
install -m 0755 stop-cvmfs-snapshots $RPM_BUILD_ROOT/usr/bin/stop-cvmfs-snapshots

%post
%systemd_post cvmfs-snapshot.service

%preun
%systemd_preun cvmfs-snapshot.service

%postun
%systemd_postun_with_restart cvmfs-snapshot.service


%files

%{_unitdir}/cvmfs-snapshot.service
%{_unitdir}/cvmfs-snapshot@.service
%{_unitdir}/cvmfs-snapshot@.timer
/usr/lib/systemd/system-generators/cvmfs-snapshot-generator
/usr/bin/see-cvmfs-snapshot
/usr/bin/stop-cvmfs-snapshots

%changelog
* Thu Apr 05 2018 Dave Dykstra <dwd@fnal.gov> - 0.3-1
- Add see-cvmfs-snapshot and stop-cvmfs-snapshots commands.
- Use a %release_prefix macro to work better with the OpenSUSE Build Service.
- Change build architecture to noarch.

* Thu Apr 05 2018 Dave Dykstra <dwd@fnal.gov> - 0.2-1
- Don't generate a repository replicator service until the initial
  snapshot is completed.
- Add a timestamp to the entries in /tmp/genlog.

* Wed Jan 11 2017 Brian Bockelman <bbockelm@cse.unl.edu> - 0.1-1
- Initial version
