
import hashlib
import urllib.parse
import json
import uuid

class Hmac:
    @staticmethod
    def create(data, key, algo='sha256'):
        if algo not in hashlib.algorithms_available:
            return False
        
        data = Hmac.stringify(data)
        sorted_data = Hmac.sort(data)
        serialized_data = json.dumps(sorted_data, ensure_ascii=False).encode('utf-8')
        
        h = hashlib.new(algo)
        h.update(serialized_data)
        h.update(key.encode('utf-8'))  # Использование ключа для хеширования
        return h.hexdigest()

    @staticmethod
    def verify(data, key, sign, algo='sha256'):
        computed_sign = Hmac.create(data, key, algo)
        return computed_sign and computed_sign.lower() == sign.lower()

    @staticmethod
    def sort(data):
        if isinstance(data, dict):
            return {k: Hmac.sort(v) for k, v in sorted(data.items())}
        elif isinstance(data, list):
            return [Hmac.sort(v) for v in data]
        else:
            return data

    @staticmethod
    def stringify(data):
        def stringify_helper(obj):
            if isinstance(obj, (int, float)):
                return str(obj)
            elif isinstance(obj, str):
                return obj
            elif isinstance(obj, dict):
                return {k: stringify_helper(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [stringify_helper(v) for v in obj]
            else:
                return str(obj)
        
        return stringify_helper(data)