# Playing around with Synthesia's API 

This uses Synthesia's api to make  ai-generated videos based on a given script template and download and save them. 
When running the Python script, the user will be asked to write an input. 

The input needs to be in the form:

```
personalise -s “Hey {name}. I just made my first synthetic video, made with the Synthesia API!” -b background.jpg -d data.csv -o videos
```
Following ```-s``` the desired script template should be written (in quotation marks) with the parts of the template to be changed written between ```{}```. These labels here should refer to the column names found in the ```.csv``` file pointed to after ```-d```. This ```.csv``` file will contain the values for the template plus an ```id``` field that will be used as a file name for the video.

Following ```-b``` is the name of a ```.jpg``` file that will be the background of the video(s). The ```.jpg``` file must be the same size as the video i.e. 1920 x 1080 pixels. 

Both the ```.csv``` file and the ```.jpg``` file have to be in the same folder as the python script.

Following ```-o``` is the name of the directory that the generated videos will be saved to. Please note, this is the path from your home folder. E.g. on a Mac, for the example above, it will save to ```/Users/Username/videos```

This Python script will generate the videos and save them as desired. 

## Test cases
1) Example given in Tech Challenge 
```
personalise -s “Hey {name}. I just made my first synthetic video, made with the Synthesia API!” -b background.jpg -d data.csv -o videos
``` 

2) F1 results bulletin (for fun)

```
personalise -s "Good afternoon. Today was a very exciting {race}. Here is an interview with our winner, {winner}, driving for {constructor}." -b background.jpg -d f1_results.csv -o videos
``` 
First five races were in the ```.csv```. Interestingly and impressively, it worked reasonably well when pronouncing drivers' names etc (though of course, most of those names were Lewis Hamilton 😂). Does not recognise "grand" has to be pronounced in the French way. Background image not really suitable either.   


## Notes

* Error handling needs to be improved:
    * It is assumed the user inputs the command as explained above. Error handling needs to be implemented that ensures input is in the correct form etc
    * It is assumed that the ```.csv``` file has the required information. Error handling should check that the ```.csv``` file contains the required information and if not, stops the operation/inform user etc.
    * Can try to improve FFMPEG implementation so it works for background images that are not the correct size.
* Code needs to be modularised. (As this is only one task of personalising a video, it isn't necessary to make a function but if we want other commands other than ```personalise``` then it's better to put things into functions.)
* The green screens videos are not deleted afterwards but kept in the  output directory. The ```background.jpg``` file is also copied to this directory. (FFmpeg cannot edit existing files in-place and command line commands to delete these files not included in the python script) 
* Decided to keep a few print statements for debugging and so the user can see them when running the script. 

    


