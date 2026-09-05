# Regras comuns para agentes de IA

Estas regras aplicam-se a todos os domínios suportados.

1. Inspecione o repositório real, o ambiente de execução, as dependências, os testes e os requisitos de segurança antes de alterar o código.
2. Detete e meça o ambiente real antes de escolher configurações sensíveis a recursos.
3. Nunca assuma como requisito uma máquina, sistema operativo, CPU, RAM, GPU, acelerador ou IDE específicos.
4. Mantenha a lógica de domínio reutilizável em módulos e limite notebooks/scripts à orquestração.
5. Use configuração explícita, metadados de reprodutibilidade e caminhos determinísticos.
6. Mantenha os segredos fora do controlo de versões.
7. Valide primeiro com o teste significativo mínimo e depois execute a suíte mais ampla.
8. Após validar o ambiente, remova caminhos de execução não utilizados e código obsoleto, salvo quando o suporte multiplataforma for intencional.
9. Cargas longas devem usar validação, Early Stopping, o melhor Checkpoint e Resume quando apropriado.
10. As experiências devem definir baseline, variantes controladas, seeds, métricas e acompanhamento de recursos.

## Ciclo padrão

```text
Explorar → Detetar → Medir → Resolver → Smoke Test → Fixar → Implementar → Validar → Documentar
```
