from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js,set_env
from pywebio import start_server
from convert import vid_to_audio,vid_to_avi,vid_to_gif,vid_to_mp4,yt_to_mp4,yt_to_audio, yt_videotitle
import os
import pywebio
from pywebio import config








@config(title="Uniconv")


# We create our webapp
def webapp():
    set_env(output_max_width='110%')
    image_url="https://res.cloudinary.com/dj9urm5ic/image/upload/v1637080520/logo_7_biwhaz.png"
    run_js("""
    $('#favicon32,#favicon16').remove();
    $('head').append('<link rel="icon" type="image/png" href="%s">')
    """ % image_url)

    put_html("""
    <style type="text/css">
      .pywebio { padding-top: 0; }
      body {
        margin: 0;
        padding-top: 80px;
      }
      .header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        min-height: 80px;
        width: 100%;
        background-color: #2400ff;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .logoBox {
        padding-left: 2vw;
      }
      .coffee {
        padding-right: 10px;
        height: 80px;
      }
      .header img {
        max-height: 80px;
        background-color: inherit !important;
      }
      .coffeeImg {
        height: 80px!important;
      }
      .buttonWrap{
        display:flex;
        padding-top: 4px;
      }
      .ph{
        height: 60px;
      }
    </style>
    <header class="header">
      <div class="logoBox">
        <img src="https://res.cloudinary.com/dj9urm5ic/image/upload/v1637080521/logo_8_p4ww0l.png" />
      </div>
     <div class="buttonWrap">
      <div class="ph">
        <a href="" target="_blank"
          ><img src="https://res.cloudinary.com/dj9urm5ic/image/upload/v1636980992/ProductHuntButton_nowhh5.png" alt="Product Hunt Link"
        /></a>
      </div>
      <div class="coffee">
        <a href="https://www.patreon.com/bePatron?u=10145585" target="_blank"
          ><img
            class="coffeeImg"
            src="https://res.cloudinary.com/dj9urm5ic/image/upload/v1637682600/ProductHuntButton_nowhh5_2_.png_xzmrcl.png"
            alt="Buy Me A Coffee Link"
        /></a>
      </div>
     </div>
    </header>
        <!-- Yandex.Metrika counter -->
    <script type="text/javascript" >
       (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
       m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
       (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
       ym(86550879, "init", {
            clickmap:true,
            trackLinks:true,
            accurateTrackBounce:true,
            webvisor:true
       });
    </script>
    <noscript><div><img src="https://mc.yandex.ru/watch/86550879" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
    <!-- /Yandex.Metrika counter -->
    """)


    def file_tutorial():
        popup(title='Tutorial',content=[
            put_html('<iframe src="https://scribehow.com/embed/PyWebIO_Application__AxO3BZKGRfeScJIq28BRDw?skipIntro=true" width="100%" height="640" allowfullscreen frameborder="0"></iframe>')
        ],closable=True,size='large')
    def yt_tutorial():
        popup(title='Tutorial',content=[
            put_html('<iframe src="https://scribehow.com/embed/PyWebIO_Application__kpw-4cuoR2mzGLNPUeO1Zw?skipIntro=true" width="100%" height="640" allowfullscreen frameborder="0"></iframe>')
        ],closable=True,size='large')

    def put_explainer():
        popup(title='What is it?',content =[put_image(open('screenshot (2).png', 'rb').read())],size='large',closable=True)

    #setup the basic layout

    toast(content = 'Click here to learn how this app works!',duration=0,color='warn',onclick=lambda : put_explainer())
    #put_row([put_button('How to download the video/audio from youtube',color='warning',onclick=lambda : yt_tutorial()), put_button('How to convert a videofile',color='warning',onclick= lambda : file_tutorial())])
    put_text('''
            ''')
    output_box = output()
    put_scrollable(output_box, height=500,keep_bottom=True)
    put_link(name='Report a bug',url='https://forms.gle/wNiCuo7d3c1vsBb66',new_window=True)

    set_scope(name='output_md')
    output_box.append(put_markdown('> Hey there! Your output files will appear here \U0001F916',scope='output_md'))


    #collect the file/ yt video
    while True:

