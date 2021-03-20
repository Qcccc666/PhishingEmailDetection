
from default_funcs import *

if __name__ == "__main__":
    mbox = mailbox.mbox(phishing_name, factory=mbox_reader)

    for message in mbox:
        message_Date = message.get('Date')
        message_formal = getBody(message)
        date = exDate(message_Date)

        all_url = all_link(str(message_formal))
        modal = find_modal(all_url)

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
            x11) + ',' + str(x12) + ',' + str(x10) + ',' + str(x14) + ',' + str(host) + ',' + str(date)


        file_write = open(file_phishing_contrast_1, 'a+')
        file_write.writelines(Fsentence + '\n')

