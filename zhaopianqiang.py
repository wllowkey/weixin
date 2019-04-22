import itchat
import math
import PIL.Image as Image
import os

new_list = []

itchat.auto_login()  # 登陆微信
friends = itchat.get_friends(update=True)  # 获取微信好友
num = 0
# 创建image文件夹保存微信好友头像照片
if not os.path.exists("image"):
    os.mkdir("image")
for friend in friends:
    # 根据用户名获取微信好友头像
    img = itchat.get_head_img(userName=friend["UserName"])
    # 保存微信好友图像
    fileImage = open("image" + "/" + str(num) + ".jpg", "wb")
    fileImage.write(img)
    fileImage.close()
    num += 1

all_image = os.listdir("image")  # 获取头像列表
each_size = int(math.sqrt(float(1920 * 1920) / len(all_image)))  # 拼接头像大小
lines = int(1920 / each_size)  # 照片墙行数
image = Image.new("RGBA", (1890, 1890))  # 创建Image对象，初始化大小
x = 0
y = 0
for i in range(1, len(all_image)):
    if i not in new_list:
        try:
            # 打开头像
            img = Image.open("image" + "/" + str(i) + ".jpg")
            # 重新设置头像大小
            img = img.resize((each_size, each_size), Image.ANTIALIAS)
            # 根据x,y坐标位置拼接图像
            image.paste(img, (x * each_size, y * each_size))
            # 下一张照片
            x += 1
            if x == lines:  # 一行一行拼接
                x = 0  # 如果一行满了，设置 x 为 0
                y += 1  # y+1 进入下一行
        except:
            pass
image.save("image" + "/" + "all.png")  # 保存照片墙
# 发送微信文件传输助手，手机可以查看
itchat.send_image("image" + "/" + "all.png", "filehelper")
