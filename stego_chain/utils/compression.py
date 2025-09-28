import zlib

def compress(data):
    """Kompresi data menggunakan zlib"""
    print("-> (Compressing data)")
    return zlib.compress(data)

def decompress(data):
    """Dekompresi data menggunakan zlib"""
    print("-> (Decompressing data)")
    return zlib.decompress(data)