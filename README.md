# LangFlow POC - Agentic Lead Engine

## Stack
- LangFlow 1.8.0
- Python (VENV_NAME)
- AWS Lambda + API Gateway
- OpenAI gpt-4o-mini

## Status das Etapas
- [x] Etapa 1: Setup + Componente Customizado
- [x] Etapa 2: Prospecção + AWS Lambda 	 
- [ ] Etapa 3: Cadência + Memória + HITL
	3.1 ✅ Teste a memória primeiro — é o mais simples, já está no OpenAI
	3.2 🔜 Adicione o HITL Validator como novo componente customizado
	3.3 🔜 Configure o Conditional Router para conectar tudo
- [ ] Etapa 4: RAG + Embeddings
	Para fechar o POC, a Etapa 4 adicionaria:
	Um Vector Store (ex: Astra DB nativo no LangFlow ou ChromaDB)
	OpenAI Embeddings (text-embedding-3-small)
	Um mini banco de currículos/perfis simulados (3-5 PDFs ou textos)
	O Agent consultaria o Vector Store antes de gerar o perfil do lead

## Componente customizado
- Arquivo: main.py (AWSConnector)
- Herda de Component (langflow.custom)
- Usa MessageInput para receber dados do OpenAI

## URLs importantes
- API Gateway: https://vbrnfx8dni.execute-api.us-east-1.amazonaws.com/prod/leads
- LangFlow local: http://localhost:7860

## Problemas já resolvidos
- input_types inválido no build_config → usar Component + MessageInput
- any inválido como tipo → usar MessageInput
- Retorno JSON no Playground → conectar OpenAI direto ao Chat Output também