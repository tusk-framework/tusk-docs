# Integração: Engine e Framework

O **Tusk Engine** e o **Tusk Framework** foram desenhados para trabalhar em perfeita harmonia. O Engine provê um servidor web de altíssima performance em Go, enquanto o Framework constrói a lógica de negócio através de um container robusto no PHP. 

Diferente do ecossistema clássico (Apache + mod_php ou Nginx + PHP-FPM), o Tusk trabalha com o conceito de **Long-Lived Process** (Processos de Longa Duração).

## O Problema do "Boot-and-Die"

Em um servidor tradicional como o Apache, a cada nova requisição HTTP:
1. Um novo processo do PHP é criado.
2. O framework é inteiramente carregado na memória (autoloader, configurações, container de injeção de dependência).
3. A rota é resolvida e a resposta é gerada.
4. O processo PHP é destruído.

Esse ciclo (conhecido como *boot-and-die*) consome uma grande quantidade de recursos e adiciona latência, apenas para fazer o "boot" da aplicação.

## A Solução do Tusk

Com o Tusk, a sua aplicação faz o "boot" **apenas uma vez**.

O `tusk-engine` (em Go) gerencia um ou mais processos do PHP em background. Quando uma requisição HTTP chega ao servidor, o Go converte os dados da requisição para **NDJSON** (Newline Delimited JSON) e injeta diretamente no `STDIN` do processo PHP que já está rodando. O framework processa a requisição e devolve a resposta no `STDOUT`.

Isso significa que conexões de banco de dados, containers e rotas já estão prontos em memória!

## Como Funciona na Prática

Ao iniciar um projeto usando o Tusk Framework, você terá um arquivo chamado `worker.php` na raiz do seu projeto. Ele atua como a ponte entre o Engine e o Framework.

### O Arquivo `worker.php`

Um worker básico do Tusk tem a seguinte estrutura:

```php
<?php

// Requer o autoloader do Composer
require 'vendor/autoload.php';

use Tusk\Core\Container\Container;
use Tusk\Runtime\Kernel;
use Tusk\Runtime\Adapters\NativeLoopAdapter;

// Inicializa o Container de Injeção de Dependência
$container = new Container();

// Inicializa o Kernel informando que usaremos o NativeLoopAdapter (Comunicação NDJSON)
$kernel = new Kernel($container, new NativeLoopAdapter());

// O método start() é bloqueante! Ele cria o loop infinito que aguardará as requisições da Engine.
$kernel->start();
```

Ao rodar o comando `tusk start` no terminal, o Engine detecta o `tusk.json` (ou `composer.json`) e inicia automaticamente esse `worker.php`.

## Rodando em Produção (Docker)

Por ser uma arquitetura autocontida (onde o `tusk-engine` substitui o Apache/Nginx e o PHP-FPM), colocar o Tusk em produção com Docker é extremamente simples e resulta em imagens muito leves.

### Exemplo de Dockerfile

Aqui está um exemplo funcional usando a imagem Alpine do PHP CLI:

```dockerfile
# Usamos apenas a versão CLI do PHP (sem FPM, sem Apache)
FROM php:8.2-cli-alpine

# Instala a versão mais recente do Tusk Engine em Go
RUN curl -L https://github.com/tusk-framework/tusk-engine/releases/latest/download/tusk_Linux_x86_64.tar.gz | tar xz \
    && mv tusk /usr/local/bin/tusk \
    && chmod +x /usr/local/bin/tusk

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala as dependências de produção do Framework
RUN composer install --no-dev --optimize-autoloader

# Expõe a porta padrão que o tusk-engine usa
EXPOSE 8080

# Inicia o servidor de aplicação
CMD ["tusk", "start", "worker.php"]
```

Com esse Dockerfile, você tem um servidor web pronto para produção em um único container, consumindo o mínimo de RAM e oferecendo uma velocidade excepcional graças à comunicação NDJSON entre o Go e o PHP.
