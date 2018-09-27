FROM ufoym/deepo:all-jupyter-py36

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        xvfb python-opengl openjdk-8-jdk && \
    pip install gym spellsource && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8888

CMD xvfb-run -s "-screen 0 1400x900x24" jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token="$TOKEN" --notebook-dir='/notebook'
