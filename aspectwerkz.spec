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

%define section devel

Summary:        AOP for Java
Name:           aspectwerkz
Version:        2.0
Release:        %mkrel 2.0.1
Epoch:          0
License:        BSD-style License
URL:            http://aspectwerkz.codehaus.org/
Group:          Development/Libraries/Java
Vendor:         JPackage Project
Distribution:   JPackage
Source0:        http://dist.codehaus.org/aspectwerkz/distributions/aspectwerkz-2.0.zip
Patch0:         aspectwerkz2-build_xml.patch
Patch1:         aspectwerkz2-script.patch
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  java-1.7.0-icedtea
BuildRequires:	junit
BuildRequires:  ant >= 0:1.6
BuildRequires:  java-devel 
BuildRequires:  asm
BuildRequires:  concurrent
BuildRequires:  dom4j
BuildRequires:  geronimo-j2ee-management-1.0-api
BuildRequires:  jarjar
BuildRequires:  javassist
BuildRequires:  jrexx
BuildRequires:  piccolo
BuildRequires:  qdox
BuildRequires:  gnu.trove
BuildRequires:  junitperf
Requires:  concurrent
Requires:  dom4j
Requires:  javassist
Requires:  jrexx
Requires:  piccolo
Requires:  qdox
Requires:  gnu.trove
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
AspectWerkz is a dynamic, lightweight and 
high-performant AOP/AOSD framework for Java. 
AspectWerkz utilizes runtime bytecode modification 
to weave your classes at runtime. It hooks in and 
weaves classes loaded by any class loader except 
the bootstrap class loader. It has a rich join 
point model. Aspects, advices and introductions 
are written in plain Java and your target classes 
can be regular POJOs. You have the possibility to 
add, remove and re-structure advices as well as 
swapping the implementation of your introductions at 
runtime. Your aspects can be defined using either an 
XML definition file or using Runtime Attributes. 


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation

%description javadoc
%{summary}.

%package manual
Summary:        Documents for %{name}
Group:          Development/Documentation

%description manual
%{summary}.

%package demo
Summary:        Samples for %{name}
Group:          Development/Documentation

%description demo
%{summary}.

%prep
%setup -q -n %{name}-%{version}
%remove_java_binaries
chmod +x bin/aspectwerkz

%patch0 -b .sav
%patch1 -b .sav

# FIXME Remove the BEA JRockit specific code or it will only build on BEA JDK
# org/codehaus/aspectwerkz/extension/jrockit/JRockitPreProcessor.class
rm -fr src/extensions/org/codehaus/aspectwerkz/extension/jrockit

%build
export ASPECTWERKZ_HOME=$RPM_BUILD_DIR/%{name}-%{version}
build-jar-repository -s -p lib \
jarjar \
asm/asm \
asm/asm-attrs \
asm/asm-util \
dom4j \
gnu.trove \
concurrent \
j2ee-management \
junit \
jrexx \
javassist \
qdox \
piccolo \
junitperf \

export JAVA_HOME=%{_jvmdir}/java-icedtea
ant test cleandist

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p target/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p target/%{name}-core-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-core-%{version}.jar
cp -p target/%{name}-extensions-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-extensions-%{version}.jar
cp -p target/%{name}-jdk14-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-jdk14-%{version}.jar
cp -p target/%{name}-nodeps-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-nodeps-%{version}.jar
cp -p target/%{name}-nodeps-jdk14-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-nodeps-jdk14-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp -p bin/aspectwerkz $RPM_BUILD_ROOT%{_bindir}


# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} 
rm -rf docs/apidocs

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/src
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/classes
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/bin
# FIXME Can only build samples with a JDK 5
#cp -pr target/samples-classes/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/classes
cp -pr src/samples/* $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/src

# manual
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr docs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -p LICENSE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
  rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}/LICENSE.txt
%{_javadir}/*.jar
%attr(755, root, root) %{_bindir}/aspectwerkz

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%doc %{_docdir}/%{name}-%{version}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}-%{version}
