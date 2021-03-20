from default_vars import *
import collections
import mailbox
import re
import os
import email

from urllib.parse import splittype,splithost,splitport


#初始化九个情感特征列表
def initiate_word():
    k = 0
    emo_file = open("C:/Users/10753/Desktop/database/emotions.txt")
    for line in emo_file:
        # print(line)
        emo_words = re.split(', |，|,|， ', line.strip().strip(' '))
        emotions_dict[keys_list[k]] = emo_words
        # print(emo_words)
        k += 1
    emo_file.close()
    return emotions_dict

#提取mailbox类型的邮件正文
def getBody(message):
    content = ""
    if message.is_multipart():
        for part in message.get_payload():
            if part.get_payload(decode=True):
                content += str(part.get_payload(decode=True))
    else:
        content = message.get_payload(decode=True)

    return content

#remake the factory of class 'mbox'
def mbox_reader(stream):
    """Read a non-ascii message from mailbox"""
    data = stream.read()
    text = data.decode(encoding="latin-1")
    return mailbox.mboxMessage(text)

#找到邮件中所有链接
def all_link(string):
    all_url_list = []
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    all_url = re.findall(pattern, string)
    for url in all_url:
        if url not in all_url_list:
            all_url_list.append(url)
        else:
            pass
    return all_url_list



#x1 - 邮件标题是否出现伪装词
def is_fake_subject(subject):
    subject = str(subject)
    if subject:
        subject_words = re.split(':|/| ',subject.strip())
        print(subject_words)
        for word in subject_words:
            if word in subject_list:
                return 1
        return 0
    else:
        return 0

#x2 - 邮件发件人地址和回复地址是否相同
def is_From_Reply_Same(from_address,Reply_address):
    flag = 0
    from_address = str(from_address).strip().replace('\n','')
    Reply_address = str(Reply_address).strip().replace('\n','')

    if Reply_address != 'None' and Reply_address != '':
        #format Reply_address
        if '<' not in Reply_address and '>' not in Reply_address:
            Reply_address_tackle = '<'+Reply_address+'>'
        else:
            match_0 = re.match(r'.*<(.*)>', Reply_address)
            Reply_address_tackle = '<'+match_0[1]+'>'

        #format from_address
        match_1 = re.match(r'.*<(.*)>',from_address)
        match_2 = re.match(r'.*@.*',from_address) and ',' not in from_address
        if match_1:
            from_address_tackle = '<'+match_1[1]+'>'
        elif match_2:
            from_address_tackle = '<'+from_address+'>'
        else:
            #in this cluster, it means wrong.
            from_address_tackle = from_address

        #get return var
        #print(from_address_tackle)
        if from_address_tackle == Reply_address_tackle:
            flag = 0
        else:
            flag = 1
    else:
        flag = 0
    return flag

#x3 - Message-Id的域名是否是发件人的域名
def is_Domain_Name_Same(from_address,message_id):
    flag = 0
    fdomain_name = ''
    mdomain_name = ''
    assert isinstance(from_address,str) is True, "Please check the type of from_address"
    assert isinstance(message_id, str) is True, "Please check the type of Message_Id"
    from_address_tackle = from_address.strip().replace(' ','').replace('\n','')
    message_id_tackle = message_id.strip().replace(' ','').replace('\n','')
    match_1 = re.match(r'.*@(.*)>.*',from_address_tackle)
    match_2 = re.match(r'.*@(.*).*',from_address_tackle)
    match_3 = re.match('.*<(.*)>',from_address_tackle)

    #format from_address
    if match_1:
        fdomain_name = match_1
    elif match_2 :
        fdomain_name = match_2
    elif match_3 :
        fdomain_name = match_3

    #format message_id
    mdomain_name = re.match(r'.*<.*@(.*)>.*',message_id_tackle)

    #return flag
    if fdomain_name and mdomain_name:
        if fdomain_name[1] == mdomain_name[1]:
            flag = 0
        else:
            flag = 1
    else:
        flag = 0
    return flag

#x4 - 是否是html格式正文
def is_html(string):
    if "</html>" in string:
        is_html = 1
    else:
        is_html = 0
    return str(is_html)

