PYTHON := python
PIP := pip
PROJECT_NAME := projeto_valgroup
VENV_DIR := venv
VENV_PYTHON := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_DIR)/bin/pip
MODULE := src.main
REQ_FILE := config/requirements.txt

venv: # Cria o ambiente virtual do projeto

	@echo "Criando ambiente virtual..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Ambiente virtual criado em $(VENV_DIR)"
	@echo "Para ativar o ambiente virtual no tetrminal digite:"
	@echo "$(VENV_DIR)/Scripts/activate (No Windows)" 

run: # Executa a aplicação

	$(PYTHON) -m $(MODULE)

install: # Instala as dependencias

	@echo "Instalando dependencias..."
	$(PYTHON) -m pip install -r $(REQ_FILE)
	@echo "Dependencias instaladas com sucesso!!"

.PHONY: run install venv