# Projeto Valgroup

## 📌 Descrição

O **Projeto Valgroup** tem como objetivo **baixar relatórios de funcionários**, **cadastrá-los em um sistema** e, logo após, **enviar por e-mail os resultados do cadastro**, indicando quais funcionários foram cadastrados com sucesso e quais apresentaram erro.

Após o processo de cadastro, o usuário deverá **retornar ao terminal de execução** para **preencher os dados necessários para o envio do e-mail** com os resultados.

---

## ⚙️ Pré-requisitos

* Windows
* Python instalado (versão recomendada: 3.10+)
* PowerShell

---

## 🍫 Instalando o Chocolatey (PowerShell)

Abra o **PowerShell como Administrador** e execute o comando abaixo:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; \
[System.Net.ServicePointManager]::SecurityProtocol = \
[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; \
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

Após a instalação, feche e abra novamente o PowerShell.

Verifique se o Chocolatey foi instalado corretamente:

```powershell
choco --version
```

---

## 🛠️ Instalando o Make com o Chocolatey

Com o Chocolatey instalado, execute:

```powershell
choco install make
```

Confirme a instalação:

```powershell
make --version
```

---

## 📋 Comandos disponíveis no Makefile

### 🔹 `make venv`

Cria um ambiente virtual Python:

```bash
python -m venv venv
```

Após a criação, **ative o ambiente virtual**:

```bash
source venv/Scripts/activate
```

---

### 🔹 `make install`

Instala as dependências do projeto:

```bash
python -m pip install -r config/requirements.txt
```

---

### 🔹 `make run`

Executa o projeto:

```bash
python -m src.main
```

Durante a execução, após o cadastro dos funcionários, o terminal solicitará o **preenchimento das informações para envio do e-mail** com os resultados.

---

## 🧹 Linter (Ruff)

O projeto utiliza o **Ruff** como linter.

Para verificar o código, execute apenas:

```bash
ruff check .
```

---

## ✅ Fluxo resumido de uso

```bash
make venv
source venv/Scripts/activate
make install
make run
```

Após a execução:

1. O relatório de funcionários é baixado
2. Os funcionários são cadastrados no sistema
3. Retorne ao terminal
4. Preencha os dados solicitados para envio do e-mail com os resultados

---

🚀 Projeto pronto para execução e validação de cadastros!
