# Github: https://github.com/batmanpriv 
# Telegram: @BatmanPriv

import os
import sys
import zlib
import gzip
import lzma
import base64
import marshal
import py_compile
import random
import string
import threading
import time
import ast
import hashlib
import subprocess
import bz2
import secrets
import importlib
from typing import Callable, Union, Any, Optional

def _ensure_crypto():
    try:
        from Crypto.Cipher import AES, ChaCha20, Salsa20
        from Crypto.Util.Padding import pad
        from Crypto.Protocol.KDF import scrypt
        from Crypto.Random import get_random_bytes
        return AES, ChaCha20, Salsa20, pad, scrypt, get_random_bytes
    except ImportError:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pycryptodome', '-q', '--no-cache-dir'], timeout=20)
        except:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pycryptodome', '--no-cache-dir'], timeout=20)
            except:
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pycryptodomex', '-q', '--no-cache-dir'], timeout=20)
                except:
                    pass
        try:
            from Crypto.Cipher import AES, ChaCha20, Salsa20
            from Crypto.Util.Padding import pad
            from Crypto.Protocol.KDF import scrypt
            from Crypto.Random import get_random_bytes
            return AES, ChaCha20, Salsa20, pad, scrypt, get_random_bytes
        except ImportError:
            try:
                from Cryptodome.Cipher import AES, ChaCha20, Salsa20
                from Cryptodome.Util.Padding import pad
                from Cryptodome.Protocol.KDF import scrypt
                from Cryptodome.Random import get_random_bytes
                return AES, ChaCha20, Salsa20, pad, scrypt, get_random_bytes
            except ImportError:
                print("[!] pycryptodome not installed. Please install manually: pip install pycryptodome")
                sys.exit(1)

AES, ChaCha20, Salsa20, pad, scrypt, get_random_bytes = _ensure_crypto()

COLOR = {
    'red': '\033[00;31m',
    'green': '\033[00;32m',
    'lgreen': '\033[01;32m',
    'yellow': '\033[01;33m',
    'lred': '\033[01;31m',
    'blue': '\033[94m',
    'purple': '\033[01;35m',
    'cyan': '\033[00;36m',
    'gray': '\033[90m',
    'brown': '\033[38;5;130m'
}

SYMBOL = {
    'success': f'{COLOR["red"]}[{COLOR["green"]}+{COLOR["red"]}]{COLOR["green"]}',
    'error': f'{COLOR["red"]}[{COLOR["lred"]}-{COLOR["red"]}]{COLOR["lred"]}'
}

class EncryptorError(Exception):
    pass

class EnvironmentValidator:
    @staticmethod
    def validate_python_version() -> str:
        version = sys.version_info
        if version[0] == 2:
            return "raw_input('%s')"
        elif version[0] == 3:
            return "input('%s')"
        raise EncryptorError("Python version not supported")

    @staticmethod
    def validate_imports() -> None:
        required_modules = ['os', 'sys', 'zlib', 'gzip', 'lzma', 'base64', 'marshal', 'py_compile', 'random', 'string', 'threading', 'time', 'ast', 'hashlib', 'bz2', 'secrets']
        for module in required_modules:
            try:
                __import__(module)
            except ImportError as e:
                raise EncryptorError(f"Module {module} not found: {e}\nInstall with: pip install {module}")

class CodecEngine:
    def __init__(self):
        self.encoders = {
            'zlib': zlib.compress,
            'gzip': gzip.compress,
            'lzma': lzma.compress,
            'base16': base64.b16encode,
            'base32': base64.b32encode,
            'base64': base64.b64encode,
            'marshal': lambda x: marshal.dumps(compile(x, '<x>', 'exec'))
        }
        
        self.decoders = {
            'zlib': zlib.decompress,
            'gzip': gzip.decompress,
            'lzma': lzma.decompress,
            'base16': base64.b16decode,
            'base32': base64.b32decode,
            'base64': base64.b64decode,
            'marshal': marshal.loads
        }
        
        self.encoding_map = {
            1: ('marshal',),
            2: ('zlib',),
            3: ('base16',),
            4: ('base32',),
            5: ('base64',),
            6: ('lzma',),
            7: ('gzip',),
            8: ('zlib', 'base16'),
            9: ('zlib', 'base32'),
            10: ('zlib', 'base64'),
            11: ('gzip', 'base16'),
            12: ('gzip', 'base32'),
            13: ('gzip', 'base64'),
            14: ('lzma', 'base16'),
            15: ('lzma', 'base32'),
            16: ('lzma', 'base64'),
            17: ('marshal', 'zlib'),
            18: ('marshal', 'gzip'),
            19: ('marshal', 'lzma'),
            20: ('marshal', 'base16'),
            21: ('marshal', 'base32'),
            22: ('marshal', 'base64'),
            23: ('marshal', 'zlib', 'base16'),
            24: ('marshal', 'zlib', 'base32'),
            25: ('marshal', 'zlib', 'base64'),
            26: ('marshal', 'lzma', 'base16'),
            27: ('marshal', 'lzma', 'base32'),
            28: ('marshal', 'lzma', 'base64'),
            29: ('marshal', 'gzip', 'base16'),
            30: ('marshal', 'gzip', 'base32'),
            31: ('marshal', 'gzip', 'base64'),
            32: ('marshal', 'zlib', 'lzma', 'base16'),
            33: ('marshal', 'zlib', 'lzma', 'base32'),
            34: ('marshal', 'zlib', 'lzma', 'base64'),
            35: ('marshal', 'zlib', 'gzip', 'base16'),
            36: ('marshal', 'zlib', 'gzip', 'base32'),
            37: ('marshal', 'zlib', 'gzip', 'base64'),
            38: ('marshal', 'zlib', 'lzma', 'gzip', 'base16'),
            39: ('marshal', 'zlib', 'lzma', 'gzip', 'base32'),
            40: ('marshal', 'zlib', 'lzma', 'gzip', 'base64')
        }

    def build_encoding_chain(self, option: int) -> tuple:
        return self.encoding_map.get(option, ())

    def encode_data(self, data: str, encoding_chain: tuple) -> bytes:
        encoded = data.encode('utf-8')
        for encoder_name in encoding_chain:
            encoded = self.encoders[encoder_name](encoded)
        return encoded[::-1]

    def build_decoder_chain(self, encoding_chain: tuple) -> str:
        reverse_chain = encoding_chain[::-1]
        decoder_parts = []
        
        for decoder_name in reverse_chain:
            if decoder_name == 'marshal':
                decoder_parts.append(f"self.decoders['{decoder_name}']")
            else:
                decoder_parts.append(f"self.decoders['{decoder_name}']")
        
        decoder_expr = "("
        for i, decoder in enumerate(reverse_chain):
            if i == 0:
                decoder_expr += f"self.decoders['{decoder}']("
            else:
                decoder_expr += f"self.decoders['{decoder}']("
        decoder_expr += "__[::-1]" + ")" * len(reverse_chain)
        
        return f"__import__('base64').b64decode({decoder_expr})" if 'base64' in reverse_chain else decoder_expr

