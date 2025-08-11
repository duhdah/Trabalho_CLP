#include "mandelbrot.h"

/*
    -----------------
    Função mandelbrot
    -----------------

    A parte do trabalho que implementa um serviço de cálculo foi feita com a linguagem C.

    A implementação gera a representação numérica do conjunto de Mandelbrot para uma determinada região
    do plano complexo, armazenando o número de iterações de cada pixel até a divergência.

    Parâmetros:
      -> largura, altura: dimensões da imagem em pixels
      -> max_iter: número máximo de iterações (maior = mais detalhes, mais lento)
      -> x_min, x_max, y_min, y_max: limites da região no plano complexo
      -> resultado: array onde cada elemento corresponde ao número de iterações
      de um pixel até divergir

*/

void mandelbrot(int largura, int altura, int max_iter, double x_min, double x_max, double y_min, double y_max, int *resultado) {
    for (int lin = 0; lin < altura; lin++) {
        for (int col = 0; col < largura; col++) {
            int iter = 0;
            double c_real, c_imag, z_real, z_imag;
            c_real = x_min + (x_max - x_min) * col / (largura - 1);
            c_imag = y_max - (y_max - y_min) * lin / (altura - 1);
            z_real = 0;
            z_imag = 0;
            // se o módulo de z² for maior que 4, está fora do conjunto
            // se chegar até o número máximo de iterações sem estourar esse valor, pertence ao conjunto
            while (z_real * z_real + z_imag * z_imag < 4 && iter < max_iter) {
                double z_real_novo = z_real * z_real - z_imag * z_imag + c_real;
                z_imag = 2 * z_real * z_imag + c_imag;
                z_real = z_real_novo;
                iter++;
            }
            resultado[lin * largura + col] = iter;
        }
    }
}