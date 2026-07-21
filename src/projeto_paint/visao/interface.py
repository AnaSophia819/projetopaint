import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox 
<<<<<<< HEAD
=======
from modelo.figuras import Linha, Retangulo, Oval, Poligono, MaoLivre, FiguraComposta
>>>>>>> df66a714b4321b323c88a7689f7aa1f8cd9edebd

class Interface:
    def __init__(self, root, controlador):
        self.root = root
        self.root.title("Mini Paint")
        self.controlador = controlador

        self.painel = tk.Frame(self.root)  
        self.painel.pack(pady=5)
<<<<<<< HEAD

        tk.Label(self.painel, text="Ferramenta:").grid(row=0, column=0, padx=5, pady=5)

        self.cb_ferramenta = ttk.Combobox(
            self.painel, 
            values=["Selecionar", "Linha", "Retângulo", "Oval", "Polígono", "Mão livre"], 
            state="readonly"
        )
=======
        
        # --- LINHA 0: Ferramentas e Cores ---
        tk.Label(self.painel, text="Ferramenta:").grid(row=0, column=0, padx=5, pady=5)

        self.cb_ferramenta = ttk.Combobox(self.painel, values=["Selecionar", "Linha", "Retângulo", "Oval", "Polígono", "Mão livre"], state="readonly")
>>>>>>> df66a714b4321b323c88a7689f7aa1f8cd9edebd
        self.cb_ferramenta.set("Linha") 
        self.cb_ferramenta.grid(row=0, column=1, padx=5, pady=5)
        self.cb_ferramenta.bind("<<ComboboxSelected>>", lambda e: self.controlador.mudar_ferramenta(self.cb_ferramenta.get()))
        
        self.btn_borda = ttk.Button(self.painel, text="Cor da Borda", command=self.escolher_borda)
        self.btn_borda.grid(row=0, column=2, padx=5, pady=5)
        
        self.btn_fundo = ttk.Button(self.painel, text="Cor do Fundo", command=self.escolher_preenchimento)
        self.btn_fundo.grid(row=0, column=3, padx=5, pady=5)

        self.btn_salvar = ttk.Button(self.painel, text="Salvar", command=self.acao_salvar)
        self.btn_salvar.grid(row=0, column=4, padx=5, pady=5)
        
        self.btn_abrir = ttk.Button(self.painel, text="Abrir", command=self.acao_abrir)
        self.btn_abrir.grid(row=0, column=5, padx=5, pady=5)

<<<<<<< HEAD
        self.btn_selecionar = tk.Button(self.painel, text="Selecionar", command=self.selecionar_ferramenta_selecao)
        self.btn_selecionar.grid(row=0, column=6, padx=5, pady=5)
=======
        # --- LINHA 1: Controles de Seleção e Composite (Entrega 5 e 6) ---
        self.btn_selecionar = tk.Button(self.painel, text="Selecionar", command= lambda: self.controlador.mudar_ferramenta("Selecionar"))
        self.btn_selecionar.grid(row=1, column=1, padx=5, pady=5)

        self.btn_apagar = ttk.Button(self.painel, text="Apagar", command=self.controlador.apagar_selecionados)
        self.btn_apagar.grid(row=1, column=2, padx=5, pady=5)

        self.btn_frente = ttk.Button(self.painel, text="Trazer p/ Frente", command=self.controlador.trazer_para_frente)
        self.btn_frente.grid(row=1, column=3, padx=5, pady=5)

        self.btn_tras = ttk.Button(self.painel, text="Enviar p/ Trás", command=self.controlador.enviar_para_tras)
        self.btn_tras.grid(row=1, column=4, padx=5, pady=5)

        # ADICIONADO: Botões de Agrupar e Desagrupar (Entrega 6)
        self.btn_agrupar = ttk.Button(self.painel, text="Agrupar", command=self.controlador.agrupar_selecionadas)
        self.btn_agrupar.grid(row=1, column=5, padx=5, pady=5)

        self.btn_desagrupar = ttk.Button(self.painel, text="Desagrupar", command=self.controlador.desagrupar_selecionadas)
        self.btn_desagrupar.grid(row=1, column=6, padx=5, pady=5)
>>>>>>> df66a714b4321b323c88a7689f7aa1f8cd9edebd

        self.btn_apagar = ttk.Button(self.painel, text="Apagar", command=self.controlador.apagar_selecionados)
        self.btn_apagar.grid(row=0, column=7, padx=5, pady=5)

        self.canvas = tk.Canvas(self.root, bg='white', width=600, height=600)
        self.canvas.pack()
        
        # Binds do Mouse
        self.canvas.bind('<ButtonPress-1>', self.controlador.inicia_desenho) 
        self.canvas.bind('<B1-Motion>', self.controlador.atualiza_desenho)
        self.canvas.bind('<ButtonRelease-1>', self.controlador.finaliza_desenho)
        self.canvas.bind('<ButtonPress-3>', self.controlador.encerra_poligono) 
