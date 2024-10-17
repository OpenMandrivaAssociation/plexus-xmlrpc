# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'
%global with_maven %{!?_without_maven:1}%{?_without_maven:0}
%global without_maven %{?_without_maven:1}%{!?_without_maven:0}

%global parent plexus
%global subname xmlrpc

Name:           plexus-xmlrpc
Version:        1.0
Release:        0.5.b4.5
Summary:        Plexus XML RPC Component
License:        ASL 1.1 and MIT
Group:          Development/Java
URL:            https://plexus.codehaus.org/
# svn export svn://svn.plexus.codehaus.org/plexus/tags/plexus-xmlrpc-1.0-beta-4/
# tar czf plexus-xmlrpc-1.0-beta-4-src.tar.gz plexus-xmlrpc-1.0-beta-4/
Source0:        plexus-xmlrpc-1.0-beta-4-src.tar.gz
Source1:        %{name}-1.0-build.xml

Patch0:         %{name}-add-codec-dep.patch

BuildArch:      noarch

BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-nodeps
%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4-9
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-doxia
BuildRequires:  maven-doxia-sitetools
BuildRequires:  plexus-maven-plugin
%endif
BuildRequires:  classworlds >= 0:1.1
BuildRequires:  apache-commons-codec
BuildRequires:  plexus-container-default
BuildRequires:  plexus-utils
BuildRequires:  xmlrpc

Requires:  apache-commons-codec
Requires:  classworlds >= 0:1.1
Requires:  plexus-container-default
Requires:  plexus-utils
Requires:  xmlrpc

Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

%description
The Plexus project seeks to create end-to-end developer tools for
writing applications. At the core is the container, which can be
embedded or for a full scale application server. There are many
reusable components for hibernate, form processing, jndi, i18n,
velocity, etc. Plexus also includes an application server which
is like a J2EE application server, without all the baggage.


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.


%prep
%setup -q -n plexus-xmlrpc-1.0-beta-4
cp %{SOURCE1} build.xml

%patch0 -b .sav

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

%if %{with_maven}
    mvn-jpp \
        -e \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc
%else
mkdir -p target/lib
build-jar-repository -s -p target/lib \
classworlds \
commons-codec \
plexus/container-default \
plexus/utils \
xmlrpc \

ant jar javadoc
%endif

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -pm 644 target/plexus-xmlrpc-%{version}-beta-4.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/xmlrpc.jar
%add_to_maven_depmap org.codehaus.plexus plexus-xmlrpc 1.0-beta-4 JPP/plexus xmlrpc

#poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.plexus-xmlrpc.pom

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%doc LICENSE.txt
%{_mavendepmapfragdir}/plexus-xmlrpc


%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/*

