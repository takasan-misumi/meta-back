import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# CORS設定を更新 
CORS(app, resources={
    r"/api/*": {"origins": ["https://tech0-gen-8-step3-app-node-5.azurewebsites.net"]},
    r"/static/*": {"origins": ["https://tech0-gen-8-step3-app-node-5.azurewebsites.net"]}
})

# In-memory store data
stores = [
    {
        'id': 1,
        'name': "コストコ",
        'description': "大容量・大満足の会員制スーパーです。\nここならではの商品が沢山あり、面白いです。",
        'image': "/public/images/costco.jpg",  # 修正済み
        'votes': 60,
        'type': "retail"
    },
    {
        'id': 2, 
        'name': "ロピア",
        'description': "出来立てピザを筆頭にプライベートブランドを多数保有しているスーパーです。",
        'image': "/public/images/ロピア.jpg",  # 修正済み
        'votes': 30,
        'type': "retail"
    },
    {
        'id': 3,
        'name': "成城石井",
        'description': "ブランド力のあるプライベートブランドを多数取り揃えています。",
        'image': "/public/images/成城石井店舗.png",  # 修正済み
        'votes': 10,
        'type': "retail"
    },
    {
        'id': 4,
        'name': "ボンラパス", 
        'description': "高級ブランドを取りそろえた物ばかりが集まっています。お値段以上です。",
        'image': "/static/images/ボンラパス店舗.jpg",  # 修正済み
        'votes': 10,
        'type': "retail"
    },
    {
        'id': 5,
        'name': "西部ガスグループ",
        'description': "西部ガスグループの飲食店舗です。",
        'image': "/static/images/saibugas.png",  # 修正済み
        'votes': 100,
        'type': "restaurant"
    },
    {
        'id': 6,
        'name': "鈴懸",
        'description': "鈴の最中が有名な高級和菓子店です。",
        'image': "/static/images/鈴懸.jpg",  # 修正済み
        'votes': 33,
        'type': "restaurant"
    }
]

@app.route('/')
def index():
    return 'Welcome to the Store API'

# Fetch all stores
@app.route('/api/stores', methods=['GET'])
def get_stores():
    return jsonify(stores)
    
# 静的ファイルへのアクセスを提供
@app.route('/public/images/<path:filename>')
def static_files(filename):
    static_folder = os.path.join(os.path.dirname(__file__), 'static/images')
    return send_from_directory(static_folder, filename)

# Handle voting
@app.route('/api/vote/<int:store_id>', methods=['POST'])
def vote(store_id):
    data = request.get_json()
    increment = data.get('increment', True)
    
    # Find the store by ID
    store = next((store for store in stores if store['id'] == store_id), None)
    if store is None:
        return jsonify({'error': 'Store not found'}), 404
        
    # Update votes based on increment flag
    if increment:
        store['votes'] = min(store['votes'] + 1, 100)
    else:
        store['votes'] = max(store['votes'] - 1, 0)
    
    return jsonify({'success': True, 'votes': store['votes']})

if __name__ == '__main__': 
  # 環境変数PORTを取得（デフォルトは8000） 
  port = int(os.environ.get('PORT', 8000)) 
  # デバッグモードをローカル環境では有効に、本番では無効に 
  app.run(host='0.0.0.0', port=port, debug=False)
