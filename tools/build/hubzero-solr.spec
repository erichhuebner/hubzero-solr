
%define debug_package %{nil}

Name:          hubzero-solr
Version:       6.1.0
Release:       4
Summary:       HUBzero - Solr - Ultra-fast Lucene-based Search Server
License:       Apache License, Version 2.0
Packager:      Nicholas J. Kisseberth <nkissebe@purdue.edu>
URL:           http://lucene.apache.org/solr
Group:         Development/Libraries
Vendor:        Apache Software Foundation, http://lucene.apache.org/solr
BuildArch:     x86_64
Source0:       %{name}-%{version}.tar.gz
Requires(pre): shadow-utils

%description
HUBzero - Solr is an enterprise search server configured for HUBzero

Solr is the popular, blazing fast, open source NoSQL search platform
from the Apache Lucene project. Its major features include powerful
full-text search, hit highlighting, faceted search and analytics,
rich document parsing, geospatial search, extensive REST APIs as well
as parallel SQL. Solr is enterprise grade, secure and highly scalable,
providing fault tolerant distributed search and indexing, and powers
the search and navigation features of many of the world's largest
internet sites.

This version has been customized for use in the HUBzero environment.


%prep
%setup -q -n %{name}-%{version}

%build
        make

%install
        rm -rf $RPM_BUILD_ROOT
        make --makefile=/home/abuild/rpmbuild/SOURCES/Makefile install DESTDIR=$RPM_BUILD_ROOT

%pre
        getent group hubzero-solr >/dev/null || groupadd -r hubzero-solr
        getent passwd hubzero-solr >/dev/null || \
                useradd -r -g hubzero-solr -d /srv/hubzero-solr -s /bin/bash \
                -c "HUBzero Solr Search Service Account" hubzero-solr

%post
        SOLR_ARCHIVE=solr-6.1.0.tgz
        SOLR_DIR=solr-6.1.0
        SOLR_EXTRACT_DIR=/usr/share/hubzero-solr
        SOLR_INSTALL_DIR="${SOLR_EXTRACT_DIR}/${SOLR_DIR}"
        SOLR_SERVICE=hubzero-solr
        SOLR_BASENAME=solr
        SOLR_USER=hubzero-solr
        SOLR_VAR_DIR=/srv/hubzero-solr
        SOLR_PORT=8444

        mkdir -p "${SOLR_VAR_DIR}"
        chmod 0750 "${SOLR_VAR_DIR}"
        chown "${SOLR_USER}:" "${SOLR_VAR_DIR}"

        mkdir -p "${SOLR_VAR_DIR}/data"
        chmod 0750 "${SOLR_VAR_DIR}/data"
        chown "${SOLR_USER}:" "${SOLR_VAR_DIR}/data"

        mkdir -p "${SOLR_VAR_DIR}/logs"
        chmod 0750 "${SOLR_VAR_DIR}/logs"
        chown "${SOLR_USER}:" "${SOLR_VAR_DIR}/logs"

        cp "${SOLR_INSTALL_DIR}/server/solr/solr.xml" "${SOLR_VAR_DIR}/data/solr.xml"
        chmod 0640  "${SOLR_VAR_DIR}/data/solr.xml"
        chown "${SOLR_USER}:" "${SOLR_VAR_DIR}/data/solr.xml"

        cp "${SOLR_INSTALL_DIR}/server/resources/log4j.properties" "${SOLR_VAR_DIR}/log4j.properties"
        chmod 0640 "${SOLR_VAR_DIR}/log4j.properties"
        chown "${SOLR_USER}:" "${SOLR_VAR_DIR}/log4j.properties"

        cp -r "${SOLR_INSTALL_DIR}/hubzero-solr-core" "${SOLR_VAR_DIR}/data"
        chown -R "${SOLR_USER}:" "${SOLR_VAR_DIR}/data/hubzero-solr-core"
        chmod o-rwx "${SOLR_VAR_DIR}/data/hubzero-solr-core"

        if [ "$1" -eq "1" ]; then
                /sbin/chkconfig --add hubzero-solr
        fi


%preun
        if [ "$1" = "0" ] ; then
                service hubzero-solr stop > /dev/null 2>&1 ||:
                /sbin/chkconfig --del hubzero-solr
        fi


%postun
        if [ "$1" -ge 1 ]; then
                service hubzero-solr restart > /dev/null 2>&1 ||:
        fi 

%clean
        rm -rf $RPM_BUILD_ROOT
        make clean

%files
%defattr(-,root,root,-)
/usr/share/hubzero-solr
/usr/lib/hubzero-solr
/etc/init.d/hubzero-solr
/etc/default/hubzero-solr.in.sh

%doc copyright

%changelog