<<<<<<< HEAD

        self.root.bind("<Delete>", self.controlador.apagar_selecionados)
        self.root.bind("<BackSpace>", self.controlador.apagar_selecionados)
        self.root.bind("<Control-z>", self.controlador.undo)
        self.root.bind("<Control-Z>", self.controlador.undo)
        self.root.bind("<Control-y>", self.controlador.redo)
        self.root.bind("<Control-Y>", self.controlador.redo)
        
    def selecionar_ferramenta_selecao(self):
        self.cb_ferramenta.set("Selecionar")
        self.controlador.mudar_ferramenta("Selecionar")
    
=======
        
        # Binds do Teclado 
        self.root.bind("<Delete>", self.controlador.apagar_selecionados)
        self.root.bind("<BackSpace>", self.controlador.apagar_selecionados)
        self.root.bind("<Control-c>", self.controlador.copiar_selecionados)
        self.root.bind("<Control-v>", self.controlador.colar_copiados)
        self.root.bind("<Control-g>", self.controlador.agrupar_selecionadas) # Atalho para Agrupar
        self.root.bind("<Control-u>", self.controlador.desagrupar_selecionadas) # Atalho para Desagrupar
  
    # Abre a janela de cor e manda o resultado pro controlador
>>>>>>> df66a714b4321b323c88a7689f7aa1f8cd9edebd
    def escolher_borda(self):
        cor = colorchooser.askcolor(title="Cor da Borda")[1]
        if cor: self.controlador.atualizar_cor_borda(cor)

    def escolher_preenchimento(self):
        cor = colorchooser.askcolor(title="Cor do Preenchimento")[1]
        if cor: self.controlador.atualizar_cor_preenchimento(cor)

<<<<<<< HEAD
=======
    # O MÉTODO QUE FALTAVA: A Visão desenha as figuras usando as ferramentas do Tkinter
    def renderizar_figura(self, figura, tag="temporario"):
        # ADICIONADO: Se for um grupo, manda desenhar cada filho recursivamente! (Padrão Composite)
        if isinstance(figura, FiguraComposta):
            for filho in figura.filhos:
                self.renderizar_figura(filho, tag)
            return # Sai da função, pois a caixa em si é invisível, só os filhos aparecem

        id_tk = None
        if isinstance(figura, Linha):
            id_tk = self.canvas.create_line(figura.x1, figura.y1, figura.x2, figura.y2, fill=figura.cor_borda, tags=tag)
        elif isinstance(figura, Retangulo):
            id_tk = self.canvas.create_rectangle(figura.x1, figura.y1, figura.x2, figura.y2, outline=figura.cor_borda, fill=figura.cor_preenchimento, tags=tag)
        elif isinstance(figura, Oval):
            id_tk = self.canvas.create_oval(figura.x1, figura.y1, figura.x2, figura.y2, outline=figura.cor_borda, fill=figura.cor_preenchimento, tags=tag)
        elif isinstance(figura, Poligono):
            id_tk = self.canvas.create_polygon(figura.coordenadas, outline=figura.cor_borda, fill=figura.cor_preenchimento, tags=tag)
        elif isinstance(figura, MaoLivre):
            id_tk = self.canvas.create_line(figura.coordenadas, fill=figura.cor_borda, tags=tag)
        
        # Guarda o ID gerado pelo Tkinter direto na figura
        if id_tk is not None:
            figura.id_tk = id_tk

    #  COMUNICAÇÃO DO JSON COM A TELA
>>>>>>> df66a714b4321b323c88a7689f7aa1f8cd9edebd
    def acao_salvar(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os Arquivos", "*.*")],
            title="Salvar Desenho"
        )
        if caminho:
            try:
                self.controlador.modelo_desenho.salvar_json(caminho)
                messagebox.showinfo("Sucesso", "Desenho salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao salvar: {e}")

    def acao_abrir(self):
        caminho = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os Arquivos", "*.*")],
            title="Abrir Desenho"
        )
        if caminho:
            try:
                self.controlador.modelo_desenho.abrir_json(caminho)
<<<<<<< HEAD
                self.controlador.figuras_selecionadas.clear()
                self.controlador.pilha_undo.clear()
                self.controlador.pilha_redo.clear()
                self.controlador.redesenhar_canvas()
=======
                self.canvas.delete("all") 
                
                # Manda a VISÃO desenhar as figuras que foram carregadas
                for figura in self.controlador.modelo_desenho.figuras:
                    self.renderizar_figura(figura, tag="figura_definitiva")
                    
>>>>>>> df66a714b4321b323c88a7689f7aa1f8cd9edebd
                messagebox.showinfo("Sucesso", "Desenho carregado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao abrir: {e}")