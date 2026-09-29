# Kit do candidato — Prêmio Turim, 9ª edição

`exemplo-agente/` mostra o FORMATO de um agente que passa no Andar 1.

**O exemplo não é o case.** O cliente dele é uma associação náutica inventada.
Isso é deliberado: entregar um exemplo já escrito sobre a família do enunciado
seria entregar o Andar 2 pronto. Copie a ESTRUTURA — manifesto, contrato,
prompts, ferramentas — e escreva o conteúdo do case você mesmo.

## O manifesto do seu agente

Todo agente é dois arquivos que contam a MESMA história, de dois jeitos:

- `Claude.md` (ou `AGENTS.md`) — a história em prosa, na raiz da sua pasta. É o
  que o Porteiro (Andar 1) audita por conteúdo: o que o agente faz, com que
  regras, com que ferramentas;
- `contrato.json` — a mesma história em máquina: nome, descrição e qual
  `prompt` cada andar chama. É o que o Andar 1 valida contra o schema oficial
  antes de deixar a dupla lutar.

O `contrato.json` **não declara mais uma lista de funções** com `entrada` e
`saida` tipadas — esse formato (`funcoes`, uma por andar, cada uma com JSON
Schema próprio) era do case anterior e não existe mais. O que ele declara hoje
é bem mais simples: um `prompt` por andar, do 2 ao 6.

| Andar | O `prompt` desse andar tem de ensinar o método para... |
|-------|----------------------------------------------------------|
| 2 | quem é o cliente, em números, e o que falta saber |
| 3 | quanto dá para gastar por ano, para sempre |
| 4 | as carteiras, por classe, com o risco de cada uma |
| 5 | a mesma tese sob contestação |
| 6 | os slides que o cliente receberia |

O Andar 7 (o case surpresa, ao vivo diante da banca) não tem prompt submetido —
fica de fora do manifesto.

## O que vem no kit

- `material/case-premio-turim-9a-edicao.pdf` — o enunciado;
- `material/retornos-mensais-2005-2026.xlsx` — a série do backtest do Andar 4;
- `material/dossie/` — os documentos que o Juiz entrega ao seu agente durante as
  lutas (`familia`, `patrimonio`, `governanca`, `premissas`). É neles que os
  números e as lacunas do case vivem — não existe um campo de citação formal na
  saída, então ler o dossiê é o que decide o turno, não apontar para ele;
- `exemplo-agente/apresentacao_template.pptx` — o template OFICIAL da Turim, com
  as seções na ordem em que a família espera ouvi-las; é referência de estrutura,
  não gabarito, e a entrega final sai em **PDF**, gerada no Andar 6 e
  **baixável no modal MATERIAIS** assim que você lutar aquele andar;
- `exemplo-agente/contrato.json` — um manifesto válido **NA FORMA**: nome,
  descrição e os cinco andares declarados. A `descricao` é a do exemplo, e é a
  primeira coisa que o Andar 1 recusa — veja o motivo mais abaixo;
- `exemplo-agente/Claude.md` — manifesto de exemplo comentado;
- `exemplo-agente/prompts/andar2.md` … `andar6.md` — um ESQUELETO por andar:
  cada um diz o que aquele andar cobra e deixa o método em branco, marcado com
  `ESCREVA AQUI`. O Andar 1 recusa qualquer prompt que ainda tenha o marcador;
- `exemplo-agente/tools/` — esboços de ferramenta (leitura da planilha de
  retornos, resolução de uma fonte por id), só com a assinatura: o corpo lança
  `NotImplementedError`. São **referência opcional**. O Juiz não executa nem lê
  nada de `tools/` durante as batalhas (veja "O que o Juiz lê em cada chamada").

---

## O `contrato.json` — o que é, para que serve e como preencher

### O que é

`contrato.json` é a **carteira de identidade do seu agente**. É um arquivo JSON
que fica na **raiz** da pasta que você submete e que declara **quem é o
agente** (`nome`, `descricao`) e **como cada andar da torre chama ele**
(`andares`, um `prompt` por andar).

Ele não é código: nada dentro dele é executado. É uma **declaração** — o Juiz
não negocia interface com você no meio da batalha: ele lê o contrato antes de
tudo, confirma que ele está na forma esperada, e só então libera a submissão
para lutar. Todas as duplas são avaliadas na mesma régua porque todas declaram
no mesmo formato.

