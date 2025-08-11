# Fractal de Mandelbrot  
**Trabalho 2 de Conceitos de Linguagem de Programação**  
Eduarda Pereira Medeiros


A aplicação desenvolvida gera fractais de Mandelbrot e exibe-os na tela. Para implementar os cálculos necessários, um código na linguagem C foi elaborado, e para o desenvolvimento de uma interface com o usuário, a linguagem Python foi escolhida.

Os arquivos que compõem o repositório estão listados a seguir:
* `mandelbrot.h`: Arquivo de cabeçalho para o código C. Declara a assinatura da função principal, utilizada para calcular o conjunto de Mandelbrot.
* `mandelbrot.c`: Implementação em C da função que calcula os valores de cada pixel da imagem que forma o fractal.
* `interface.py`: Interface gráfica de usuário desenvolvida em Python com a biblioteca Tkinter. Permite que o usuário defina os próprios parâmetros para a geração do fractal e exibe a imagem resultante.
* `Makefile`: Arquivo utilizado para compilar o código C e executar o programa.
* `README.md`: Descrição do repositório.
* 

## Dependências:
* Python 3: Interpretador utilizado para executar a aplicação.
* PIP: Gerenciador de pacotes de Python utilizado para instalar as bibliotecas necessárias.
* gcc: Necessário para compilar o arquivo `mandelbrot.c` e gerar a bibilioteca compartilhada.
* Tkinter: Biblioteca Python utilizada para elaborar a interface gráfica.
     * Este módulo faz parte da biblioteca padrão do Python, mas se for necessário instalá-lo separadamente, utilize `sudo apt-get install python3-tk`.
* Numpy e Pillow: Bibiliotecas Python adicionais utilizadas na implementação da aplicação gráfica. Podem ser instaladas através do seguinte comando:
```bash
make install-deps
```

## Como compilar?
No Linux:
* A compilação do código C em uma biblioteca compartilhada (`.so`) é feita utilizando o `Makefile`. No terminal, basta executar o seguinte comando:
```bash
make
```  

No Windows:
* A compilação deve ser feita manualmente com o comando a seguir para gerar a biblioteca compartilhada:
```PowerShell
gcc -shared -o mandelbrot.dll mandelbrot.c -O2
```  

## Como executar?
No Linux:
```bash
make run
```  

No Windows:
```PowerShell
python interface.py
```
