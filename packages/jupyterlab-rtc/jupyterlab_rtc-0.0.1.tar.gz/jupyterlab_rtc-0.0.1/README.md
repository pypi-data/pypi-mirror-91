# Jupyter RTC with Automerge

This folder contains (WIP) implementation for Jupyter Real Time Collaboration with [Automerge](https://github.com/automerge/automerge) CRDT Library.

### makefile

You can use the provided `Makefile` to simplify development.

```sh
make install
make build
make start-node
```

### Run manually

- install 
```bash
conda env create -f environment.yml && \
  conda activate jupyter-rtc
cd rust && \
  make all && \
  pip list | grep glootalk && \
  cd ./../externals
git clone https://github.com/datalayer-contrib/automerge automerge-wasm-bundler && \
  cd automerge-wasm-bundler && \
  git checkout wasm-bundler && \
  cd ./..
git clone https://github.com/datalayer-contrib/automerge automerge-wasm-nodejs && \
  cd automerge-wasm-nodejs && \
  git checkout wasm-nodejs && \
  cd ./../..
yarn && \
  yarn build
pip install -e .
```

- build
```bash
# Build JupyterLab Extension.
conda activate jupyter-rtc
cd packages/jupyterlab-rtc
jupyter labextension develop --overwrite
jupyter labextension list
cd ../..
```

- start all (equiv. of `make start-node`)
```bash
# Start JupyterLab, Node.js Server and TextArea UI.
conda activate jupyter-rtc
yarn dev
open http://localhost:8888/lab
open http://localhost:3001
open http://localhost:4321
```


- Start JupyterLab only
```bash
conda activate jupyter-rtc
jupyter lab \
  --watch \
  --ServerApp.jpserver_extensions="{'jupyterlab_rtc': True}" \
  --ServerApp.allow_origin="*" \
  --ServerApp.token=
open http://localhost:8888/lab
open http://localhost:8888/jupyterlab_rtc/default
```

- If you don't need JupyterLab, start Jupyter Server.
```bash
conda activate jupyter-rtc
jupyter server \
  --ServerApp.jpserver_extensions="{'jupyterlab_rtc': True}" \
  --ServerApp.allow_origin="*"
```

- start Start the TextArea application.
```bash
conda activate jupyter-rtc
yarn textarea:start
open http://localhost:3001
```
