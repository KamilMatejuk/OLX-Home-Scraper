FROM huggingface/transformers-pytorch-gpu

WORKDIR /app

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION python

RUN python3 -m pip install selenium
RUN python3 -m pip install sentencepiece