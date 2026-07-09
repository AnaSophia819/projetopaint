import tkinter as tk
from tkinter import ttk, colorchooser, filedialog, messagebox 
from modelo.figuras import Linha, Retangulo, Oval, Poligono, MaoLivre

# responsavel por toda a parte visual do paint cria a tela, botões. e repassa o que o usuario escolheu 
class Interface:
    def __init__(self, root, controlador):
        self.root = root
        self.root.title("Mini Paint")
        self.controlador = controlador
        self.painel = tk.Frame(self.root)  
        self.painel.pack(pady=5)
        tk.Label(self.painel, text="Ferramenta:").grid(row=0, column=0, padx=5, pady=5)

        # criando o combobox e iniciando a ferramenta linha para o usuario
        self.cb_ferramenta = ttk.Combobox(self.painel, values=["Linha", "Retângulo", "Oval", "Polígono", "Mão livre"], state="readonly")
        self.cb_ferramenta.set("Linha") 
        self.cb_ferramenta.grid(row=0, column=1, padx=5, pady=5)
        
        # aqui serve para passar a informação para o controlador do que o usuario escolheu
        self.cb_ferramenta.bind("<<ComboboxSelected>>", lambda e: self.controlador.mudar_ferramenta(self.cb_ferramenta.get()))
        
        # botões de cores avisa o controlador quando clicados
        self.btn_borda = ttk.Button(self.painel, text="Cor da Borda", command=self.escolher_borda)
        self.btn_borda.grid(row=0, column=2, padx=5, pady=5)
        
        self.btn_fundo = ttk.Button(self.painel, text="Cor do Fundo", command=self.escolher_preenchimento)
        self.btn_fundo.grid(row=0, column=3, padx=5, pady=5)

        # BOTÕES PARA SALVAR E ABRIR
        
        self.btn_salvar = ttk.Button(self.painel, text="Salvar", command=self.acao_salvar)
        self.btn_salvar.grid(row=0, column=4, padx=5, pady=5)
        
        self.btn_abrir = ttk.Button(self.painel, text="Abrir", command=self.acao_abrir)
        self.btn_abrir.grid(row=0, column=5, padx=5, pady=5)

        # A tela que o usuario vai utilizar para desenhar
        self.canvas = tk.Canvas(self.root, bg='white', width=600, height=600)
        self.canvas.pack()
        self.canvas.bind('<ButtonPress-1>', self.controlador.inicia_desenho) 
        self.canvas.bind('<B1-Motion>', self.controlador.atualiza_desenho)
        self.canvas.bind('<ButtonRelease-1>', self.controlador.finaliza_desenho)
        self.canvas.bind('<ButtonPress-3>', self.controlador.encerra_poligono) 

  
    # Abre a janela de cor e manda o resultado pro controlador
    def escolher_borda(self):
        cor = colorchooser.askcolor(title="Cor da Borda")[1]
        if cor: self.controlador.atualizar_cor_borda(cor)

    def escolher_preenchimento(self):
        cor = colorchooser.askcolor(title="Cor do Preenchimento")[1]
        if cor: self.controlador.atualizar_cor_preenchimento(cor)


    #  COMUNICAÇÃO DO JSON COM A TELA
   
    def acao_salvar(self):
        # Abre uma janela pedindo pro usuário escolher a pasta e o nome do arquivo
        caminho = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os Arquivos", "*.*")],
            title="Salvar Desenho"
        )
        if caminho:
            try:
                # Se ele não cancelar, manda salvar o modelo 
                self.controlador.modelo_desenho.salvar_json(caminho)
                messagebox.showinfo("Sucesso", "Desenho salvo com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao salvar: {e}")

    def acao_abrir(self):
        # Abre a janela pedindo pro usuário selecionar um arquivo JSON
        caminho = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os Arquivos", "*.*")],
            title="Abrir Desenho"
        )
        if caminho:
            try:
                #  Pede pro Modelo ler o arquivo e recriar os objetos
                self.controlador.modelo_desenho.abrir_json(caminho)
                
                self.canvas.delete("all") 
                
                #  Manda cada figura que foi recarregada se desenhar de novo na tela
                for figura in self.controlador.modelo_desenho.figuras:
                    figura.desenhar(self.canvas, tags="figura_definitiva")
                    
                messagebox.showinfo("Sucesso", "Desenho carregado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao abrir: {e}")




