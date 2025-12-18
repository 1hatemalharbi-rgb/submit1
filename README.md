```powershell
git clone https://github.com/1hatemalharbi-rgb/submit1.git
cd submit1
python -m pip install -r requirements.txt
uvicorn backend:app --port 8000
# open a SECOND PowerShell window and run:
streamlit run app.py