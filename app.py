from flask import Flask, request, jsonify
from flask_cors import CORS
import pymssql  # ✅ 改用 pymssql

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return {'message': 'Flask API is running on Render!'}

# ✅ pymssql 資料庫連線設定
server = 'shoppingsystem666.database.windows.net'
database = 'ShoppingSystem'
username = 'systemgod666'
password = 'Crazydog888'

@app.route("/api/product", methods=["GET"])
def get_product():
    product_id = request.args.get("id")
    if not product_id:
        return jsonify({"error": "請提供 id 參數"}), 400

    try:
        # ✅ 改為 pymssql 連線
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        cursor = conn.cursor()

        query = """
            SELECT ProductID, Category, SubCategory, ProductName, Brand
            FROM dbo.Products
            WHERE ProductID = %s
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
