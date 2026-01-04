# Implementação de um Sistema de Chat Seguro Ponto-a-Ponto

## 1. Introdução

Este trabalho apresenta a implementação de um protótipo de sistema de chat seguro
ponto-a-ponto, cujo objetivo é garantir a confidencialidade das mensagens trocadas
entre dois usuários. Para isso, foram aplicados conceitos fundamentais de
criptografia assimétrica, criptografia simétrica e modos de operação de cifras
de bloco.

O sistema utiliza uma arquitetura cliente-servidor simples, onde o servidor atua apenas
como intermediário de mensagens, sem acesso ao conteúdo em texto plano.

## 2. Arquitetura do Sistema

O sistema foi desenvolvido em Python e organizado de forma modular, conforme a
estrutura abaixo:

```bash
    src/
    ├── main.py
    ├── server/
    │   └── server.py
    ├── client/
    │   └── client.py
    └── crypto/
        ├── aes_block.py
        ├── cbc.py
        ├── ctr.py
        └── rsa_utils.py
```

### 2.1 Funcionamento Geral

* O servidor aceita no máximo dois clientes simultaneamente.
* Cada cliente recebe um ID único (1 ou 2).
* O servidor apenas repassa bytes, não realizando criptografia ou descriptografia.
* A segurança é implementada exclusivamente nos clientes.

### 2.2 Execução do Sistema

#### 2.2.1 Criação do Ambiente Virtual

```bash
    python -m venv venv
```

Ativação do ambiente virtual:

* **Linux / macOS**

```bash
    source venv/bin/activate
```

* **Windows**

```bash
    venv\Scripts\activate
```

#### 2.2.2 Instalação das Dependências

```bash
    pip install -r requirements.txt
```

#### 2.2.3 Execução do Sistema

1. Inicie o servidor em um terminal:

```bash
    python src/main.py server
```

2. Em outros dois terminais, inicie os clientes:

```bash
    python src/main.py client
```

3. O Cliente 1 escolhe o modo de operação (CBC ou CTR).

4. O Cliente 2 carrega automaticamente o modo escolhido.

## 3. Decisões de Projeto

### 3.1 Criptografia Assimétrica

