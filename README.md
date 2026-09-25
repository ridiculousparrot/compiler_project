<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=230&section=header&text=Ludus&fontSize=65&fontColor=ffffff&fontAlignY=32&animation=fadeIn&desc=Linguagem%20educacional%20para%20estudo%20de%20compiladores%20e%20linguagens%20formais&descAlignY=58&descSize=16" width="100%"/>

<img src="https://readme-typing-svg.demolab.com/?font=Fira+Code&size=20&pause=1200&color=6C63FF&center=true&vCenter=true&width=680&lines=Um+projeto+de+introdu%C3%A7%C3%A3o+a+linguagens+formais+e+aut%C3%B4matos+%F0%9F%A7%A9;Construindo+um+compilador%2Finterpretador+passo+a+passo+%E2%9A%99%EF%B8%8F;Escrito+em+Python+%F0%9F%90%8D+%7C+Snapshot+atual%3A+v0.1.0" alt="Typing SVG" />

<!--
  ✦ Nota para quem for editar: dava pra colocar aqui gifs pequenininhos
  estilo GeoCities/anos 2000 (ex: baixados de https://gifcities.org),
  mas a maioria vive em páginas pessoais antigas que podem cair a
  qualquer hora. Pra não arriscar link quebrado no README, deixei só
  os separadores ★ abaixo. Se quiser o visual raiz de verdade, baixe
  uns gifs e salve numa pasta assets/ do repo — aí o link nunca morre.
-->

★ ﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏﹏ ★

</div>

---

## 📖 Sobre o projeto

**Ludus** é uma linguagem de programação e um compilador/interpretador criados com fins **educacionais**, voltados à introdução ao estudo de **linguagens formais, autômatos e construção de compiladores**. A sintaxe é inspirada em pseudocódigos e em português estruturado, justamente para deixar mais claro o que está acontecendo "por baixo do capô" em cada etapa da compilação.

A ideia central do projeto é **construir o compilador de forma incremental**: começando por um interpretador simples (lexer → parser → AST → execução) e evoluindo, aos poucos, rumo a conceitos mais formais — como definição de gramáticas, autômatos finitos e geração de código/bytecode — servindo como material de estudo prático para quem está aprendendo teoria da computação e construção de linguagens.

> 🧩 Este snapshot representa a versão **v0.1.2** do projeto — as bases da linguagem já funcionam de ponta a ponta (lexer → parser → interpretador), e as próximas etapas vão aprofundar a parte formal (autômatos e geração de código).

---

## ✨ Funcionalidades suportadas

| Ícone | Recurso                              | Palavra-chave                 |
| :---: | ------------------------------------ | ----------------------------- |
|  🎮   | Entrada do programa                  | `principal(){}`               |
|  📦   | Declaração de variáveis e vetores    | `var`                         |
|  ➕   | Atribuição e expressões aritméticas  | `=`, `+`, `-`, `*`, `/`       |
|  ⚖️   | Operadores de comparação e igualdade | `>`, `<`, `==`, `!=`          |
|  🔀   | Estruturas condicionais              | `se` / `senao`                |
|  🔁   | Laço de repetição (pré-teste)        | `enquanto`                    |
|  🔂   | Laço de repetição (pós-teste)        | `faca ... enquanto`           |
|  🎛️   | Estrutura de múltipla escolha        | `trocar` / `caso` / `quebrar` |
|  🧠   | Declaração de funções                | `funcao`                      |
|  📤   | Retorno de valores                   | `retorno`                     |
|  🖨️   | Comando de saída                     | `mostrar`                     |

A execução principal está em [`dist/LUDUS.exe`](dist/LUDUS.exe), que executa um IDE que esta sendo utilizado como teste da linguagem.

---

## 🗂️ Estrutura do projeto

```text
📁 src/
 ├── 🔤 lexer/lexer.py          → análise léxica: tokens e palavras reservadas
 ├── 🌳 parser/ast.py           → definição da árvore sintática abstrata (AST)
 ├── 🧵 parser/parser.py        → parser da gramática da linguagem
 ├── ⚙️ semantic/analyzer.py    → interpretador que executa statements e expressões
 └── 🛠️ codegen/generator.py   → gerador de código/bytecode (em desenvolvimento)

📁 src/compiler/main.py         → ponto de entrada para testes e exemplos
📁 examples/                    → exemplos de scripts na linguagem Ludus
📁 tests/                       → testes de lexer, parser e codegen
```

---

## 💻 Exemplo de sintaxe

```ludus
funcao somar(a, b) {
    retorno a + b;
}

funcao maior(a, b) {
    se (a > b) {
        retorno a;
    } senao {
        retorno b;
    }
}

principal() {

    var numeros = [10, 20, 30, 40, 50];

    mostrar("=== LUDUS ===");
    mostrar("Vetor criado:");
    mostrar(numeros);

    var x = 10;

    se (x > 5) {
        mostrar("x e maior que 5");
    } senao {
        mostrar("x nao e maior que 5");
    }

    enquanto (x > 5) {
        x = x - 1;
    }

    mostrar("Valor de x:");
    mostrar(x);

    var resultado = somar(7, 8);

    mostrar("Resultado da soma:");
    mostrar(resultado);

    var maior_valor = maior(25, 42);

    mostrar("Maior valor:");
    mostrar(maior_valor);

    faca {
        x = x + 1;
    } enquanto (x < 10);

    mostrar("Valor final de x:");
    mostrar(x);
}
```

---

## ▶️ Como executar

Na raiz do projeto, execute:

```bash
python src/compiler/main.py
```

Esse comando dispara o fluxo completo:

1. 📄 Leitura do código-fonte
2. 🔤 Geração de tokens pelo lexer
3. 🌳 Parsing para AST
4. ⚙️ Execução pelo interpretador

---

## 🚧 Observações

- 🔨 O projeto ainda está em fase de evolução; o gerador de código em `src/codegen/generator.py` está em estágio inicial de desenvolvimento.
- ✅ Lexer, parser e interpretador já funcionam de forma estável no fluxo atual.
- 📝 Este README foi escrito com base no código presente no repositório e nos exemplos já implementados.

---

## 🚧 Changelog

- **v0.1.1** (2026-06-15)
  - Incrementação de "principal(){}" como main para comecar o bloco de codigo
  - Adicao de vetores para trabalhar com estrutura de dados
  - Estrutura do enquanto ja corrigida de bugs
  - Atualizado README com informações sobre o novo comando.

- **v0.1.2** (2026-8-25)
  - Adicionamos uma IDE de teste rapida para facilitar o trabalho de testes.
  - Vetores possuem indices, ajudando a trabalhar com expressoes e indices dentro dele.
  - bugs corrigidos.
  - Herobrine removido.

## 📜 Licença

Este projeto está sob a licença presente no arquivo [`LICENSE`](LICENSE).

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=20,11,6&height=100&section=footer" width="100%"/>

★ Um projeto de estudo — compiladores, autômatos e linguagens formais, um `token` de cada vez ★

</div>
