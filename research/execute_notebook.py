"""Execute every notebook cell in a fresh kernel; fail on error or timeout."""
from pathlib import Path
import os
import sys
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parent
output = Path(sys.argv[1] if len(sys.argv)>1 else root/'artifacts').resolve()
output.mkdir(parents=True, exist_ok=True)
nb = nbformat.read(root/'01_strategy_research.ipynb', as_version=4)
nbformat.validate(nb)
# The executing interpreter's environment must own the kernel, not a stale system kernelspec.
from jupyter_client.kernelspec import KernelSpecManager
import tempfile
with tempfile.TemporaryDirectory(prefix='asnya-kernel-') as temporary:
    import json
    kernel = Path(temporary)/'python3'
    kernel.mkdir()
    (kernel/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],'display_name':'Asnya Python','language':'python'}))
    manager = KernelSpecManager(kernel_dirs=[temporary])
    from jupyter_client import AsyncKernelManager
    km = AsyncKernelManager(kernel_name='python3', kernel_spec_manager=manager)
    client = NotebookClient(nb, timeout=120, allow_errors=False, kernel_name='python3', km=km,
                            resources={'metadata':{'path':str(output)}})
    client.execute()
nbformat.write(nb, output/'01_strategy_research.executed.ipynb')
artifacts=output/'artifacts'
for name in ['manifest.json','training_ranking.csv','held_out_returns.csv','held_out_equity.png']:
    assert (artifacts/name).stat().st_size>0, name
print('PASS: all notebook cells executed; outputs in', output)
