# Defining the package namespace
%global ns_name ea
%global ns_dir /opt/cpanel
%global pkg ruby24
%global gem_name mizuho

# Force Software Collections on
%global _scl_prefix %{ns_dir}
%global scl %{ns_name}-%{pkg}
# HACK: OBS Doesn't support macros in BuildRequires statements, so we have
#       to hard-code it here.
# https://en.opensuse.org/openSUSE:Specfile_guidelines#BuildRequires
%global scl_prefix %{scl}-
%{?scl:%scl_package rubygem-%{gem_name}}

# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define release_prefix 1

# Although there are tests, they don't work yet
# https://github.com/FooBarWidget/mizuho/issues/5
%global enable_tests 0

Summary:       Mizuho documentation formatting tool
Name:          %{?scl:%scl_prefix}rubygem-%{gem_name}
Version:       0.9.20
Release:       %{release_prefix}%{?dist}.cpanel
Group:         Development/Languages
License:       MIT
URL:           https://github.com/FooBarWidget/mizuho
Source0:       https://rubygems.org/gems/%{gem_name}-%{version}.gem
Patch1:        0001-Fix-native-templates-directory-path.patch
Requires:      %{?scl_prefix}ruby(rubygems)
Requires:      %{?scl_prefix}ruby(release)
Requires:      %{?scl_prefix}rubygem-nokogiri >= 1.4.0
Requires:      %{?scl_prefix}rubygem(sqlite3)
%{?scl:Requires:%scl_runtime}

BuildRequires: scl-utils
BuildRequires: scl-utils-build
%{?scl:BuildRequires: %{scl}-runtime}
BuildRequires: %{?scl_prefix}ruby
BuildRequires: %{?scl_prefix}rubygems-devel

%if 0%{?enable_tests}
BuildRequires: %{?scl_prefix}rubygem-rspec
%endif
BuildArch:     noarch
Provides:      %{?scl:%scl_prefix}rubygem(%{gem_name}) = %{version}

%description
A documentation formatting tool. Mizuho converts Asciidoc input files into
nicely outputted HTML, possibly one file per chapter. Multiple templates are
supported, so you can write your own.


%package doc
Summary:   Documentation for %{name}
Group:     Documentation
Requires:  %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}
%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%patch1 -p 1

sed -i 's/NATIVELY_PACKAGED = .*/NATIVELY_PACKAGED = true/' lib/mizuho.rb

# Fixup rpmlint failures
echo "#toc.html" >> templates/toc.html


%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
gem install \
        -V \
        --local \
        --install-dir .%{gem_dir} \
        --bindir .%{_bindir} \
        --force \
        --backtrace ./%{gem_name}-%{version}.gem
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

# Remove build leftovers.
rm -rf %{buildroot}%{gem_instdir}/{.rvmrc,.document,.require_paths,.gitignore,.travis.yml,.rspec,.gemtest,.yard*}
rm -rf %{buildroot}%{gem_instdir}/%{gem_name}.gemspec

%if 0%{?enable_tests}
%check
pushd %{buildroot}%{gem_instdir}
ruby -Ilib -S rspec -f s -c test/*_spec.rb
popd
%endif

%files
%doc %{gem_instdir}/LICENSE.txt
%dir %{gem_instdir}
%{_bindir}/mizuho
%{_bindir}/mizuho-asciidoc
%{gem_instdir}/bin
%{gem_instdir}/debian.template
%{gem_instdir}/rpm
%{gem_instdir}/source-highlight
%{gem_instdir}/templates
%{gem_instdir}/asciidoc
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_instdir}/README.markdown
%doc %{gem_dir}/doc
%{gem_instdir}/Rakefile
%{gem_instdir}/test


%changelog
* Fri Apr 14 2017 Rishwanth Yeddula <rish@cpanel.net> - 0.9.20-1
- Initial package

