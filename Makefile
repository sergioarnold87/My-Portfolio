# Makefile for common developer tasks
CONDA_ENV=vmo-py310
CONDA_PYTHON=/home/sergio/anaconda3/envs/$(CONDA_ENV)/bin/python

.PHONY: help setup-conda install-deps generate streamlit clean

help:
	@echo "Makefile targets:"
	@echo "  setup-conda   - create conda env (python 3.10)"
	@echo "  install-deps  - install dependencies into conda env"
	@echo "  generate      - run synthetic data generator"
	@echo "  streamlit     - run the Streamlit app"
	@echo "  clean         - remove generated bronze CSVs"

setup-conda:
	@echo "Creating conda env '$(CONDA_ENV)' with python 3.10..."
	eval "$(conda shell.bash hook)" && conda create -y -n $(CONDA_ENV) python=3.10 pandas=2.1 numpy=1.25 faker -c conda-forge

install-deps:
	@echo "Installing dependencies into '$(CONDA_ENV)' (may take a while)..."
	eval "$(conda shell.bash hook)" && conda activate $(CONDA_ENV) && conda install -y -c conda-forge streamlit plotly scikit-learn sdv mlflow pyarrow matplotlib seaborn tsfresh xgboost catboost scipy || echo "Conda install failed (network or package conflict), try rerunning."

generate:
	@if [ -x "$(CONDA_PYTHON)" ]; then \
		$(CONDA_PYTHON) -m src.generate_data; \
	else \
		python3 -m src.generate_data; \
	fi

streamlit:
	eval "$(conda shell.bash hook)" && conda activate $(CONDA_ENV) && streamlit run app.py

clean:
	rm -f data/bronze/*.csv
