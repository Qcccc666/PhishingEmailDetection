from html.parser import HTMLParser

#邮件正文情感特征字典
keys_list = ['deny','anxiety','anger','sad','understand','hesitation','certain','suppress','believe']
emotions_dict = {
    'deny': [],
    'anxiety' : [],
    'anger' : [],
    'sad' : [],
    'understand' : [],
    'hesitation' : [],
    'certain' : [],
    'suppress' : [],
    'believe' : []
}

#邮件标题特征列表
subject_list = ['account','Account','ACCOUNT','Debit','debit','DEBIT','recently','Recently','RECENTLY',
                'Access','access','ACCESS','INFORMATION','Information','information','RISK','Risk','risk',
                'Bank','bank','BANK','LOG','Log','log','SECURITY','Security','security','Client','client','CLIENT',
                'Notification','notification','NOTIFICATION','Service','service','SERVICE','Confirm','confirm','CONFIRM',
                'CONFIRMATION','Conformation','confirmation','limit','limits','Limit','Limited','limited','LIMITATION','Limitation','limitation',
                'Password','password','PASSWORD','USER','User','user','Credit','credit','CREDIT','PAY','Pay','pay',
                'Urgent','urgent','URGENT','WARNING','warning','Warning','Payment','payment','PAYMENT']

#邮件正文html处理类
class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)  # 调用父类的构造函数, 这里调用时有self的
        self.adata = ''
        self.f = 1

    def get_adata(self):
        return self.adata.strip('\n')

    def handle_starttag(self, tag, attrs):
        # print(self.f, "Start tag:", tag)
        # for attr in attrs:
        #     print(self.f, "     attr:", attr)
        pass

    def handle_endtag(self, tag):
        # print(self.f, "End tag  :", tag)
        pass

    def handle_data(self, data):
        # print(self.f, "Data     :", data)
        self.adata += data

    def handle_comment(self, data):
        # print(self.f, "Comment  :", data)
        pass

    def handle_charref(self, name):
        pass

    def handle_decl(self, data):
        # print(self.f, "Decl     :", data)
        pass

#输出到文件->属性
file_write_phishing = "C:/Users/10753/Desktop/database/new_result/phishing_features.txt"        #情感特征加在一起
file_write_phishing_1 = "C:/Users/10753/Desktop/database/new_result/phishing1_features.txt"     #情感特征分开
file_write_phishing_2 = "C:/Users/10753/Desktop/database/new_result/phishing2_features.txt"     #不要情感特征
file_write_formal = "C:/Users/10753/Desktop/database/new_result/formal_features.txt"
file_write_formal_1 = "C:/Users/10753/Desktop/database/new_result/formal1_features.txt"
file_write_formal_2 = "C:/Users/10753/Desktop/database/new_result/formal2_features.txt"

file_phishing_contrast_1 = "C:/Users/10753/Desktop/database/new_result/phishing_contrast_1.txt"
file_formal_contrast_1 = "C:/Users/10753/Desktop/database/new_result/formal_contrast_1.txt"
file_phishing_contrast_2 = "C:/Users/10753/Desktop/database/new_result/phishing_contrast_2.txt"
file_formal_contrast_2 = "C:/Users/10753/Desktop/database/new_result/formal_contrast_2.txt"

file_amount_feature = "C:/Users/10753/Desktop/database/new_result/phishing_amount_feature.txt"
file_famount_feature = "C:/Users/10753/Desktop/database/new_result/formal_amount_feature.txt"
#打开文件->属性
phishing_name = "C:/Users/10753/Desktop/database/private-phishing4.mbox"
formal_path = "C:/Users/10753/Desktop/database/spam"


#_1为第一个对比实验,域名寿命+钓鱼邮件检查结果的
#_2为第二个对比实验，正则化@,.,%,多个域名的



