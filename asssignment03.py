#!/usr/bin/env python 
# -*- coding:utf-8 -*-
##############################################
#copy from git user AwsomeName
#headers不懂啥意思
##############################################
url='https://baike.baidu.com/item/北京地铁/408485'
########################################################################
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0'
}
################################################################################

#初始化网页信息
#response是从服务器返回的所有信息
#response.text中存放服务器返回的网页信息，用于beautifulsoup
###############################################
import requests
response = requests.get(url, headers=headers)
html_content = response.text
###################################################
#正则表达式提取网页信息中的station_url
###########################################################################
import re
url_pattern = re.compile(
    '/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81[\d]*[%|\w|\d]+')
stations_pattern = set(url_pattern.findall(html_content))    #set强制转换为集合
stations_url = set('https://baike.baidu.com' + item for item in stations_pattern)
###################################################################


#################################################################################################
#res表示response，是服务器返回的所有信息
#content存放从服务器返回的网页信息，但是是字节码，decode, encode是解编码的格式
#mm = re.findall('/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81[\d]*[%|\w|\d]+\">'
#                '(北京地铁[\u4e00-\u9fa5]{2}线|北京地铁\d+号线)', res.content.decode('utf8'))
# 没看懂findall中的匹配pattern
# 得到line_name存放地铁线路名字
################################################################################
res = response
mm = re.findall('/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81[\d]*[%|\w|\d]+\">'
                '(北京地铁[\u4e00-\u9fa5]{2}线|北京地铁\d+号线)', res.content.decode('utf8'))
line_names = set(mm)
##############################################################################################################


#########################################################


    #urllib.parse.unquote()用于把网页信息转换为对应的可读信息，
    # urllib.parse.urlencode()把可读信息转换成html格式的信息
    # list.extend(stations.extend)用于把两个列表合为一个，
    # title = re.findall('
    #                      <title>(北京地铁[\u4e00-\u9fa5]{2}线|北京地铁[\w|\d]+线)_百度百科</title>
    #                         ', tmp_context)
    #                         中的正则匹配公式不懂
#获取line-station-distance-connection信息

#soup = BeautifulSoup(tmp_context, 'lxml')，指定lxml解析器解析tmp_context文档
#######################################################################################
from bs4 import BeautifulSoup
from collections import defaultdict

station_connection = defaultdict(list)
connection_distence = defaultdict()

for url in stations_url:
#    print('get_url: ',url)
    tmp_res = requests.get(url, headers=headers)
    tmp_res.content.decode("utf8","ignore").encode("gbk","ignore")
    tmp_context = tmp_res.content.decode('utf8')
    title = re.findall('<title>(北京地铁[\u4e00-\u9fa5]{2}线|北京地铁[\w|\d]+线)_百度百科</title>', tmp_context)
#    print(title)
 #   print('===============================================================================')
#####################################################################################################获取地铁线路名称和链接
    soup = BeautifulSoup(tmp_context, 'lxml')
    tables = soup.select('table')#得到网页信息中的table class信息赋给tables
    df_list = []
    for table in tables:
#     print(type(table.string))[\u4e00-\u9fa5].encode('utf-8','ignore').decode('utf-8','ignore')
        if re.findall("相邻站间距信息统计表", str(table)):
            connections_table = str(table)
            connections_table = str(table)
            src_stations = re.findall("([\u4e00-\u9fa5]+)——[\u4e00-\u9fa5]+", connections_table)
            dst_stations = re.findall("[\u4e00-\u9fa5]+——([\u4e00-\u9fa5]+)", connections_table)
            #            print(re.findall("[\u4e00-\u9fa5]+——[\u4e00-\u9fa5]+", connections_table))
            # [\u4e00-\u9fa5 ]+，是汉字的编码范围，用来匹配汉字，就是把table里的站点连接汉字信息匹配出来
            #            print(str(table))
            distence = re.findall("(\d+)[\u4e00-\u9fa5]*</td>", connections_table)#匹配间距距离
            #print(src_stations, '\n', dst_stations, distence)
                                           ########################################添加station_connection信息

            # zip()函数：把这三个可迭代对象对应的元素，打包为一个元组并返回这些元组组成的列表。
            # station_connection = defaultdict(list)
            # connection_distence = defaultdict()
            for src, dst, dis in zip(src_stations, dst_stations, distence):
                station_connection[src].append(dst)
                station_connection[dst].append(src)
                com = str(src) + str(dst)
                moc = str(dst) + str(src)
                connection_distence[com] = dis
                connection_distence[moc] = dis
'''
#########测试一下
print(station_connection)
print(connection_distence)
print(station_connection['霍营'])
print(connection_distence['育新霍营'])
'''
##########################################################
#上面实际就是爬取网页中的指定信息，包括line-station-distance-connection等


# 下面是应用这些信息来实现搜索功能
##############################################################
#计算站间距离的函数
def get_station_distance(origin, destination):
    tmp = str(origin) + str(destination)
    return connection_distence[tmp]

#检测current_path最后一个是不是destination，是返回True
def is_goal(desitination):
    def _wrap(current_path):
        return current_path[-1] == desitination  #return True
    return _wrap

