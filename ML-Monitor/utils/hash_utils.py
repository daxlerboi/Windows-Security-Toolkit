import hashlib

def sha256_file(filepath):
    sha256 = hashlib.sha256()

    try:
        with open(filepath, "rb") as file:
            while True:
                chunk = file.read(4096)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    except:
        return None
