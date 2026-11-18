import io
import os
import re
import sys
import traceback
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Pillow é opcional: com ele o pato fica mais nítido ao redimensionar.
# Sem ele, o código usa apenas o tkinter (funciona do mesmo jeito).
try:
    from PIL import Image, ImageTk
    PIL_OK = True
except Exception:  # pragma: no cover
    PIL_OK = False

# ----------------------------------------------------------------------
# Import dos módulos do compilador do usuário
# ----------------------------------------------------------------------
try:
    from src.lexer.lexer import Lexer
    from src.parser.parser import Parser
    from src.semantic.analyzer import Interpretador
    IMPORT_ERROR = None
except Exception as e:  # pragma: no cover
    Lexer = Parser = Interpretador = None
    IMPORT_ERROR = e


# ----------------------------------------------------------------------
# Paleta de cores (estética Dev-C++)
# ----------------------------------------------------------------------
COR_FUNDO_JANELA = "#ECE9D8"      # cinza claro clássico (tema "Luna" do XP)
COR_TOOLBAR = "#F0EFEB"
COR_EDITOR_FUNDO = "#FFFFFF"
COR_EDITOR_TEXTO = "#000000"
COR_NUM_LINHA_FUNDO = "#EDEDED"
COR_NUM_LINHA_TEXTO = "#7A7A7A"
COR_CONSOLE_FUNDO = "#1E1E1E"
COR_CONSOLE_TEXTO = "#DCDCDC"
COR_CONSOLE_ERRO = "#FF6B68"
COR_CONSOLE_OK = "#6FCF6F"
COR_SELECAO = "#316AC5"
COR_BARRA_STATUS = "#ECE9D8"

COR_KEYWORD = "#0000FF"
COR_STRING = "#A31515"
COR_COMENTARIO = "#008000"
COR_NUMERO = "#098658"
COR_FUNC_NOME = "#795E26"

PALAVRAS_CHAVE = [
    "var", "se", "senao", "enquanto", "faca", "funcao", "retorno",
    "trocar", "caso", "quebrar", "mostrar", "principal", "verdadeiro",
    "falso", "nulo", "e", "ou", "nao",
]

FONTE_EDITOR = ("Consolas", 12)
FONTE_CONSOLE = ("Consolas", 10)


# ----------------------------------------------------------------------
# Easter egg: quack!  (pato animado via spritesheet)
# ----------------------------------------------------------------------
SENTINELA_PATO = "@@DUCK@@"

# Configuração do spritesheet "duck.png" (grade de células 18x20 px,
# onde CADA LINHA é uma animação diferente).
#
# Linhas disponíveis (0 = primeira linha):
#   0  parado de frente (2 quadros)      9  andando pra esquerda (4)
#   1  andando de lado  (6 quadros)     10  andando de lado, variação (7)
#   4  coração          (2 quadros)     12  balançando de frente (4)
#   5, 6, 7, 8  outras ações (3 cada)   13  andando de frente (7)
DUCK_CELULA_L = 18          # largura de cada célula no spritesheet
DUCK_CELULA_A = 20          # altura de cada célula no spritesheet
DUCK_LINHA_ANIMACAO = 1     # qual linha do sheet usar como animação
DUCK_ESCALA = 2             # ampliação inteira (2 = 36x40 px, 3 = 54x60 px)
DUCK_DELAY_MS = 120         # tempo entre quadros (menor = mais rápido)


def preparar_codigo(codigo):
    """Troca quack!( por mostrar( e injeta um marcador antes da saída.
    Mantém tudo na mesma linha, então a numeração de erros não muda."""
    return re.sub(r'\bquack!\s*\(',
                  f'mostrar("{SENTINELA_PATO}"); mostrar(', codigo)


