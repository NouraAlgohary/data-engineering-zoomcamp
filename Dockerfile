# # Run python with bash as entrypoint
# FROM python:3.9

# RUN pip install pandas

# ENTRYPOINT ["bash"]

# # Run a python pipeline 
# FROM python:3.9

# RUN pip install pandas

# WORKDIR /app

# COPY pipeline.py pipeline.py

# ENTRYPOINT ["bash"]

# # Passing Argurments
FROM python:3.9

RUN pip install pandas

WORKDIR /app

COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]