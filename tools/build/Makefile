# @package      hubzero-solr
# @file         Makefile
# @author       Nicholas J. Kisseberth <nkissebe@purdue.edu>
# @copyright    Copyright (c) 2016 HUBzero Foundation, LLC.
# @license      http://opensource.org/licenses/MIT MIT
#
# Copyright (c) 2016 HUBzero Foundation, LLC.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# HUBzero is a registered trademark of HUBzero Foundation, LLC.
#

SOLR_ARCHIVE=${RPM_SOURCE_DIR}/solr-6.1.0.tgz
SOLR_DIR=solr-6.1.0
SOLR_EXTRACT_DIR=/usr/share/hubzero-solr
SOLR_INSTALL_DIR="${SOLR_EXTRACT_DIR}/${SOLR_DIR}"
USRBIN="${DESTDIR}/usr/bin"
SOLR_SERVICE=hubzero-solr
SOLR_BASENAME=solr
SOLR_USER=hubzero-solr
SOLR_VAR_DIR=/srv/hubzero-solr
SOLR_PORT=8445

JAVA_ARCHIVE=${RPM_SOURCE_DIR}/server-jre-8u102-linux-x64.tar.gz
JAVA_DIR=jdk1.8.0_102
JAVA_EXTRACT_DIR=/usr/lib/hubzero-solr
JAVA_INSTALL_DIR="${JAVA_EXTRACT_DIR}/${JAVA_DIR}"
JAVA_BASENAME=jdk

all:
	@true

