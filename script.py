import re
import requests
import json
import csv
import os
import time
import subprocess
import shutil

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class Api_Post_fail(Error):
    """Raised when the post to the API fails"""
    def __init__(self,  message='API Post failed'):
        self.message = message
        super().__init__(self.message)

class Api_Get_fail(Error):
    """Raised when the get to the API fails"""
    def __init__(self,  message='API Get failed'):
        self.message = message
        super().__init__(self.message)

class Api_Request_fail(Error):
    """Raised when the request to the API fails"""
    def __init__(self,  message='API request failed'):
        self.message = message
        super().__init__(self.message)

if __name__ == "__main__":
    
    #input_string='personalise -s "Hey {name}. I just made my first synthetic video, made with the Synthesia API!" -b background.jpg -d data.csv -o videos'
    input_string=input("Please input command: \n")
    d_regex=r"(-d){1}\s{1}(\S+){1}"
    data_file_name=re.search(d_regex,input_string).group(2)
    print(data_file_name)
    s_regex=r"(-s){1}[\s]{1}[\'\"“”‘’„”«»]{1}((.)+)['\"“”‘’„”«»]{1}"
    _s=re.search(s_regex,input_string).group(2)
    print(_s)
    b_regex=r"(-b){1}\s{1}(\S+){1}"
    background_image_file_name=re.search(b_regex,input_string).group(2)
    print(background_image_file_name)
    o_regex=r"(-o){1}\s{1}(\S+){1}"
    directory_to_save_to=re.search(o_regex,input_string).group(2)
    print(directory_to_save_to)
    elements_regex=r"\{{1}[\w\d\sA-Za-z]+\}{1}"
    elements_to_replace=list(set(re.findall(elements_regex,_s)))
    print(elements_to_replace)
    save_directory=os.path.join(os.path.expanduser('~'),directory_to_save_to)
    if not os.path.isdir(save_directory):
        os.mkdir(save_directory)
        print('Made directory in home folder')
    with open(data_file_name) as csv_file:
        reader = csv.DictReader(csv_file)
        template_inputs_list=[]
        for row in reader:
            template_inputs_list.append(row)
    print(template_inputs_list)

    create_video_dictionary_list=[]
    for dictionary in template_inputs_list :
        script=_s
        create_video_dictionary={}
        input_dictionary={}
        #input_dictionary['actor']='mike_costume1_cameraA'
        #input_dictionary['actor']='gloria_costume1_cameraA'
        #input_dictionary['actor']= 'sofia_costume2_cameraA'
        #input_dictionary['actor']="santa_costume2_cameraA"
        #input_dictionary['actor']='nina_costume1_cameraA'
        #input_dictionary['actor']='ruby_costume1_cameraA'
        input_dictionary['actor']="jack_costume1_cameraA"

        input_dictionary['background']='green_screen'
        create_video_dictionary['title']=dictionary['id']
        for element in elements_to_replace:
            element_to_sub=dictionary.get(element[1:-1]) #remove {}
            #print(element_to_sub)
            if element_to_sub is not None:
                script=script.replace(element,element_to_sub)
        input_dictionary['script']=script
        input_dictionary_list=[]
        input_dictionary_list.append(input_dictionary)
        create_video_dictionary['input']=input_dictionary_list
        create_video_dictionary_list.append(create_video_dictionary)
    
    url='https://api.synthesia.io/v1/videos'
    api_key='525c0648e66de982ffa6d37000e2f64a'
    authorization_header={'Authorization': api_key}
    video_id_list=[]

    for create_video_dictionary in create_video_dictionary_list:
        parameters=create_video_dictionary
        video=requests.post(url,json=parameters,headers=authorization_header)
        if video.status_code != 201:
            raise Api_Post_fail
        video_id=video.json()['id']
        video_id_list.append(video_id)

    video_id_list_copy=video_id_list[:]
    time_delay=10
    while True:
        for video_id in video_id_list_copy:
            requests_url=url+'/'+video_id
            request=requests.get(requests_url,headers=authorization_header)
            if request.status_code !=200:
                raise Api_Request_fail   
            request_status=request.json()['status']
            if request_status == 'IN_PROGRESS':
                print(video_id+' production not complete')
            
            if request_status == 'COMPLETE':
                print(video_id+' production complete')
                download_link=request.json()['download']
                video_title=request.json()['title']
                file_name=video_title+'_green.mp4'
                download=requests.get(download_link)
                save_path=os.path.join(save_directory,file_name)
                if os.path.isfile(save_path):
                    overwrite_file_check=input("Overwrite file? Type Y to continue\n").lower()
                    if overwrite_file_check=='y':
                        with open(save_path, 'wb') as f:
                            f.write(download.content)
                            print('File downloaded and saved')
                    else:
                        print('File not downloaded')
                else:
                    with open(save_path, 'wb') as f:
                        f.write(download.content)
                        print('File downloaded and saved')
                video_id_list.remove(video_id)    
            print('Waiting {} seconds to prevent hitting rate limit.'.format(time_delay)) 
            time.sleep(time_delay) #so it doesn't hit rate limit     
        video_id_list_copy=video_id_list[:]
        if video_id_list==[]:
            break
    
    shutil.copy(background_image_file_name,save_directory)
    for dictionary in create_video_dictionary_list:
        video_title=dictionary['title']
        print(save_directory)
        command=f'ffmpeg -i {background_image_file_name} -i {video_title+"_green.mp4"} -filter_complex "[1:v]chromakey=0x2CD788:0.2:0.0[ckout];[0:v][ckout]overlay[o]" -map [o] -map 1:a {video_title+".mp4"}'
        subprocess.run(command, shell=True, cwd=save_directory)



    