#!/usr/bin/env bash
# Convenience script to run and manage the project locally.
# Usage:
#   ./run_local.sh generate      # generate synthetic data
#   ./run_local.sh streamlit     # run the Streamlit app
#   ./run_local.sh install-deps  # install dependencies into conda env vmo-py310
#   ./run_local.sh help

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONDA_ENV_NAME="vmo-py310"
CONDA_PYTHON="/home/sergio/anaconda3/envs/${CONDA_ENV_NAME}/bin/python"

function ensure_conda() {
  if ! command -v conda >/dev/null 2>&1; then
    echo "Conda is not available in PATH. Install Miniconda/Anaconda or adjust this script." >&2
    exit 1
  fi
}

function install_deps() {
  ensure_conda
  echo "Installing runtime dependencies into conda env '${CONDA_ENV_NAME}' (may take a while)..."
  eval "$(conda shell.bash hook)"
  conda activate "${CONDA_ENV_NAME}"
  conda install -y -c conda-forge streamlit plotly scikit-learn sdv mlflow pyarrow matplotlib seaborn tsfresh xgboost catboost scipy || {
    echo "Conda install failed. Try rerunning or inspect network/connectivity. You can also install via pip inside a venv." >&2
    return 1
  }
  echo "Dependencies installed (or attempted)."
}

function generate() {
  if [ -x "${CONDA_PYTHON}" ]; then
    echo "Using conda env python: ${CONDA_PYTHON}"
    "${CONDA_PYTHON}" -m src.generate_data
  else
    echo "Conda env python not found at ${CONDA_PYTHON}. Falling back to system python (make sure dependencies are installed)."
    python3 -m src.generate_data
  fi
}

function run_streamlit() {
  eval "$(conda shell.bash hook)" && conda activate "${CONDA_ENV_NAME}" || true
  streamlit run app.py
}

case "${1:-help}" in
  generate)
    generate
    ;;
  streamlit)
    run_streamlit
    ;;
  install-deps)
    install_deps
    ;;
  help|*)
    echo "run_local.sh - helper script"
    echo "Usage: $0 {generate|streamlit|install-deps|help}"
    ;;
esac
