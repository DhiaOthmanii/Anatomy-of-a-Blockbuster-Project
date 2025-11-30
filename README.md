# 🎬 Blockbuster Anatomy — Movie Success Analysis  

Using *The Movies Dataset* (Kaggle)

This project explores the key factors that influence a movie’s financial and critical success.  
Using data from over 40,000 films, we analyze how **budget, genre, popularity, ratings, revenue, profit**,  
and **release year** interact to shape box office outcomes.

The project includes:

- ✔ Data cleaning & preprocessing pipeline  
- ✔ Exploratory data analysis (EDA) in Jupyter Notebook  
- ✔ Interactive **Streamlit dashboard**  
- ✔ Visualizations of trends across film history  
- ✔ ROI, genre performance, profitability, and correlations  

Dataset source:  
https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset


---

# 🛠️ Technology Stack

- **Python 3.8+**
- **Pandas** — data manipulation  
- **NumPy** — numerical operations  
- **Matplotlib / Seaborn** — data visualization  
- **Streamlit** — interactive dashboard  
- **Jupyter Notebook** — EDA presentation  
- **AST** — parsing JSON-like fields  
- **Virtual environment (venv)** — dependency isolation  

---

# ▶️ How to Run the Project

## 1. Create and activate virtual environment

### Windows (PowerShell)

powershell
python3 -m venv .venv source .venv/bin/activate


2. Install dependencies

pip install -r requirements.txt

3. Generate the cleaned dataset

python src/main.py

4. Run the Streamlit Dashboard

streamlit run dashboard/app.py

5. Run the Jupyter Notebook

Open Presentation.ipynb

📊 Visualizations Included

* Budget vs Revenue (log–log scale)

* ROI distribution (capped at 95th percentile)

* Average profit per year

* Top 10 genres by average revenue

* Rating vs revenue

* Correlation heatmap (budget, revenue, profit, ROI, ratings, etc.)

* Top 20 highest-grossing films

Each visualization includes a written interpretation.



💡 Key Insights

* Higher budgets usually lead to higher revenues — but with huge variability.

* ROI is extremely skewed: a few films generate massive returns.

* Profitability has increased over time with global markets.

* “Event” genres (Animation, Adventure, Fantasy, Action) dominate revenue.

* Ratings are not strong predictors of revenue.

* Visibility (vote count, popularity) matters more than ratings.

* Blockbusters consistently come from global franchises.

🚧 Limitations

* No marketing or advertising data (could improve revenue prediction).

* Streaming revenue and re-releases not included.

* Some original fields contain missing or inconsistent values.

🔜 Future Improvements

* Machine learning model to predict revenue or ROI


* Actor/director popularity metrics

* More advanced outlier detection

* Adding social media or sentiment data

* Profitability forecasting tool
