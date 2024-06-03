from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST' and 'file' in request.files:
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            try:
                # Save uploaded file
                uploaded_file.save(uploaded_file.filename)
                
                # Process the uploaded file
                uploaded_data = pd.read_excel(uploaded_file.filename) # Assuming XLSX format
                processed_data = perform_abc_analysis(uploaded_data)
                
                # Generate processed data
                processed_data.to_csv('processed_data.csv', index=False)
                
                # Send data to frontend
                return jsonify({"status": "success", "message": "File uploaded and processed successfully."})
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)})
        else:
            return jsonify({"status": "error", "message": "No file selected."})
    return 'No file uploaded'

def perform_abc_analysis(data):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    df = uploaded_data
    # df.head()

    df1 = df.drop(['Invoice', 'Customer ID', 'Country'], axis = 'columns')
    # df1

    df1['Revenue'] = df1['Quantity'] * df1['Price']
    # df1.head()

    df1['InvoiceDate'] = pd.to_datetime(df1['InvoiceDate'])
    # df1

    df1['Year'] = pd.DatetimeIndex(df1['InvoiceDate']).year
    df1['Month'] = pd.DatetimeIndex(df1['InvoiceDate']).month
    # df1.head()

    df2=df1.groupby(['StockCode','Year','Month'])['Revenue'].sum().to_frame().reset_index()
    df2["Month"] = df2.Month.map("{:02}".format)
    # df2.head(10)

    df2['year_month']=df2['Year'].map(str) + '-' + df2['Month'].map(str)
    # df2.tail()

    df2 = df2.pivot(index='StockCode',columns='year_month', values='Revenue').reset_index().fillna(0)
    # df2.head()

    df2['total_sales'] = df2.iloc[:,1:13].sum(axis=1,numeric_only=True)
    # df2.tail()

    df3 = df2.groupby('StockCode').agg(total_revenue=('total_sales','sum')).sort_values(by='total_revenue', ascending=False).reset_index()
    # df3

    df3['rev_cum_sum'] = df3['total_revenue'].cumsum()
    df3['rev_all'] =df3['total_revenue'].sum()
    df3['sku_rev_percent'] = df3['rev_cum_sum']/df3['rev_all']
    # df3.head(19)

    def condition_abc(x):
        if x>0 and x<=0.80:
            return "A"
        elif x>0.80 and x<=0.90:
            return "B"
        else:
            return 'C'


    df3['ABC']=df3['sku_rev_percent'].apply(condition_abc)
    # print(df3.head(12))

    df4 = df3.drop(['total_revenue', 'rev_cum_sum','rev_all','sku_rev_percent'], axis = 'columns')
    # Placeholder logic for ABC analysis
    # Assume data is a pandas DataFrame
    # Categorize items into A, B, and C based on certain criteria
    # Return processed data
    processed_data = df3.drop(['total_revenue', 'rev_cum_sum','rev_all','sku_rev_percent'], axis = 'columns')  # Placeholder
    return processed_data

if __name__ == '__main__':
    app.run(debug=True)