### Quem lê o arquivo

| Quem | Quando | O que faz com ele |
|------|--------|-------------------|
| **O Andar 1** (O Porteiro, sem LLM) | no ato da submissão | valida o arquivo contra o JSON Schema oficial. Falhou → a submissão é **reprovada na hora**, com o motivo no relatório (checks `nome_declarado`, `descricao_acionavel`, `chamada_dos_andares`, `estrutura_md`, `prompts_preenchidos`, entre outros) |
| **O Juiz** | em cada turno de batalha | usa o `prompt` do andar em jogo, combinado com o `Claude.md`, para montar o system prompt daquela chamada |
| **O avaliador humano** | na curadoria | lê `nome` e `descricao` para entender o que você se propôs a construir |

A fonte da verdade é o JSON Schema oficial do manifesto, que roda no Andar 1.
Este README explica o que ele exige, campo a campo; ele é quem decide.

### Anatomia

```json
{
  "nome": "meu-agente",
  "descricao": "O que o agente faz, para quem e com que material — em uma ou duas linhas.",
  "andares": {
    "2": { "prompt": "prompts/andar2.md" },
    "3": { "prompt": "prompts/andar3.md" },
    "4": { "prompt": "prompts/andar4.md" },
    "5": { "prompt": "prompts/andar5.md" },
    "6": { "prompt": "prompts/andar6.md" }
  }
}
```

Só isso. Sem `versao`, sem `funcoes`, sem `entrada`/`saida` por função — esse
era o contrato do case anterior.

### Os campos da raiz

| Campo | Obrigatório | Tipo | Para que serve | Como você preenche |
|-------|-------------|------|----------------|--------------------|
| `nome` | **sim** | string, 1–80 caracteres | identifica o agente no relatório de submissão e na curadoria | um nome curto para o seu agente |
| `descricao` | **sim** | string, mínimo 40 caracteres | é o que o check `descricao_acionavel` confere, e o que o avaliador humano lê para entender a sua intenção | uma ou duas frases dizendo o que O SEU agente faz, para quem e com que material — com as suas palavras. **Não pode ficar igual à do exemplo do kit**: o Andar 1 recusa essa frase especificamente, mesmo que tenha 40+ caracteres |
| `andares` | **sim** | objeto com as chaves `"2"` a `"6"` | o coração do contrato: qual `prompt` o Juiz usa em cada andar | um objeto por andar (veja a próxima tabela) |

O schema é fechado (`additionalProperties: false`) em **três níveis**:

1. **Na raiz** — só existem `nome`, `descricao` e `andares`. Um `"versao"` ou
   `"autor"` no topo reprova.
2. **No objeto `andares`** — só as chaves `"2"` a `"6"`. Uma chave a mais
   (`"7"`, `"1"`) ou faltando reprova.
3. **Dentro de cada andar** — só `prompt` e `saida`.

### Os campos de cada andar

| Campo | Obrigatório | Tipo | Para que serve | Como você preenche |
|-------|-------------|------|----------------|--------------------|
| `prompt` | **sim** | string, não vazia | caminho, dentro do zip, do `.md` que o Juiz lê para montar o system prompt daquele andar | o caminho relativo à raiz da sua pasta, ex.: `prompts/andar2.md`. Tem de **existir no zip** — declarado e ausente reprova o check `chamada_dos_andares` |
| `saida` | não | string, não vazia | nome de um arquivo que o andar produz. Hoje é **só informativo**: não há código na plataforma que leia este campo | opcional. O exemplo do kit declara `"apresentacao.pptx"` no Andar 6, mas isso não muda o formato da entrega — veja a ressalva abaixo |

**`saida` não é o formato da entrega.** O Andar 6 sempre sai em **PDF**, gerado
pela plataforma a partir dos `slides` que o seu agente devolve na saída tipada
daquele andar (veja "A saída que o Juiz julga em cada andar", mais abaixo). O
nome de arquivo em `saida` é referência solta, não um contrato que a
plataforma cumpre.