#x5 - 邮件是否包含IP地址
def real_host_ip(string):
    host_ip_num = 0
    host_ip = 0
    urls = re.findall(r'<[Aa].*?href=.*?</[Aa]>', string, re.S)
    for url in urls:
        http_url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                              str(url))
        if len(http_url)>0:
            first_url = http_url[0]
            proto, rest = splittype(first_url)
            host, rest = splithost(rest)
            host, port = splitport(host)
            if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", host):
                host_ip_num += 1
            else:
                pass
        else:
            host_ip_num = 0
    if host_ip_num == 0:
        host_ip = 0
    else:
        host_ip = 1
    return str(host_ip)

#x6 - 邮件是否包含图片链接
def img_link(string):
    pattern = re.compile(r'src="(.*?)"')
    all_img_url = re.findall(pattern, string)
    if len(all_img_url)>0:
        return 1
    else:
        return 0
    #return len(all_img_url)

#x7 - 邮件链接是否有端口
def all_port(list):
    port_num = 0
    for url in list:
        proto, rest = splittype(url)
        host, rest = splithost(rest)
        host, port = splitport(host)
        if str(port) == "None":
            pass
        else:
            port_num +=1
    if port_num > 0:
        return 1
    else:
        return 0
    # return int(port_num)

#x8 - 链接中'%'的数量
def percent_num(list):
    percent_num_list = []
    percent_num = 0
    for url in list:
        url_2 = str(url).split("%")
        url_percent_num = len(url_2) - 1
        percent_num_list.append(str(url_percent_num))
        percent_num += url_percent_num
    return percent_num

#x9 - 链接中'@'的数量
def ai_num(list):
    ai_num_list = []
    ai_num = 0
    for url in list:
        url_2 = str(url).split("@")
        url_ai_num = len(url_2)-1
        ai_num_list.append(str(url_ai_num))
        ai_num += url_ai_num
    return ai_num

#x10 - 链接中'.'的数量
def point_num(list):
    point_num_list = []
    point_num = 0
    for url in list:
        url_1 = str(url).split(".")
        url_point_num = len(url_1)-1
        point_num_list.append(str(url_point_num))
        #print(str(url))
        #print(str(url_point_num))
        point_num += url_point_num
    return point_num

#x11 - 链接数量
def url_accounts(list):
    return len(list)

#x12 - 域名数量
def domain_name(list):
    domain_name_list = []
    for url in list:
        proto, rest = splittype(url)
        host, rest = splithost(rest)
        host, port = splitport(host)
        if host not in domain_name_list:
            domain_name_list.append(host)
        else:
            pass
    return len(domain_name_list)

#x13 - 显示的链接和实际指向的链接不相同(0同1不同)
def url_differ(string):
    url_different_num = 0
    url_different = 0
    urls = re.findall(r'<[Aa].*?href=.*?</[Aa]>', string, re.S)
    for url in urls:
        http_url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                              str(url))
        if len(http_url) == 1 or len(http_url) == 0:
            pass
        else:
            http_url_1 = http_url[1].split('<')
            if http_url[0] == http_url_1:
                url_different_num = 0
            else:
                url_different_num += 1
    if url_different_num == 0:
        url_different = 0
    else:
        url_different = 1
    return str(url_different)

#x14 - 邮件中是否有javascript代码
def is_javascript(string):
    if "</script>" in string:
        is_js = 1
    else:
        is_js = 0
    return str(is_js)

#x15 - javascript脚本是否会改变状态栏
def js_change_statue(string):
    if "window.status" in string:
        is_change = 1
    else:
        is_change = 0
    return str(is_change)

#x16 - javascript脚本中是否有onclick事件
def is_js_onclick(string):
    if "onclick=" in string:
        is_js_oc = 1
    else:
        is_js_oc = 0
    return is_js_oc

#x17 - javascript脚本中是否有pop-up窗口
def is_js_pop(string):
    if "window.open" in string:
        is_pop = 1
    else:
        is_pop = 0
    return str(is_pop)

