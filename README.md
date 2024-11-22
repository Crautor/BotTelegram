# **Guia Completo de Configuração do Bot Telegram**

Este guia detalha os passos necessários para clonar, configurar e executar o projeto **Bot Telegram** utilizando Docker, além de incluir orientações para solucionar problemas e entender a estrutura do sistema.

---

## **1. Introdução**

O projeto Bot Telegram foi inicialmente desenvolvido em Java, mas recebemos o desafio de migrá-lo para Python. Nosso objetivo principal foi reescrever a aplicação, aproveitando as vantagens do Python em termos de simplicidade, flexibilidade e vasta gama de bibliotecas, garantindo um sistema mais moderno e fácil de manter.

Se consiste em uma aplicação modular que utiliza Docker para simplificar a implantação e o gerenciamento do sistema. Ele inclui uma interface front-end para login e cadastro, além de um backend que gerencia a lógica do bot e integra serviços externos. Este guia aborda desde o clone do repositório até o acesso às interfaces.

---

## **2. Passos de Configuração**

Execute os comandos abaixo para configurar o ambiente:

bash
# 1. Clone o repositório do projeto
git clone https://github.com/Crautor/BotTelegram/

# 2. Acesse o diretório do projeto
cd BotTelegram

# 3. Construa e inicie os containers com Docker Compose
docker compose up --build


### **Pré-requisitos**:
- **Docker** e **Docker Compose** devidamente instalados na máquina.
- Permissões administrativas para execução dos comandos (se necessário).

---

## **3. Links de Acesso**

Após a configuração bem-sucedida, acesse as interfaces do sistema pelos links abaixo:

- **Página de Login**: [http://localhost:3000/auth/login](http://localhost:3000/auth/login)
- **Página de Cadastro**: [http://localhost:3001/auth/cadastro](http://localhost:3001/auth/cadastro)

---

## **4. Estrutura do Sistema**

1. **Front-end**:
   - Responsável por exibir as interfaces de login e cadastro.
   - Expõe a porta `3000` no ambiente local.

2. **Back-end**:
   - Gerencia a lógica do bot e realiza integração com serviços de terceiros.
   - Configurado no `docker-compose.yml` para comunicação interna entre containers.

3. **Docker Compose**:
   - Orquestra todos os containers necessários para rodar o sistema.
   - Permite escalabilidade e fácil reprodução do ambiente.

---

## **5. Resolução de Problemas**

- **Erro de inicialização**:
  Certifique-se de que o Docker está em execução e que as portas `3000` e `3001` não estão ocupadas por outro processo.

- **Logs dos containers**:
  Use o comando abaixo para inspecionar os logs de um container específico:
  bash
  docker logs <nome_ou_id_do_container>
  

- **Reiniciar containers**:
  Caso necessário, pare e reinicie todos os serviços:
  bash
  docker compose down
  docker compose up --build
  

- **Rede e conectividade**:
  Verifique a configuração da rede do Docker para garantir a comunicação entre os containers:
  bash
  docker network ls
  

---

## **6. Expansão do Projeto**

Este é o ponto de partida para o desenvolvimento de um bot de comunicação (WhatsApp/Telegram). Próximos passos incluem:
- Integração com APIs de mensageria ( Telegram Bot API).
- Configuração de lógica personalizada para responder mensagens.
- Testes para validação de comportamento e escalabilidade.

---

💡 **Dica Final**: Documente alterações realizadas no sistema para facilitar o rastreamento de mudanças e a colaboração entre membros da equipe.

🚀 **Pronto para começar? Mãos à obra!**
