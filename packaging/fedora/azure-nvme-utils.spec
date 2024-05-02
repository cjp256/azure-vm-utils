%global commit cbf8c65d0d792b7dfc02dcaa55d5ec3077464ee6
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           azure-nvme-utils
Version:        0.1.3
Release:        %autorelease
Summary:        Utility and udev rules to help identify Azure NVMe devices

License:        MIT
URL:            https://github.com/Azure/%{name}
Source:         %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  pandoc
BuildRequires:  pkgconfig(libudev)

%description
Utility and udev rules to help identify Azure NVMe devices.

%prep
%autosetup -n azure-nvme-utils-%{commit}

%build
%cmake -DVERSION="%{version}-%{release}"
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%{_mandir}/man1/azure-nvme-id.1.gz
%{_sbindir}/azure-nvme-id
%{_udevrulesdir}/80-azure-nvme.rules

%changelog
%autochangelog
