from requests_html import HTMLSession
import re,os,pathlib,base64
import requests
import PIL.Image
from io import StringIO,BytesIO
#下載的目錄名稱

download_folder_name = "./crawler_download"
#設定要爬的張數
img_num = 300

#設定要查詢的keyword
key_word = "Pug"

download_folder_name = download_folder_name + "_" +key_word
if not os.path.exists(download_folder_name):
    os.mkdir(download_folder_name)

#爬蟲參數
sleep_time = 1
scroll_down = img_num//100*18
wait_time = 1

#設定資料夾路徑
downalod_dir = os.getcwd()+"/"+download_folder_name+"/"
print("Image will save in ",downalod_dir)

#如果資料夾不存在就新建
pathlib.Path(downalod_dir).mkdir(parents=True, exist_ok=True)

#清除資料夾裡的jpg及png檔
filelist = [ f for f in os.listdir(downalod_dir) if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".jpeg")]
for f in filelist:
    os.remove(os.path.join(downalod_dir, f))
    
    
url = 'https://www.google.com.tw/search?q='+key_word+' &rlz=1C1CAFB_enTW617TW621&source=lnms&tbm=isch&sa=X&ved=0ahUKEwienc6V1oLcAhVN-WEKHdD_B3EQ_AUICigB&biw=1128&bih=863&tbs=ift:jpg'
print(url)
#進行爬蟲
session = HTMLSession()
r = session.get(url)
js = "document.documentElement.scrollTop=1500"
r.html.render(sleep=sleep_time,scrolldown=scroll_down,wait=wait_time,script=js)
 
#找出所有html裡面tag為img的
img_arr=r.html.find("img")

#影像編號使用
img_no=0
ii = 0
for i in img_arr:
    tmp_content = ''
    try:
        #確認有沒有src的屬性
        tmp_content=(i.attrs['src'])
        if(i.attrs['class'][0] != 'rg_i'):
            tmp_content = ''
    except:
        pass
    finally:
        if tmp_content!='' and tmp_content.find('http')==-1 and tmp_content.find('/images')==-1:
            if tmp_content.find("jpeg")>-1:
                img_type='.jpg'
            else:
                img_type='.png'

            img_url=downalod_dir+'img_'+str(key_word)+'_'+str(img_no)+img_type
            print(img_url)

            with open(img_url,'wb') as file:
                #影像資料存放在 data:image/[img_type];base64,[base64編碼過的路徑]
                base64_data = re.sub('^data:image/.+;base64,', '', tmp_content)
                #進行解碼
                byte_data = base64.b64decode(base64_data)
                file.write(byte_data)
                file.flush()
                file.close() 
        elif tmp_content!='' and (tmp_content.find('https://encrypted-tbn0.gstatic.com/images')>-1):
            response = requests.get(tmp_content)
            img = PIL.Image.open(BytesIO(response.content))
            name = downalod_dir+'img_'+str(key_word)+'_'+str(img_no)
            try:
                img.save(name+".jpg")
            except:
                img.convert('RGB').save(name+".jpeg")
            
            print(name)

        if img_no < img_num:
            img_no=img_no+1
        else: 
            break