#x18 - 邮件情感特征
def negative_probability(payload,word_list):
    amount = 0
    probability = 0
    payload.strip('\n')
    arr = re.split(r'[\?\s,\:\/\<\>\!\-\"\=\#]+',payload)
    new_arr = []
    a = len(arr)
    for n in range(a):
        flag = re.search(r'0x(.*)',arr[n])
        if flag:
            pass
        else:
            new_arr.append(arr[n].replace('\\n','').replace('\\t','').replace('\t','').replace('\\',''))
    uniqueword_count = collections.Counter(new_arr)

    len_uc = 0
    for value in uniqueword_count.values():
        len_uc += value

    tackle_uniqueword_count_len = len_uc-uniqueword_count['']-uniqueword_count['\'']
    print(uniqueword_count)

    for word in word_list:
        if uniqueword_count[word]:
            amount += uniqueword_count[word]

    if tackle_uniqueword_count_len <= 0:
        probability = amount/len(uniqueword_count)
    else:
        probability = amount/tackle_uniqueword_count_len
    return probability

#x18-1 - 否定心理情感特征

#x18-2 - 焦虑心理情感特征

#x18-3 - 生气心理情感特征

#x18-4 - 伤心心理情感特征

#x18-5 - 理解心理情感特征

#x18-6 - 犹豫心理情感特征

#x18-7 - 确定心理情感特征

#x18-8 - 压抑心理情感特征

#x18-9 - 相信心理情感特征

def Nemotion_probability(payload, Edict):
    probability = 0
    prob_list = []
    arr = re.split(r'[\?\s,\:\/\<\>\!\-\"\=\#]+', payload.strip('\n'))
    new_arr = []
    a = len(arr)
    for n in range(a):
        flag = re.search(r'0x(.*)', arr[n])
        if flag:
            pass
        else:
            new_arr.append(arr[n].replace('\\n', '').replace('\\t', '').replace('\t', '').replace('\\', ''))
    uniqueword_count = collections.Counter(new_arr)

    len_uc = 0
    for value in uniqueword_count.values():
        len_uc += value

    tackle_uniqueword_count_len = len_uc - uniqueword_count[''] - uniqueword_count['\'']
    print(uniqueword_count)

    for i in range(9):
        amount = 0
        for word in Edict[keys_list[i]]:
            if uniqueword_count[word]:
                amount += uniqueword_count[word]

        if tackle_uniqueword_count_len <= 0:
            probability = 0
        else:
            probability = amount / tackle_uniqueword_count_len

        prob_list.append(probability)

    return prob_list



#找出modal_name
def find_modal(list):
    domain_list = []
    for url in list:
        http_url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                              str(url))
        if len(http_url)>0:
            first_url = http_url[0]
            proto, rest = splittype(first_url)
            host, rest = splithost(rest)
            host, port = splitport(host)
            domain_list.append(host)
            # print(host)
        else:
            host_ip_num = 0
    word_counts = collections.Counter(domain_list)
    # 出现频率最高的3个单词
    top_one = word_counts.most_common(1)
    if len(top_one)>0:
        modal = top_one[0][0]
        # print(modal)
    else:
        modal = '-'

    return modal



#x19 - here处的链接
def here(modal,string):
    ban_words = ['here','click','Here','Click','CLICK','HERE']
    here_num = 0
    ban_flag = 0
    stand_host = modal
    stand_host_1 = ''

    urls = re.findall(r'<[Aa].*?href=.*?</[Aa]>', string, re.S)
    for url in urls:
        for word in ban_words:
            if word in url:         #如果找到click、here敏感词
                ban_flag = 1
                break

        if ban_flag == 1:
            http_url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                  str(url))

            if len(http_url)>0:
                first_url = http_url[0]
                proto, rest = splittype(first_url)
                host, rest = splithost(rest)
                host, port = splitport(host)
                stand_host = host

                # print(host)
                if host in modal:           #如果域名相同->0
                    pass
                else:
                    stand_host_1 = host
                    here_num = 1            #域名不同->1
    if stand_host_1:
        stand_host = stand_host_1
    return str(here_num),str(stand_host)


#提取日期
def exDate(Date):
    ele_list = re.split(',| ', str(Date))
    time = ''
    if len(ele_list)>6:
        if ele_list[2]:
            date = str(ele_list[2])+'|'+str(ele_list[3]) + '|' +str(ele_list[4])
        else:
            date = str(ele_list[3]) + '|' + str(ele_list[4]) + '|' + str(ele_list[5])
    else:
        date = '-'

    return date

#正常邮件使用部分
def get_emls():
    eml_lists = []
    for fpath, dirname, fnames in os.walk(formal_path):
        eml_lists = fnames
    return eml_lists


