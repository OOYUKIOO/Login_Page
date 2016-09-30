import hashlib

hashObj = hashlib.sha1()

hashObj.update("foo")
print hashObj.hexdigest()
