from default_funcs import *

fake_word_list = ['Account','Inconvenience','Recently','Access',
                   'Information','Risk','Bank','Limited','Social',
                   'Credit','Log','Security' ,'Click','Minutes',
                   'Service','Identity','Password','Suspension',
                   'Verify','Debit','Suspended','Limit','Update',
                   'Member','Statement','User','Conﬁrm','Restrict',
                   'Client','Hold']

dot_max = 375
atb_max = 84
domain_max = 20
url_max = 93

def blacklist(subject,content):
    subject = str(subject)
    content = str(content)
    if subject:
        subject_words = re.split(':|/| ',subject.strip())
        # print(subject_words)
        for word in subject_words:
            if word in fake_word_list:
                return 1

    if content:
        for word in fake_word_list:
            if word in content:
                return 1

    return 0

def get_max(now,max):
    max_i = max
    if int(now) > int(max):
        max_i = now

    return max_i

if __name__ == "__main__":

    mbox = mailbox.mbox(phishing_name, factory=mbox_reader)
    for message in mbox:
        try:
            message_subject = message['Subject']
            message_from = message['From']
            message_reply_to = message['Reply-To']
            message_Id = message['Message-Id']
            message_formal = getBody(message)

            all_url = all_link(str(message_formal))

            # p1 = point_num(all_url)
            # p2 = percent_num(all_url) + ai_num(all_url)
            # p3 = domain_name(all_url)
            # p4 = url_accounts(all_url)
            #
            # dot_max = get_max(p1,dot_max)
            # atb_max = get_max(p2,atb_max)
            # domain_max = get_max(p3,domain_max)
            # url_max = get_max(p4,url_max)


            x1 = is_Domain_Name_Same(str(message_from), str(message_Id))
            x2 = blacklist(str(message_subject),str(message_formal))
            x3 = real_host_ip(str(message_formal))
            x4 = point_num(all_url)/dot_max
            x5 = (percent_num(all_url) + ai_num(all_url))/atb_max
            x6 = domain_name(all_url)/domain_max
            x7 = url_accounts(all_url)/url_max
            x8 = url_differ(str(message_formal))
            x9 = is_From_Reply_Same(message_from,message_reply_to)
            # print(message)
            print(dot_max, atb_max, domain_max, url_max)
            print(x5,x6,x7)


            Fsentence = str(x1) + ',' + str(x2) + ',' + str(x3) + ',' + str(x4) + ',' + str(
                x5) + ',' + str(x6) + ',' + str(x7) + ',' + str(x8) + ',' + str(x9)

            file_write = open(file_phishing_contrast_2, 'a+')
            file_write.writelines(Fsentence + '\n')


        except UnicodeDecodeError as error:
            print(error)

        print("--------------------------------------------------")
