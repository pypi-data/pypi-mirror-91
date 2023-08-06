# youku-upload
Upload videos to Youku from the command line

# Usage

`youku-upload --client-id YOUR-CLIENT-ID  --access-token YOUR-ACCESS-TOKEN file-to-upload.mp4`

More command arguments, please check:

```
usage: command.py [-h] --client-id CLIENT_ID --access-token ACCESS_TOKEN
                  [--title TITLE] [--tags TAGS] [--description DESCRIPTION]
                  [--copyright-type COPYRIGHT_TYPE]
                  [--public-type PUBLIC_TYPE] [--category CATEGORY]
                  [--watch-password WATCH_PASSWORD]
                  FILE [FILE ...]

Upload videos to Youku from the command line

Before you use this tool, you should create your application at https://cloud.youku.com/app

Youku support these formats: 
    wmv,avi,dat,asf,rm,rmvb,ram,mpg,mpeg,3gp,mov,mp4,m4v,dvix,dv,dat,mkv,flv,vob,ram,qt,divx,cpk,fli,flc,mod

positional arguments:
  FILE                  file to upload

optional arguments:
  -h, --help            show this help message and exit
  --client-id CLIENT_ID
                        application client id
  --access-token ACCESS_TOKEN
                        access token
  --title TITLE         2-50 characters, default is file name
  --tags TAGS           1-10 tags joined with comma
  --description DESCRIPTION
                        less than 2000 characters
  --copyright-type COPYRIGHT_TYPE
                        'original' or 'reproduced', default is 'original'
  --public-type PUBLIC_TYPE
                        'all' or 'friend' or 'password'
  --category CATEGORY   
                        default is 'Others', options contains:
                        TV => 电视剧
                        Movies => 电影
                        Variety => 综艺
                        Anime => 动漫
                        Music => 音乐
                        Education => 教育
                        Documentary => 纪实
                        News => 资讯
                        Entertainment => 娱乐
                        Sports => 体育
                        Autos => 汽车
                        Tech => 科技
                        Games => 游戏
                        LifeStyle => 生活
                        Fashion => 时尚
                        Travel => 旅游
                        Parenting => 亲子
                        Humor => 搞笑
                        Wdyg => 微电影
                        Wgju => 网剧
                        Pker => 拍客
                        Chyi => 创意视频
                        Zpai => 自拍
                        Ads => 广告
                        Others => 其他
  --watch-password WATCH_PASSWORD
                        if --public-type is password

```