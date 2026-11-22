# B2B Research Agent

Um agente de pesquisa B2B construído **do zero em TypeScript (sem frameworks de agentes)** para pesquisar empresas, utilizar ferramentas externas e produzir relatórios estruturados validados em runtime com Zod.

> Projeto desenvolvido com foco em fundamentos reais de **AI Engineering**: Structured Outputs, Agent Loop puro, Tool Calling, Evals determinísticos, Tracing e Human-in-the-loop.

---

## Arquitetura Atual (Semana 2)

```mermaid
flowchart LR
  A["Nome da Empresa"] --> B["OpenAI Chat Completions (Strict JSON Schema)"]
  B --> C["Zod safeParse (Validação em Runtime)"]
  C --> D["Relatório B2B Tipado"]
```

### Decisões Técnicas
- **Single Source of Truth com Zod v4:** o contrato `EmpresaSchema` define a tipagem TypeScript, gera o JSON Schema enviado à API via `z.toJSONSchema()` e valida a resposta em runtime com `.safeParse()`. Isso elimina divergência entre prompt, schema da API e código.
- **Structured Outputs (`strict: true`):** força o modelo na camada de decodificação a obedecer ao contrato, usando `.nullable()` para campos opcionais conforme exigência do modo estrito da OpenAI.
- **Separação de papéis (`system` vs `user`):** instruções comportamentais e regras anti-alucinação ficam na mensagem `system`, separadas da entrada variável do usuário, com `temperature: 0` para maior previsibilidade.

---

## Stack Tecnológica

- **Linguagem / Runtime:** TypeScript (strict mode) + Node.js (ESM)
- **LLM SDK:** OpenAI Node SDK (`gpt-4o-mini`)
- **Validação & Contratos:** Zod v4 (`z.toJSONSchema`, `safeParse`)
- **Execução local:** `tsx` + `dotenv`

---

## Como Executar

### 1. Instalar dependências
```bash
npm install
```

### 2. Configurar variáveis de ambiente
Copie o arquivo de exemplo e insira sua chave da OpenAI:
```bash
cp .env.example .env
```

```env
OPENAI_API_KEY=sua_chave_aqui
```

### 3. Validar tipos e rodar o projeto
```bash
npx tsc --noEmit
npx tsx index.ts
```

---

## Exemplo de Saída

```json
{
  "nome": "Apple",
  "setor": "Tecnologia",
  "tecnologias": [
    "Hardware",
    "Software",
    "Serviços em Nuvem",
    "Inteligência Artificial",
    "Realidade Aumentada"
  ],
  "resumoModeloNegocio": "A Apple projeta, fabrica e vende produtos eletrônicos, software e serviços, focando em inovação e experiência do usuário. Seu modelo de negócios é baseado na integração de hardware e software, criando um ecossistema fechado que fideliza os clientes.",
  "estimativaFuncionarios": 147000,
  "nivelConfianca": "alto"
}
```

---

## Achados de Engenharia — Auditoria da Semana 2

Ao testar o pipeline com empresas reais (`Apple`, `SpaceX`, `Starlink`) e uma empresa fictícia (`Kestrel Quantun Logistics`), observamos três limitações críticas de uma chamada isolada a um LLM:

1. **Structured Outputs garantem formato, não veracidade:** mesmo com `temperature: 0`, `strict: true` e instrução explícita para não inventar dados, o modelo atribuiu setor, tecnologias (TMS, IA) e modelo de negócio à empresa fictícia `Kestrel Quantun Logistics` baseando-se apenas na palavra `"Logistics"` do nome.
2. **Conhecimento congelado:** estimativas como número de funcionários (`Apple: 147000`, `SpaceX: 12000`) refletem dados antigos do treinamento do modelo.
3. **Contexto societário superficial:** `Starlink` foi tratada como entidade isolada sem explicitar claramente sua relação como divisão da `SpaceX`.

**Conclusão arquitetural:** prompts e validação de schema são a fundação, mas para produzir relatórios B2B confiáveis o sistema precisa consultar fontes reais via **Agent Loop + Tool Calling** (próxima etapa).

---

## Roadmap

- [x] **Semana 1:** Setup TypeScript (ESM + strict), Node.js, JSON e contratos com Zod
- [x] **Semana 2:** Integração com LLM, Prompt Engineering, Structured Outputs (`strict: true`) e auditoria de alucinação
- [ ] **Semana 3:** Agent Loop puro, Tool Calling e limites de execução (`maxSteps`)
- [ ] **Semana 4:** Ferramentas de pesquisa real na web e tratamento de erros (retry / backoff)
- [ ] **Semana 5:** Evals, Golden Dataset e testes determinísticos
- [ ] **Semana 6:** Tracing, observabilidade, segurança e Human-in-the-loop
