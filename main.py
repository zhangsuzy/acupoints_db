import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# 连接 Supabase PostgreSQL
DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL, sslmode='prefer')


@app.route('/', methods=['GET', 'HEAD'])
def index():
        if request.method == 'HEAD':
            return '', 200  # 处理 HEAD 请求，避免报错
        return render_template('index.html')

@app.route('/get_acupoints', methods=['GET'])
def get_acupoints():
    meridian = request.args.get('meridian')
    category = request.args.get('category')

    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT name, code, indications, pairing, pairing_code FROM acupoints WHERE meridian=? AND category=?"
    cursor.execute(query, (meridian, category))
    data = cursor.fetchall()
    conn.close()

    acupoints = [{
        'name': d[0],
        'code': d[1],
        'indications': d[2],
        'pairing': d[3],
        'pairing_code': d[4]
    } for d in data]

    return jsonify(acupoints)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 1888))
    app.run(host='0.0.0.0', port=port, debug=True)
