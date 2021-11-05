from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js
from pywebio.session import download
from pywebio import start_server
from convert import vid_to_audio,vid_to_avi,vid_to_gif,vid_to_mp4,yt_to_vid,yt_to_audio
import os
from io import BytesIO
from moviepy.editor import *
import pytube




# We create our webapp
def webapp():
    #setup the basic layout
    output_box = output()
    put_scrollable(output_box, height=500,keep_bottom=True)


    #collect the file/ yt video
    while True:
#data input
        data = input_group ("File input", [
            file_upload(placeholder="Upload your video file here", multiple=False, max_size='60M',name='source', value=0,accept=['.mp4','.avi','.mov'],),
            input(label='Youtube url',placeholder='Or paste your Youtube url here.', type=URL,name='url'),
            actions (name='cmd', buttons=['Proceed to conversion', {'label': 'Reset', 'type': 'reset'}])






        ])
        # if data is None:
        #     break

        if data['source'] != None:
            if data['source'].get('filename').lower().endswith('mp4')==True or data['source'].get('filename').lower().endswith('avi') or data['source'].get('filename').lower().endswith('mov') == True and data['url'] == '':
                while True:
                    format = input_group("Choose your export format",[
                        radio(label='Export format',options=['mp4','avi','gif','mp3'],required=False, name='radio'),
                        select(label='Select the size of your new file that you want relative to the original file.',options=['The Same Size','0.9x','0.5x','0.3x','0.1x'], name='resizer' ),
                        actions(name='last', buttons=['Submit', 'Go back'])
                    ])
#resizing factors
                    if format['resizer'] == 'The Same Size':
                        resize_fac = 1

                    if format['resizer'] == '0.9x':
                        resize_fac = 0.9

                    if format['resizer'] == '0.5x':
                        resize_fac = 0.5

                    if format['resizer'] == '0.3x':
                        resize_fac = 0.3

                    if format['resizer'] == '0.1x':
                        resize_fac = 0.1


                    if format['last'] == 'Submit' and format['radio'] == None:
                        put_warning('Please choose the format to convert to , try again',closable=True)

                    if format['last'] == 'Go back':
                        run_js('window.location.reload()')

                    if format['radio'] != None:
                        break
                if format['last'] == 'Submit' and format['radio'] == 'mp4':
                            FILE_OUTPUT = 'output.mp4'
                            if os.path.isfile (FILE_OUTPUT):
                                os.remove (FILE_OUTPUT)
                            with use_scope('vid_to_mp4'):
                                put_loading(shape='border',color='info')
                            with open (FILE_OUTPUT, "wb") as out_file:
                                out_file.write(data['source'].get('content'))

                            clear('vid_to_mp4')
                            output_box.append(put_file(FILE_OUTPUT,content=open('output.mp4', 'rb').read(),label='output.mp4'))


                if format['last'] == 'Submit' and format['radio'] == 'mp3':
                            FILE_OUTPUT = 'output.mp4'
                            if os.path.isfile (FILE_OUTPUT):
                                os.remove (FILE_OUTPUT)
                            with open (FILE_OUTPUT, "wb") as out_file:
                                out_file.write(data['source'].get('content'))
                            with use_scope('vid_to_audio'):
                                put_loading(shape='border',color='info')
                            vid_to_audio(source=FILE_OUTPUT,resize_factor=resize_fac,export='output.mp3')
                            clear('vid_to_audio')


                            output_box.append(put_file('output.mp3',content=open('output.mp3', 'rb').read(),label='output.mp3'))


                if format['last'] == 'Submit' and format['radio'] == 'gif':
                            FILE_OUTPUT = 'output.mp4'
                            if os.path.isfile (FILE_OUTPUT):
                                os.remove (FILE_OUTPUT)
                            with open (FILE_OUTPUT, "wb") as out_file:
                                out_file.write(data['source'].get('content'))

                            with use_scope('vid_to_gif'):
                                put_loading(shape='border',color='info')

                            vid_to_gif(source=FILE_OUTPUT,resize_factor=resize_fac,export='output.gif')
                            clear('vid_to_gif')
                            output_box.append(put_file('output.gif',content=open('output.gif', 'rb').read(),label='output.gif'))

                if format['last'] == 'Submit' and format['radio'] == 'avi':
                    FILE_OUTPUT = 'output.avi'
                    if os.path.isfile (FILE_OUTPUT):
                        os.remove (FILE_OUTPUT)

                    with use_scope('vid_to_avi'):
                                put_loading(shape='border',color='info')

                    with open (FILE_OUTPUT, "wb") as out_file:
                        out_file.write (data['source'].get ('content'))
                    clear('vid_to_avi')
                    output_box.append (put_file (FILE_OUTPUT, content=open ('output.avi', 'rb').read (), label='output.avi'))

        # format the user wants from yt video
        if data['url'] != '' and data['source'] == None:
            if not (data['url'].startswith('https://www.youtube.com/watch?v=') or data['url'].startswith('www.youtube.com/watch?v=') or data['url'].startswith('https://youtu.be/') or data['url'].startswith('http://www.youtube.com/watch?v=')):
                popup ('Error yt', [
                    put_markdown ("We only support youtube as a website to download things from"),
                    put_buttons (['Ok'], onclick=lambda _: close_popup ())
                ])
            if data['url'].startswith('https://www.youtube.com/watch?v=') or data['url'].startswith('www.youtube.com/watch?v=') or data['url'].startswith('https://youtu.be/') or data['url'].startswith('http://www.youtube.com/watch?v='):
                while True:
                    linker = input_group ("Choose your export format", [
                        radio (label='Export format', options=['mp4', 'mp3'], required=False,
                               name='radio'),
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
                    if os.path.isfile ('output.mp4'):
                        os.remove ('output.mp4')
                    with use_scope('yt_to_mp4'):
                       put_loading(shape='border',color='info')
                    yt_to_vid(data['url'],export='output')
                    clear('yt_to_mp4')
                    output_box.append(put_file(name='output.mp4',content=open('output.mp4', 'rb').read(),label='download me!'))

                if linker['last'] == 'Submit' and linker['radio'] == 'mp3':

                    if os.path.isfile ('output.mp3'):
                        os.remove ('output.mp3')
                    with use_scope('vid_to_mp3'):
                       put_loading(shape='border',color='info')
                    yt_to_audio(data['url'], export='output')
                    clear('vid_to_mp3')
                    put_loading(shape='border',color='info')

                    output_box.append (put_file (name='output.mp3', content=open ('output.mp3', 'rb').read()))

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
    start_server(webapp, debug = True, port=port,cdn=False)