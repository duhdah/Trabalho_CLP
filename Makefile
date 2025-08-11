# Comandos disponíveis no Makefile:
# make: compila o código em C em uma biblioteca compartilhada
# make run: compila (se necessário) e executa a interface gráfica
# make clean: remove a biblioteca compilada (.so ou .dll)
# make install-deps: instala as bibliotecas Python necessárias (numpy, Pillow)

CC=gcc
CFLAGS=-fPIC -shared -O2
TARGET=mandelbrot.so
PYTHON=python3
PIP=pip3
SRCS=mandelbrot.c

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRCS)

run: all
	$(PYTHON) interface.py

install-deps:
	$(PIP) install numpy Pillow

clean:
	rm -f $(TARGET)

.PHONY: all run clean install-deps