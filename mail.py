# -*- coding: utf-8 -*-
import poplib
import email
import base64
import quopri
import re
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


Emails = []
Students = []
# 输入邮件地址, 口令和POP3服务器地址:
email = '595084778@qq.com' or input('Email: ')
password = 'xibozagnptribcfj' or input('Password: ')
pop3_server = 'pop.qq.com' or input('POP3 server: ')

f_err = open('error.txt', 'w')
err_cnt = 0

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def print_info(msg, indent=0):
    global err_cnt
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            # print('%s%s: %s' % ('  ' * indent, header, value))
            if header == 'From':
                print str(len(Emails)) + ' : ' + addr
                Emails.append(addr)
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            # print('%spart %s' % ('  ' * indent, n))
            # print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            # print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))
            for part in msg.walk():
                filename = part.get_filename()
                print filename
                data = part.get_payload(decode=True)
                if re.match(r'^=\?([A-Za-z0-9-]*)\?([A-Za-z])\?(.*)\?=', filename):
                    group = re.match(r'^=\?([A-Za-z0-9-]*)\?([A-Za-z])\?(.*)\?=', filename).groups()
                else:
                    err_cnt += 1
                    template = str(err_cnt) + ' : somebody attachment format wrong\n'
                    print template,
                    f_err.write(template)
                    f_att = open('attachment/'+filename, 'wb')
                    f_att.write(data)
                    f_att.close()
                    return
                filename = group[2]
                if group[1].upper() == 'B':
                    if group[0][0].upper() == 'G':
                        filename = str(base64.b64decode(filename))
                    elif group[0][0].upper() == 'U':
                        filename = str(base64.b64decode(filename)).decode('utf8')
                    else:
                        err_cnt += 1
                        template = str(err_cnt) + ' : ' + str(group[1]) + ' wrong filename format\n'
                        print template,
                        f_err.write(template)  
                elif group[1].upper() == 'Q':
                    if group[0][0].upper() == 'G':
                        filename = str(quopri.decodestring(filename))
                    elif group[0][0].upper() == 'U':
                        filename = str(quopri.decodestring(filename)).decode('utf8')
                    else:
                        err_cnt += 1
                        template = str(err_cnt) + ' : ' + str(group[1]) + ' wrong filename format\n'
                        print template,
                        f_err.write(template)  
                else:
                    err_cnt += 1
                    template = str(err_cnt) + ' : ' + str(group[1]) + ' wrong filename format\n'
                    print template,
                    f_err.write(template)                    
                # missing_padding = 4 - len(filename) % 4
                # if missing_padding:
                #     filename += b'='* missing_padding
                # filename = str(base64.b64decode(filename))
                print filename
                student_id = []
                if re.match(r'([\d]{8})', filename):
                    student_id =  re.match(r'([\d]{8})', filename).groups(0)
                else:
                    for i in filename:
                        if i.isdigit():
                            student_id.append(str(i))
                student_id = ''.join(student_id)
                f_att = open('attachment/'+filename, 'wb')
                f_att.write(data)
                f_att.close()
                print student_id + '....'
                if not re.match(r'[\d]{8}', student_id):
                    err_cnt += 1
                    template = str(err_cnt) + ' : ' + str(student_id) + ' wrong student_id format whose filename is ' + filename +'\n'
                    print template,
                    f_err.write(template) 
                    return
                print student_id + '....'
                Students.append(student_id)

# 连接到POP3服务器:
# pp = poplib.POP3_SSL(host)
server = poplib.POP3_SSL(pop3_server)
# 可以打开或关闭调试信息:
# server.set_debuglevel(1)
# 可选:打印POP3服务器的欢迎文字:
# print(server.getwelcome().decode('utf-8'))

# 身份认证:
server.user(email)
server.pass_(password)

# stat()返回邮件数量和占用空间:
# print('Messages: %s. Size: %s' % server.stat())
# list()返回所有邮件的编号:
resp, mails, octets = server.list()
# 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
# print(mails)

# 获取最新一封邮件, 注意索引号从1开始:
index = len(mails)
for i in range(1, index+1):
    resp, lines, octets = server.retr(i)
    # lines存储了邮件的原始文本的每一行,
    # 可以获得整个邮件的原始文本:
    try:
        msg_content = b'\r\n'.join(lines).decode('utf-8')
    except UnicodeDecodeError as e:
        print 'UnicodeDecodeError happen:'
        pass
    # 稍后解析出邮件:
    msg = Parser().parsestr(msg_content)
    print_info(msg)
Emails = sorted(Emails)
uniEmails = [Emails[0]]
for i in range(1,len(Emails)):
    if Emails[i-1] == Emails[i]:
        print 'repeat ' + Emails[i]
        pass
    else:
        uniEmails.append(Emails[i])
print 'total = ' + str(len(uniEmails))
f= open('Emails.txt', 'w') #open
for i in range(len(uniEmails)):
    template = "%d : %s\n" %(i+1, uniEmails[i])
    print template,
    f.write(template)
f.close()
Students = sorted(Students)
uniStudents = [Students[0]]
for i in range(1,len(Students)):
    if Students[i-1] == Students[i]:
        print 'repeat ' + Students[i]
        pass
    else:
        uniStudents.append(Students[i])
f= open('Students.txt', 'w') #open
for i in range(len(uniStudents)):
    template = "%d : %s\n" %(i+1, uniStudents[i])
    print template,
    f.write(template)
f.close()
# 可以根据邮件索引号直接从服务器删除邮件:
# server.dele(index)
# 关闭连接:
server.quit()