**Onde pegar o arquivo.** Ele nasce na sua primeira batalha do Andar 6 —
vitória **ou** derrota — e fica no modal **MATERIAIS**, botão BAIXAR MINHA
APRESENTAÇÃO. Perder o andar e ainda assim receber o PDF é de propósito: é
olhando o arquivo que você confere o que `estrutura_minima` e
`contagem_de_slides` enxergaram, em vez de adivinhar pelo diagnóstico.

Esse PDF é uma entrega válida. Se preferir, diagrame a sua própria versão e
envie essa ao comitê: **o conteúdo é o que foi avaliado, e a forma fica a seu
critério.**

### O que reprova na hora

1. **Chave extra na raiz.** Só existem `nome`, `descricao` e `andares`.
2. **`andares` incompleto ou com chave a mais.** Exatamente as chaves `"2"` a
   `"6"` — nem menos, nem mais.
3. **Andar sem `prompt`, ou `prompt` que aponta para um arquivo ausente no
   zip.**
4. **`descricao` com menos de 40 caracteres, ou idêntica à do exemplo do
   kit.**
5. **`nome` ausente ou vazio.**
6. **Arquivo fora da raiz do zip, com outro nome** (inclusive por causa de
   maiúsculas: tem de ser exatamente `contrato.json`, em minúsculas) **ou JSON
   inválido** — vírgula sobrando, comentário de barra dupla, aspas simples,
   BOM. Salve em UTF-8 sem BOM.

Isso cobre só a FORMA. Nenhum desses checks lê o CONTEÚDO dos seus prompts —
essa régua é outra, e está na seção "O QUE REPROVA O ANDAR E O QUE SÓ SOMA
PONTO", logo abaixo.

### Passo a passo

1. Copie `exemplo-agente/contrato.json` para a raiz da sua pasta. **Ele já é
   válido na forma** — comece de algo que passa. O que não vale é o conteúdo: a
   `descricao` é a do exemplo (o Andar 1 recusa essa frase de propósito) e os
   prompts que ele aponta ainda têm `ESCREVA AQUI`.
2. Troque `nome` e `descricao` pelos seus, com as suas palavras — dizendo o que
   o **seu** agente faz, não a associação náutica do exemplo.
3. Copie `exemplo-agente/prompts/` para a sua pasta e escreva, em cada
   `andarN.md`, o método do seu agente para aquele andar — substituindo
   `ESCREVA AQUI`. É esse texto que vira o system prompt do Juiz naquele turno.
4. Crie a pasta `tools/` com **ao menos um arquivo**: o check `pasta_tools`
   exige que ela exista, e pasta vazia não conta, porque o zip não guarda
   diretório vazio. Copiar `exemplo-agente/tools/` resolve, e um `.md`
   descrevendo as ferramentas do seu método também. O conteúdo não é avaliado,
   e o Juiz não executa nada dali.
5. Cite os cinco andares no seu `Claude.md`, como o exemplo faz — o Porteiro
   confere se manifesto e contrato contam a mesma história.
6. Suba o `.zip` da sua pasta na arena (tela do fliperama → botão de inserir
   pasta) e leia o relatório do Andar 1. Os checks
   que decidem a forma são `manifesto_raiz`, `nome_declarado`,
   `descricao_acionavel`, `chamada_dos_andares`, `estrutura_md`,
   `prompts_preenchidos`, `pasta_tools`, `sem_executaveis` e
   `nomes_no_padrao` — o `detail` de cada um aponta exatamente o que falta.

### Esqueleto mínimo válido

Válido no schema, pronto para preencher:

```json
{
  "nome": "meu-agente",
  "descricao": "Agente do case do Premio Turim: diagnostica a familia, dimensiona o patrimonio, aloca as carteiras e defende a tese sob contestacao.",
  "andares": {
    "2": { "prompt": "prompts/andar2.md" },
    "3": { "prompt": "prompts/andar3.md" },
    "4": { "prompt": "prompts/andar4.md" },
    "5": { "prompt": "prompts/andar5.md" },
    "6": { "prompt": "prompts/andar6.md" }
  }
}
```

`exemplo-agente/contrato.json` é essencialmente este esqueleto, com a descrição
que o Andar 1 recusa. Leia os dois lado a lado.

---

