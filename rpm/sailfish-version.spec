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
%define _version_appendix (TARGET_CPU)
%else
%define _version_appendix (TARGET_CPU,%{_build_flavour})
%endif

%define _version_name %(cat %{SOURCE1})

Name: sailfish-version
Version: 0.0.1
Release: 1
Summary: SailfishOS %{version}.%{_obs_build_count} (%{_build_flavour})
Group: System/Libraries
License: Proprietary
Source: %{name}-%{version}.tar.gz
Source1: version_name
BuildArch: noarch

# UI & Applications
BuildRequires: csd
BuildRequires: jolla-camera
BuildRequires: jolla-contacts
BuildRequires: jolla-gallery
BuildRequires: jolla-keyboard
BuildRequires: jolla-messages
BuildRequires: jolla-sessions-qt5
BuildRequires: jolla-settings-accounts
BuildRequires: jolla-settings-bluetooth
BuildRequires: jolla-settings-networking
BuildRequires: jolla-settings-system
BuildRequires: jolla-settings-transferui-qt5
BuildRequires: jolla-startupwizard
BuildRequires: jolla-vault
BuildRequires: lipstick-jolla-home-qt5
BuildRequires: sailfish-tutorial
BuildRequires: simkit
BuildRequires: store-client
BuildRequires: voicecall-ui-jolla

# Core & MW
BuildRequires: apkd
BuildRequires: PackageKit
BuildRequires: alsa-plugins-pulseaudio
BuildRequires: buteo-mtp
BuildRequires: buteo-sync-plugins-qt5
BuildRequires: connman
BuildRequires: connman-configs-sailfish
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
%{_oneshotdir}/sailfish-version-update

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
VERSION_NAME=`cat %{SOURCE1}`
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
cp %{buildroot}/%{_sysconfdir}/sailfish-release.template %{buildroot}/%{_datadir}/doc/SailfishOS/
install -m755 -D sailfish-version-update %{buildroot}/%{_oneshotdir}/sailfish-version-update

%post
%{_bindir}/add-oneshot --now sailfish-version-update
