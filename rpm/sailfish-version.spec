%define _build_flavour %{?qa_stage_name}%{!?qa_stage_name:unknown}

# needs to match the prjconf in pj:tools
%if 0%{?_forced_sailfish_version_build_count:1}
%define _obs_build_count %{_forced_sailfish_version_build_count}
%else
%define _obs_build_count %(echo %{release} | awk -F . '{if (NF >= 3) print $3; else print $1 }')
%endif

%define _obs_commit_count %(echo %{release} | awk -F . '{if (NF >= 2) print $2; else print $1 }')

%if "%{_build_flavour}" == "release"
%define _version_appendix %{nil}
%else
%define _version_appendix \ (%{_build_flavour})
%endif

%define _version_name %(cat %{SOURCE1})

Name: sailfish-version
Version: 0.0.1
Release: 1
Summary: Sailfish OS %{version}.%{_obs_build_count} (%{_build_flavour})
URL: https://github.com/sailfishos/sailfish-version
License: BSD
Source: %{name}-%{version}.tar.gz
Source1: version_name
BuildArch: noarch
# Limit only for aarch64 as other architectures are handled with aggregate in OBS
ExclusiveArch: aarch64

# NOTE: patterns-sailfish-ui depends on patterns-sailfish-core-device which
# then in turn depends on patterns-sailfish-{core,mw}
BuildRequires: patterns-sailfish-ui

# Miscellanious things that are adaptation specific selections, which
# we try to select all here to ensure we build last.
BuildRequires: csd
BuildRequires: geoclue-provider-mlsdb
BuildRequires: jolla-settings-networking-multisim
BuildRequires: jolla-settings-system-nfc
BuildRequires: mapplauncherd-booster-silica-qt5-media
BuildRequires: patterns-sailfish-applications
BuildRequires: patterns-sailfish-cellular-apps
BuildRequires: patterns-sailfish-consumer-generic

Requires: sailfish-release-variant

%description
Sailfish OS core "%{_version_name}" (%{version}.%{_obs_build_count}) %{_build_flavour}.

%files
%defattr(-,root,root,-)
%license LICENSE.BSD
%attr(0644, root, root) %{_sysconfdir}/sailfish-release
%config %{_sysconfdir}/profile.d/sailfish-version.sh
%{_bindir}/version

%package variant
Summary: Sailfish OS release variant package
Requires: %{name}
Provides: sailfish-release-variant

%description variant
Package that replaces this one should always provide all the files
that this package is providing.

%files variant
%defattr(-,root,root,-)
%config %{_sysconfdir}/os-release
%config %{_sysconfdir}/issue
%config %{_sysconfdir}/issue.net

%package doc
Summary: Sailfish OS %{version}.%{_obs_build_count} (%{_build_flavour})

%description doc
%{summary}.

%files doc
%defattr(-,root,root,-)
%doc %{_datadir}/doc/SailfishOS

%prep
%setup -q


%build


%install
echo "Building for %{_build_flavour}"
mkdir -p %{buildroot}/%{_sysconfdir}
cat > %{buildroot}/%{_sysconfdir}/sailfish-release <<EOF
NAME="Sailfish OS"
ID=sailfishos
VERSION="%{version}.%{_obs_build_count} (%{_version_name})%{_version_appendix}"
VERSION_ID=%{version}.%{_obs_build_count}
PRETTY_NAME="Sailfish OS %{version}.%{_obs_build_count} (%{_version_name})%{_version_appendix}"
SAILFISH_BUILD=%{_obs_build_count}
SAILFISH_FLAVOUR=%{_build_flavour}
HOME_URL="https://sailfishos.org/"
EOF
ln -s sailfish-release %{buildroot}/%{_sysconfdir}/os-release

cat > %{buildroot}/%{_sysconfdir}/issue <<EOF
Sailfish OS %{version}.%{_obs_build_count} (%{_version_name})%{_version_appendix}
Kernel \r on an \m
EOF
cp -p %{buildroot}/%{_sysconfdir}/issue %{buildroot}/%{_sysconfdir}/issue.net
echo >> %{buildroot}/%{_sysconfdir}/issue

install -m 644 -D sailfish-version.sh %{buildroot}/%{_sysconfdir}/profile.d/sailfish-version.sh
install -m 755 -D version %{buildroot}/%{_bindir}/version
cat %{buildroot}/%{_sysconfdir}/sailfish-release
mkdir -p %{buildroot}/%{_datadir}/doc/SailfishOS
cp %{buildroot}/%{_sysconfdir}/sailfish-release %{buildroot}/%{_datadir}/doc/SailfishOS/
