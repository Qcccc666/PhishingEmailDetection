from default_funcs import *

if __name__ == "__main__":


    eml_lists = get_emls()
    for eml in eml_lists:
        fp = open(formal_path + '/' + eml, "r", encoding='latin-1')
        message = email.message_from_file(fp)

        # extract the features of email
        message_from = message.get('From')
        message_Id = message.get('Message-Id')
        message_reply_to = message.get('Reply-To')
        message_subject = message.get('Subject')
        for par in message.walk():
            if not par.is_multipart():  # 这里要判断是否是multipart，是的话，里面的数据是无用的，至于为什么可以了解mime相关知识。
                name = par.get_param("name")  # 如果是附件，这里就会取出附件的文件名
                if name:
                    h = email.header.Header(name)
                    dh = email.header.decode_header(h)
                    fname = dh[0][0]
                    print('附件名:', fname)
                    data = par.get_payload(decode=True)  # 解码出附件数据，然后存储到文件中
                    # print(data)

                else:
                    # 不是附件，是文本内容
                    # print(par.get_payload(decode=True))  # 解码出文本内容，直接输出来就可以了。
                    message_formal = par.get_payload(decode=True)

                print('+' * 60)  # 用来区别各个部分的输出
        message_date = message.get('Date')

        #print('========================================================================')

        try:
            all_url = all_link(str(message_formal))
            modal = find_modal(all_url)
            date = exDate(message_date)

            x5 = real_host_ip(str(message_formal))
            x13 = url_differ(str(message_formal))
            x19,host = here(str(modal), str(message_formal))
            x4 = is_html(str(message_formal))
            x11 = url_accounts(all_url)
            x12 = domain_name(all_url)
            x10 = point_num(all_url)
            x14 = is_javascript(str(message_formal))
            print(x19)

            print("--------")

            Fsentence = str(x5) + ',' + str(x13) + ',' + str(x19) + ',' + str(x4) + ',' + str(
                x11) + ',' + str(x12) + ',' + str(x10) + ',' + str(x14) + ',' + str(host).replace('\n','') + ',' + str(date)

            file_write = open(file_formal_contrast_1, 'a+')
            file_write.writelines(Fsentence + '\n')

        except UnicodeDecodeError as error:
            print(error)