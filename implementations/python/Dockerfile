ARG DEBIAN_NAME=stretch
FROM python:3.7-${DEBIAN_NAME}

ENV APP_HOME /app
ENV PATH="/root/.pyenv/bin:$PATH"
RUN pip install tox
RUN touch /root/.bashrc \
    && echo 'eval "$(pyenv init -)"' >> /root/.bashrc \
    && echo 'eval "$(pyenv virtualenv-init -)"' >> /root/.bashrc

RUN bash -c "pyenv install 3.5 && pyenv install 3.6.11 && pyenv install 3.7.6 && pyenv install 3.8.1"
RUN pyenv local 3.5 3.6.11 3.7.6 3.8.1

WORKDIR ${APP_HOME}