def carregar_frames_pato(caminho):
    """Recorta UMA linha do spritesheet e devolve os quadros da animação."""
    if not caminho or not os.path.exists(caminho):
        return []

    cl, ca = DUCK_CELULA_L, DUCK_CELULA_A
    y0 = DUCK_LINHA_ANIMACAO * ca
    frames = []
    try:
        if PIL_OK:
            sheet = Image.open(caminho).convert("RGBA")
            w, h = sheet.size
            if y0 + ca > h:
                print("DUCK_LINHA_ANIMACAO fora do spritesheet.")
                return []
            for c in range(w // cl):
                quadro = sheet.crop((c * cl, y0, (c + 1) * cl, y0 + ca))
                if quadro.getbbox() is None:      # célula vazia = fim da animação
                    continue
                quadro = quadro.resize((cl * DUCK_ESCALA, ca * DUCK_ESCALA),
                                       Image.NEAREST)
                frames.append(ImageTk.PhotoImage(quadro))
        else:
            src = tk.PhotoImage(file=caminho)
            w, h = src.width(), src.height()
            if y0 + ca > h:
                print("DUCK_LINHA_ANIMACAO fora do spritesheet.")
                return []
            for c in range(w // cl):
                dst = tk.PhotoImage(width=cl, height=ca)
                dst.tk.call(dst, "copy", src, "-from",
                            c * cl, y0, (c + 1) * cl, y0 + ca, "-to", 0, 0)
                # descarta células totalmente transparentes
                if not any(dst.transparency_get(x, y) is False
                           for x in range(cl) for y in range(ca)):
                    continue
                frames.append(dst.zoom(DUCK_ESCALA) if DUCK_ESCALA > 1 else dst)
    except Exception as e:
        print(f"Não foi possível carregar duck.png: {e}")
        return []

    return frames


# ----------------------------------------------------------------------
# Documentação da linguagem LUDUS
# ----------------------------------------------------------------------
DOCUMENTACAO_LUDUS = """# Documentação da Linguagem LUDUS

## 1. Variáveis

Declaração simples:

    var x = 10;

Expressão com operadores:

    var soma = 5 + 3 * 2;

String:

    var nome = "Pedro";

## 2. Condicional (SE / SENAO)

    se (x > 5) {
        mostrar(x);
    } senao {
        mostrar(0);
    }

## 3. Laço ENQUANTO (while)

    enquanto (x > 0) {
        x = x - 1;
    }

## 4. Laço FACA ... ENQUANTO (do-while)

    faca {
        x = x + 1;
    } enquanto (x < 10);

## 5. Funções e retorno

    funcao soma(a, b) {
        retorno a + b;
    }

## 6. TROCAR / CASO / QUEBRAR (switch/case)

    trocar (x) {
        caso 1:
            mostrar("um");
            quebrar;
        caso 2:
            mostrar("dois");
            quebrar;
    }

## 7. Comparações

Operadores suportados: >, <, >=, <=, ==, != (diferente)

    se (x != 10) {
        mostrar("diferente");
    }

## 8. Listas / Vetores

    var numeros = [10, 20, 30, 40, 50];
    var y = numeros[0] + numeros[1];
    mostrar(y);

## 9. Função principal

Todo programa LUDUS pode iniciar por uma função especial `principal`:

    principal() {
        mostrar("Ola Mundo!");
    }

## 10. Comentários

Comentários de linha podem ser feitos com `//` ou `##`:

    // isto é um comentário
    ## isto também é um comentário

## 11. Palavras reservadas

var, se, senao, enquanto, faca, funcao, retorno, trocar, caso, quebrar,
mostrar, principal, verdadeiro, falso, nulo, e, ou, nao

## 12. Exemplo completo

    principal() {

        var x = 10;

        se (x > 5) {
            mostrar(x);
        } senao {
            mostrar(0);
        }

        enquanto (x > 0) {
            x = x - 1;
        }

        faca {
            x = x + 1;
        } enquanto (x < 10);

        funcao soma(a, b) {
            retorno a + b;
        }

        trocar (x) {
            caso 1:
                mostrar("um");
                quebrar;
            caso 2:
                mostrar("dois");
                quebrar;
        }
    }
"""


class LinhaNumerada(tk.Canvas):
    """Canvas que desenha os números de linha ao lado do editor."""

    def __init__(self, master, editor, **kwargs):
        super().__init__(master, width=44, bg=COR_NUM_LINHA_FUNDO,
                          highlightthickness=0, **kwargs)
        self.editor = editor

    def redesenhar(self, *_args):
        self.delete("all")
        i = self.editor.index("@0,0")
        while True:
            dline = self.editor.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linha = str(i).split(".")[0]
            self.create_text(38, y, anchor="ne", text=linha,
                              fill=COR_NUM_LINHA_TEXTO,
                              font=("Consolas", 10))
            i = self.editor.index(f"{i}+1line")


class EditorLudus(tk.Frame):
    """Editor de texto com números de linha e realce de sintaxe."""

    def __init__(self, master, on_change=None):
        super().__init__(master, bg=COR_EDITOR_FUNDO)
        self.on_change = on_change

        self.texto = tk.Text(
            self, wrap="none", undo=True, bg=COR_EDITOR_FUNDO,
            fg=COR_EDITOR_TEXTO, insertbackground="#000000",
            selectbackground=COR_SELECAO, selectforeground="#FFFFFF",
            font=FONTE_EDITOR, padx=6, pady=4, borderwidth=0,
            highlightthickness=0
        )

        self.linhas = LinhaNumerada(self, self.texto)

        self.scroll_y = ttk.Scrollbar(self, orient="vertical",
                                       command=self._on_scroll_y)
        self.scroll_x = ttk.Scrollbar(self, orient="horizontal",
                                       command=self.texto.xview)
        self.texto.configure(yscrollcommand=self._yscroll,
                              xscrollcommand=self.scroll_x.set)

        self.linhas.grid(row=0, column=0, sticky="ns")
        self.texto.grid(row=0, column=1, sticky="nsew")
        self.scroll_y.grid(row=0, column=2, sticky="ns")
        self.scroll_x.grid(row=1, column=1, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._configurar_tags()

        self.texto.bind("<KeyRelease>", self._ao_digitar)
        self.texto.bind("<KeyPress>", self._ao_pressionar)
        self.texto.bind("<MouseWheel>", lambda e: self.linhas.redesenhar())
        self.texto.bind("<Button-4>", lambda e: self.linhas.redesenhar())
        self.texto.bind("<Button-5>", lambda e: self.linhas.redesenhar())
        self.texto.bind("<Configure>", lambda e: self.linhas.redesenhar())

    def _configurar_tags(self):
        self.texto.tag_configure("keyword", foreground=COR_KEYWORD,
                                  font=(FONTE_EDITOR[0], FONTE_EDITOR[1], "bold"))
        self.texto.tag_configure("string", foreground=COR_STRING)
        self.texto.tag_configure("comentario", foreground=COR_COMENTARIO,
                                  font=(FONTE_EDITOR[0], FONTE_EDITOR[1], "italic"))
        self.texto.tag_configure("numero", foreground=COR_NUMERO)
        self.texto.tag_configure("funcao_nome", foreground=COR_FUNC_NOME,
                                  font=(FONTE_EDITOR[0], FONTE_EDITOR[1], "bold"))
        self.texto.tag_configure("linha_erro", background="#5A1E1E")

    def _ao_pressionar(self, event):
        """Gerencia chaves, parênteses e indentação automática."""

        # Abrir chave / parênteses / colchetes: fecha automaticamente
        pares = {"{": "{}", "(": "()", "[": "[]"}
        if event.char in pares:
            self.texto.insert("insert", pares[event.char])
            self.texto.mark_set("insert", "insert-1c")
            return "break"

        # ENTER
        if event.keysym == "Return":
            linha_atual = self.texto.get("insert linestart", "insert")
            indentacao = re.match(r"\s*", linha_atual).group()

            # Linha terminou com {  -> abre bloco indentado
            if linha_atual.rstrip().endswith("{"):
                nova_indentacao = indentacao + "    "
                self.texto.insert(
                    "insert", "\n" + nova_indentacao + "\n" + indentacao)
                self.texto.mark_set("insert", "insert-1line lineend")
                return "break"

            # ENTER logo antes de um }
            resto = self.texto.get("insert", "insert lineend")
            if resto.strip().startswith("}"):
                self.texto.insert("insert", "\n" + indentacao + "    ")
                return "break"

            # ENTER normal: mantém a indentação
            self.texto.insert("insert", "\n" + indentacao)
            return "break"

        # Fechar chave: reduz a indentação se a linha estiver vazia
        if event.char == "}":
            linha_atual = self.texto.get("insert linestart", "insert")
            indentacao = re.match(r"\s*", linha_atual).group()

            if linha_atual.strip() == "" and len(indentacao) >= 4:
                self.texto.delete("insert linestart", "insert")
                self.texto.insert("insert", indentacao[:-4] + "}")
                return "break"

        return None

    def _on_scroll_y(self, *args):
        self.texto.yview(*args)
        self.linhas.redesenhar()

    def _yscroll(self, *args):
        self.scroll_y.set(*args)
        self.linhas.redesenhar()

    def _ao_digitar(self, event=None):
        self.destacar_sintaxe()
        self.linhas.redesenhar()
        if self.on_change:
            self.on_change()

    def destacar_sintaxe(self):
        t = self.texto
        for tag in ("keyword", "string", "comentario", "numero", "funcao_nome"):
            t.tag_remove(tag, "1.0", "end")

        conteudo = t.get("1.0", "end-1c")

        for m in re.finditer(r'"[^"\n]*"', conteudo):
            self._marcar(t, "string", m.start(), m.end())

        for m in re.finditer(r'\b\d+(\.\d+)?\b', conteudo):
            self._marcar(t, "numero", m.start(), m.end())

        for m in re.finditer(r'\bfuncao\s+(\w+)', conteudo):
            self._marcar(t, "funcao_nome", m.start(1), m.end(1))

        palavras = r'\b(' + '|'.join(PALAVRAS_CHAVE) + r')\b'
        for m in re.finditer(palavras, conteudo):
            self._marcar(t, "keyword", m.start(), m.end())

        # easter egg
        for m in re.finditer(r'\bquack!', conteudo):
            self._marcar(t, "keyword", m.start(), m.end())

        for m in re.finditer(r'//.*', conteudo):
            self._marcar(t, "comentario", m.start(), m.end())
        for m in re.finditer(r'##.*', conteudo):
            self._marcar(t, "comentario", m.start(), m.end())

    def _marcar(self, t, tag, ini, fim):
        t.tag_add(tag, f"1.0+{ini}c", f"1.0+{fim}c")

    def obter_codigo(self):
        return self.texto.get("1.0", "end-1c")

    def definir_codigo(self, codigo):
        self.texto.delete("1.0", "end")
        self.texto.insert("1.0", codigo)
        self.destacar_sintaxe()
        self.linhas.redesenhar()

    def marcar_erro_na_linha(self, numero_linha):
        self.texto.tag_remove("linha_erro", "1.0", "end")
        try:
            self.texto.tag_add("linha_erro", f"{numero_linha}.0",
                                f"{numero_linha}.end+1c")
            self.texto.see(f"{numero_linha}.0")
        except tk.TclError:
            pass


class ConsoleSaida(tk.Frame):
    """Console inferior estilo Dev-C++ (aba de compilação / execução)."""

    def __init__(self, master, caminho_pato=None):
        super().__init__(master, bg=COR_CONSOLE_FUNDO)
        self.texto = tk.Text(
            self, bg=COR_CONSOLE_FUNDO, fg=COR_CONSOLE_TEXTO,
            font=FONTE_CONSOLE, padx=6, pady=4, borderwidth=0,
            highlightthickness=0, state="disabled", wrap="word"
        )
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.texto.yview)
        self.texto.configure(yscrollcommand=scroll.set)
        self.texto.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.texto.tag_configure("erro", foreground=COR_CONSOLE_ERRO)
        self.texto.tag_configure("ok", foreground=COR_CONSOLE_OK)
        self.texto.tag_configure("info", foreground="#9CDCFE")
        self.texto.tag_configure("normal", foreground=COR_CONSOLE_TEXTO)

        # Animação do pato
        self.frames_pato = carregar_frames_pato(caminho_pato)
        self._patos = []          # nomes das imagens embutidas no Text
        self._indice_frame = 0
        self._anim_id = None

    # ------------------------------------------------------------ texto
    def limpar(self):
        self.texto.configure(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.configure(state="disabled")
        self._patos.clear()       # o loop de animação para sozinho

    def escrever(self, msg, tag="normal"):
        self.texto.configure(state="normal")
        self.texto.insert("end", msg, tag)
        self.texto.see("end")
        self.texto.configure(state="disabled")

    def escrever_com_pato(self, msg, tag="normal"):
        """Escreve a linha com o patinho animado à esquerda."""
        self.texto.configure(state="normal")
        if self.frames_pato:
            nome = self.texto.image_create(
                "end", image=self.frames_pato[self._indice_frame],
                padx=6, align="center")
            self._patos.append(nome)
            self._iniciar_animacao()
        self.texto.insert("end", msg, tag)
        self.texto.see("end")
        self.texto.configure(state="disabled")

    # -------------------------------------------------------- animação
    def _iniciar_animacao(self):
        if self._anim_id is None and len(self.frames_pato) > 1:
            self._anim_id = self.after(DUCK_DELAY_MS, self._animar)

    def _animar(self):
        if not self._patos:
            self._anim_id = None
            return

        self._indice_frame = (self._indice_frame + 1) % len(self.frames_pato)
        quadro = self.frames_pato[self._indice_frame]

        vivos = []
        for nome in self._patos:
            try:
                self.texto.image_configure(nome, image=quadro)
                vivos.append(nome)
            except tk.TclError:   # imagem removida (console limpo)
                pass
        self._patos = vivos

        self._anim_id = self.after(DUCK_DELAY_MS, self._animar)


class _EscritorConsole(io.TextIOBase):
    """Redireciona stdout (usado por `mostrar`) para o console,
    tratando o marcador do pato."""

    def __init__(self, console, tag="normal"):
        self.console = console
        self.tag = tag
        self.buffer = ""
        self.pato_pendente = False

    def write(self, s):
        if not s:
            return 0
        self.buffer += s
        while "\n" in self.buffer:
            linha, self.buffer = self.buffer.split("\n", 1)
            self._processar(linha + "\n")
        return len(s)

    def _processar(self, linha):
        if linha.strip() == SENTINELA_PATO:
            self.pato_pendente = True      # a próxima linha é do quack!
            return
        if self.pato_pendente:
            self.console.escrever_com_pato(linha, self.tag)
            self.pato_pendente = False
        else:
            self.console.escrever(linha, self.tag)

    def finalizar(self):
        if self.buffer:
            self._processar(self.buffer)
            self.buffer = ""

    def flush(self):
        pass


class JanelaDocumentacao(tk.Toplevel):
    """Janela com a documentação da linguagem LUDUS e opção de download."""

    def __init__(self, master):
        super().__init__(master)
        self.title("Documentação — LUDUS")
        self.geometry("760x620")
        self.configure(bg=COR_FUNDO_JANELA)
        self.transient(master)

        topo = tk.Frame(self, bg=COR_FUNDO_JANELA)
        topo.pack(side="top", fill="x")

        tk.Label(topo, text="Documentação da Linguagem LUDUS",
                 bg=COR_FUNDO_JANELA, font=("Segoe UI", 11, "bold")
                 ).pack(side="left", padx=10, pady=8)

        tk.Button(topo, text="💾 Baixar documentação", command=self._baixar,
                  bg="#DCE6F1", relief="raised", bd=1,
                  font=("Segoe UI", 9), padx=8, pady=3, cursor="hand2"
                  ).pack(side="right", padx=10, pady=6)

        corpo = tk.Frame(self, bg=COR_FUNDO_JANELA)
        corpo.pack(side="top", fill="both", expand=True, padx=8, pady=(0, 8))

        scroll = ttk.Scrollbar(corpo, orient="vertical")
        self.texto = tk.Text(
            corpo, wrap="word", bg="#FFFFFF", fg="#000000",
            font=("Consolas", 11), padx=10, pady=10,
            yscrollcommand=scroll.set, borderwidth=0, highlightthickness=0
        )
        scroll.config(command=self.texto.yview)
        scroll.pack(side="right", fill="y")
        self.texto.pack(side="left", fill="both", expand=True)

        self.texto.insert("1.0", DOCUMENTACAO_LUDUS)
        self.texto.configure(state="disabled")

    def _baixar(self):
        caminho = filedialog.asksaveasfilename(
            title="Salvar documentação como...",
            defaultextension=".md",
            initialfile="documentacao_ludus.md",
            filetypes=[("Markdown", "*.md"), ("Texto", "*.txt"),
                       ("Todos os arquivos", "*.*")]
        )
        if not caminho:
            return
        try:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write(DOCUMENTACAO_LUDUS)
            messagebox.showinfo("Documentação",
                                 f"Documentação salva em:\n{caminho}")
        except Exception as e:
            messagebox.showerror("Erro ao salvar",
                                  f"Não foi possível salvar o arquivo:\n{e}")


class IDELudus(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LUDUS IDE — Novo Projeto")
        self.geometry("1100x720")
        self.configure(bg=COR_FUNDO_JANELA)

        self.caminho_arquivo = None
        self._modificado = False

        self._carregar_icone()
        self._montar_menu()
        self._montar_toolbar()
        self._montar_corpo()
        self._montar_status()

        self.bind("<F5>", lambda e: self.executar())
        self.bind("<F9>", lambda e: self.compilar())
        self.bind("<Control-n>", lambda e: self.novo_arquivo())
        self.bind("<Control-o>", lambda e: self.abrir_arquivo())
        self.bind("<Control-s>", lambda e: self.salvar_arquivo())

        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)

        if IMPORT_ERROR is not None:
            self.after(300, self._avisar_erro_import)

        exemplo = """principal(){

    mostrar("Ola Mundo!");

}
"""
        self.editor.definir_codigo(exemplo)

    # ---------------------------------------------------------- ícone

    def caminho_recurso(self, nome):
        if getattr(sys, "frozen", False):
            pasta = sys._MEIPASS
        else:
            pasta = os.path.dirname(os.path.abspath(__file__))

        return os.path.join(pasta, nome)

    def _carregar_icone(self):
        """Carrega o ícone da janela.

        tk.PhotoImage NÃO suporta .ico; no Windows usamos iconbitmap().
        Em Linux/Mac, usamos um ludus.png (se existir) via iconphoto.
        """
        caminho_ico = self.caminho_recurso("ludus.ico")
        caminho_png = self.caminho_recurso("ludus.png")

        try:
            if sys.platform.startswith("win"):
                if os.path.exists(caminho_ico):
                    self.iconbitmap(caminho_ico)
                elif os.path.exists(caminho_png):
                    self.icone_janela = tk.PhotoImage(file=caminho_png)
                    self.iconphoto(True, self.icone_janela)
                else:
                    print(f"Ícone não encontrado: {caminho_ico}")
            else:
                if os.path.exists(caminho_png):
                    self.icone_janela = tk.PhotoImage(file=caminho_png)
                    self.iconphoto(True, self.icone_janela)
                else:
                    print(
                        "Aviso: em Linux/macOS use um 'ludus.png' junto do "
                        "script/executável para o ícone da janela aparecer "
                        "(arquivos .ico não são suportados aqui)."
                    )
        except Exception as e:
            print(f"Não foi possível carregar o ícone: {e}")

    # ---------------------------------------------------------- menu
    def _montar_menu(self):
        barra = tk.Menu(self)

        m_arquivo = tk.Menu(barra, tearoff=0)
        m_arquivo.add_command(label="Novo\tCtrl+N", command=self.novo_arquivo)
        m_arquivo.add_command(label="Abrir...\tCtrl+O", command=self.abrir_arquivo)
        m_arquivo.add_command(label="Salvar\tCtrl+S", command=self.salvar_arquivo)
        m_arquivo.add_command(label="Salvar como...", command=self.salvar_como)
        m_arquivo.add_separator()
        m_arquivo.add_command(label="Sair", command=self._ao_fechar)
        barra.add_cascade(label="Arquivo", menu=m_arquivo)

        m_editar = tk.Menu(barra, tearoff=0)
        m_editar.add_command(label="Desfazer", command=lambda: self.editor.texto.edit_undo())
        m_editar.add_command(label="Refazer", command=lambda: self.editor.texto.edit_redo())
        barra.add_cascade(label="Editar", menu=m_editar)

        m_exec = tk.Menu(barra, tearoff=0)
        m_exec.add_command(label="Compilar\tF9", command=self.compilar)
        m_exec.add_command(label="Executar\tF5", command=self.executar)
        barra.add_cascade(label="Executar", menu=m_exec)

        m_ajuda = tk.Menu(barra, tearoff=0)
        m_ajuda.add_command(label="Documentação da Linguagem",
                             command=self.abrir_documentacao)
        m_ajuda.add_separator()
        m_ajuda.add_command(label="Sobre", command=self._sobre)
        barra.add_cascade(label="Ajuda", menu=m_ajuda)

        self.config(menu=barra)

    # -------------------------------------------------------- toolbar
    def _montar_toolbar(self):
        tb = tk.Frame(self, bg=COR_TOOLBAR, height=40)
        tb.pack(side="top", fill="x")

        def botao(txt, cmd, cor="#F5F5F5"):
            b = tk.Button(tb, text=txt, command=cmd, relief="raised",
                          bd=1, bg=cor, activebackground="#D9D9D9",
                          font=("Segoe UI", 10), padx=10, pady=4, cursor="hand2")
            b.pack(side="left", padx=3, pady=3)
            return b

        botao("📄 Novo", self.novo_arquivo)
        botao("📂 Abrir", self.abrir_arquivo)
        botao("💾 Salvar", self.salvar_arquivo)
        tk.Frame(tb, width=2, bg="#BFBFBF").pack(side="left", fill="y", padx=6, pady=6)
        botao("🛠 Compilar (F9)", self.compilar, cor="#DCE6F1")
        botao("▶ Executar (F5)", self.executar, cor="#DFF0D8")
        tk.Frame(tb, width=2, bg="#BFBFBF").pack(side="left", fill="y", padx=6, pady=6)
        botao("🧹 Limpar console", lambda: self.console.limpar())
        tk.Frame(tb, width=2, bg="#BFBFBF").pack(side="left", fill="y", padx=6, pady=6)
        botao("📘 Documentação", self.abrir_documentacao, cor="#FFF2CC")

    # ---------------------------------------------------------- corpo
    def _montar_corpo(self):
        divisor = tk.PanedWindow(self, orient="vertical", bg=COR_FUNDO_JANELA,
                                  sashwidth=6, sashrelief="raised")
        divisor.pack(side="top", fill="both", expand=True)

        painel_editor = tk.Frame(divisor, bg=COR_FUNDO_JANELA)
        rotulo_editor = tk.Label(painel_editor, text=" Editor — LUDUS",
                                  anchor="w", bg="#D9E4F5",
                                  font=("Segoe UI", 9, "bold"))
        rotulo_editor.pack(side="top", fill="x")
        self.editor = EditorLudus(painel_editor, on_change=self._marcar_modificado)
        self.editor.pack(side="top", fill="both", expand=True)
        divisor.add(painel_editor, stretch="always", minsize=200)

        painel_console = tk.Frame(divisor, bg=COR_FUNDO_JANELA)
        rotulo_console = tk.Label(painel_console, text=" Saída / Console",
                                   anchor="w", bg="#D9E4F5",
                                   font=("Segoe UI", 9, "bold"))
        rotulo_console.pack(side="top", fill="x")
        self.console = ConsoleSaida(
            painel_console, caminho_pato=self.caminho_recurso("duck.png"))
        self.console.pack(side="top", fill="both", expand=True)
        divisor.add(painel_console, stretch="always", minsize=120)

    # --------------------------------------------------------- status
    def _montar_status(self):
        self.status = tk.Label(self, text="Pronto", anchor="w",
                                bg=COR_BARRA_STATUS, bd=1, relief="sunken",
                                font=("Segoe UI", 9))
        self.status.pack(side="bottom", fill="x")

    def _definir_status(self, texto):
        self.status.config(text=texto)

    # -------------------------------------------------- ações arquivo
    def _marcar_modificado(self):
        self._modificado = True
        nome = os.path.basename(self.caminho_arquivo) if self.caminho_arquivo else "Novo Projeto"
        self.title(f"LUDUS IDE — {nome} *")

    def novo_arquivo(self):
        self.editor.definir_codigo("")
        self.caminho_arquivo = None
        self._modificado = False
        self.title("LUDUS IDE — Novo Projeto")

    def abrir_arquivo(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Arquivos LUDUS", "*.ldu *.ludus"), ("Todos os arquivos", "*.*")]
        )
        if not caminho:
            return
        with open(caminho, "r", encoding="utf-8") as f:
            self.editor.definir_codigo(f.read())
        self.caminho_arquivo = caminho
        self._modificado = False
        self.title(f"LUDUS IDE — {os.path.basename(caminho)}")

    def salvar_arquivo(self):
        if not self.caminho_arquivo:
            return self.salvar_como()
        with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
            f.write(self.editor.obter_codigo())
        self._modificado = False
        self.title(f"LUDUS IDE — {os.path.basename(self.caminho_arquivo)}")
        self._definir_status(f"Salvo em {self.caminho_arquivo}")

    def salvar_como(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".ldu",
            filetypes=[("Arquivos LUDUS", "*.ldu"), ("Todos os arquivos", "*.*")]
        )
        if not caminho:
            return
        self.caminho_arquivo = caminho
        self.salvar_arquivo()

    def _ao_fechar(self):
        if self._modificado:
            resp = messagebox.askyesnocancel("Sair", "Salvar alterações antes de sair?")
            if resp is None:
                return
            if resp:
                self.salvar_arquivo()
        self.destroy()

    def _sobre(self):
        messagebox.showinfo(
            "Sobre",
            "LUDUS IDE\nAmbiente gráfico para a linguagem LUDUS.\n"
            "Compilador: Lexer + Parser + Interpretador (src/)."
        )

    def abrir_documentacao(self):
        """Abre a janela de documentação da linguagem LUDUS."""
        JanelaDocumentacao(self)

    def _avisar_erro_import(self):
        self.console.escrever(
            "Não foi possível importar os módulos do compilador (src.lexer, "
            "src.parser, src.semantic).\n", "erro"
        )
        self.console.escrever(f"Detalhe: {IMPORT_ERROR}\n", "erro")
        self.console.escrever(
            "Verifique se este arquivo está na raiz do projeto, no mesmo "
            "nível da pasta 'src/'.\n", "info"
        )

    # ------------------------------------------------------- compilar
    def compilar(self):
        """Executa apenas Lexer + Parser, sem interpretar (checagem sintática)."""
        if IMPORT_ERROR is not None:
            self._avisar_erro_import()
            return

        self.console.limpar()
        self.editor.texto.tag_remove("linha_erro", "1.0", "end")
        codigo = preparar_codigo(self.editor.obter_codigo())
        self._definir_status("Compilando...")
        self.console.escrever("== Compilando ==\n", "info")

        try:
            lexer = Lexer(codigo)
            tokens = lexer.scanear_tokens()
            parser = Parser(tokens)
            parser.parse()
            self.console.escrever("Compilação concluída sem erros.\n", "ok")
            self._definir_status("Compilação concluída sem erros.")
        except Exception as e:
            self._reportar_erro(e)
            self._definir_status("Erro de compilação.")

    # ------------------------------------------------------- executar
    def executar(self):
        """Executa Lexer + Parser + Interpretador, capturando a saída."""
        if IMPORT_ERROR is not None:
            self._avisar_erro_import()
            return

        self.console.limpar()
        self.editor.texto.tag_remove("linha_erro", "1.0", "end")
        codigo = preparar_codigo(self.editor.obter_codigo())
        self._definir_status("Executando...")
        self.console.escrever("== Executando ==\n", "info")

        escritor = _EscritorConsole(self.console, tag="normal")
        stdout_original = sys.stdout
        sys.stdout = escritor
        try:
            lexer = Lexer(codigo)
            tokens = lexer.scanear_tokens()

            parser = Parser(tokens)
            statements = parser.parse()

            interpretador = Interpretador()
            if hasattr(interpretador, "analisar_arvore_sintatica"):
                interpretador.analisar_arvore_sintatica(statements)

            resultado = None
            for stmt in statements:
                resultado = interpretador.executar(stmt)

            escritor.finalizar()
            sys.stdout = stdout_original
            if resultado is not None and hasattr(interpretador, "stringify"):
                self.console.escrever(interpretador.stringify(resultado) + "\n", "normal")

            self.console.escrever("\n== Execução concluída ==\n", "ok")
            self._definir_status("Execução concluída com sucesso.")
        except Exception as e:
            escritor.finalizar()
            sys.stdout = stdout_original
            self._reportar_erro(e)
            self._definir_status("Erro durante a execução.")
        finally:
            sys.stdout = stdout_original

    # -------------------------------------------------------- erros
    def _reportar_erro(self, excecao):
        self.console.escrever(f"\n[Erro] {type(excecao).__name__}: {excecao}\n", "erro")

        linha = self._extrair_numero_linha(excecao)
        if linha:
            self.editor.marcar_erro_na_linha(linha)
            self.console.escrever(f"(linha {linha} destacada no editor)\n", "erro")

        detalhe = traceback.format_exc()
        self.console.escrever(detalhe + "\n", "erro")

    @staticmethod
    def _extrair_numero_linha(excecao):
        for atributo in ("linha", "line", "line_number", "lineno"):
            if hasattr(excecao, atributo):
                try:
                    return int(getattr(excecao, atributo))
                except (TypeError, ValueError):
                    pass
        m = re.search(r"linha\s+(\d+)", str(excecao), re.IGNORECASE)
        if m:
            return int(m.group(1))
        m = re.search(r"line\s+(\d+)", str(excecao), re.IGNORECASE)
        if m:
            return int(m.group(1))
        return None


if __name__ == "__main__":
    app = IDELudus()
    app.mainloop()