import pandas
import numpy as np
import matplotlib.pyplot as plt
import datetime
import jieba

# 聊天记录文件路径（需在QQ消息管理器以TXT格式导出）
chat_log_path = './chat_log.txt'

# TXT文件行号
line_num = 0
# 聊天记录总条数
item_sum = 0
# 聊天文字总和
total_text = ''

# 修改分词权重
jieba.suggest_freq('亲爱的', True)
jieba.suggest_freq('大可爱', True)
jieba.suggest_freq('小可爱', True)
jieba.suggest_freq('吧唧', True)
jieba.suggest_freq('亲亲', True)
jieba.suggest_freq('哼唧', True)
jieba.suggest_freq('emmm', True)
jieba.del_word('一下')
jieba.del_word('然后')
jieba.del_word('这样')
jieba.del_word('这个')
jieba.del_word('还是')
jieba.del_word('就是')
jieba.del_word('一个')
jieba.del_word('晚上')
jieba.del_word('什么')
jieba.del_word('那个')
jieba.del_word('觉得')
jieba.del_word('不是')
jieba.del_word('感觉')
jieba.del_word('可能')
jieba.del_word('没有')
jieba.del_word('有点')
jieba.del_word('怎么')
jieba.del_word('还有')

# 配置单字
single_word = {'嗷', '嗯', '嬲'}

hours = {}


# 处理时间
def countTime(str_date):
    # print(str_date)
    # date = datetime.datetime.strptime(str_date, "%Y-%m-%d %H:%M:%S")
    # print(date)
    try:
        hour = int(str_date[10:13])
        hours[hour] = hours.get(hour, 0) + 1
    except:
        hour = int(str_date[10:12])
        hours[hour] = hours.get(hour, 0) + 1
        return


# 读取文本文件
for line in open(chat_log_path, 'r', encoding='utf-8'):
    line_num = line_num + 1
    if line_num < 9:
        continue
    if line == '':
        continue
    else:
        # 时间戳特判
        if line.startswith('2017-') or line.startswith('2018-') or line.startswith('2019-'):
            item_sum = item_sum + 1
            countTime(line[0:19])
            continue
        else:
            # 过滤聊天图片和表情
            if not (line.startswith('[图片]') or line.startswith('[表情]')):
                total_text = total_text + line

print("记录总条数：" + str(item_sum))

words = jieba.cut(total_text)
counts = {}

for word in words:
    if len(word) == 1:
        if word in single_word:
            counts[word] = counts.get(word, 0) + 1
    else:
        counts[word] = counts.get(word, 0) + 1

# 将键值对转换成列表
items = list(counts.items())
# 根据词语出现的次数进行从大到小排序
items.sort(key=lambda x: x[1], reverse=True)

for i in range(30):
    word, count = items[i]
    print(word + '    \t' + str(count))

# 绘制分时聊天频率折线图
hours = [(k, hours[k]) for k in sorted(hours.keys())]
plt.plot(hours)
plt.title('聊天记录条数24小时分布图')
plt.ylabel('消息条数')
plt.xlabel('时间(小时)')
plt.show()
