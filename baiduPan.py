import requests
import threading
from time import time
import json
import re


def downloadFile(URL, spos, epos, fp):
    try:
        header = {}
        header["Range"] = "bytes={}-{}".format(spos, epos)
        result = requests.get(URL, headers=header)
        fp.seek(spos)
        fp.write(result.content)
        print('1/{} of file is downloaded...'.format(thread_num))
    except Exception:
        print(Exception)


def split_file(file_size):
    start_p = []
    end_p = []
    per_size = int(file_size / thread_num)
    int_size = per_size * thread_num  # 整除部分
    for i in range(0, int_size, per_size):
        start_p.append(i)
        end_p.append(i + per_size - 1)
    if int_size < file_size:  # size 不一定 n 等分，将不能等分余下的部分添加到最后一个 sub 里
        end_p[-1] = file_size
    return start_p, end_p


# 线程数
thread_num = 50

# 需要填写的变量
url='https://d11.baidupcs.com/file/1804a730f5f7e9ab8e75ea255639987e?bkt=p3-14001804a730f5f7e9ab8e75ea255639987e45ab5d6b0000005cfd3b&xcode=c9036e388e787d3cc4a904bddb2ef72dd323fe7a72ec32cd211735c73dc42ee0b4cd52bf4987675245656623cb9fc910316128a2cdfcce4d&fid=2841264168-250528-849077322098671&time=1541510836&sign=FDTAXGERLQBHSK-DCb740ccc5511e5e8fedcff06b081203-RW1TqCiF6wGjPyFRA1oedm06BIU%3D&to=d11&size=6094139&sta_dx=6094139&sta_cs=6314&sta_ft=pdf&sta_ct=6&sta_mt=5&fm2=MH%2CYangquan%2CAnywhere%2C%2Cguangdong%2Cce&ctime=1512439449&mtime=1531644579&resv0=cdnback&resv1=0&vuk=2841264168&iv=0&htype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=14001804a730f5f7e9ab8e75ea255639987e45ab5d6b0000005cfd3b&sl=76480590&expires=8h&rt=pr&r=138828163&mlogid=7187315258942731246&vbdid=1464471049&fin=%E7%BE%8E%E5%9B%BD%E5%8E%9F%E7%89%88%E8%AF%BB%E7%89%A91.pdf&fn=%E7%BE%8E%E5%9B%BD%E5%8E%9F%E7%89%88%E8%AF%BB%E7%89%A91.pdf&rtype=1&dp-logid=7187315258942731246&dp-callid=0.1.1&hps=1&tsl=80&csl=80&csign=5E%2BkFNXm00TXGYHNUcLjnqWQucY%3D&so=0&ut=6&uter=4&serv=0&uc=4192912830&ti=90e00819b6f542503ad4268cf83c67e33e53a67e445ab9b6&by=themis'
down_file_name = '美国原版读物1.pdf'
# 如果该变量不填就会下载到运行程序的目录下
address='D:/' #记得最后要加斜杠

file = open(address+down_file_name, 'wb')
res = requests.head(url)
# 若有单引号替换成双引号
json_data = re.sub('\'', '\"', str(res.headers))
head_dict = json.loads(json_data)
size = int(head_dict['Content-Length'])
start_pos, end_pos = split_file(size)

tmp = []
print('start download...')
t0 = time()
for i in range(0, thread_num):
    t = threading.Thread(
        target=downloadFile,
        args=(
            url,
            start_pos[i],
            end_pos[i],
            file))
    t.setDaemon(True)  # 主进程结束时，线程也随之结束
    t.start()
    tmp.append(t)
for i in tmp:
    i.join()

file.close()
t1 = time()
total_time = t1 - t0
speed = float(size) / (1000 * total_time)
print('total_time:%.2f s' % total_time)
print('speed:%.2f KB/s' % speed)
