from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

# ✅ 測試首頁
@app.route('/')
def hello():
    return {'message': 'Flask API is running on Render!'}

# ✅ Azure SQL Server 資料庫設定
server = 'shoppingsystem666.database.windows.net'
database = 'ShoppingSystem'
username = 'systemgod666'
password = 'Crazydog888'
driver = '{ODBC Driver 17 for SQL Server}'

# 🔍 查詢產品（用 ProductID 查）
@app.route("/api/product", methods=["GET"])
def get_product():
    product_id = request.args.get("id")
    if not product_id:
        return jsonify({"error": "請提供 id 參數"}), 400

    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        cursor = conn.cursor()

        query = """
            SELECT ProductID, Category, SubCategory, ProductName, Brand
            FROM dbo.Products
            WHERE ProductID = ?
        """
        cursor.execute(query, (product_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            result = {
                "ProductID": row[0],
                "Category": row[1],
                "SubCategory": row[2],
                "ProductName": row[3],
                "Brand": row[4]
            }
            return jsonify(result)
        else:
            return jsonify({"message": "查無商品"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ 啟動伺服器（Render 會自動處理，不用加 port）
if __name__ == "__main__":
    app.run()
