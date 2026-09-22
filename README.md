# Projeto de linguagem interpretada em Python 

## LUDUS Version: 0.1.0

Este repositório contém um interpretador/compilador simples de uma linguagem de programação com sintaxe inspirada em pseudocódigos e em português estruturado. O projeto foi organizado em módulos para separar análise léxica, análise sintática, AST, interpretação e geração de código.

## Visão geral

A linguagem implementada suporta:

- Declaração de variáveis com `var`
- Atribuição e expressões aritméticas
- Operadores de comparação e igualdade
- Estruturas condicionais com `se` e `senao`
- Laços `enquanto` e `faca ... enquanto`
- Estrutura `trocar`/`caso`/`quebrar`
- Declaração de funções com `funcao`
- Retorno com `retorno`
- Comando de saída com `print`

A execução principal está no arquivo [src/compiler/main.py](src/compiler/main.py), que cria um exemplo de código para testar a linguagem.

## Estrutura do projeto

- `src/lexer/lexer.py` — análise léxica, identificação de tokens e palavras reservadas
- `src/parser/ast.py` — definição da árvore sintática abstrata (AST)
- `src/parser/parser.py` — parser responsável por interpretar a gramática da linguagem
- `src/semantic/analyzer.py` — interpretador que executa os statements e expressões
- `src/codegen/generator.py` — gerador de código/bytecode em desenvolvimento
- `src/compiler/main.py` — ponto de entrada para execução de testes e exemplos
- `examples/` — exemplos de scripts da linguagem
- `tests/` — arquivos de testes relacionados a lexer, parser e codegen

## Exemplos de sintaxe

```txt
var x = 10;

se (x > 5) {
    print(x);
} senao {
    print(0);
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
        print("um");
        quebrar;
    caso 2:
        print("dois");
        quebrar;
}
```

## Como executar

Na raiz do projeto, execute:

```bash
python src/compiler/main.py
```

Esse arquivo monta um código de exemplo e passa por:

1. Leitura do código fonte
2. Geração de tokens pelo lexer
3. Parsing para AST
4. Execução pelo interpretador

## Observações

- O projeto ainda está em fase de evolução e alguns módulos, como o gerador de código em `src/codegen/generator.py`, parecem estar em desenvolvimento inicial.
- A parte principal que já funciona no fluxo atual é a análise léxica, o parser e a interpretação de instruções da linguagem.
- O README foi escrito com base no código presente no repositório e nos exemplos já implementados.

## Licença

Este projeto está sob a licença presente no arquivo `LINCENSE`.
