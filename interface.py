import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import numpy as np
from PIL import Image, ImageTk  

# Valores padrões definidos para as coordenadas:
X_MIN_DEFAULT, X_MAX_DEFAULT = -2.0, 1.0
Y_MIN_DEFAULT, Y_MAX_DEFAULT = -1.5, 1.5

# Implementação da interface:
class Interface_Mandelbrot:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Fractal de Mandelbrot")
        self.janela.rowconfigure(0, weight=1)
        self.janela.columnconfigure(0, weight=1)
        self.zoom_inicial_x = 0
        self.zoom_inicial_y = 0
        self.id_retangulo = None
        self.id_redimensionar = None

        try:
            # tenta carregar a biblioteca compartilhada (se for Linux):
            self.mandelbrot_lib = ctypes.CDLL('./mandelbrot.so')
        except OSError:
            try:
                # tenta carregar a biblioteca compartilhada (se for Windows):
                self.mandelbrot_lib = ctypes.CDLL('./mandelbrot.dll')
            except OSError:
                 messagebox.showerror("Erro", "A biblioteca C não foi carregada corretamente.")
                 self.janela.destroy()
                 return

        self.mandelbrot_lib.mandelbrot.argtypes = [
            ctypes.c_int, ctypes.c_int, ctypes.c_int,
            ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
            np.ctypeslib.ndpointer(dtype=np.int32, flags="C_CONTIGUOUS")
        ]

        self.inicializa_UI()
        self.modifica_zoom()
        self.desenho.bind("<Configure>", self.redimensionando)

    # Cria e organiza os elementos da interface:
    def inicializa_UI(self):
        main_frame = ttk.Frame(self.janela, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        parametros_frame = ttk.LabelFrame(main_frame)
        parametros_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ttk.Label(parametros_frame, text="Largura:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.var_largura = tk.StringVar(value="800")
        ttk.Entry(parametros_frame, textvariable=self.var_largura).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(parametros_frame, text="Altura:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.var_altura = tk.StringVar(value="600")
        ttk.Entry(parametros_frame, textvariable=self.var_altura).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(parametros_frame, text="Max Iterações:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.var_max_iter = tk.StringVar(value="100")
        ttk.Entry(parametros_frame, textvariable=self.var_max_iter).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(parametros_frame, text="X Min:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.var_x_min = tk.StringVar(value=str(X_MIN_DEFAULT))
        ttk.Entry(parametros_frame, textvariable=self.var_x_min).grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(parametros_frame, text="X Max:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.var_x_max = tk.StringVar(value=str(X_MAX_DEFAULT))
        ttk.Entry(parametros_frame, textvariable=self.var_x_max).grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(parametros_frame, text="Y Min:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        self.var_y_min = tk.StringVar(value=str(Y_MIN_DEFAULT))
        ttk.Entry(parametros_frame, textvariable=self.var_y_min).grid(row=5, column=1, sticky=tk.W, padx=5, pady=2)

        ttk.Label(parametros_frame, text="Y Max:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=2)
        self.var_y_max = tk.StringVar(value=str(Y_MAX_DEFAULT))
        ttk.Entry(parametros_frame, textvariable=self.var_y_max).grid(row=6, column=1, sticky=tk.W, padx=5, pady=2)
        
        botoes_frame = ttk.Frame(parametros_frame)
        botoes_frame.grid(row=7, column=0, columnspan=2, pady=10)

        botao_gerar = ttk.Button(botoes_frame, text="Gerar Fractal", command=self.gerar_fractal)
        botao_gerar.pack(side=tk.LEFT, padx=5)

        botao_reset = ttk.Button(botoes_frame, text="Resetar Zoom", command=self.resetar)
        botao_reset.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(parametros_frame, text="Clique e arraste para dar zoom!", font=("", 8, "italic")).grid(row=8, column=0, columnspan=2)

        desenho_frame = ttk.LabelFrame(main_frame)
        desenho_frame.grid(row=0, column=1, padx=5, pady=5, rowspan=2, sticky="nsew")
        
        self.desenho = tk.Canvas(desenho_frame, width=800, height=600, bg="black", cursor="crosshair")
        self.desenho.pack(fill=tk.BOTH, expand=True)

        self.janela.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

    # Chama as funções necessárias para modificar o zoom:
    def modifica_zoom(self):
        self.desenho.bind("<ButtonPress-1>", self.clica_mouse)
        self.desenho.bind("<B1-Motion>", self.arrasta_mouse)
        self.desenho.bind("<ButtonRelease-1>", self.solta_mouse)

    # Guarda a posição inicial do novo retângulo (zoom)
    def clica_mouse(self, evento):
        self.zoom_inicial_x = evento.x
        self.zoom_inicial_y = evento.y
        self.id_retangulo = self.desenho.create_rectangle(
            self.zoom_inicial_x, self.zoom_inicial_y,
            self.zoom_inicial_x, self.zoom_inicial_y,
            outline='white', dash=(4, 4)
        )

    # Atualiza as dimensões do retângulo selecionado
    def arrasta_mouse(self, evento):
        if self.id_retangulo:
            self.desenho.coords(self.id_retangulo, self.zoom_inicial_x, self.zoom_inicial_y, evento.x, evento.y)

    # Gera um novo fractal de acordo com a área selecionada no zoom
    def solta_mouse(self, evento):
        if self.id_retangulo:
            self.desenho.delete(self.id_retangulo)
            self.id_retangulo = None

            x1, y1 = self.zoom_inicial_x, self.zoom_inicial_y
            x2, y2 = evento.x, evento.y

            # faz com que o zoom funcione para qualquer direção arrastada
            if x1 > x2: x1, x2 = x2, x1
            if y1 > y2: y1, y2 = y2, y1
        
            # não faz nada em caso de clique
            if (x2 - x1) < 5 or (y2 - y1) < 5:
                return
        
            # valores necessários para o cálculo das novas coordenadas:
            x_min_antigo = float(self.var_x_min.get())
            x_max_antigo = float(self.var_x_max.get())
            y_min_antigo = float(self.var_y_min.get())
            y_max_antigo = float(self.var_y_max.get())
            intervalo_x = x_max_antigo - x_min_antigo
            intervalo_y = y_max_antigo - y_min_antigo
            largura_desenho = self.desenho.winfo_width()
            altura_desenho = self.desenho.winfo_height()

            # calcula as novas coordenadas proporcionalmente
            x_min_novo = x_min_antigo + (x1 / largura_desenho) * intervalo_x
            x_max_novo = x_min_antigo + (x2 / largura_desenho) * intervalo_x
            y_max_novo = y_max_antigo - (y1 / altura_desenho) * intervalo_y
            y_min_novo = y_max_antigo - (y2 / altura_desenho) * intervalo_y

            # atualiza as coordenadas na interface
            self.var_x_min.set(f"{x_min_novo:.16f}")
            self.var_x_max.set(f"{x_max_novo:.16f}")
            self.var_y_min.set(f"{y_min_novo:.16f}")
            self.var_y_max.set(f"{y_max_novo:.16f}")
            
            self.gerar_fractal()

    # Espera o usuário terminar de redimensionar a janela
    def redimensionando(self, evento):
        if self.id_redimensionar:
            self.janela.after_cancel(self.id_redimensionar)
        self.id_redimensionar = self.janela.after(300, lambda: self.redimensionar(evento))

    # Atualiza o tamanho real e gera o novo fractal corretamente
    def redimensionar(self, evento):
        try: # ignora o redimensionamento ao abrir a janela 
            largura_atual = int(self.var_largura.get())
            altura_atual = int(self.var_altura.get())
            if (evento.width, evento.height) in [(800, 600), (804, 604)]:
                self.gerar_fractal()
                return
            if evento.width == largura_atual and evento.height == altura_atual:
                return
        except ValueError:
            pass
        self.var_largura.set(str(evento.width))
        self.var_altura.set(str(evento.height))
        self.gerar_fractal()

    # Retorna ao fractal inicial (Valores padrões)
    def resetar(self):
        self.var_x_min.set(str(X_MIN_DEFAULT))
        self.var_x_max.set(str(X_MAX_DEFAULT))
        self.var_y_min.set(str(Y_MIN_DEFAULT))
        self.var_y_max.set(str(Y_MAX_DEFAULT))
        self.gerar_fractal()

    # Gera um novo fractal 
    def gerar_fractal(self):
        try:
            largura = self.desenho.winfo_width()
            altura = self.desenho.winfo_height()
            max_iter = int(self.var_max_iter.get())
            x_min = float(self.var_x_min.get())
            x_max = float(self.var_x_max.get())
            y_min = float(self.var_y_min.get())
            y_max = float(self.var_y_max.get())
        except ValueError: # caso algum dos valores inseridos não seja um valor numérico aceitável
            messagebox.showerror("Erro", "Os valores inseridos são inválidos.")
            return

        # cria uma array de tamanho igual ao número de pixels da imagem
        resultado= np.zeros(largura * altura, dtype=np.int32)

        # chama a função mandelbrot definida no código em C
        self.mandelbrot_lib.mandelbrot(
            largura, altura, max_iter,
            x_min, x_max, y_min, y_max,
            resultado
        )

        # transforma os resultados dos cálculos em uma imagem
        # cada pixel recebe uma cor na escala de cinza de acordo com o número de iterações
        # a biblioteca Pillow é usada para criar a imagem, que é convertida em um formato compatível com Tkinter 
        resultado = resultado.reshape((altura, largura))
        imagem_valores = np.uint8(255 * (resultado / max_iter))
        imagem = Image.fromarray(imagem_valores) 
        imagem_cor = imagem.convert("RGB")
        self.imagem_convertida = ImageTk.PhotoImage(image=imagem_cor)
        self.desenho.delete("all")
        self.desenho.create_image(0, 0, anchor=tk.NW, image=self.imagem_convertida)

# Abre a janela com o fractal inicial
if __name__ == "__main__":
    janela = tk.Tk()
    interface = Interface_Mandelbrot(janela)
    interface.gerar_fractal()
    janela.mainloop()