install:
	@# extract
	@echo "Extracting ${SOLR_ARCHIVE} to ${DESTDIR}/${SOLR_EXTRACT_DIR}"
	mkdir -p ${DESTDIR}/${SOLR_INSTALL_DIR}
	mkdir -p ${USRBIN}
	tar zxf "${SOLR_ARCHIVE}" -C "${DESTDIR}/${SOLR_EXTRACT_DIR}"
	mkdir -p "${DESTDIR}/${JAVA_INSTALL_DIR}"
	tar zxf "${JAVA_ARCHIVE}" -C "${DESTDIR}/${JAVA_EXTRACT_DIR}"
	find "${DESTDIR}/${SOLR_INSTALL_DIR}" -type d -print0 | xargs -0 chmod 0755
	find "${DESTDIR}/${SOLR_INSTALL_DIR}" -type f -print0 | xargs -0 chmod 0644
	chmod -R 0755 "${DESTDIR}/${SOLR_INSTALL_DIR}/bin"
	install --mode 0755 hzsolrindex ${USRBIN}/hzsolrindex
	install --mode 0755 -D cron-hzsolrindex ${DESTDIR}/etc/cron.d/cron-hzsolrindex

	@# create a symlink for easier scripting
	@echo "Installing symlink ${DESTDIR}/${SOLR_EXTRACT_DIR}/${SOLR_BASENAME} -> ${DESTDIR}/${SOLR_INSTALL_DIR} ..."
	ln -s "${SOLR_INSTALL_DIR}" "${DESTDIR}/${SOLR_EXTRACT_DIR}/${SOLR_BASENAME}"
	ln -s "${JAVA_INSTALL_DIR}" "${DESTDIR}/${JAVA_EXTRACT_DIR}/${JAVA_BASENAME}"
	
	@# install init.d script
	@echo "Installing ${DESTDIR}/etc/init.d/${SOLR_SERVICE} script ..."
	mkdir -p "${DESTDIR}/etc/init.d"
	chmod 0755 "${DESTDIR}/etc/init.d"
	cp -p "${DESTDIR}/${SOLR_INSTALL_DIR}/bin/init.d/solr" "${DESTDIR}/etc/init.d/${SOLR_SERVICE}"
	chmod 0755 "${DESTDIR}/etc/init.d/${SOLR_SERVICE}"
	@# do some basic variable substitution on the init.d script
	sed -i -e "s#SOLR_INSTALL_DIR=.*#SOLR_INSTALL_DIR=\"${SOLR_EXTRACT_DIR}/${SOLR_BASENAME}\"#" "${DESTDIR}/etc/init.d/${SOLR_SERVICE}"
	sed -i -e "s#SOLR_ENV=.*#SOLR_ENV=\"/etc/default/${SOLR_SERVICE}.in.sh\"#" "${DESTDIR}/etc/init.d/${SOLR_SERVICE}"
	sed -i -e "s#RUNAS=.*#RUNAS=\"${SOLR_USER}\"#" "${DESTDIR}/etc/init.d/${SOLR_SERVICE}"
	sed -i -e "s#Provides:.*#Provides: ${SOLR_SERVICE}#" "${DESTDIR}/etc/init.d/${SOLR_SERVICE}"
	@# user does not have a shell, run the init script 
	sed -i -e "s/su -c/su -s \/bin\/sh -c/g" "${DESTDIR}/etc/init.d/${SOLR_SERVICE}"

	@echo "Installing ${DESTDIR}/etc/default/${SOLR_SERVICE}.in.sh ..."
	@# install/move configuration
	mkdir -p "${DESTDIR}/etc/default"
	chmod 0755 "${DESTDIR}/etc/default"
	cp -p "${DESTDIR}/${SOLR_INSTALL_DIR}/bin/solr.in.sh" "${DESTDIR}/etc/default/${SOLR_SERVICE}.in.sh"
	echo "SOLR_PID_DIR=\"${SOLR_VAR_DIR}\"" >> "${DESTDIR}/etc/default/${SOLR_SERVICE}.in.sh"
	echo "SOLR_HOME=\"${SOLR_VAR_DIR}/data\""  >> "${DESTDIR}/etc/default/${SOLR_SERVICE}.in.sh"
	echo "LOG4J_PROPS=\"${SOLR_VAR_DIR}/log4j.properties\""  >> "${DESTDIR}/etc/default/${SOLR_SERVICE}.in.sh"
	echo "SOLR_LOGS_DIR=\"${SOLR_VAR_DIR}/logs\""  >> "${DESTDIR}/etc/default/${SOLR_SERVICE}.in.sh"
	echo "SOLR_PORT=\"${SOLR_PORT}\""  >> "${DESTDIR}/etc/default/${SOLR_SERVICE}.in.sh"
	echo "SOLR_JAVA_HOME=\"${JAVA_EXTRACT_DIR}/${JAVA_BASENAME}\"" >> "${DESTDIR}/etc/default/${SOLR_SERVICE}.in.sh"
	echo "SOLR_HOST=\"localhost\""  >> "${DESTDIR}/etc/default/${SOLR_SERVICE}.in.sh"

	chmod 0644 "${DESTDIR}/etc/default/${SOLR_SERVICE}.in.sh"

	sed -i -e "s#solr.log=.*#solr.log=\$${solr.solr.home}/../logs#" "${DESTDIR}/${SOLR_INSTALL_DIR}/server/resources/log4j.properties"

	cp -r hubzero-solr-core "${DESTDIR}/${SOLR_INSTALL_DIR}"
	mkdir "${DESTDIR}/${SOLR_INSTALL_DIR}/hubzero-solr-core/lib"
	find "${DESTDIR}/${SOLR_INSTALL_DIR}/hubzero-solr-core" -type d -print0 | xargs -0 chmod 0750
	find "${DESTDIR}/${SOLR_INSTALL_DIR}/hubzero-solr-core" -type f -print0 | xargs -0 chmod 0640

uninstall:
	@true

postinst:
	adduser --system --shell /bin/false --group --disabled-password --home "$SOLR_VAR_DIR" "$SOLR_USER"
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
 
	update-rc.d "${SOLR_SERVICE}" defaults
	service "${SOLR_SERVICE}" start
	sleep 5
	service "${SOLR_SERVICE}" status
	@echo "Service ${SOLR_SERVICE} installed."

clean:
	@true

.PHONY: all install uninstall postinst clean
