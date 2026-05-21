import time
from functools import wraps # 保护原函数名称，不被装饰器覆盖

# ====== 这是一个性能监测装饰器，用于监测各函数运行时间 ======
def timer(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start=time.time()
        result=func(*args,**kwargs)
        print(f'{func.__name__}耗时：{time.time()-start:.3f}s')
        return result
    return wrapper
