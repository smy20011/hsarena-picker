FROM ufoym/deepo:all-jupyter-py36

# Install openai-gym and virtual buffer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        xvfb python-opengl openjdk-8-jdk && \
    pip install gym && \
    rm -rf /var/lib/apt/lists/*

# Install spell source, build from source.
COPY Spellsource-Server/ /spellsource

ENV LANG C.UTF-8
RUN cd /spellsource && \
    pip install setuptools wheel && \
    python3 setup.py sdist bdist_wheel && \
    pip install dist/*.whl && \
    rm -rf /spellsource


EXPOSE 8888

CMD xvfb-run -s "-screen 0 1400x900x24" jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token="$TOKEN" --notebook-dir='/notebook'
