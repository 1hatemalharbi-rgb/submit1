# open a PowerShell window and run:

cd ~
git clone https://github.com/1hatemalharbi-rgb/submit1.git
cd submit1
python -m pip install -r requirements.txt
uvicorn backend:app --port 8000

# open a SECOND PowerShell window and run:

cd ~\submit1
streamlit run app.py
