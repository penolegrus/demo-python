import os
import re

def patch_imports(grpc_gen_dir):
    for fname in os.listdir(grpc_gen_dir):
        if fname.endswith('.py'):
            path = os.path.join(grpc_gen_dir, fname)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Патчим только строки import *_pb2 as *_pb2
            new_content = re.sub(
                r'^import (\w+_pb2) as (\w+__\w+__pb2)$',
                r'from grpc_gen import \1 as \2',
                content,
                flags=re.MULTILINE
            )
            if new_content != content:
                print(f"Patched imports in {fname}")
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

if __name__ == "__main__":
    patch_imports(os.path.dirname(__file__)) 