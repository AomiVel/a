import pytube, subprocess
import sys, os, textwrap


# エラーを無視するやつ
def _try(func, excepted_value=None):
    try:
        return func()
    except:
        return excepted_value

# ターミナルをクリア　clsコマンド
def clear():
    subprocess.call('cls', shell=True)
    print('== YouTube Local Player ==')


clear()


while True:
    # 取得するYouTube動画のURL
    url = input('YouTube URL:')
    
    clear()
    print('YouTube URL:', url)

    # YouTubeオブジェクトを作成
    yt = pytube.YouTube(url)

    # streamsを取得
    streams = yt.streams

    # video, audioを仕分け
    videos = []
    audios = []
    video_audios = []

    for stream in streams:
        if stream.includes_video_track and stream.includes_audio_track:
            video_audios.append(stream)
        elif stream.includes_video_track and not stream.includes_audio_track:
            videos.append(stream)
        else:
            audios.append(stream)


    while True:
        # ダウンロード方法の取得
        how_to_dl = input(
        textwrap.dedent("""
        ダウンロードの方法を選択してください
        ・va  : 動画と音声両方が含まれるストリームをダウンロードします（高速、低質）
        ・v+a : 動画と音声を片方ずつダウンロードし、結合します（低速）
        ・v   : 動画のみダウンロードします（高速）
        ・a   : 音声のみダウンロードします（高速）

        ・c   : URL再選択

        ダウンロード方法:""")
        )


        # URL再入力
        if how_to_dl == 'c':
            clear()
            break

        # VA
        elif how_to_dl == 'va':
            clear()
            print('YouTube URL:', url)
            print('ダウンロード方法:', 'VA')
            print()

            # 選択肢を表示
            for index, video_audio in enumerate(video_audios):
                print(f"番号：{index}")
                print("  情報：{0.resolution} / {0.fps}fps / {0.abr}".format(video_audio))
            print()
            print('c：ダウンロード方法再選択')
            print()

            # ダウンロード番号を入力
            inputed_value = input('ダウンロード番号:')

            # ダウンロード方法再選択
            if inputed_value == 'c':
                clear()
                print('YouTube URL:', url)
                continue
        
            # 選択されたインデックスのストリームをとる
            dl_stream = video_audios[int(inputed_value)]

            clear()
            print('YouTube URL:', url)
            print('ダウンロード方法:', 'VA')
            print('情報:', "{0.resolution} / {0.fps}fps / {0.abr}".format(dl_stream))
            print()

            # ダウンロードするディレクトリのパスを作成
            downloaded_dir = os.sep.join(__file__.split(os.sep)[:-1]) + os.sep + 'downloaded'

            # ダウンロード
            dl = dl_stream.download(downloaded_dir)

            # ダウンロードしたファイルを開く
            subprocess.call(dl, shell=True)
            print()

            # ダウンロードされたファイルを消すかどうか聞く
            remove_file = input('ダウンロードされたファイルを削除しますか？[y/n]')
            # 消す
            if remove_file.upper() == 'Y':
                os.remove(dl)
                clear()
                print('YouTube URL:', url)
                print('ダウンロード方法:', 'VA')
                print('情報:', "{0.resolution} / {0.fps}fps / {0.abr}".format(dl_stream))
                print('ファイル: 削除')
                print()
            # 消さない
            else:
                clear()
                print('YouTube URL:', url)
                print('ダウンロード方法:', 'VA')
                print('情報:', "{0.resolution} / {0.fps}fps / {0.abr}".format(dl_stream))
                print('ファイル: 保持')
                print('場所:', downloaded_dir)
                print()
            sys.exit(0)
        
        # V + A
        elif how_to_dl in ('v+a', 'vpa'):
            clear()
            print('YouTube URL:', url)
            print('ダウンロード方法:', 'V+A')
            print()

            # 選択肢を出力
            for index in range(max(len(videos), len(audios))):
                print(textwrap.dedent(f"""\
                番号：{index}
                  動画：{_try(lambda: '{0.resolution} / {0.fps}fps'.format(videos[index]), '-')}
                  音声：{_try(lambda: audios[index].abr, '-')}"""))
            print()
            print('c：ダウンロード方法再選択')
            print()

            # ダウンロード番号を入力
            download_no = input('ダウンロード番号(vid aud)：')

            # ダウンロード方法再選択
            if download_no == 'c':
                clear()
                print('YouTube URL:', url)
                continue
            
            # 動画と音声のインデックスを取得
            vid_num = int(download_no.split()[0])
            aud_num = int(download_no.split()[1])

            # 取得したインデックスからオブジェクトを取得
            video = videos[vid_num]
            audio = audios[aud_num]
            

            clear()
            print('YouTube URL:', url)
            print('ダウンロード方法:', 'V+A')
            print('情報', "{0.resolution} / {0.fps}fps / {1.abr}".format(video, audio))

            # ダウンロードディレクトリのパスを作成
            dl_dir = os.sep.join(__file__.split(os.sep)[:-1])

            # 拡張し、フォルダを除いたファイル名を取得
            filename = '.'.join(video.default_filename.split('.')[:-1])

            # ダウンロード
            video_path = video.download(filename=dl_dir + os.sep + 'video')
            audio_path = audio.download(filename=dl_dir + os.sep + 'audio')

            # 結果が出力されるパスを作成
            result_path = dl_dir + os.sep + 'downloaded' + os.sep + filename + '.mp4'

            # 結合するコマンド
            cmd = "ffmpeg -i \"{0}\" -i \"{1}\" -map 0:0 -map 1:0 \"{2}\"".format(video_path, audio_path, result_path)

            # コマンドを実行
            subprocess.call(cmd, shell=True)

            # 音声、動画ファイルを削除
            os.remove(video_path)
            os.remove(audio_path)

            # ファイルを開く
            subprocess.call(result_path, shell=True)


            clear()
            print('YouTube URL:', url)
            print('ダウンロード方法:', 'V+A')
            print('情報', "{0.resolution} / {0.fps}fps / {1.abr}".format(video, audio))
            print()

            # ダウンロードされたファイルの削除関連
            remove_file = input('ダウンロードされたファイルを削除しますか？[y/n]')
            if remove_file.upper() == 'Y':
                os.remove(result_path)
                clear()
                print('YouTube URL:', url)
                print('ダウンロード方法:', 'V+A')
                print('情報', "{0.resolution} / {0.fps}fps / {1.abr}".format(video, audio))
                print('ファイル: 削除')
                print()
            else:
                clear()
                print('YouTube URL:', url)
                print('ダウンロード方法:', 'V+A')
                print('情報', "{0.resolution} / {0.fps}fps / {1.abr}".format(video, audio))
                print('ファイル: 保持')
                print('場所:', dl_dir + os.sep + 'downloaded')
                print()
            sys.exit(0)

        # V
        elif how_to_dl == 'v':
            clear()
            print('YouTube URL:', url)
            print('ダウンロード方法:', 'V')
            print()

            # 選択肢を出力
            for index, video in enumerate(videos):
                print(textwrap.dedent("""\
                番号：{1}
                  情報：{0.resolution} / {0.fps}fps""".format(video, index)))
            print()
            print('c：ダウンロード方法再選択')
            print()

            # ダウンロード番号を入力
            dl_no = input('ダウンロード番号：')

            # ダウンロード方法再選択
            if dl_no == 'c':
                clear()
                print('YouTube URL:', url)
                continue

            # 動画を取得
            video = videos[int(dl_no)]

            clear()
            print('YouTube URL:', url)
            print('ダウンロード方法:', 'V')
            print('情報:', "{0.resolution} / {0.fps}fps".format(video))

            # ダウンロードディレクトリ
            dl_dir = os.sep.join(__file__.split(os.sep)[:-1]) + os.sep + 'downloaded'

            # ダウンロード
            dl = video.download(dl_dir)

            # ファイルを開く
            subprocess.call(dl, shell=True)
            print()

            # ダウンロードされたファイルの削除関連
            remove_file = input('ダウンロードされた動画を削除しますか？[y/n]')
            if remove_file.upper() == 'Y':
                os.remove(dl)
                clear()
                print('YouTube URL:', url)
                print('ダウンロード方法:', 'V+A')
                print('情報', "{0.resolution} / {0.fps}fps".format(video))
                print('ファイル: 削除')
                print()
            else:
                clear()
                print('YouTube URL:', url)
                print('ダウンロード方法:', 'V+A')
                print('情報', "{0.resolution} / {0.fps}fps".format(video))
                print('ファイル: 保持')
                print('場所:', dl_dir)
                print()
            sys.exit(0)
        
        # A
        elif how_to_dl == 'a':
            clear()
            print('YouTube URL:', url)
            print('ダウンロード方法:', 'V')
            print()

            # 選択肢
            for index, audio in enumerate(audios):
                print(textwrap.dedent("""\
                番号：{1}
                  情報：{0.abr}""".format(audio, index)))
            print()
            print('c：ダウンロード方法再選択')
            print()

            # DL番号
            dl_no = input('ダウンロード番号：')

            # DL方法再選択
            if dl_no == 'c':
                clear()
                print('YouTube URL:', url)
                continue
            
            # 音声ファイル取得
            audio = audios[int(dl_no)]

            clear()
            print('YouTube URL:', url)
            print('ダウンロード方法:', 'V')
            print('情報:', audio.abr)

            # DLディレクトリパス
            dl_dir = os.sep.join(__file__.split(os.sep)[:-1]) + os.sep + 'downloaded'

            # DL
            dl = audio.download(dl_dir)

            # ファイル開く
            subprocess.call(dl, shell=True)
            print()

            # ファイル削除関連
            remove_file = input('ダウンロードされた音声を削除しますか？[y/n]')
            if remove_file.upper() == 'Y':
                os.remove(dl)
                clear()
                print('YouTube URL:', url)
                print('ダウンロード方法:', 'V+A')
                print('情報:', audio.abr)
                print('ファイル: 削除')
                print()
            else:
                clear()
                print('YouTube URL:', url)
                print('ダウンロード方法:', 'V+A')
                print('情報:', audio.abr)
                print('ファイル: 保持')
                print('場所:', dl_dir)
                print()
            sys.exit(0)