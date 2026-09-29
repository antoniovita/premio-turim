# Conferência local do agente

Esta pasta fica **fora** do ZIP. A arena lê apenas `agent/Claude.md`, o prompt
declarado para o andar, o schema de saída e os documentos entregues na chamada.
Ela não executa os programas abaixo.

## Comandos

```sh
python3 validation/validate_agent.py
python3 validation/case_math.py
python3 validation/check_math.py
python3 validation/validate_agent.py --package dist/agent-turim.zip
```

O último comando produz um ZIP com `Claude.md`, `contrato.json`, `prompts/` e
`tools/` diretamente na raiz, sem a pasta `agent/` como prefixo. Para conferir
um pacote existente: `python3 validation/validate_agent.py --zip CAMINHO.zip`.

`case_math.py` usa `openpyxl` e a planilha oficial. Os pesos opcionais
`--onshore-equity` e `--offshore-equity` são frações entre 0 e 1; exemplos de
cenário, não recomendações. `--annual-fee-millions` explicita um custo anual
hipotético. Sem custo informado, o padrão é zero e o relatório mostra a renda
**antes** desse custo desconhecido. Não converta o retorno em US$ em renda de
R$ sem uma hipótese cambial.

## Convenções auditáveis do backtest

- Série de janeiro de 2005 a agosto de 2026, conforme a planilha do kit.
- Pesos de renda fixa e variável repostos mensalmente.
- Imposto de 15% sobre lucro anual positivo no encerramento de cada ano civil
  completo; sem compensação de prejuízos. O ano parcial de 2026 ainda não recebe
  imposto. Esta é uma interpretação explícita da premissa do case.
- Drawdown calculado sobre a curva de riqueza após o imposto quando cobrado,
  em BRL para carteiras onshore e em USD para carteiras offshore. Retornos em USD
  só são convertidos para a visão consolidada em BRL por composição com o retorno
  mensal USDBRL.

O verificador estrutural cobre regras documentadas no starter kit. O schema
completo da resposta só aparece na chamada da arena; a validação local não
substitui o veredito do Juiz. Os cenários de leitura para revisão dos prompts
estão em `scenarios.md`.
