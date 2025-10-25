# 🩺 API (Lacrei Saúde)

API REST desenvolvida com **Django REST Framework (DRF)** para o gerenciamento de **profissionais de saúde** e **consultas médicas**.

O projeto é totalmente containerizado com **Docker**, utiliza **PostgreSQL** como banco de dados e implementa um pipeline de **CI/CD** com **GitHub Actions** para build, teste, push para o **Docker Hub** e deploy automatizado em uma instância **AWS EC2**.

---

## Tabela de Conteúdo

- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Arquitetura e Estrutura do Projeto](#-arquitetura-e-estrutura-do-projeto)
- [Configuração do Ambiente Local](#-configuração-do-ambiente-local)
- [Documentação da API (Endpoints)](#-documentação-da-api-endpoints)
- [Autenticação](#-autenticação)
- [Testes Automatizados](#-testes-automatizados)
- [Pipeline de CI/CD](#-pipeline-de-cicd)
- [Deploy na AWS EC2](#-deploy-na-aws-ec2)
- [Segurança e GitHub Secrets](#-segurança-e-github-secrets)
- [Autor](#-autor)

---

## 🚀 Tecnologias Utilizadas

Este projeto utiliza um stack moderno focado em escalabilidade e boas práticas de DevOps:

-   🐍 **Python** & **Poetry**: Gerenciamento de dependências e ambiente virtual.
-   💻 **Django** & **Django REST Framework**: Backend robusto para criação da API.
-   🗃️ **PostgreSQL**: Banco de dados relacional.
-   🐳 **Docker** & **Docker Compose**: Containerização e orquestração dos serviços.
-   ☁️ **AWS EC2**: Servidor em nuvem para hospedagem da aplicação.
-   📦 **Docker Hub**: Registro para armazenamento das imagens Docker.
-   🔄 **GitHub Actions**: Automação do pipeline de Integração Contínua e Deploy Contínuo (CI/CD).

---

## 📁 Arquitetura e Estrutura do Projeto

A estrutura do projeto segue o padrão Django, separando a lógica da API em um app dedicado (`api`) e as configurações do projeto em `lacrei_saude`.

```bash
    .
├── api
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations/
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests
│   ├── urls.py
│   └── views.py
├── docker-compose.yaml
├── Dockerfile
├── lacrei_saude
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── poetry.lock
├── pyproject.toml
├── README.md
└── script.sh
└── .github/workflows
    ├── ci_cd.yaml



```

---

##  Configuração do Ambiente Local

Para executar este projeto localmente usando Docker, siga os passos abaixo.

### Pré-requisitos

-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/get-started)
-   [Docker Compose](https://docs.docker.com/compose/install/)

### Instruções para rodar o projeto

1.  **Clone o repositório:**
    ```sh
    git clone [https://github.com/Carlos98770/desafio-tecnico](https://github.com/Carlos98770/desafio-tecnico)
    cd desafio-tecnico
    ```

2.  **Crie o arquivo de ambiente:**
    Crie o arquivo`.env` no diretorio do projeto:

    ```bash
    API_KEY=sua_api_key
    DB_HOST=db  #manter "db"
    DB_NAME=seu_nome_banco
    DB_USER=seu-user
    DB_PASSWORD=sua-senha
    DB_PORT=5432
    DEBUG=True
    ALLOWED_HOSTS=localhost
        
    DATABASE_URL=postgres://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}

    ```

3.  **Ajuste o `docker-compose.yaml` para Desenvolvimento:**
    O arquivo `docker-compose.yaml` vem configurado por padrão para **produção** (usando a imagem pronta `carlos98770/django_rest-api:latest`). Para rodar em modo de **desenvolvimento local**, você precisa alterá-lo:

    * **Comente** as linhas da seção `#producao`.
    * **Descomente** as linhas da seção `#desenvolvimento`.

    **Antes (Padrão - Produção):**
    ```yaml
      app:
        #producao
        image: carlos98770/django_rest-api:latest
        container_name: app_app_1
        env_file:
          - .env
        depends_on:
          - db
        ports:
          - "8000:8000"  

        #desenvolvimento
        # build: .
        # volumes:
        #   - .:/app
        # env_file:
        #   - .env
        # depends_on:
        #   - db
        # ports:
        #   - "8000:8000"
    ```

    **Depois (Modo Desenvolvimento):**
    ```yaml
      app:
        #producao
        # image: carlos98770/django_rest-api:latest
        # container_name: app_app_1
        # env_file:
        #   - .env
        # depends_on:
        #   - db
        # ports:
        #   - "8000:8000"  

        #desenvolvimento
        build: .
        volumes:
          - .:/app
        env_file:
          - .env
        depends_on:
          - db
        ports:
          - "8000:8000"
    ```
    * **Por quê?** O modo desenvolvimento usa `build: .` (constrói a imagem localmente) e `volumes: - .:/app` (espelha seu código local dentro do container). Isso permite que o servidor Django reinicie automaticamente (hot-reload) sempre que você salvar uma alteração no código.

4.  **Construa e suba os containers:**
    Este comando irá construir a imagem da aplicação (se não existir) e iniciar os serviços `app` (Django) e `db` (PostgreSQL) em background.
    ```sh
    sudo docker-compose up -d --build
    ```
     -  **Nota:** O container da API (`app`) executa o `script.sh` na inicialização, que já **aguarda o PostgreSQL**, **aplica as migrações** automaticamente (`python manage.py migrate`) e **inicia o servidor Django**. Caso o `script.sh` tenha sido editado no Windows, certifique-se de que ele esteja utilizando o formato de quebra de linha **LF (Unix)** para evitar erros de execução no ambiente Linux do container.

5.  **(Opcional) Crie um superusuário:**
    Para acessar a interface de admin do Django (`/admin`).
    ```sh
    docker-compose exec app poetry run python manage.py createsuperuser
    ```

🎉 **Pronto!** A API estará acessível em `http://localhost:8000/api/`.

---

## 🗺️ Documentação da API (Endpoints)

A URL base para todos os endpoints é `/api/`.

| Método HTTP | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/profissionais/` | Lista todos os profissionais de saúde. |
| `POST` | `/profissionais/` | Cria um novo profissional. |
| `GET` | `/profissionais/<id>/` | Obtém detalhes de um profissional específico. |
| `PUT` | `/profissionais/<id>/` | Atualiza (completo) um profissional específico. |
| `PATCH` | `/profissionais/<id>/` | Atualiza (parcial) um profissional específico. |
| `DELETE` | `/profissionais/<id>/` | Remove um profissional. |
| `GET` | `/consultations/` | Lista todas as consultas agendadas. |
| `POST` | `/consultations/` | Agenda uma nova consulta. |
| `GET` | `/consultations/<id>/` | Obtém detalhes de uma consulta específica. |
| `DELETE` | `/consultations/<id>/` | Cancela (remove) uma consulta. |
| `GET` | `/consultations/profissional/<id>/` | Lista todas as consultas de um profissional específico. |

---


## 🔑 Autenticação

O acesso à API é protegido por **API Key**. Esta implementação utiliza uma classe de permissão customizada (`api/permissions.py`) que verifica a chave em cada requisição.

Para se autenticar, inclua a chave no cabeçalho `Authorization` da sua requisição, prefixada com `ApiKey`.

**Exemplo de Header:**

```sh
    Authorization: ApiKey SUA_CHAVE_SECRETA_DEFINIDA_NO_ENV
```

A chave utilizada pelo servidor é definida na variável de ambiente `API_KEY`.

---


## 🧪 Testes Automatizados

O projeto possui uma suíte de testes (localizada em `api/tests/`) que valida:
-   A lógica dos **Models** (Profissional e Consulta).
-   As operações **CRUD** via API.
-   O funcionamento correto dos **Endpoints**, incluindo códigos de status e validações de dados.

Para executar os testes, utilize o seguinte comando (com os containers rodando):

```sh
docker-compose exec app poetry run python manage.py test api
```

---

---

## 🔄 Pipeline de CI/CD

Este projeto utiliza **GitHub Actions** para automação de Integração Contínua (CI) e Deploy Contínuo (CD). O fluxo de trabalho está definido no arquivo `.github/workflows/ci_cd.yaml`.

O pipeline é acionado automaticamente a cada `push` ou `pull request` para a branch `main`.

### 1. Integração Contínua (CI)

A etapa de CI é executada em **todas as atualizações** (`push` ou `pull request`) e garante a qualidade e integridade do código.

1.  **Setup do Ambiente:** O job configura o Python 3.13 e instala o Poetry.
2.  **Banco de Testes:** Um container de serviço com **PostgreSQL 15** é iniciado para ser usado durante os testes.
3.  **Instalação:** As dependências do projeto são instaladas usando `poetry install`.
4.  **Lint & Formatação:** O código é verificado contra padrões de formatação (`black`) e linting (`flake8`).
5.  **Testes Automatizados:** O pipeline aguarda o banco de dados de teste ficar pronto, aplica as migrações (`manage.py migrate`) e executa a suíte de testes completa (`manage.py test api`).

### 2. Deploy Contínuo (CD)

A etapa de CD só é executada se a etapa de CI for bem-sucedida:

1.  **Build da Imagem:** A imagem Docker da aplicação é construída localmente no runner do GitHub.
2.  **Login no Docker Hub:** O pipeline se autentica no Docker Hub usando as credenciais `DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN` armazenadas nos secrets.
3.  **Push da Imagem:** A imagem recém-construída é enviada para o registro do Docker Hub com a tag `latest` (ex: `carlos98770/django-api:latest`).
4.  **Deploy na AWS EC2:**
    * O pipeline se conecta à instância EC2 via SSH (usando `EC2_HOST`, `EC2_USER`, `EC2_KEY`).
    * Um script é executado remotamente no servidor para:
        * Navegar até o diretório da aplicação (`~/app`).
        * Parar os serviços atuais com `docker-compose down`.
        * Baixar a nova imagem que acabamos de enviar para o Docker Hub (`docker pull ${{ secrets.DOCKERHUB_USERNAME }}/django-api:latest`).
        * Iniciar os serviços novamente com a imagem atualizada (`docker-compose up -d --build`).

---

## ☁️ Deploy na AWS EC2

A aplicação é hospedada em uma instância **AWS EC2** (Ubuntu Server).

### Configuração do Servidor

Para que o deploy automatizado funcione, o servidor EC2 deve ter:

1.  **Docker** instalado.
2.  **Docker Compose** instalado.
3.  As portas necessárias (ex: `8000`) liberadas no Security Group.
4.  A chave pública SSH correspondente à chave privada (`EC2_SSH_KEY`) adicionada ao arquivo `~/.ssh/authorized_keys` do usuário de deploy.

### Processo de Deploy

O pipeline de CI/CD é responsável por todo o processo. Ao receber um `push | pull request` na `main`, o GitHub Actions constrói a nova imagem e "avisa" o servidor EC2 (via SSH) para baixar e executar essa nova versão, garantindo um deploy "zero-downtime" (ou com o mínimo possível) gerenciado pelo Docker Compose.

---

## 🔒 Segurança e GitHub Secrets

A segurança das credenciais é fundamental e é tratada da seguinte forma:

1.  **Localmente:** O arquivo `.env` NUNCA deve ser comitado no repositório. Ele está incluído no `.gitignore` por padrão.
2.  **CI/CD (GitHub Actions):** As credenciais para o deploy não são expostas no código. Elas são armazenadas de forma segura na seção **Settings > Secrets and variables > Actions** do repositório no GitHub.

Os secrets necessários para o pipeline de CI/CD são:

-   `DOCKER_USERNAME`: Seu nome de usuário do Docker Hub.
-   `DOCKER_PASSWORD`: Sua senha ou (recomendado) um Access Token do Docker Hub.
-   `EC2_HOST`: O endereço IP ou DNS da sua instância EC2.
-   `EC2_USERNAME`: O nome de usuário para se conectar via SSH (ex: `ubuntu`).
-   `EC2_SSH_KEY`: A chave SSH privada (formato PEM) usada para autenticar na instância EC2.


---

## 💡 Explicações sobre Decisões Técnicas

Diversas escolhas de arquitetura e tecnologia foram feitas para garantir robustez, simplicidade de deploy e boas práticas.

### 1. Poetry para Gerenciamento de Dependências

* **Poetry** foi adotado por seu robusto gerenciamento de dependências através do arquivo `pyproject.toml`.
* O principal benefício é o arquivo `poetry.lock`, que garante um **resolvedor de dependências determinístico**. Isso significa que os ambientes de desenvolvimento, CI e produção usarão *exatamente* as mesmas versões de todas as bibliotecas, garantindo compilações 100% reprodutíveis e evitando conflitos.

### 2. Stack Docker (Docker, Docker Compose e Docker Hub)

* **Docker:** Foi utilizado para containerizar a aplicação. O `Dockerfile` define um ambiente exato e imutável (Python, bibliotecas do sistema), garantindo **paridade de ambiente** entre desenvolvimento e produção.
* **Docker Compose:** Foi usado para orquestrar os serviços. O `docker-compose.yaml` define e conecta os serviços necessários (`app` para o Django e `db` para o PostgreSQL), simplificando a inicialização de todo o ambiente com um único comando.
* **Docker Hub:** Foi escolhido como o **Registro de Imagens** (Image Registry). O pipeline de CI/CD envia a imagem Docker da aplicação para o Docker Hub após um build bem-sucedido. O servidor de produção (EC2) então baixa essa imagem, desacoplando o processo de build do processo de deploy.

### 3. Autenticação por API Key (Customizada)

* Foi implementada uma autenticação simples baseada em uma **API Key estática**, validada por uma permissão customizada (`api/permissions.py`). O `Header` esperado é `Authorization: ApiKey SUA_CHAVE`.
*  Esta é uma abordagem pragmática e segura para proteger endpoints de API (especialmente para comunicação máquina-a-máquina ou M2M). Ela é *stateless* (não exige uma sessão de banco de dados) e sua implementação é direta e adequada ao escopo do projeto.

### 4. Deploy na AWS EC2 via SSH

* O deploy foi direcionado a uma instância **AWS EC2** (Infraestrutura como Serviço).
* Esta escolha oferece **controle total sobre o ambiente** de produção. O pipeline de CI/CD (GitHub Actions) simplesmente se conecta via **SSH** e executa comandos do `docker-compose` (`pull` e `up`). Isso torna o processo de deploy direto, transparente e fácil de depurar, pois depende apenas de Docker e SSH instalados no servidor.

### 5. Script.sh (Container Entrypoint)

* Este script é utilizado como o `CMD` do `Dockerfile` da aplicação.
*  Ele atua como um "script de inicialização" que garante a ordem correta das operações ao iniciar o container, resolvendo um problema clássico de *race condition* em ambientes orquestrados como o Docker Compose.

    1.  **Espera pelo Banco:** O comando `until nc -z $DB_HOST $DB_PORT` força o script a pausar e testar a conexão com o banco de dados em *loop*. A aplicação só prossegue quando o container do PostgreSQL está totalmente pronto para aceitar conexões.
    2.  **Migrações Automáticas:** Antes de iniciar o servidor, o script aplica automaticamente quaisquer migrações pendentes (`makemigrations` e `migrate`). Isso garante que o *schema* do banco de dados esteja sempre sincronizado com o código da aplicação, automatizando o setup.
    3.  **Execução do Servidor:** Somente após o banco estar pronto e as migrações aplicadas, o servidor Django é iniciado. Ele é executado em `0.0.0.0:8000` para ser acessível de fora do container, permitindo que o Docker exponha a porta `8000` para a máquina host.


## 📝 Decisões de Implementação e Melhorias Propostas
melhorias: automatizar a questao do docker-compose.yaml producao e densevolvimento




## 👨‍💻 Autor

Projeto desenvolvido por **Carlos Eduardo Medeiros da Silva** como parte do Desafio Técnico Lacrei Saúde.

-   **GitHub:** [Carlos98770](https://github.com/Carlos98770)
-   **Repositório do Projeto:** [github.com/Carlos98770/desafio-tecnico](https://github.com/Carlos98770/desafio-tecnico)