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

# 🔍 查詢產品（用條碼 barcode 查）
@app.route("/api/product", methods=["GET"])
def get_product():
    barcode = request.args.get("barcode")
    if not barcode:
        return jsonify({"error": "請提供 barcode 參數"}), 400

    try:
        # 建立資料庫連線
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        cursor = conn.cursor()

        # 執行查詢
        query = "SELECT * FROM dbo.Products WHERE barcode = ?"
        cursor.execute(query, (barcode,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            # 請根據你的欄位順序修改下列欄位（假設為 id, name, barcode, price）
            result = {
                "id": row[0],
                "name": row[1],
                "barcode": row[2],
                "price": float(row[3])
            }
            return jsonify(result)
        else:
            return jsonify({"message": "查無商品"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ 啟動伺服器
if __name__ == "__main__":
    app.run(debug=True, port=5000)
