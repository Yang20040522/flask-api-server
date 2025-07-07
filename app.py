from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)

# ✅ Azure SQL Server 資料庫設定
server = 'shoppingsystem666.database.windows.net'
database = 'ShoppingSystem'
username = 'systemgod666'
password = 'Crazydog888'
driver = '{ODBC Driver 17 for SQL Server}'

# 🔍 查詢產品（用 ProductID 查）
@app.route("/api/product", methods=["GET"])
def get_product():
    product_id = request.args.get("id")  # 改用 id 查詢
    if not product_id:
        return jsonify({"error": "請提供 id 參數"}), 400

    try:
        # 建立資料庫連線
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        cursor = conn.cursor()

        # 查詢 ProductID 對應的商品資料
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

# ✅ 啟動伺服器
if __name__ == "__main__":
    app.run(debug=True, port=5000)
