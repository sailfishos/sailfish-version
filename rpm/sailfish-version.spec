Name: sailfish-version
Version: 0.0.1
Release: 1
Summary: Version of Sailfish
Group: System/Libraries
License: TBD
Source: %{name}-%{version}.tar.gz
BuildRequires: rpm
BuildRequires: ssu, ssu-vendor-data-jolla
BuildRequires: lipstick-jolla-home-qt5, store-client
BuildRequires: jolla-camera, jolla-contacts, voicecall-ui-jolla
BuildRequires: jolla-gallery, jolla-messages, jolla-mediaplayer
BuildRequires: jolla-sessions-qt5, jolla-keyboard, sailfish-browser

%if 0%{?_obs_build_project:1}
%define _build_flavour %(echo %{_obs_build_project} | awk -F : '{if (NF == 3) print $3; else if (NF == 2) print strdevel; else print strunknown}' strdevel=devel strunknown=unknown)
%else
%define _build_flavour unknown
%endif

# needs to match the prjconf in pj:tools
%define _obs_build_count %(echo %{release} | awk -F . '{if (NF >= 3) print $3; else print $1 }')
%define _obs_commit_count %(echo %{release} | awk -F . '{if (NF >= 2) print $2; else print $1 }')

%description
%{summary}.

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/sailfish-release
%config %{_sysconfdir}/os-release
%config %{_sysconfdir}/profile.d/sailfish-version.sh
%{_datadir}/%{name}/packagelist


%prep
%setup -q


%build


%install
echo "Building for %{_build_flavour}"
mkdir -p %{buildroot}/%{_datadir}/%{name}
RPM_PATH=${RPM_SOURCE_DIR:-rpm}/${RPM_PACKAGE_NAME:-mce}.spec
for req in `rpmspec -q --buildrequires $RPM_PATH`; do
    rpm -qa $req >> %{buildroot}/%{_datadir}/%{name}/packagelist
done
mkdir -p %{buildroot}/%{_sysconfdir}
cat > %{buildroot}/%{_sysconfdir}/sailfish-release <<EOF
NAME=SailfishOS
ID=sailfishos
VERSION=%{version}.%{_obs_build_count}
VERSION_ID=%{version}.%{_obs_build_count}
PRETTY_NAME="SailfishOS %{version}.%{_obs_build_count} (%{_target_cpu},%{_build_flavour})"
SAILFISH_BUILD=%{_obs_build_count}
SAILFISH_FLAVOUR=%{_build_flavour}
HOME_URL="https://sailfishos.org/"
EOF
ln -s %{_sysconfdir}/sailfish-release %{buildroot}/%{_sysconfdir}/os-release
install -m 644 -D sailfish-version.sh %{buildroot}/%{_sysconfdir}/profile.d/sailfish-version.sh
