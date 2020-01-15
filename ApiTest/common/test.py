import os

def close_locust_by_pid():
    locust_process = os.popen('lsof -i:8089').readlines()[-1]
    res = locust_process.split(" ")
    res_filter = list(filter(None, res))
    print(res_filter[1])
    command = "kill -9 {}".format(res_filter[1])
    # command = "pwd"
    res = os.system(command)
    print("我在你之后执行")
    return res

if __name__ == "__main__":
    a = close_locust_by_pid()
    print(a)