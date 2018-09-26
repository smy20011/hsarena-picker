FROM ufoym/deepo:all-jupyter-py36

RUN pip install gym

EXPOSE 8888

CMD jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token= --notebook-dir='/notebook'