class XOREngine:
    @staticmethod
    def rand_var(length: int = 10) -> str:
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    @staticmethod
    def xor_encrypt(data: bytes, key: bytes) -> bytes:
        return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
    
    @staticmethod
    def xor_decrypt(data: bytes, key: bytes) -> bytes:
        return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
    
    @classmethod
    def deep_xor_obfuscate(cls, code: str, key: Optional[bytes] = None, layers: int = 4) -> str:
        if key is None:
            key = os.urandom(16)
        
        compressed = zlib.compress(code.encode())
        encrypted = cls.xor_encrypt(compressed, key)
        encoded = base64.b64encode(encrypted).decode()
        
        var_data = cls.rand_var()
        var_key = cls.rand_var()
        var_xor = cls.rand_var()
        var_check = cls.rand_var()
        var_thread = cls.rand_var()
        
        stub = f'''
import base64 as b64, zlib as zl, marshal as ms, sys, threading, time, os

def {var_xor}(d,k):
    return bytes([b ^ k[i % len(k)] for i,b in enumerate(d)])

def {var_check}():
    start = time.time()
    for _ in range(100000): pass
    if time.time() - start > 0.5:
        sys.exit()
    if hasattr(sys, 'gettrace') and sys.gettrace():
        sys.exit()
    try:
        import pydevd, traceback, pdb, inspect
        sys.exit()
    except:
        pass
    try:
        import subprocess, psutil
        for proc in psutil.process_iter():
            if 'debug' in proc.name().lower():
                sys.exit()
    except:
        pass

{var_check}()
def {var_thread}():
    while True:
        pass
threading.Thread(target={var_thread}, daemon=True).start()

{var_data} = "{encoded}"
{var_key} = {repr(key)}
exec(compile(zl.decompress({var_xor}(b64.b64decode({var_data}), {var_key})), "<decrypted>", "exec"))
'''
        
        wrapped = compile(stub, "<xored>", "exec")
        for _ in range(layers):
            wrapped = compile(f"exec(marshal.loads({repr(marshal.dumps(wrapped))}))", "<layer>", "exec")
        
        return f"import marshal\nexec(marshal.loads({repr(marshal.dumps(wrapped))}))"

class ASTObfuscator:
    @staticmethod
    def _rand_ident(prefix="_", length=8):
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return prefix + "".join(random.choice(alphabet) for _ in range(length))
    
    class VariableCollector(ast.NodeVisitor):
        def __init__(self):
            self.assigned = set()
            self.globals = set()
            self.args = set()
        def visit_Global(self, node):
            self.globals.update(node.names)
        def visit_Name(self, node):
            if isinstance(node.ctx, ast.Store):
                self.assigned.add(node.id)
        def visit_arg(self, node):
            self.args.add(node.arg)
            self.assigned.add(node.arg)
    
    class VariableRenamer(ast.NodeTransformer):
        def __init__(self, assigned, args, globals_):
            self.rename = set(assigned) - set(args) - set(globals_)
            self.map = {}
        def _new(self, name):
            return "v_" + hashlib.shake_128(name.encode()).hexdigest(8)
        def visit_Name(self, node):
            if node.id in self.rename:
                if node.id not in self.map:
                    self.map[node.id] = self._new(node.id)
                node.id = self.map[node.id]
            return node
    
    class ControlFlowFlattener(ast.NodeTransformer):
        BLOCKED = (ast.Return, ast.Yield, ast.YieldFrom, ast.Try, ast.With, ast.Break, ast.Continue, ast.AsyncFunctionDef, ast.Global, ast.Nonlocal)
        def visit_FunctionDef(self, node):
            self.generic_visit(node)
            if any(isinstance(n, self.BLOCKED) for n in ast.walk(node)):
                return node
            if any(isinstance(n, ast.FunctionDef) for n in node.body):
                return node
            original = list(node.body)
            if not original:
                return node
            new_body = []
            state = f"_st_{random.randint(1000, 9999)}"
            new_body.append(ast.Assign(targets=[ast.Name(state, ast.Store())], value=ast.Constant(0)))
            while_body = []
            for i, stmt in enumerate(original):
                while_body.append(ast.If(test=ast.Compare(ast.Name(state, ast.Load()), [ast.Eq()], [ast.Constant(i)]), body=[stmt, ast.AugAssign(ast.Name(state, ast.Store()), ast.Add(), ast.Constant(1))], orelse=[]))
            new_body.append(ast.While(test=ast.Compare(ast.Name(state, ast.Load()), [ast.Lt()], [ast.Constant(len(original))]), body=while_body, orelse=[]))
            new_body.append(ast.Return(ast.Constant(None)))
            node.body = new_body
            return node
    
    class StringEncryptor(ast.NodeTransformer):
        def __init__(self, key, decrypt_func):
            self.key = key
            self.decrypt_func = decrypt_func
            self.in_fstring = False
        def visit_JoinedStr(self, node):
            self.in_fstring = True
            self.generic_visit(node)
            self.in_fstring = False
            return node
        def _encrypt(self, data: bytes):
            iv = os.urandom(16)
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return iv + cipher.encrypt(pad(data, 16))
        def visit_Constant(self, node):
            if self.in_fstring:
                return node
            if isinstance(node.value, str):
                enc = self._encrypt(node.value.encode())
                return ast.Call(ast.Name(self.decrypt_func, ast.Load()), [ast.Constant(enc)], [])
            if isinstance(node.value, (bytes, bytearray)):
                enc = self._encrypt(bytes(node.value))
                return ast.Call(ast.Name(self.decrypt_func, ast.Load()), [ast.Constant(enc)], [])
            return node
    
    @classmethod
    def obfuscate(cls, code: str, key: bytes) -> tuple:
        decrypt_str = cls._rand_ident("_ds_")
        decrypt_bytes = cls._rand_ident("_db_")
        
        tree = ast.parse(code)
        vc = cls.VariableCollector()
        vc.visit(tree)
        
        for t in (cls.ControlFlowFlattener(), cls.VariableRenamer(vc.assigned, vc.args, vc.globals), cls.StringEncryptor(key, decrypt_str)):
            tree = t.visit(tree)
            ast.fix_missing_locations(tree)
        
        return marshal.dumps(compile(tree, "<obf>", "exec")), decrypt_str, decrypt_bytes

