import threading

import multiprocessing as mp
import time
def test(num,q):
    for n in num:
        list_n = [n]
        for i in range(1,1000):
            # print(i)
            y =i**2-20+100-i*3+n
            # time.sleep(0.01)
            # print(f"{n}.{i} y is {y}")
            list_n.append(y)
        q.put(list_n)
    print('結束', num)


def set_mp(q):
    t_list = []
    data = [[1,2],[3,4],[5,6]]
    for i in data:
        t1 = threading.Thread(target=test, args=(i,q))
        t_list.append(t1)

    return t_list

def main():
    q = mp.Queue()
    start = time.time()
    t_list = set_mp(q)

    for t in t_list:
        t.start()
        # t.join()
    for t in t_list:
        t.join()
    end = time.time()
    print("time is "+str(end-start))
    while not q.empty():
        print(q.qsize())
        print(len(q.get()))
        # print(q.empty())
main()



#

#
# def test(num,q):
#     for n in num:
#         list_n = [n]
#         for i in range(0,376):
#             # print(i)
#             y =i**2-20+100-i*3+n
#             # time.sleep(0.01)
#             # print(f"{n}.{i} y is {y}")
#             list_n.append(y)
#         q.put(list_n)
#
#     print('結束', num)
#     print(q.full())
#
# def set_mp(q):
#     t_list = []
#     data = [[1,2],[3,4],[5,6]]
#     for i in data:
#         t1 = mp.Process(target=test, args=(i,q))
#         t_list.append(t1)
#     # t2 = mp.Process(target=test, args=([[3, 4]]))
#     # t_list.append(t2)
#     # t3 = mp.Process(target=test, args=([[5, 6]]))
#     # t_list.append(t3)
#     return t_list
#
# # 開始工作
# if __name__ == '__main__':
#     def main():
#         q = mp.Queue()
#         t_list = set_mp(q)
#         start = time.time()
#         for t in t_list:
#             t.start()
#             # t.join()
#         for t in t_list:
#             t.join()
#         end = time.time()
#         print("time is " + str(end - start))
#         while not q.empty():
#             print(q.get())
#         print(mp.cpu_count())
#     main()


