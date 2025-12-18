open a PowerShell window and run:

```powershell
cd ~
git clone https://github.com/1hatemalharbi-rgb/submit1.git
cd submit1
python -m pip install -r requirements.txt
uvicorn backend:app --port 8000
##open a second Powershell window and run:
cd ~\submit1
streamlit run app.py