#data input
        data = input_group ("File input", [
            file_upload(placeholder="Upload your video file here", multiple=False, max_size='100M',name='source', value=0,accept=['.mp4','.avi','.mov'],),
            input(label='Youtube url',placeholder='Or paste your Youtube url here.', type=URL,name='url'),
            actions (name='cmd', buttons=['Proceed to conversion', {'label': 'Reset', 'type': 'reset'}])
        ])

        # if data is None:
        #     break
        file__name = os.path.splitext(data['source'].get('filename'))[0]

        if data['source'] != None:
            if data['source'].get('filename').lower().endswith('mp4')==True or data['source'].get('filename').lower().endswith('avi') or data['source'].get('filename').lower().endswith('mov') == True and data['url'] == '':
                while True:
                    format = input_group("Choose your export format",[
                        radio(label='Export format',options=['mp4','avi','gif','mp3'],required=False, name='radio'),
                        actions(name='last', buttons=['Submit', 'Go back'])
                    ])

                    resize_fac = 1
                    toast('It can take some time to process your file, be patient ',duration=0,color='warn')




                    if format['last'] == 'Submit' and format['radio'] == None:
                        put_warning('Please choose the format to convert to , try again',closable=True)

                    if format['last'] == 'Go back':
                        run_js('window.location.reload()')

                    if format['radio'] != None:
                        break
                if format['last'] == 'Submit' and format['radio'] == 'mp4':

                            FILE_OUTPUT = f'{file__name}.mp4'
                            if os.path.isfile (FILE_OUTPUT):
                                os.remove (FILE_OUTPUT)
                            with use_scope('vid_to_mp4'):
                                put_row([put_loading(shape='border',color='info'),put_text('Your file is being processed')])

                            with open (FILE_OUTPUT, "wb") as out_file:
                                out_file.write(data['source'].get('content'))

                            clear('vid_to_mp4')
                            output_box.append(put_file(FILE_OUTPUT,content=open(f'{file__name}.mp4', 'rb').read(),label=f'{file__name}.mp4'))


                if format['last'] == 'Submit' and format['radio'] == 'mp3':

                            FILE_OUTPUT = f'{file__name}.mp4'
                            if os.path.isfile (FILE_OUTPUT):
                                os.remove (FILE_OUTPUT)
                            with open (FILE_OUTPUT, "wb") as out_file:
                                out_file.write(data['source'].get('content'))
                            with use_scope('vid_to_audio'):
                                 put_row([put_loading(shape='border',color='info'),put_text('Your file is being processed')])
                            vid_to_audio(source=FILE_OUTPUT,resize_factor=resize_fac,export=f'{file__name}.mp3')
                            clear('vid_to_audio')


                            output_box.append(put_file(f'{file__name}.mp3',content=open(f'{file__name}.mp3', 'rb').read(),label=f'{file__name}.mp3'))


                if format['last'] == 'Submit' and format['radio'] == 'gif':

                            FILE_OUTPUT = f'{file__name}.mp4'
                            if os.path.isfile (FILE_OUTPUT):
                                os.remove (FILE_OUTPUT)
                            with open (FILE_OUTPUT, "wb") as out_file:
                                out_file.write(data['source'].get('content'))

                            with use_scope('vid_to_gif'):
                                 put_row([put_loading(shape='border',color='info'),put_text('Your file is being processed')])
                            toast('Gifs usually take some time to process',duration=0,color='warn')
                            vid_to_gif(source=FILE_OUTPUT,resize_factor=resize_fac,export=f'{file__name}.gif')
                            clear('vid_to_gif')
                            output_box.append(put_file(f'{file__name}.gif',content=open(f'{file__name}.gif', 'rb').read(),label=f'{file__name}.gif'))

                if format['last'] == 'Submit' and format['radio'] == 'avi':

                    FILE_OUTPUT = f'{file__name}.avi'
                    if os.path.isfile (FILE_OUTPUT):
                        os.remove (FILE_OUTPUT)

                    with use_scope('vid_to_avi'):
                         put_row([put_loading(shape='border',color='info'),put_text('Your file is being processed')])

                    with open (FILE_OUTPUT, "wb") as out_file:
                        out_file.write (data['source'].get ('content'))


                    clear('vid_to_avi')
                    output_box.append (put_file (FILE_OUTPUT, content=open (f'{file__name}.avi', 'rb').read (), label=f'{file__name}.avi'))

        # format the user wants from yt video
        if data['url'] != '' and data['source'] == None:
            if not (data['url'].startswith('https://www.youtube.com/watch?v=') or data['url'].startswith('www.youtube.com/watch?v=') or data['url'].startswith('https://youtu.be/') or data['url'].startswith('http://www.youtube.com/watch?v=')):
                popup ('Error yt', [
                    put_markdown ("We only support youtube as a website to download things from"),
                    put_buttons (['Ok'], onclick=lambda _: close_popup ()),
                    run_js('window.location.reload()')
                ])
            if data['url'].startswith('https://www.youtube.com/watch?v=') or data['url'].startswith('www.youtube.com/watch?v=') or data['url'].startswith('https://youtu.be/') or data['url'].startswith('http://www.youtube.com/watch?v='):
                yt_title = yt_videotitle(data['url'])
                while True:
                    linker = input_group ("Choose your export format", [
                        radio (label='Export format', options=['mp4', 'mp3'], required=False,name='radio'),
                        actions (name='last', buttons=['Submit', 'Go back'])
                    ])
                    if linker['radio'] != None:
                        break
                if linker['last'] == 'Submit' and linker['radio'] == None:
                    put_warning ('Please choose the format to convert to , try again', closable=True)

                if linker['last'] == 'Go back':
                    run_js ('window.location.reload()')

