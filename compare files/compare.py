
# ��Python�Ƚ������ļ�
# �����ͬ����0

def cmpstr(str1, str2):
    col = 0
    for c1, c2 in zip(str1, str2):
        if c1 == c2:
            col += 1
            continue
        else :
            break
        
    #�ж��������˳�ѭ���ģ�����һ������Ǵ����Ȳ�ͬ
    if c1 != c2 or len(str1) != len(str2):
        return col+1
    else :
        return 0
    
file1 = open("C:\\01_MY_job\\A_TO_DO\\TWR-K60D100M_PKG_sdk_2_0_windows_all\\boards\\twrk60d100m/demo_apps/sai/sai.c",'r')
file2 = open("C:\\01_MY_job\\A_TO_DO\\TWR-K24F120M_PKG_sdk_2_0_windows_all/boards/twrk24f120m/demo_apps/sai/sai.c",'r')

fa = file1.readlines()
fb = file2.readlines()
file1.close()
file2.close()

#��GBK���룬�������Դ��������ַ�
fa = [ str.decode("gbk") for str in fa]
fb = [ str.decode("gbk") for str in fb]

row = 0
col = 0

#��ʼ�Ƚ�����
for str1, str2 in zip(fa, fb):
    col = cmpstr(str1,str2)
    # col=0��˵���������
    if col == 0 :
        row += 1
        continue
    else:
        break

##�����һ�в�ͬ�������ļ����Ȳ�һ��
if str1 != str2 or len(fa) != len(fb):
    #��ӡ����ͬ����������򣬲��Ѳ�ͬ��ǰһ��󱾾��ӡ����
    #��������ַ��ǲ�ͬ�ĵط�
    print "row:", row+1, "col:", col
    print "file a is:n", fa[row-1],fa[row][:col+1], "n"
    print "file b is:n", fb[row-1],fb[row][:col+1], "n"
else :
    print "All are same!"

#��ȡ�û����롣    
raw_input("Press Enter to exit.")
