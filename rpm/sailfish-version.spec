%if 0%{?_obs_build_project:1}
%define _build_flavour %(echo %{_obs_build_project} | awk -F : '{if ($NF == "testing" || $NF == "release") print $NF; else if ($NF ~ /[0-9]\.[0-9]\.[0-9]/ && NF == 3) print strdevel; else if (NF == 2) print strdevel ;else print strunknown}' strdevel=devel strunknown=unknown)
%else
%define _build_flavour unknown
%endif

# needs to match the prjconf in pj:tools
%if 0%{?_forced_sailfish_version_build_count:1}
%define _obs_build_count %{_forced_sailfish_version_build_count}
%else
%define _obs_build_count %(echo %{release} | awk -F . '{if (NF >= 3) print $3; else print $1 }')
%endif

%define _obs_commit_count %(echo %{release} | awk -F . '{if (NF >= 2) print $2; else print $1 }')

%if "%{_build_flavour}" == release
%define _version_appendix %{nil}
%else
%define _version_appendix \ (%{_build_flavour})
%endif

%define _version_name %(cat %{SOURCE1})

Name: sailfish-version
Version: 0.0.1
Release: 1
Summary: Sailfish OS %{version}.%{_obs_build_count} (%{_build_flavour})
Group: System/Libraries
URL: https://sailfishos.org/
License: Proprietary
Source: %{name}-%{version}.tar.gz
Source1: version_name
BuildArch: noarch

# UI & Applications
# We should use patterns, but because of JB#38246 we cant.
# Store apps cannot be here because apps repo is above non-oss repository.
BuildRequires: csd
BuildRequires: jolla-keyboard
BuildRequires: jolla-sessions-qt5
BuildRequires: lipstick-jolla-home-qt5
BuildRequires: patterns-sailfish-applications
BuildRequires: patterns-sailfish-cellular-apps
BuildRequires: patterns-sailfish-consumer-generic

# Core & MW
# We should use patterns, but because of JB#38246 we cant
BuildRequires: PackageKit
BuildRequires: alsa-plugins-pulseaudio
BuildRequires: buteo-mtp
BuildRequires: buteo-sync-plugins-qt5
BuildRequires: connman
BuildRequires: jolla-common-configurations
BuildRequires: jolla-firstsession
BuildRequires: ofono
BuildRequires: ohm
BuildRequires: qt5-plugin-bearer-connman
BuildRequires: rpm
BuildRequires: ssu
BuildRequires: ssu-vendor-data-jolla

Requires: PackageKit
%{_oneshot_requires_post}
Requires: oneshot
Requires(post): ssu
# mer-release provides /etc/issue* as well
Obsoletes: mer-release

Requires: sailfish-release-variant

%description
Sailfish OS core "%{_version_name}" (%{version}.%{_obs_build_count}) %{_build_flavour}.

%files
%defattr(-,root,root,-)
%attr(0644, root, root) %{_sysconfdir}/sailfish-release
%config %{_sysconfdir}/profile.d/sailfish-version.sh
%dir %{_datadir}/%{name}/packagelist.d
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
mkdir -p %{buildroot}/%{_datadir}/%{name}/packagelist.d
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