## O QUE REPROVA O ANDAR E O QUE SÓ SOMA PONTO

Não são a mesma coisa, e a diferença decide se você sobe ou não.

**OBRIGATÓRIO — errar um só reprova o andar inteiro.** Os números do dossiê, a
parcela imobilizada, a renda contra o gasto, o imposto da venda, a renda
perpétua, o padrão da filha, as carteiras e as classes somando 100%, o drawdown,
o prêmio de risco, a estabilidade sob pressão, a contagem e a estrutura dos
slides, a coerência numérica entre os andares e a resistência a instrução
embutida em documento.

Número inconsistente com as premissas do case não tem meio-termo: a integridade
vai a zero e o andar não abre. Não existe "acertei três de quatro".

**DIFERENCIAL — acertar soma ponto, errar não tira nada.** O custo da própria
casa, as lacunas percebidas, a visão consolidada da família, a nota metodológica
e o nível do material. O enunciado trata cada um deles como "vale ponto", nunca
como requisito.

É por isso que o seu rank no encontro (S, A, B) sai dos diferenciais: o
obrigatório é o portão, o diferencial é a régua.

## A CONFIANÇA DA FAMÍLIA TEM TETO, E O TETO NÃO VOLTA

O placar diz até onde vocês chegaram. A confiança da família diz **como** vocês
chegaram.

Cada derrota derruba o teto da confiança em 3 pontos, para sempre. Limpar a
torre inteira sem perder nenhuma vez dá 100%. Limpar a mesma torre com quatro
derrotas dá 88%. Com doze, 64%.

Perder refazendo um andar que vocês já venceram conta igual — derrota é derrota.
O que não conta é falha nossa: se o Juiz cair, a tentativa vira `error` e não
custa nada a vocês.

Vocês veem esse número na tela o tempo todo, e a família comenta. Tentar até
acertar funciona, mas aparece.

---

## O que o Juiz lê em cada chamada

Em cada andar, o Juiz faz **uma chamada ao modelo**, sem uso de ferramentas.
Nada do que está na sua pasta é executado. O agente responde só com o que vem
nessa chamada:

| Parte da chamada | O que entra | Limite |
|------------------|-------------|--------|
| system | o seu `Claude.md` (ou `AGENTS.md`) | os primeiros **3.000 caracteres** |
| system | o `prompt` que o `contrato.json` declara para aquele andar | os primeiros **2.500 caracteres** |
| system | as regras de saída do andar, com o schema tipado | — |
| user | os documentos que o Juiz entrega naquele andar e a pergunta do andar | — |

**O que passa do limite é cortado e não chega ao modelo, sem aviso.** Ponha o
essencial no começo de cada arquivo. O exemplo do kit cabe nos dois limites.

Por isso `tools/` não muda nenhuma batalha. Ela é exigida pelo Andar 1 como
parte da forma da pasta, e só. Se o seu método depende de uma conta ou de uma
regra, escreva essa conta ou regra no manifesto ou no prompt do andar: é o
único lugar em que o modelo a lê.

**`.py` é permitido**, em `tools/` ou em qualquer outro lugar. O check
`sem_executaveis` barra apenas binários: `.exe`, `.dll`, `.bat`, `.cmd`,
`.msi` e `.scr`.

## A saída que o Juiz julga em cada andar

O `contrato.json` não declara o formato da resposta — isso não é mais trabalho
do contrato. Quem decide o que a sua saída precisa ter é o **schema tipado de
cada andar**, que o Juiz manda **junto com o prompt do sistema**, na própria
chamada, `enum`s inclusos. Você não precisa decorar nada: leia o schema na hora
e responda no formato que ele descreve.

Os campos obrigatórios de cada andar, para você planejar antes de escrever o
prompt (o schema completo chega ao seu agente na hora da chamada):

| Andar | Campos obrigatórios da saída |
|-------|--------------------------------------|
| 2 | `patrimonio_total`, `parcela_imobilizada_pct`, `renda_fazenda_anual`, `gasto_familia_anual`, `informacoes_ausentes`, `justificativa` |
| 3 | `renda_perpetua_real_anual`, `retorno_nominal_premissa_pct`, `venda_fazenda_recomendada`, `produto_liquido_venda`, `perfil_pai`, `perfil_filha`, `offshore_pai_pct`, `offshore_filha_pct`, `filha_sustenta_padrao`, `justificativa` |
| 4 | `carteiras`, `justificativa` |
| 5 | `perfil_pai`, `perfil_filha`, `manteve_posicao`, `justificativa` |
| 6 | `slides` |

