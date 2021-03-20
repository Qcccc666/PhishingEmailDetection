import email
import os
from capture_funcs import *

def extract_formal(path, name1):
    Edict = initiate_word()
    all_words = []
    for i in range(9):
        all_words += Edict[keys_list[i]]
    DIR = './email/' #要统计的文件夹
    number = len([name2 for name2 in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name2))])
    print('number')
    print(number)    
    file = path
    efp = open(path,"r",encoding="latin-1")
    message = email.message_from_file(efp)

    for par in message.walk():
        if not par.is_multipart():  # 这里要判断是否是multipart，是的话，里面的数据是无用的，至于为什么可以了解mime相关知识。
            name = par.get_param("name")  # 如果是附件，这里就会取出附件的文件名
            if name:
                h = email.header.Header(name)
                dh = email.header.decode_header(h)
                fname = dh[0][0]
                #print('附件名:', fname)
                data = par.get_payload(decode=True)  # 解码出附件数据，然后存储到文件中
                # print(data)

            else:
                # 不是附件，是文本内容
                # print(par.get_payload(decode=True))  # 解码出文本内容，直接输出来就可以了。
                message_formal = par.get_payload(decode=True)

            #print('+' * 60)  # 用来区别各个部分的输出


    # extract the features of email
    message_from = message.get('From')
    message_Id = message.get('Message-Id')
    message_reply_to = message.get('Reply-To')
    message_subject = message.get('Subject')
    # message_formal = message.get_payload(decode=True)
    #print(message_formal)

    try:
        # print(message_formal)
        all_url = all_link(str(message_formal))
        x1 = is_fake_subject(message_subject)
        x2 = is_From_Reply_Same(message_from, message_reply_to)
        x3 = is_Domain_Name_Same(str(message_from), str(message_Id))
        x4 = is_html(str(message_formal))
        x5 = real_host_ip(str(message_formal))
        x6 = img_link(str(message_formal))
        x7 = all_port(all_url)
        x8 = percent_num(all_url)
        x9 = ai_num(all_url)
        x10 = point_num(all_url)
        x11 = url_accounts(all_url)
        x12 = domain_name(all_url)
        x13 = url_differ(str(message_formal))
        x14 = is_javascript(str(message_formal))
        x15 = js_change_statue(str(message_formal))
        x16 = is_js_onclick(str(message_formal))
        x17 = is_js_pop(str(message_formal))
        # x18 = 0
        x18 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        if int(x4) == 1:
            # print(str(content)[1:])
            my = MyParser()
            htmlStr = str(message_formal)[1:].replace('\n', ' ')
            my.feed(htmlStr)
            all_content = my.get_adata()
            # x18 = negative_probability(all_content,all_words)
            x18 = Nemotion_probability(all_content, Edict)
            #print(x18)
        elif int(x4) == 0:
            String = str(message_formal)[1:].replace('\n', ' ')
            # x18 = negative_probability(String,all_words)
            x18 = Nemotion_probability(String, Edict)
            #print(x18)

        Fsentence = str(x1) + ',' + str(x2) + ',' + str(x3) + ',' + str(x4) + ',' + str(
            x5) + ',' + str(x6) + ',' + str(x7) + ',' + str(x8) + ',' + str(x9) + ',' + str(
            x10) + ',' + str(x11) + ',' + str(x12) + ',' + str(x13) + ',' + str(x14) + ',' + str(
            x15) + ',' + str(x16) + ',' + str(x17) + ',' + str(x18)[1:-1]

        filename = "./dataset/"+name1+'.txt'
        file_write = open(filename, 'w')
        file_write.writelines(Fsentence + '\n')

    except UnicodeDecodeError as error:
        print(error)
    print('capu'+filename)
    result = []
    average_list = []
    average_list = initial_average()
    print("********")    # print(average_list)
    print(x4)
    if x1 == 1:
        result.append("Yes") 
    else:
        result.append("No")
    if x2 == 1:
        result.append("Yes") 
    else:
        result.append("No")
    if x3 == 1:
        result.append("Yes")
    else:
        result.append("No")
    if int(x4) == 1:
        result.append("Yes")
    else:
        result.append("No")
    if x5 == 1:
        result.append("Yes")
    else:
        result.append("No")
    if x6 == 1:
        result.append("Yes")
    else:
        result.append("No")
    if x7 == 1:
        result.append("Yes")
    else:
        result.append("No")
    # if float(x8) > average_list[7]:
    result.append(x8)
    result.append(x9)
    result.append(x10)
    result.append(x11)
    result.append(x12)
    if x13 == 1:
        result.append("No")
    else:
        result.append("Yes")
    if x14 == 1:
        result.append("Yes")
    else:
        result.append("No")
    if x15 == 1:
        result.append("Yes")
    else:
        result.append("No")
    if x16 == 1:
        result.append("Yes")
    else:
        result.append("No")
    if x17 == 1:
        result.append("Yes")
    else:
        result.append("No")
    print(result)
    return filename, result, Fsentence