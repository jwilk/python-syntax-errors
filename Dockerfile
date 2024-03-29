ARG image
FROM ${image}
RUN printf 'Apt::Install-Recommends "false";\n' | tee -a /etc/apt/apt.conf
RUN \
  if grep '"Ubuntu 1[0-3]' /etc/lsb-release; \
  then \
    sed -i 's,/archive[.]ubuntu[.]com/,/old-releases.ubuntu.com/,g' /etc/apt/sources.list; \
  fi
ARG pyver
RUN \
  if [ ${pyver} = 3.0 ] && grep -w lucid /etc/apt/sources.list; \
  then \
    sed -i 's/lucid/karmic/g' /etc/apt/sources.list; \
  fi
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN \
  if grep '"Ubuntu 2' /etc/os-release; \
  then \
    apt-get install -y software-properties-common && \
    apt-add-repository -y ppa:deadsnakes/ppa; \
  fi
RUN apt-get -o APT::Cmd::Pattern-Only=true install -y python${pyver}
COPY *.py /srv/
ENV PYTHON python${pyver}
CMD cd /srv \
  && ${PYTHON} -c 'import sys; print(sys.version)' \
  && ${PYTHON} test.py -v

# vim:ts=4 sts=4 sw=4 et
