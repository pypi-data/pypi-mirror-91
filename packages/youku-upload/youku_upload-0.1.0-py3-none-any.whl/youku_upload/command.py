import argparse
import progressbar

from youku_upload import YoukuUpload

description = '''
Upload videos to Youku from the command line

Before you use this tool, you should create your application at https://cloud.youku.com/app

Youku support these formats: 
    wmv,avi,dat,asf,rm,rmvb,ram,mpg,mpeg,3gp,mov,mp4,m4v,dvix,dv,dat,mkv,flv,vob,ram,qt,divx,cpk,fli,flc,mod
'''


class DictNameSpace(dict):
    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item)

    def __delattr__(self, item):
        try:
            del self[item]
        except KeyError:
            raise AttributeError(item)


def main():
    parse = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=description)
    parse.add_argument('file', metavar='FILE', nargs='+', help='file to upload')
    parse.add_argument('--client-id', required=True, help='application client id')
    parse.add_argument('--access-token', required=True, help='access token')
    parse.add_argument('--title', required=False, help='2-50 characters, default is file name')
    parse.add_argument('--tags', required=False, help='1-10 tags joined with comma')
    parse.add_argument('--description', required=False, help='less than 2000 characters')
    parse.add_argument('--copyright-type', required=False, help="'original' or 'reproduced', default is 'original'")
    parse.add_argument('--public-type', required=False, help="'all' or 'friend' or 'password'")
    parse.add_argument('--category', required=False,
                       help="""
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
""")
    parse.add_argument('--watch-password', required=False, help="if --public-type is password")

    options = parse.parse_args(namespace=DictNameSpace())
    ignore_keys = ['file', 'client_id', 'access_token']
    dict_options = {k: v for k, v in options.items() if v is not None and k not in ignore_keys}
    bar = progressbar.ProgressBar(widgets=[
        progressbar.Percentage(),
        ' ', progressbar.Bar(),
        ' ', progressbar.FileTransferSpeed(),
        ' ', progressbar.DataSize(), '/', progressbar.DataSize('max_value'),
        ' ', progressbar.Timer(),
        ' ', progressbar.AdaptiveETA(),
    ])

    def callback(completed, total_size):
        if not hasattr(bar, "next_update"):
            if hasattr(bar, "maxval"):
                bar.maxval = total_size
            else:
                bar.max_value = total_size
            bar.start()
        bar.update(completed)

    def finish():
        if hasattr(bar, "next_update"):
            return bar.finish()

    for file in options.file:
        video_id = None

        try:
            print(f'start upload file: {file}...')
            video_id = YoukuUpload(options.client_id, options.access_token,
                                   file).upload(callback=callback, **dict_options)
        finally:
            finish()

        print(f'\nfinish upload, please check: https://v.youku.com/v_show/id_{video_id}.html')


if __name__ == '__main__':
    main()