O mundo é **aberto** de propósito: campo obrigatório ausente é falha do turno,
campo a mais é ignorado. Um `enum` fechado faria erro de digitação virar
reprovação — o schema pune ausência, não sobra.

**Não existe mais um envelope fixo `{texto, fontes, confianca}` em toda
resposta.** Isso era do case anterior, e saiu de propósito: ele entrava sempre
que a chamada tinha documento, sem olhar o andar, e brigava com o schema
tipado por espaço no teto de saída — o candidato gastava tokens escrevendo
`texto` de prosa e uma lista de `fontes` que aquele andar simplesmente não lê.
Hoje cada andar julga só os campos tipados da tabela acima.

### Teto de saída — leia isto antes de escrever prosa

A resposta de cada chamada tem um **teto de tokens de saída**, aplicado pelo
Juiz. Não é sugestão: o texto é cortado ao bater no teto, e **objeto JSON que
não fecha é turno inválido** — o veredito vem como
`SAIDA DO ANDAR N CORTADA NO TETO DE X TOKENS`.

| Andar | Teto de saída |
|-------|---------------|
| 2, 3, 5 | 700 tokens |
| 4 | 1.100 tokens |
| 6 | 6.000 tokens |

O teto também vem declarado no prompt de cada andar. Coloque os campos
obrigatórios **primeiro** no objeto e deixe qualquer prosa extra para o fim, se
sobrar: um campo obrigatório que nunca chega a ser escrito porque o teto bateu
antes é falha de forma, e ela zera a integridade do andar igual a uma falha de
conteúdo.

### `informacoes_ausentes` (Andar 2) tem vocabulário fechado

O check `percebeu_lacunas` é **diferencial** (vale ponto, não reprova) e compara
sua lista com um vocabulário fechado. String fora dele não conta como lacuna —
conta como erro. Os valores válidos são:

`perfil_risco_declarado`, `gasto_anual_filha`, `custo_da_casa`, `gasto_anual_familia`,
`cesta_de_moedas`, `custo_aquisicao_fazenda`, `idade_do_pai`, `renda_anual_da_fazenda`,
`avaliacao_da_fazenda`, `liquidez_financeira`, `valor_da_doacao_a_filha`

Cuidado: **parte dessa lista é isca.** Alguns desses itens o material ENTREGA, e
apontar um deles como ausente reprova o diferencial. Ler o dossiê é o
exercício.

### `segmentacao` (Andar 2) é **opcional** e vale diferencial

O schema do Andar 2 tem um campo a mais que **não está na lista de
obrigatórios**: `segmentacao`, uma string que aceita exatamente dois valores —
`turim` ou `tori`. Omitir não reprova nada: o campo é opcional de propósito, e
quem não o declara perde apenas o ponto, nunca o andar.

Declarar o valor **certo** vale ponto de diferencial. Qual dos dois é o certo
para esta família é justamente o que o andar mede — a ficha do Andar 2 sempre
anunciou "SEGMENTAÇÃO TURIM OU TORI" entre o que ele testa. O veredito é o
mesmo (`SEGMENTACAO NAO PONTUADA`) tanto para quem não declarou quanto para
quem declarou o outro: o Juiz não diz qual era.

Caixa e espaços não importam: `turim`, `Turim` e `  TURIM  ` valem a mesma
coisa. Os dois valores vão em `examples`, e não em `enum`, justamente para que
uma digitação nunca custe o andar — o campo só precisa ser uma string. Na dúvida
entre os dois, declarar é melhor que omitir: errar o segmento custa só o ponto.

`material/dossie/` (`familia`, `patrimonio`, `governanca`, `premissas`) é o
material que o Juiz entrega ao seu agente durante as lutas — é nele que os
números e as lacunas do case vivem. Não existe um campo de citação formal na
saída: o que decide o turno é o número certo e a `justificativa`, nunca uma
lista de fontes.
