/*
    Declara a função responsável por gerar o conjunto de Mandelbrot para
    uma região específica do plano complexo. O resultado é armazenado em
    um array de inteiros, onde cada valor representa o número de iterações
    até a divergência do ponto correspondente.
*/

#ifndef MANDELBROT_H
#define MANDELBROT_H

void mandelbrot(int largura, int altura, int max_iter, double x_min, double x_max, double y_min, double y_max, int *resultado) ;

#endif