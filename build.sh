[[ ! -d venv ]] && python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
[[ -d _build ]] && rm -rf _build
make html
deactivate
