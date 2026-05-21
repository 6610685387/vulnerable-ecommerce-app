import os
import re
from app import create_app

def get_port_from_config():
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'config.js')
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'TARGET_PORT\s*=\s*(\d+)', content)
            if match:
                return int(match.group(1))
    except Exception as e:
        pass
    return 5000

app = create_app()

if __name__ == '__main__':
    port = get_port_from_config()
    app.run(debug=True, host="0.0.0.0", port=port)