class CJKObfuscator:
    _KOR = [i for i in range(0xAC00, 0xD7A3) if chr(i).isprintable() and chr(i).isidentifier()]
    _CHI = [i for i in range(0x4E00, 0x9FFF) if chr(i).isprintable() and chr(i).isidentifier()]
    _JPN = [i for i in range(0x3040, 0x30FF) if chr(i).isprintable() and chr(i).isidentifier()]
    
    @staticmethod
    def _vk(n=11): return ''.join(random.choices([chr(i) for i in CJKObfuscator._KOR], k=n))
    @staticmethod
    def _vc(n=11): return ''.join(random.choices([chr(i) for i in CJKObfuscator._CHI], k=n))
    @staticmethod
    def _vj(n=11): return ''.join(random.choices([chr(i) for i in CJKObfuscator._JPN], k=n))
    @staticmethod
    def _vm(n=14): return ''.join(random.choices([chr(i) for i in (CJKObfuscator._KOR + CJKObfuscator._CHI + CJKObfuscator._JPN)], k=n))
    
    @staticmethod
    def _cjk_str(n=80):
        return ''.join(chr(random.randint(0x4E00, 0x9FFF)) for _ in range(n))
    
    @staticmethod
    def _ast_arg(name):
        return ast.arguments(posonlyargs=[], args=[ast.arg(arg=name)],
            vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[])
    
    @staticmethod
    def _ast_junk():
        v1, v2, v3 = CJKObfuscator._vk(), CJKObfuscator._vk(), CJKObfuscator._vk()
        t = random.randint(0, 9)
        if t == 0:
            return ast.Assign(targets=[ast.Name(v1, ast.Store())],
                value=ast.ListComp(ast.BinOp(ast.Name(v2, ast.Load()), ast.BitXor(), ast.Constant(random.randint(1,255))),
                [ast.comprehension(ast.Name(v2, ast.Store()), ast.Call(ast.Name('range',ast.Load()),[ast.Constant(random.randint(10,60))],[]), [],0)]), lineno=0)
        elif t == 1:
            return ast.Assign(targets=[ast.Name(v1, ast.Store())],
                value=ast.DictComp(ast.Name(v2, ast.Load()), ast.BinOp(ast.Name(v2,ast.Load()),ast.Mult(),ast.Constant(random.randint(2,99))),
                [ast.comprehension(ast.Name(v2,ast.Store()), ast.Call(ast.Name('range',ast.Load()),[ast.Constant(random.randint(5,30))],[]), [],0)]), lineno=0)
        elif t == 2:
            return ast.Assign(targets=[ast.Name(v1,ast.Store())],
                value=ast.List([ast.Constant(random.randint(0,9999)) for _ in range(random.randint(5,20))],ast.Load()), lineno=0)
        elif t == 3:
            return ast.Assign(targets=[ast.Name(v1,ast.Store())],
                value=ast.Lambda(CJKObfuscator._ast_arg(v2), ast.BinOp(ast.Name(v2,ast.Load()),ast.Add(),ast.Constant(random.randint(1,9999)))), lineno=0)
        elif t == 4:
            return ast.For(ast.Name(v1,ast.Store()), ast.Call(ast.Name('range',ast.Load()),[ast.Constant(0)],[]), [ast.Pass()],[],lineno=0)
        elif t == 5:
            n = random.randint(100,9999)
            return ast.Assign(targets=[ast.Name(v1,ast.Store())],
                value=ast.BinOp(ast.BinOp(ast.Constant(n*7),ast.BitXor(),ast.Constant(n*3)), ast.Add(),ast.Constant(random.randint(0,255))), lineno=0)
        elif t == 6:
            return ast.Assign(targets=[ast.Name(v1,ast.Store())],
                value=ast.Lambda(CJKObfuscator._ast_arg(v2),ast.Lambda(CJKObfuscator._ast_arg(v3), ast.BinOp(ast.Name(v2,ast.Load()),ast.Mult(),ast.Name(v3,ast.Load())))), lineno=0)
        elif t == 7:
            rows,cols = random.randint(2,5),random.randint(2,8)
            return ast.Assign(targets=[ast.Name(v1,ast.Store())],
                value=ast.ListComp(ast.ListComp(ast.BinOp(ast.Name(v2,ast.Load()),ast.BitXor(),ast.Constant(random.randint(1,127))),
                [ast.comprehension(ast.Name(v2,ast.Store()), ast.Call(ast.Name('range',ast.Load()),[ast.Constant(cols)],[]), [],0)]),
                [ast.comprehension(ast.Name(v3,ast.Store()), ast.Call(ast.Name('range',ast.Load()),[ast.Constant(rows)],[]), [],0)]), lineno=0)
        else:
            return ast.Assign(targets=[ast.Name(v1,ast.Store())],
                value=ast.Constant(random.choice([True,False,None,'',0,1,-1])), lineno=0)
    
    @staticmethod
    def _ast_many(n=18): return [CJKObfuscator._ast_junk() for _ in range(n)]
    
    @staticmethod
    def _ast_wrap(node):
        return [
            *CJKObfuscator._ast_many(random.randint(8,18)),
            ast.Try(body=[ast.Expr(ast.Tuple([ast.BinOp(ast.Constant(1),ast.Div(),ast.Constant(0))],ast.Load()))],
                handlers=[ast.ExceptHandler(body=[node])], orelse=[], finalbody=[]),
            *CJKObfuscator._ast_many(random.randint(5,12)),
        ]
    
    class _FStrFix(ast.NodeTransformer):
        def visit_JoinedStr(self, node):
            parts = []
            for val in node.values:
                if isinstance(val, ast.Constant):
                    parts.append(val)
                elif isinstance(val, ast.FormattedValue):
                    inner = val.value
                    fn = {115:'str',114:'repr',97:'ascii'}.get(val.conversion,'str')
                    inner = ast.Call(ast.Name(fn,ast.Load()),[inner],[])
                    parts.append(inner)
                else:
                    parts.append(ast.Call(ast.Name('str',ast.Load()),[val],[]))
            if not parts: return ast.Constant('')
            if len(parts)==1 and isinstance(parts[0],ast.Constant): return parts[0]
            return ast.Call(ast.Attribute(ast.Constant(''),'join',ast.Load()), [ast.Tuple(parts,ast.Load())],[])
    
    class _AddJunk(ast.NodeTransformer):
        def _proc(self, body):
            out = []
            for s in body: out.extend(CJKObfuscator._ast_wrap(s))
            return out
        def visit_Module(self, node):
            for s in node.body:
                if isinstance(s,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)): self.visit(s)
            node.body = self._proc(node.body)
            return node
        def visit_FunctionDef(self, node):
            node.body = self._proc(node.body)
            return node
        def visit_ClassDef(self, node):
            node.body = self._proc(node.body)
            return node
    
    class _ObfConst(ast.NodeTransformer):
        def _mk_obfstr(self, s):
            if not s: return ast.Constant('')
            v = CJKObfuscator._vk()
            lst = [ord(c) for c in s]
            lam3 = ast.Lambda(CJKObfuscator._ast_arg(CJKObfuscator._vk()),
                ast.Call(ast.Attribute(ast.Call(ast.Name('str',ast.Load()),[],[]),'join',ast.Load()),
                    [ast.GeneratorExp(ast.Call(ast.Name('chr',ast.Load()),[ast.Name(v,ast.Load())],[]),
                    [ast.comprehension(ast.Name(v,ast.Store()), ast.List([ast.Constant(x) for x in lst],ast.Load()),[],0)])],[]))
            lam2 = ast.Lambda(CJKObfuscator._ast_arg(CJKObfuscator._vk()), ast.Call(lam3,[ast.Constant(0)],[]))
            lam1 = ast.Lambda(CJKObfuscator._ast_arg(CJKObfuscator._vk()), ast.Call(lam2,[ast.Constant(0)],[]))
            return ast.Call(lam1,[ast.Constant(0)],[])
        
        def _mk_obfint(self, i):
            offset = random.randint(1000,99999)
            lam3 = ast.Lambda(CJKObfuscator._ast_arg(CJKObfuscator._vk()),
                ast.Call(ast.Name('int',ast.Load()), [ast.BinOp(ast.Constant(i+offset),ast.Sub(),ast.Constant(offset))],[]))
            lam2 = ast.Lambda(CJKObfuscator._ast_arg(CJKObfuscator._vk()), ast.Call(lam3,[ast.Constant(0)],[]))
            lam1 = ast.Lambda(CJKObfuscator._ast_arg(CJKObfuscator._vk()), ast.Call(lam2,[ast.Constant(0)],[]))
            return ast.Call(lam1,[ast.Constant(0)],[])
        
        def visit_Constant(self, node):
            if isinstance(node.value,str) and node.value:
                return self._mk_obfstr(node.value)
            elif isinstance(node.value,int) and not isinstance(node.value,bool) and node.value!=0:
                return self._mk_obfint(node.value)
            return node
    
    @classmethod
    def _xor_b(cls, data, key): return bytes(b^key[i%len(key)] for i,b in enumerate(data))
    
    @classmethod
    def _rc4(cls, data, key):
        S=list(range(256)); j=0
        for i in range(256):
            j=(j+S[i]+key[i%len(key)])%256; S[i],S[j]=S[j],S[i]
        i=j=0; out=[]
        for b in data:
            i=(i+1)%256; j=(j+S[i])%256; S[i],S[j]=S[j],S[i]
            out.append(b^S[(S[i]+S[j])%256])
        return bytes(out)
    
    @classmethod
    def _roll_xor(cls, data, seed):
        out=bytearray(); state=seed&0xFFFFFFFFFFFFFFFF
        for b in data:
            state=(state*6364136223846793005+1442695040888963407)&0xFFFFFFFFFFFFFFFF
            out.append(b^(state&0xFF))
        return bytes(out)
    
    @classmethod
    def _shuffle(cls, data, seed):
        lst=list(data); rng=random.Random(seed)
        idx=list(range(len(lst))); rng.shuffle(idx)
        out=[0]*len(lst)
        for ni,oi in enumerate(idx): out[ni]=lst[oi]
        return bytes(out), idx
    
    @classmethod
    def _out_junk(cls, count=250):
        lines = []
        for _ in range(count):
            ch = random.randint(0, 13)
            v1 = cls._vm(random.randint(12, 28))
            v2 = cls._vm(random.randint(8, 18))
            v3 = cls._vm(random.randint(8, 18))
            n1 = random.randint(2, 120)
            n2 = random.randint(0, 9999)
            n3 = random.randint(1, 255)
            n4 = random.randint(2, 15)
            if ch == 0:
                lines.append(f'{v1} = [{n2} for _ in range({n1})]')
            elif ch == 1:
                lines.append(f'{v1} = {{(lambda {v2}: {v2} ^ {n3})(i) for i in range({n1})}}')
            elif ch == 2:
                lines.append(f'{v1} = [(lambda {v2}, {v3}: {v2} * {v3})(i, j) for i in range({n1}) for j in range({n4})]')
            elif ch == 3:
                lines.append(f'{v1} = lambda {v2}: {v2} * {n2} + {n3}')
            elif ch == 4:
                inner = random.randint(2, 18)
                outer = random.randint(2, 12)
                lines.append(f'{v1} = [[(lambda {v2}: {v2} ^ {n3})(i) for i in range({inner})] for j in range({outer})]')
            elif ch == 5:
                lines.append(f'{v1} = [(lambda {v2}: {v2})({n2}) for _ in range({n1})]')
            elif ch == 6:
                cjk = cls._cjk_str(random.randint(80, 220))
                lines.append(f"'''\n{cjk}\n'''")
            elif ch == 7:
                cjk = cls._cjk_str(random.randint(40, 100))
                lines.append(f'# {cjk}')
            elif ch == 8:
                lines.append(f'{v1} = (lambda {v2}: (lambda {v3}: {v3} ^ {n3})({v2} + {n2}))({n1})')
            elif ch == 9:
                lines.append(f'{v1} = {{{n2} ^ i for i in range({n1})}}')
            elif ch == 10:
                lines.append(f'{v1} = lambda {v2}: lambda {v3}: {v2} * {n3} ^ {v3} + {n2}')
            elif ch == 11:
                lines.append(f'{v1} = [(lambda {v2}: {v2} + {n3})(i) for i in range({n1}) for j in range({n4})]')
            elif ch == 12:
                rows = random.randint(2, 8)
                cols = random.randint(2, 12)
                lines.append(f'{v1} = {{(lambda {v2}: {v2} ^ {n3})(i) for i in range({rows} * {cols})}}')
            else:
                lines.append(f'{v1} = {n2} ^ {n3} * {random.randint(1, 100)} + {random.randint(0, 9999)}')
        return '\n'.join(lines)
    
    @classmethod
    def cjk_obfuscate(cls, source_code: str) -> str:
        tree = ast.parse(source_code)
        cls._FStrFix().visit(tree)
        ast.fix_missing_locations(tree)
        cls._ObfConst().visit(tree)
        ast.fix_missing_locations(tree)
        cls._AddJunk().visit(tree)
        ast.fix_missing_locations(tree)
        
        try:
            unparsed = ast.unparse(tree)
            compiled = compile(unparsed, '<KTN>', 'exec')
            raw = marshal.dumps(compiled)
        except Exception as e:
            raise Exception(f'Compile error: {e}')
        
        raw = zlib.compress(raw, 9)
        raw = zlib.compress(raw, 9)
        raw = bz2.compress(raw)
        raw = lzma.compress(raw)
        raw = base64.b85encode(raw)
        
        xor_key = os.urandom(32)
        rc4_key = os.urandom(16)
        shuffle_seed = random.randint(0, 2**31)
        rolling_seed = random.randint(0, 2**31)
        
        raw = cls._xor_b(raw, xor_key)
        raw, indices = cls._shuffle(raw, shuffle_seed)
        raw = cls._rc4(raw, rc4_key)
        raw = cls._roll_xor(raw, rolling_seed)
        raw = base64.b64encode(raw)
        
        j1 = cls._out_junk(320)
        j2 = cls._out_junk(100)
        j3 = cls._out_junk(120)
        j4 = cls._out_junk(80)
        
        c1 = cls._vm(12)
        c2 = cls._vm(6)
        c3 = cls._vm(6)
        c4 = cls._vm(6)
        c5 = cls._vm(6)
        c6 = cls._vm(6)
        c7 = cls._vm(8)
        c8 = cls._vm(8)
        c9 = cls._vm(6)
        c10 = cls._vm(8)
        c11 = cls._vm(6)
        
        loader = f'''import sys,base64,bz2,zlib,lzma,marshal

class {c1}:
    def __init__(self,x):
        self.{c2}=x
        self.{c3}={repr(xor_key)}
        self.{c4}={repr(rolling_seed)}
        self.{c5}={repr(rc4_key)}
        self.{c6}={repr(indices)}
    def {c7}(self,d,k):
        S=list(range(256));j=0
        for i in range(256):
            j=(j+S[i]+k[i%len(k)])%256;S[i],S[j]=S[j],S[i]
        i=j=0;o=[]
        for b in d:
            i=(i+1)%256;j=(j+S[i])%256;S[i],S[j]=S[j],S[i]
            o.append(b^S[(S[i]+S[j])%256])
        return bytes(o)
    def {c8}(self,d,s):
        o=bytearray();st=s&0xFFFFFFFFFFFFFFFF
        for b in d:
            st=(st*6364136223846793005+1442695040888963407)&0xFFFFFFFFFFFFFFFF
            o.append(b^(st&0xFF))
        return bytes(o)
    def {c9}(self,d,k):
        return bytes(b^k[i%len(k)] for i,b in enumerate(d))
    def {c10}(self,d):
        o=[0]*len(d)
        for i,j in enumerate(self.{c6}): o[j]=d[i]
        return bytes(o)
    def {c11}(self):
        x1=base64;x2=bz2;x3=zlib;x4=lzma;x5=marshal
        d=x1.b64decode(self.{c2})
        d=self.{c8}(d,self.{c4})
        d=self.{c7}(d,self.{c5})
        d=self.{c10}(d)
        d=self.{c9}(d,self.{c3})
        d=x1.b85decode(d)
        d=x4.decompress(d)
        d=x2.decompress(d)
        d=x3.decompress(d)
        d=x3.decompress(d)
        return x5.loads(d)

exec({c1}({repr(raw)}).{c11}())
'''
        
        final = f'''# -*- coding: utf-8 -*-
# {cls._cjk_str(200)}
# {cls._cjk_str(150)}

{j1}

{loader}

{j2}

{j3}

{j4}
'''
        return final