############################################################################################
#search_route_of_subway, strategy参数方便继续定义搜索策略。                                #
# 没明白
def search(graph, start, is_goal, search_strategy):                                        #
    graph = station_connection
    pathes = [[start]]
    seen = set()
    # Python 字典 pop() 方法删除字典给定键 key 及对应的值，返回值为被删除的值              #
    while pathes:
        path = pathes.pop(0)                                                               #
        froniter = path[-1]
        if froniter in seen: continue
        successors = graph[froniter]
        for city in successors:
            if city in path: continue                                                      #
            new_path = path + [city]
            pathes.append(new_path)
            if is_goal(new_path): return new_path
        seen.add(froniter)                                                                 #
        pathes = search_strategy(pathes)

print(search(station_connection, start='霍营',
       is_goal=is_goal('北京西站'), search_strategy=lambda n: n))                          #

###########################################################################################基本实现了线路搜索
# 后面定义一些函数传入search_strategy，实现自定义的搜索策略

def sort_path(cmp_func, beam=-1):
    def _sorted(pathes):
        return sorted(pathes, key=cmp_func)[:beam]
        #sorted():把pathes列表按cmp_func排序得到新的列表，原列表不变
    return _sorted

#得到总路线的distance
# enumerate：枚举，列举()中的所有元素，下标和元素形成一对元组，最终以列表的形式返回
def get_path_distance(path):
    distance = 0
    for i, c in enumerate(path[:-1]):
        distance += int(get_station_distance(c, path[i + 1]))
    return distance

def get_total_station(path):#得到站点数目
    return len(path)

def get_comprehensive_path(path):
    return get_path_distance(path)/100 + get_total_station(path)*10
def get_as_much_path(path):
    return -1 * len(path)

print(
search(station_connection, start='霍营',
       is_goal=is_goal('北京西站'),
       search_strategy=sort_path(get_path_distance, beam=100)))


#############################################################
################################################################
#后面没看
#################################################################
'''
发现两个问题，一个是宣武门到菜市口，高德地图中是不支持2号线到4号线直接换乘的。
另一个是我们的寻找程序，是有问题的。它设置了标志位SEEN，但是这个标志位比较简
单，当很多站有交叉的情况，就会导致一些路径不能遍历。比如西直门到平安里，可以
4号线直达，但是这里先检查了2号线，2号线可以在车公庄换乘
6号线到达平安里，这样平安里就被标记了，当检查4号线时，整个4号线的路径都被抛弃了。
仔细检查，发现问题挺多的。这里应该用广度优先搜索(BFS)比较合适。所以重写了寻路算法
'''
def search_N(graph, start, is_goal, search_strategy):
    pathes = [[start]]
    ans = []
    while pathes:
        new_pathes = []
        for path in pathes:
            if len(path) > 30: continue
            laster = path[-1]
            nexts = graph[laster]
            for n in nexts:
                if n in path: continue
                new_path = path + [n]
                if is_goal(new_path):
                    ans.append(new_path)
                #                     print('+++++++++++++++++++++++++++')
                #                     print(new_path)

                new_pathes.append(new_path)

        pathes = search_strategy(new_pathes)
    #         print('len(pathes)={}'.format(len(pathes)), pathes)
    ans = search_strategy(ans)
    return ans[0]

'''
两个search函数需要再好好看看，弄明白写熟练
'''


'''
另外又检查了一下，发现是百度百科里的地铁9号线数据不全，没有站点距离表，所以整个算法缺少9号线的数据，而刚好我的实验站点北京西站就是9号线终点站
'''
search_N(station_connection, start='西直门',
       is_goal=is_goal('菜市口'), search_strategy=sort_path(get_total_line, beam=100))
station_connection['平安里']
search_N(station_connection, start='霍营',
       is_goal=is_goal('北京西站'), search_strategy=sort_path(get_total_line, beam=100))
'''
这样的结果，在高德地图中选择地铁优先，就是步行最少的方案。
实际上，如果只看地铁图导航，我也会选择这种方案。但是高德的默认结果中并没有。
因为高德是根据时间来具体估算的，包括每站之间的时间和换乘的
时间。所以这里无法得到和地图一样的时间优先结果。但是如果要考虑做的话也是差不多的流程
'''
def get_comprehensive_path_N(path):
    return get_path_distance(path)/100 + get_total_station(path)*10 + get_total_line(path)*100
search_N(station_connection, start='霍营',
       is_goal=is_goal('北京西站'), search_strategy=sort_path(get_comprehensive_path_N, beam=1000))
search_N(station_connection, start='霍营',
       is_goal=is_goal('北京南站'), search_strategy=sort_path(get_comprehensive_path_N, beam=1000))


def search_ND(graph, start, is_goal, search_strategy):
    pathes = [[start]]
    ans = []
    while pathes:
        new_pathes = []
        for path in pathes:
            if len(path) > 30: continue

            laster = path[-1]
            nexts = graph[laster]
            for n in nexts:
                if n in path: continue

                new_path = path + [n]
                if is_goal(new_path):
                    ans.append(new_path)
                #                     print('+++++++++++++++++++++++++++')
                #                     print(new_path)
                new_pathes.append(new_path)
        pathes = search_strategy(new_pathes)
    #         print('len(pathes)={}'.format(len(pathes)), pathes)
    ans = search_strategy(ans)
    if len(ans) < 10:
        return ans
    return ans[0:10]


search_ND(station_connection, start='霍营',
       is_goal=is_goal('四惠东'), search_strategy=sort_path(get_comprehensive_path_N, beam=1000))
