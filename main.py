import os
import psycopg2
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# 连接 Supabase PostgresSQL
def connect_db():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        print("ERROR: DATABASE_URL is not set!")
        return None
    try:
        return psycopg2.connect(DATABASE_URL, sslmode='prefer')
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

@app.route('/', methods=['GET', 'HEAD'])
def index():
    if request.method == 'HEAD':
        return '', 200  # 处理 HEAD 请求，避免报错
    return render_template('index.html')


@app.route('/get_acupoints', methods=['GET'])
def get_acupoints():
    meridian = request.args.get('meridian')
    category = request.args.get('category')

    # ✅ 添加日志，确保参数传递正确
    print(f"📌 Received request: meridian={meridian}, category={category}")

    if not meridian or not category:
        return jsonify({"error": "Missing required parameters: meridian or category"}), 400

    conn = connect_db()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        query = "SELECT name, code, indications, pairing, pairing_code FROM acupoints WHERE meridian=%s AND category=%s"
        cursor.execute(query, (meridian, category))
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        acupoints = [{'name': d[0], 'code': d[1], 'indications': d[2], 'pairing': d[3], 'pairing_code': d[4]} for d in
                     data]

        return jsonify({"status": "success", "acupoints": acupoints})

    except Exception as e:
        print(f" 查询数据库失败: {e}")
        return jsonify({"error": "Database query failed"}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render 可能分配端口 10000
    app.run(host='0.0.0.0', port=port, debug=True)