class UltraObfuscator:
    def __init__(self):
        self.master_entropy = secrets.token_bytes(64)
        self.aes_key = self._derive_key("AES_LAYER", 32)
        self.chacha_key = self._derive_key("CHACHA_LAYER", 32)
        self.salsa_key = self._derive_key("SALSA_LAYER", 32)
        self.xor_key = self._derive_key("XOR_LAYER", 256)

    def _derive_key(self, purpose: str, length: int) -> bytes:
        salt = hashlib.sha256(purpose.encode()).digest()
        return scrypt(self.master_entropy, salt, length, N=2**16, r=8, p=1)

    def _ultra_encrypt_payload(self, data: bytes) -> bytes:
        aes_cipher = AES.new(self.aes_key, AES.MODE_GCM)
        aes_encrypted, aes_tag = aes_cipher.encrypt_and_digest(data)
        aes_data = aes_cipher.nonce + aes_tag + aes_encrypted
        chacha_nonce = get_random_bytes(12)
        chacha_cipher = ChaCha20.new(key=self.chacha_key, nonce=chacha_nonce)
        chacha_encrypted = chacha_cipher.encrypt(aes_data)
        chacha_data = chacha_nonce + chacha_encrypted
        salsa_nonce = get_random_bytes(8)
        salsa_cipher = Salsa20.new(key=self.salsa_key, nonce=salsa_nonce)
        salsa_encrypted = salsa_cipher.encrypt(chacha_data)
        xor_encrypted = bytes(a ^ b for a, b in zip(salsa_encrypted, (self.xor_key * (len(salsa_encrypted) // len(self.xor_key) + 1))[:len(salsa_encrypted)]))
        return salsa_nonce + xor_encrypted

    def generate_obfuscated_name(self, length: int = 16) -> str:
        confusing_chars = 'OoIl0_'
        patterns = ['Il0O', 'oO0l', 'I1lO', 'o0Ol', 'lI0o', 'OIl0', 'l0oO', 'O0oI', 'l1Oo', 'I0ol']
        name = random.choice(['O', 'I', 'l', 'o'])
        for _ in range(length - 1):
            if random.random() < 0.4:
                name += random.choice(patterns)
            else:
                name += random.choice(confusing_chars)
        name = name[:20]
        if name[0].isdigit():
            name = 'O' + name[1:]
        return name

    def obfuscate(self, source_code: str) -> str:
        encrypted_payload = self._ultra_encrypt_payload(source_code.encode())
        encoded_payload = base64.b64encode(encrypted_payload).decode()
        names = [self.generate_obfuscated_name() for _ in range(15)]
        
        loader = f'''#!/usr/bin/env python3
import sys, base64, hashlib, secrets, random
try:
    from Crypto.Cipher import AES, ChaCha20, Salsa20
    from Crypto.Protocol.KDF import scrypt
except:
    __import__('subprocess').check_call([sys.executable, '-m', 'pip', 'install', 'pycryptodome', '-q'])
    from Crypto.Cipher import AES, ChaCha20, Salsa20
    from Crypto.Protocol.KDF import scrypt

{names[0]} = bytes.fromhex('{self.master_entropy.hex()}')

def {names[1]}(purpose: str, length: int) -> bytes:
    global {names[0]}
    salt = hashlib.sha256(purpose.encode()).digest()
    return scrypt({names[0]}, salt, length, N=2**16, r=8, p=1)

def {names[2]}(data: bytes) -> bytes:
    try:
        aes_key = {names[1]}("AES_LAYER", 32)
        chacha_key = {names[1]}("CHACHA_LAYER", 32)
        salsa_key = {names[1]}("SALSA_LAYER", 32)
        xor_key = {names[1]}("XOR_LAYER", 256)
        salsa_nonce = data[:8]
        encrypted_data = data[8:]
        xor_decrypted = bytes(a ^ b for a, b in zip(encrypted_data, (xor_key * (len(encrypted_data) // len(xor_key) + 1))[:len(encrypted_data)]))
        salsa_cipher = Salsa20.new(key=salsa_key, nonce=salsa_nonce)
        chacha_data = salsa_cipher.decrypt(xor_decrypted)
        chacha_nonce = chacha_data[:12]
        chacha_encrypted = chacha_data[12:]
        chacha_cipher = ChaCha20.new(key=chacha_key, nonce=chacha_nonce)
        aes_data = chacha_cipher.decrypt(chacha_encrypted)
        aes_nonce = aes_data[:16]
        aes_tag = aes_data[16:32]
        aes_encrypted = aes_data[32:]
        aes_cipher = AES.new(aes_key, AES.MODE_GCM, nonce=aes_nonce)
        return aes_cipher.decrypt_and_verify(aes_encrypted, aes_tag)
    except Exception:
        sys.exit(1)

def {names[3]}():
    try:
        {names[4]} = base64.b64decode('{encoded_payload}')
        {names[5]} = {names[2]}({names[4]})
        exec({names[5]}.decode(), {{'__name__': '__main__', '__file__': __file__}})
    except Exception:
        sys.exit(1)

def {names[6]}():
    fake_key = secrets.token_bytes(32)
    fake_data = base64.b64encode(secrets.token_bytes(2048)).decode()
    return hashlib.sha512(fake_data.encode() + fake_key).hexdigest()

def {names[7]}():
    operations = random.randint(100, 500)
    for i in range(operations):
        _ = secrets.randbits(64) ^ secrets.randbits(64)
        _ = random.randint(0, 2**32) * random.randint(0, 2**16)
    return secrets.token_hex(32)

def {names[8]}():
    fake_metrics = {{
        'entropy': random.uniform(7.8, 8.0),
        'compression_ratio': random.uniform(0.25, 0.75),
        'pattern_count': random.randint(50, 200),
        'complexity_score': random.uniform(0.85, 0.99)
    }}
    return fake_metrics

if __name__ == "__main__":
    decoy_functions = [{names[6]}, {names[7]}, {names[8]}]
    random.shuffle(decoy_functions)
    execution_pattern = random.randint(1, 3)
    if execution_pattern == 1:
        decoy_functions[0]()
        {names[3]}()
        decoy_functions[1]()
    elif execution_pattern == 2:
        decoy_functions[1]()
        decoy_functions[2]()
        {names[3]}()
    else:
        decoy_functions[2]()
        {names[3]}()
        decoy_functions[0]()
'''
        return loader

class ObfuscatorEngine:
    def __init__(self):
        self.codec = CodecEngine()
        self.xor = XOREngine()
        self.ultra = UltraObfuscator()
        self.prompt = f"{SYMBOL['success']} Encode Count : "
        
    def _get_input(self, prompt: str) -> str:
        if sys.version_info[0] == 2:
            return raw_input(prompt)
        return input(prompt)

    def _get_loop_count(self) -> int:
        try:
            return int(self._get_input(self.prompt))
        except ValueError:
            raise EncryptorError("Invalid loop count")

    def _generate_header(self) -> str:
        return "# Encrypted by PyObfuscator\n# Gitub & Tg: @BatmanPriv\n\n"

    def obfuscate(self, option: int, source: str, output_path: str) -> None:
        chain = self.codec.build_encoding_chain(option)
        if not chain:
            raise EncryptorError("Invalid encoding option")
        
        loop_count = self._get_loop_count()
        encoded_data = self.codec.encode_data(source, chain)
        
        template = f'''{self._generate_header()}
class _:
    def __init__(self):
        self.c = __import__
    def __call__(self, d):
        return self.c('marshal').loads(self.c('zlib').decompress(d[::-1]))

exec((_())({repr(encoded_data)}))
'''
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for _ in range(loop_count):
                encoded_data = self.codec.encode_data(template, chain)
                template = f'''{self._generate_header()}
class _:
    def __init__(self):
        self.c = __import__
    def __call__(self, d):
        return self.c('marshal').loads(self.c('zlib').decompress(d[::-1]))

exec((_())({repr(encoded_data)}))
'''
            
            f.write(template)

    def simple_obfuscate(self, source: str, output_path: str) -> None:
        encoded = base64.b64encode(
            zlib.compress(
                lzma.compress(
                    gzip.compress(
                        marshal.dumps(compile(source, '<obfuscated>', 'exec'))
                    )
                )
            )
        )[::-1]
        
        template = f'''import marshal, gzip, lzma, zlib, base64
exec(marshal.loads(gzip.decompress(lzma.decompress(zlib.decompress(base64.b64decode({repr(encoded)}))))))
'''
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(template)
        
        py_compile.compile(output_path, output_path)

    def deep_xor_obfuscate(self, source: str, output_path: str, key: Optional[bytes] = None, layers: int = 4) -> None:
        final_code = self.xor.deep_xor_obfuscate(source, key, layers)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_code)
        py_compile.compile(output_path, output_path)

    def ast_obfuscate(self, source: str, output_path: str) -> None:
        key = os.urandom(32)
        payload, decrypt_str, decrypt_bytes = ASTObfuscator.obfuscate(source, key)
        payload = zlib.compress(payload, 9)
        
        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(payload, 16))
        
        key_b64 = base64.b64encode(key).decode()
        iv_b64 = base64.b64encode(iv).decode()
        data_b64 = base64.b64encode(encrypted).decode()
        
        loader = f'''{self._generate_header()}
import sys,base64,marshal,zlib
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
except:
    __import__('subprocess').check_call([sys.executable,'-m','pip','install','pycryptodome','-q'])
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad

def {decrypt_str}(d):
    i,p=d[:16],d[16:]
    return unpad(AES.new(base64.b64decode("{key_b64}"),AES.MODE_CBC,i).decrypt(p),16).decode()

def {decrypt_bytes}(d):
    i,p=d[:16],d[16:]
    return unpad(AES.new(base64.b64decode("{key_b64}"),AES.MODE_CBC,i).decrypt(p),16)

_e=base64.b64decode("{data_b64}")
_p=unpad(AES.new(base64.b64decode("{key_b64}"),AES.MODE_CBC,base64.b64decode("{iv_b64}")).decrypt(_e),16)
exec(marshal.loads(zlib.decompress(_p)))
'''
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(loader)
        py_compile.compile(output_path, output_path)

    def cjk_obfuscate(self, source: str, output_path: str) -> None:
        result = CJKObfuscator.cjk_obfuscate(source)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        py_compile.compile(output_path, output_path)

    def ultra_obfuscate(self, source: str, output_path: str) -> None:
        result = self.ultra.obfuscate(source)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        py_compile.compile(output_path, output_path)

class Interface:
    def __init__(self):
        self.clear = lambda: os.system('cls' if sys.platform == 'win32' else 'clear')
        
    def display_banner(self) -> None:
        self.clear()
        banner = f'''
   {COLOR["brown"]}                                      
         .+#-                                           
         .+@@%-                                         
           .*@@%-   {COLOR["cyan"]}          ..     {COLOR["brown"]}                   
             .*@@%- {COLOR["cyan"]}         .@@# {COLOR["brown"]}                      
               .*@@%- {COLOR["cyan"]}       +@@-    {COLOR["brown"]}                   
               :#@@@@%-{COLOR["cyan"]}      @@#     -@@=               
             :#@@*.{COLOR["brown"]}.+@@%-{COLOR["cyan"]}   =@@:      =@@@=             
           :#@@*. {COLOR["brown"]}   .+@@#:{COLOR["cyan"]}  -+         =@@@=           
         :#@@*.   {COLOR["brown"]}     .+@@%-   {COLOR["cyan"]}          =@@@=         
        +@@@-     {COLOR["brown"]}       .#@@#:   {COLOR["cyan"]}          %@@%.       
         :#@@*.          {COLOR["brown"]} #@@@@%-        {COLOR["cyan"]} =@@@=         
        {COLOR["cyan"]}   -#@@*.        -@@+.{COLOR["brown"]}*@@#:    {COLOR["cyan"]} =@@@=           
        {COLOR["cyan"]}     :#@@#:      %@@  {COLOR["brown"]} .+@@%- {COLOR["cyan"]} :#%=             
               :#@*  {COLOR["cyan"]}   -@@=    {COLOR["brown"]} .*@@%-                 
                     {COLOR["cyan"]}   %@%     {COLOR["brown"]}   .+@@%-               
                     {COLOR["cyan"]}  -@@-        {COLOR["brown"]}  .*@@%-             
                         .        {COLOR["brown"]}     .+@@%-           
                                   {COLOR["brown"]}      .*@@%-         
                                   {COLOR["brown"]}        .+*:
    {COLOR["green"]}PyObfuscator | Advanced Edition | Join Git & Tg: @BatmanPriv
'''
        print(banner)

    def display_menu(self) -> None:
        menu_items = [
            ("1", "Marshal Encode"),
            ("2", "Zlib Encode"),
            ("3", "Base16 Encode"),
            ("4", "Base32 Encode"),
            ("5", "Base64 Encode"),
            ("6", "LZMA Encode"),
            ("7", "GZIP Encode"),
            ("8", "Zlib + Base16"),
            ("9", "Zlib + Base32"),
            ("10", "Zlib + Base64"),
            ("11", "GZIP + Base16"),
            ("12", "GZIP + Base32"),
            ("13", "GZIP + Base64"),
            ("14", "LZMA + Base16"),
            ("15", "LZMA + Base32"),
            ("16", "LZMA + Base64"),
            ("17", "Marshal + Zlib"),
            ("18", "Marshal + GZIP"),
            ("19", "Marshal + LZMA"),
            ("20", "Marshal + Base16"),
            ("21", "Marshal + Base32"),
            ("22", "Marshal + Base64"),
            ("23", "Marshal + Zlib + Base16"),
            ("24", "Marshal + Zlib + Base32"),
            ("25", "Marshal + Zlib + Base64"),
            ("26", "Marshal + LZMA + Base16"),
            ("27", "Marshal + LZMA + Base32"),
            ("28", "Marshal + LZMA + Base64"),
            ("29", "Marshal + GZIP + Base16"),
            ("30", "Marshal + GZIP + Base32"),
            ("31", "Marshal + GZIP + Base64"),
            ("32", "Marshal + Zlib + LZMA + Base16"),
            ("33", "Marshal + Zlib + LZMA + Base32"),
            ("34", "Marshal + Zlib + LZMA + Base64"),
            ("35", "Marshal + Zlib + GZIP + Base16"),
            ("36", "Marshal + Zlib + GZIP + Base32"),
            ("37", "Marshal + Zlib + GZIP + Base64"),
            ("38", "Marshal + Zlib + LZMA + GZIP + Base16"),
            ("39", "Marshal + Zlib + LZMA + GZIP + Base32"),
            ("40", "Marshal + Zlib + LZMA + GZIP + Base64"),
            ("41", "Simple Obfuscation"),
            ("42", "Deep XOR Obfuscation"),
            ("43", "AST Obfuscation (Control Flow + Strings)"),
            ("44", "AST Obfuscation (CJK + Junk + Multi-layer)"),
            ("45", "Ultra Obfuscation (AES+ChaCha20+Salsa20+XOR)"),
            ("46", "Exit")
        ]
        
        print(f"{COLOR['brown']}")
        for num, desc in menu_items:
            print(f"{COLOR['red']}[{COLOR['yellow']}{num}{COLOR['red']}] {COLOR['green']}{desc}")

    def get_user_option(self) -> int:
        try:
            option = int(self._get_input(f"{SYMBOL['success']} Option:{COLOR['cyan']} "))
            if 1 <= option <= 46:
                return option
            raise EncryptorError("Invalid option")
        except ValueError:
            raise EncryptorError("Invalid option format")

    def _get_input(self, prompt: str) -> str:
        if sys.version_info[0] == 2:
            return raw_input(prompt)
        return input(prompt)

class PyObfuscator:
    def __init__(self):
        self.interface = Interface()
        self.engine = ObfuscatorEngine()
        self.validator = EnvironmentValidator()

    def _get_source_file(self) -> tuple:
        filepath = self.interface._get_input(f"{SYMBOL['success']} File Name : ")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read(), filepath
        except IOError:
            raise EncryptorError("File not found")
        except UnicodeDecodeError:
            try:
                with open(filepath, 'r', encoding='latin-1') as f:
                    return f.read(), filepath
            except:
                raise EncryptorError("Cannot read file encoding")

    def _calculate_size(self, filepath: str) -> str:
        size = os.path.getsize(filepath)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"

    def _get_xor_options(self) -> tuple:
        key_option = self.interface._get_input(f"{SYMBOL['success']} Use custom key? (y/n): {COLOR['cyan']}")
        key = None
        if key_option.lower() == 'y':
            key_str = self.interface._get_input(f"{SYMBOL['success']} Enter key (hex or string): {COLOR['cyan']}")
            try:
                key = bytes.fromhex(key_str)
            except:
                key = key_str.encode()
        
        layers = 4
        try:
            layers_input = self.interface._get_input(f"{SYMBOL['success']} Layers (default 4): {COLOR['cyan']}")
            if layers_input.strip():
                layers = int(layers_input)
        except:
            pass
        
        return key, layers

    def run(self) -> None:
        try:
            self.validator.validate_imports()
            self.interface.display_banner()
            self.interface.display_menu()
            
            option = self.interface.get_user_option()
            if option == 46:
                print(f"{SYMBOL['success']} Goodbye!")
                sys.exit(0)
            
            source_code, source_path = self._get_source_file()
            
            if option == 42:
                output_path = source_path.replace('.py', '') + '_xored.py'
                key, layers = self._get_xor_options()
                self.engine.deep_xor_obfuscate(source_code, output_path, key, layers)
            elif option == 41:
                output_path = source_path.replace('.py', '') + '_simple.py'
                self.engine.simple_obfuscate(source_code, output_path)
            elif option == 43:
                output_path = source_path.replace('.py', '') + '_ast.py'
                self.engine.ast_obfuscate(source_code, output_path)
            elif option == 44:
                output_path = source_path.replace('.py', '') + '_cjk.py'
                self.engine.cjk_obfuscate(source_code, output_path)
            elif option == 45:
                output_path = source_path.replace('.py', '') + '_ultra.py'
                self.engine.ultra_obfuscate(source_code, output_path)
            else:
                output_path = source_path.replace('.py', '') + '_obfuscated.py'
                self.engine.obfuscate(option, source_code, output_path)
            
            print(f"\n{SYMBOL['success']} Obfuscation complete: {source_path}")
            print(f"{SYMBOL['success']} Output: {output_path}")
            print(f"{SYMBOL['success']} Size: {self._calculate_size(output_path)}")
            
        except EncryptorError as e:
            print(f"{SYMBOL['error']} {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print(f"\n{SYMBOL['error']} Operation cancelled")
            sys.exit(0)

if __name__ == "__main__":
    app = PyObfuscator()
    app.run()