# B2B Research Agent

Um agente de pesquisa B2B construído **do zero em Python (sem frameworks de agentes)** para pesquisar empresas, utilizar ferramentas externas e produzir relatórios estruturados validados em runtime com Zod.

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
- **Single Source of Truth com Pydantic:** o modelo `Empresa` define a tipagem, gera o JSON Schema enviado à API (`response_format`) e valida a resposta em runtime. Isso elimina divergência entre prompt, schema da API e código.
- **Structured Outputs (`strict: true`):** força o modelo na camada de decodificação a obedecer ao contrato, usando `.nullable()` para campos opcionais conforme exigência do modo estrito da OpenAI.
- **Separação de papéis (`system` vs `user`):** instruções comportamentais e regras anti-alucinação ficam na mensagem `system`, separadas da entrada variável do usuário, com `temperature: 0` para maior previsibilidade.

---

## Stack Tecnológica

- **Linguagem:** Python 3.12+
- **LLM SDK:** OpenAI Python SDK (`gpt-4o-mini`), isolado em `src/b2b_agent/llm.py`
- **Validação & Contratos:** Pydantic v2 (`response_format=Empresa`, validação em runtime)
- **Execução local:** `venv` + `python-dotenv`

---

## Como Executar

### 1. Instalar dependências
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente
Copie o arquivo de exemplo e insira sua chave da OpenAI:
```bash
cp .env.example .env
```

```env
OPENAI_API_KEY=sua_chave_aqui
```

### 3. Rodar o projeto
```bash
cd src
python -m b2b_agent            # empresas de exemplo
python -m b2b_agent Apple      # empresa específica
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

Segue o plano revisado (`Doc/Plano de Estudo — AI Engineering.pdf`, Python-first). As semanas 1–2 foram feitas em TypeScript como protótipo; o Projeto 1 passa a ser construído em Python puro, sem frameworks.

- [x] **Semanas 1–2 (protótipo em TypeScript):** Zod, Structured Outputs (`strict: true`), Prompt Engineering e auditoria de alucinação
- [ ] **Semana 3:** Agent loop puro (perceive-think-act), tool calling manual e limites de execução (max steps, timeout)
- [ ] **Semana 4:** Ferramentas e pesquisa real (web scraping, APIs públicas), retry com backoff, structured outputs com Pydantic
- [ ] **Semana 5:** Evals e Golden Dataset (20–30 casos), testes determinísticos e LLM-as-judge
- [ ] **Semana 6:** Tracing (Phoenix/Langfuse), segurança contra prompt injection e Human-in-the-loop
