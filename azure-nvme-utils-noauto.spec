Name:           azure-nvme-utils
Version:        0.1.3
Release:        1
Summary:        Utilities to assist managing NVMe devices on Azure

License:        MIT
URL:            https://github.com/Azure/%{name}
Source:         %{url}/archive/v%{version}/%{name}-v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  pandoc
BuildRequires:  pkgconfig(libudev)

%description
This package provides azure-nvme-id for NVMe device identification and udev
rules to provide symlinks using available identifiers.

%prep
%autosetup -n %{name}-%{version}

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
* Fri May 03 2024 Chris Patterson <cpatterson@microsoft.com> - 0.1.3-1
- Initial version.
