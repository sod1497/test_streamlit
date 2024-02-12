FROM continuumio/miniconda3

RUN conda install python=3.11 -y

WORKDIR /app

COPY . ./

RUN conda install --file requirements.txt -y -c conda-forge

EXPOSE 8080

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
