import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox 

class Interface:
    def __init__(self, root, controlador):
        self.root = root
        self.root.title("Mini Paint")
        self.controlador = controlador

        self.painel = tk.Frame(self.root)  
        self.painel.pack(pady=5)

        tk.Label(self.painel, text="Ferramenta:").grid(row=0, column=0, padx=5, pady=5)

        self.cb_ferramenta = ttk.Combobox(
            self.painel, 
            values=["Selecionar", "Linha", "Retângulo", "Oval", "Polígono", "Mão livre"], 
            state="readonly"
        )
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

        self.btn_selecionar = tk.Button(self.painel, text="Selecionar", command=self.selecionar_ferramenta_selecao)
        self.btn_selecionar.grid(row=0, column=6, padx=5, pady=5)

        self.btn_apagar = ttk.Button(self.painel, text="Apagar", command=self.controlador.apagar_selecionados)
        self.btn_apagar.grid(row=0, column=7, padx=5, pady=5)

        self.canvas = tk.Canvas(self.root, bg='white', width=600, height=600)
        self.canvas.pack()
        self.canvas.bind('<ButtonPress-1>', self.controlador.inicia_desenho) 
        self.canvas.bind('<B1-Motion>', self.controlador.atualiza_desenho)
        self.canvas.bind('<ButtonRelease-1>', self.controlador.finaliza_desenho)
        self.canvas.bind('<ButtonPress-3>', self.controlador.encerra_poligono) 

        self.root.bind("<Delete>", self.controlador.apagar_selecionados)
        self.root.bind("<BackSpace>", self.controlador.apagar_selecionados)
        self.root.bind("<Control-z>", self.controlador.undo)
        self.root.bind("<Control-Z>", self.controlador.undo)
        self.root.bind("<Control-y>", self.controlador.redo)
        self.root.bind("<Control-Y>", self.controlador.redo)
        
    def selecionar_ferramenta_selecao(self):
        self.cb_ferramenta.set("Selecionar")
        self.controlador.mudar_ferramenta("Selecionar")
    
    def escolher_borda(self):
        cor = colorchooser.askcolor(title="Cor da Borda")[1]
        if cor: self.controlador.atualizar_cor_borda(cor)

    def escolher_preenchimento(self):
        cor = colorchooser.askcolor(title="Cor do Preenchimento")[1]
        if cor: self.controlador.atualizar_cor_preenchimento(cor)

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
                self.controlador.figuras_selecionadas.clear()
                self.controlador.pilha_undo.clear()
                self.controlador.pilha_redo.clear()
                self.controlador.redesenhar_canvas()
                messagebox.showinfo("Sucesso", "Desenho carregado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao abrir: {e}")