#check if the yt url is valid
            try:
                if linker['last'] == 'Submit' and linker['radio'] == 'mp4':

                    if os.path.isfile (f'{yt_title}.mp4'):
                        os.remove (f'{yt_title}.mp4')
                    with use_scope('yt_to_mp4'):
                        put_row([put_loading(shape='border',color='info'),put_text('Your file is being processed')])
                    yt_to_mp4(data['url'],export=yt_title)
                    clear('yt_to_mp4')
                    output_box.append(put_file(name=f'{yt_title}.mp4',content=open(f'{yt_title}.mp4', 'rb').read()))

                if linker['last'] == 'Submit' and linker['radio'] == 'mp3':

                    if os.path.isfile (f'{yt_title}.mp3'):
                        os.remove (f'{yt_title}.mp3')
                    with use_scope('vid_to_mp3'):
                        put_row([put_loading(shape='border',color='info'),put_text('Your file is being processed')])
                    yt_to_audio(data['url'], export=yt_title)
                    clear('vid_to_mp3')

                    output_box.append ((put_file (name=f'{yt_title}.mp3', content=open (f'{yt_title}.mp3', 'rb').read())))




            except pytube.exceptions.VideoUnavailable:
                popup ('Invalid url', [
                    put_markdown("You have inputed an invalid youtube url, try again"),
                    put_buttons (['Ok'], onclick=lambda _: close_popup())
                ])

# #errors


        if data['url'] != '' and data['source'] != None:
            popup('Error, both formats', [
                put_markdown ("You can't convert a file and a youtube link at the same  time"),
                put_buttons (['Ok'], onclick=lambda _: close_popup())
            ])
#app launch


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    start_server(webapp, debug = False, port=port, websocket_ping_interval=30,session_expire_seconds=999999, session_cleanup_interval=999999)