Foi utilizado o algoritmo RSA com chaves de 2048 bits, por meio da biblioteca
`PyCryptodome`, juntamente com o esquema de padding OAEP (PKCS#1 OAEP).

O RSA é usado exclusivamente para a troca segura da chave de sessão, e não para
criptografar mensagens de chat, evitando sobrecarga computacional.

### 3.2 Troca de Chaves de Sessão

O protocolo de troca de chaves funciona da seguinte forma:

1. Cada cliente gera localmente um par de chaves RSA (pública e privada).
2. Os clientes trocam suas chaves públicas.
3. O Cliente 1 gera uma chave simétrica aleatória de 128 bits (AES).
4. Essa chave é criptografada com a chave pública do Cliente 2.
5. O Cliente 2 descriptografa a chave usando sua chave privada.
6. A partir desse ponto, ambos compartilham a mesma chave de sessão.

Esse processo garante confidencialidade mesmo em um canal inseguro.

## 4. Criptografia Simétrica da Sessão

Após a troca de chaves, todas as mensagens passam a ser criptografadas com AES,
usando um dos modos de operação implementados manualmente: CBC ou CTR.

A primitiva AES foi utilizada apenas no modo ECB como cifrador de bloco base.

## 5. Implementação do Modo CBC

### 5.1 Funcionamento

O modo CBC (Cipher Block Chaining) foi implementado manualmente seguindo a definição
clássica:

* Um IV aleatório de 16 bytes é gerado no início da sessão.
* Cada bloco de texto plano é combinado com o bloco cifrado anterior via operação XOR.
* O resultado é criptografado com AES.
* O IV é enviado junto com o texto cifrado.

### 5.2 Padding

Foi utilizado o esquema de padding PKCS#7, pois o AES opera sobre blocos de tamanho
fixo (16 bytes). O padding é removido após a descriptografia.

### 5.3 Gerenciamento do IV

* O IV é único por sessão.
* O IV não é secreto, mas é imprevisível.
* O IV é concatenado ao início do ciphertext.


## 6. Implementação do Modo CTR

### 6.1 Funcionamento

O modo CTR (Counter Mode) foi implementado como um cifrador de fluxo:

* Um nonce aleatório de 8 bytes é gerado para cada mensagem.
* Um contador de 8 bytes é incrementado a cada bloco.
* O AES é usado para gerar um keystream.
* O keystream é combinado com o texto plano via XOR.

### 6.2 Gerenciamento do Nonce

* O nonce é único para cada mensagem.
* O nonce não é secreto.
* O nonce é enviado junto com o ciphertext.

## 7. Comparação entre CBC e CTR

| Critério                | CBC               | CTR                |
| ----------------------- | ----------------- | ------------------ |
| Tipo                    | Cifrador de bloco | Cifrador de fluxo  |
| Necessidade de padding  | Sim               | Não                |
| Uso de IV / Nonce       | IV por sessão     | Nonce por mensagem |
| Paralelismo             | Limitado          | Total              |
| Facilidade de uso       | Média             | Alta               |
| Sensível a reutilização | IV                | Nonce              |

O modo CTR é mais simples e flexível, enquanto o CBC exige maior cuidado com padding e
ordem dos blocos.

## 9. 9. Decisões de Projeto, Desafios e Soluções

### 9.1 Decições do Projeto

* A linguagem escolhida foi Python, devido à sua facilidade de
aprendizado, legibilidade do código e ampla disponibilidade de
bibliotecas criptográficas, o que facilitou a comunicação e o
desenvolvimento em dupla.
* A limitação do sistema a dois clientes foi uma decisão de projeto
adotada para simplificar a implementação e o controle de variáveis
compartilhadas, reduzindo problemas de concorrência entre threads.
* A modularização do sistema foi adotada como escolha de projeto,
separando o código em módulos distintos (cliente, servidor e
criptografia), o que facilitou a organização, manutenção e
compreensão geral da aplicação.
* A utilização de ambiente virtual e instalação das dependências via
requirements.txt foi adotada para garantir isolamento do ambiente,
reprodutibilidade do sistema e evitar conflitos entre versões de
bibliotecas.

### 9.2 Dificuldades

* **Dificuldade 1:** Compreensão e implementação do processo de troca de
chaves, incluindo a geração da chave de sessão utilizando criptografia
assimétrica (RSA).
* **Dificuldade 2:** Implementação dos modos de operação do AES (CBC e
CTR), bem como a definição de um mecanismo confiável para a escolha e
compartilhamento do modo entre os clientes.
* **Dificuldade 3:** Problemas relacionados à concorrência, principalmente
no uso de variáveis globais em conjunto com threads, causando conflitos
e comportamentos inesperados durante a execução.

### 9.3 Soluções

* **Solução 1:** O sistema foi limitado a dois usuários identificados, o
que simplificou o controle do fluxo de mensagens e da troca de chaves,
reduzindo a complexidade da comunicação.
* **Solução 2:** Inicialmente, tentou-se armazenar o modo de operação em
variáveis globais, porém essa abordagem gerou conflitos entre threads.
Como solução, a escolha do modo de operação passou a ser salva em um
arquivo .txt no lado do cliente.
* **Solução 3:** O Cliente 1 escolhe o modo de operação criptográfico, o
programa salva essa escolha no arquivo e o Cliente 2 carrega o modo a
partir desse arquivo, garantindo consistência na comunicação sem
conflitos de concorrência.

## 10. Considerações de Segurança

* O servidor não possui acesso ao texto em claro.
* O uso incorreto de IVs ou nonces pode comprometer a segurança.
* O sistema não implementa autenticação de mensagens sendo vulnerável a ataques de
  modificação (ex: bit-flipping).
* O objetivo do trabalho é educacional, focado na compreensão dos conceitos.
