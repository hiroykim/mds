import zlib
import base64

data = "Life is too short, You need python." * 100
compress_data = zlib.compress(data.encode(encoding='utf-8'))
print(len(compress_data))  # 1077 출력
base64_en = base64.b64encode(compress_data)
print(len(base64_en))
print(base64_en)

compress_data = base64.b64decode(base64_en)
org_data = zlib.decompress(compress_data).decode('utf-8')
print(len(org_data))  # 350000 출력
print(org_data)
