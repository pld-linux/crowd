# NOTE:
# Do not remove NoSource tags. Make sure DistFiles won't fetch Crowd sources.
#
# Todd Revolt from Atlassian told that:
#   * We are free to integrate Atlassian products into PLD. So we can write
#     installer scripts, create nosrc packages etc.
#   * We are not permitted to redistribute their products. That mean during
#     installation each user has to download Crowd from atlassian web page.
#
# See Atlassian_EULA_3.0.pdf for more details.

%if 0
# Download sources manually:
wget -c http://downloads.atlassian.com/software/crowd/downloads/atlassian-crowd-2.0.4-war.zip
wget -c http://www.atlassian.com/about/licensing/Atlassian_EULA_3.0.pdf
wget -c http://repository.atlassian.com/org.apache.felix/jars/org.apache.felix.main-2.0.5.jar
%endif

%include	/usr/lib/rpm/macros.java

Summary:	SSO server
Name:		crowd
Version:	2.0.4
Release:	0.1
License:	Proprietary, not distributable
Group:		Networking/Daemons/Java/Servlets
Source0:	atlassian-%{name}-%{version}-war.zip
# NoSource0-md5:	be0c6d073297fb040c5c29550463252b
NoSource:	0
Source1:	Atlassian_EULA_3.0.pdf
# NoSource1-md5:	9e87088024e3c5ee2e63a72a3e99a6cb
NoSource:	1
Source2:	tomcat-context.xml
Source3:	%{name}-init.properties
Source4:	org.apache.felix.main-2.0.5.jar
# NoSource4-md5:	edfbdb9fd59aeb21022391e2934f75c0
NoSource:	4
URL:		http://www.atlassian.com/software/crowd/default.jsp
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	unzip
Requires:	java-jta
# According to crowd documentation, jre is not enough.
Requires:	jdk
Requires:	jpackage-utils
Requires:	tomcat >= 0:6.0.20-4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Crowd is a single sign-on (SSO) application for as many users, web
applications and directory servers you need — all through a single web
interface.

%prep
%setup -q -c

cp %{SOURCE1} .

# http://confluence.atlassian.com/pages/viewpage.action?pageId=208962752
find -name 'org.apache.felix.main*.jar' | xargs rm
cp %{SOURCE4} WEB-INF/lib

# TODO set paths for logs
# sed -i 's,^\(log4j\.appender\.[a-z]*\.File\)=\(.*\)$,\1=/var/log/crowd/\2,' webapp/WEB-INF/classes/log4j.properties

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a console index.jsp META-INF template WEB-INF $RPM_BUILD_ROOT%{_datadir}/%{name}

# configuration
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_sharedstatedir}/tomcat/conf/Catalina/localhost}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tomcat-context.xml
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/crowd-init.properties
ln -s %{_sysconfdir}/%{name}/tomcat-context.xml $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/%{name}.xml
mv $RPM_BUILD_ROOT%{_datadir}/crowd/WEB-INF/classes/log4j.properties $RPM_BUILD_ROOT%{_sysconfdir}/crowd/log4j.properties
ln -sf %{_sysconfdir}/crowd/log4j.properties $RPM_BUILD_ROOT%{_datadir}/crowd/WEB-INF/classes/log4j.properties
ln -sf %{_sysconfdir}/crowd/crowd-init.properties $RPM_BUILD_ROOT%{_datadir}/crowd/WEB-INF/classes/crowd-init.properties

# additional libs
ln -s %{_datadir}/java/jta.jar $RPM_BUILD_ROOT%{_datadir}/crowd/WEB-INF/lib/jta.jar

install -d $RPM_BUILD_ROOT{%{_sharedstatedir}/%{name},/var/log/%{name}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc licenses Atlassian_EULA_3.0.pdf
%{_datadir}/%{name}
%dir %attr(750,root,tomcat) %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,tomcat) %{_sysconfdir}/%{name}/*
%{_sharedstatedir}/tomcat/conf/Catalina/localhost/%{name}.xml
%attr(2775,root,servlet) %dir %{_sharedstatedir}/%{name}
%attr(2775,root,servlet) %dir /var/log/%{name}
