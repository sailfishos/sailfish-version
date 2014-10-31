%if 0%{?_obs_build_project:1}
%define _build_flavour %(echo %{_obs_build_project} | awk -F : '{if (NF == 3) print $3; else if (NF == 2) print strdevel; else print strunknown}' strdevel=devel strunknown=unknown)
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

%if %{_build_flavour} == release
%define _version_appendix (TARGET_CPU)
%else
%define _version_appendix (TARGET_CPU,%{_build_flavour})
%endif

Name: sailfish-version
Version: 0.0.1
Release: 1
Summary: SailfishOS %{version}.%{_obs_build_count} (%{_build_flavour})
Group: System/Libraries
License: TBD
Source: %{name}-%{version}.tar.gz
BuildArch: noarch
BuildRequires: rpm
BuildRequires: ssu, ssu-vendor-data-jolla
BuildRequires: lipstick-jolla-home-qt5, store-client
BuildRequires: jolla-settings-system, jolla-settings-networking, jolla-settings-bluetooth
BuildRequires: jolla-settings-accounts, jolla-settings-transferui-qt5
BuildRequires: jolla-camera, jolla-contacts, voicecall-ui-jolla
BuildRequires: jolla-gallery, jolla-messages
BuildRequires: jolla-sessions-qt5, jolla-keyboard, sailfish-browser
BuildRequires: jolla-firstsession, jolla-vault
# core MW
BuildRequires: bluez-configs-sailfish, buteo-mtp, buteo-sync-plugins-qt5
BuildRequires: qt5-plugin-bearer-connman, connman-configs-sailfish
BuildRequires: ohm, alsa-plugins-pulseaudio, connman, bluez
# currently different ofono for boston, so exclude
# BuildRequires: ofono
BuildRequires: PackageKit
Requires: PackageKit
Requires(post): ssu


%description
SailfishOS core "%{_version_name}" (%{version}.%{_obs_build_count}) %{_build_flavour}.

%files
%defattr(-,root,root,-)
%ghost %attr(0644, root, root) %{_sysconfdir}/sailfish-release
%config %{_sysconfdir}/sailfish-release.template
%config %{_sysconfdir}/os-release
%config %{_sysconfdir}/profile.d/sailfish-version.sh
%dir %{_datadir}/%{name}/packagelist.d
%{_bindir}/version

%package doc
Summary: SailfishOS %{version}.%{_obs_build_count} (%{_build_flavour})
Group: System/Libraries

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
VERSION_NAME=`cat version_name`
mkdir -p %{buildroot}/%{_sysconfdir}
cat > %{buildroot}/%{_sysconfdir}/sailfish-release.template <<EOF
NAME=SailfishOS
ID=sailfishos
VERSION="%{version}.%{_obs_build_count} ($VERSION_NAME) %{_version_appendix}"
VERSION_ID=%{version}.%{_obs_build_count}
PRETTY_NAME="SailfishOS %{version}.%{_obs_build_count} ($VERSION_NAME) %{_version_appendix}"
SAILFISH_BUILD=%{_obs_build_count}
SAILFISH_FLAVOUR=%{_build_flavour}
HOME_URL="https://sailfishos.org/"
EOF
ln -s %{_sysconfdir}/sailfish-release %{buildroot}/%{_sysconfdir}/os-release
install -m 644 -D sailfish-version.sh %{buildroot}/%{_sysconfdir}/profile.d/sailfish-version.sh
install -m 755 -D version %{buildroot}/%{_bindir}/version
cat %{buildroot}/%{_sysconfdir}/sailfish-release.template
mkdir -p %{buildroot}/%{_datadir}/doc/SailfishOS

%post
ARCH=`grep ^arch= /etc/ssu/ssu.ini | sed 's/^.*=//'`
if [ -z "$ARCH" ]; then
    sed 's/TARGET_CPU/unknown/' %{_sysconfdir}/sailfish-release.template > ${_sysconfdir}/sailfish-release
else
    sed "s/TARGET_CPU/$ARCH/" %{_sysconfdir}/sailfish-release.template > ${_sysconfdir}/sailfish-release
fi
