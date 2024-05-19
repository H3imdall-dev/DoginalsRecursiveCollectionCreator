# DoginalsRecursiveCollectionCreator
This repo is  the first dogecoin recursive doginals collection all in one  generator

doge tips are welcome details are at the bottom

this was my first python script ...

here is how you will use the tools provided to stitch an image together to make one master with all the traits embedded within the image
then move on to generating the collection based on the metadata provided
you can generate the maximum amount based on the layers or you can select an amount 
currently this build only randomises the selection when you choose a collection size lower than the full amount
i am working on v2 to work with the rarity 

this will then make the files needed to make a recursive collection on the doge blockchain
the future version will have auto inscribe feautires

here are the steps needed 

1 . please ensure all layer folders maximum of 9 layers accordingly, in the way you want the images to be layered ..
    must be the number followed by the name of the layer with a space between the number and name like in this format
    example :- 1 Background
               2 Body
               3 Eyes
               4 Smokes
               etc

2 . run imageStitcher.py
    
    you will see it creates a stitched_image.png

you need to then take this image into an online tool which will change this image into base 64 
once you have converted stitched_image.png into base 64 copy and paste it into the the part that says this <Your Stiched Image in base64> on line 10 in sketch.js

then inscribe this sketch.js file to your doginal wallet - this will be the master kanvas 

We will then run metaReader.py 
this will then print the metadata so you can see all the points inscribed within the master image 

we will then run metadata.py
this will then give you  metadata.json file with all the plotted traits and locaions 

once this is done you need to go to the inscription on ordinals wallet or drc-20 and get the master inscription id handy fot the next step
you will need doge wallet 
              image resolution eg 400x400

now we will generate all the files needed for your recursive collection

run generatehtml.py

it will prompt you for:-
the collection name 
the canvas height
the canvas width

The Inscription id of the master .. make sure this is the correct one it is vital or your whole collection will be broken IMPORTANT

then it will show you all your layers  and how many traits are in each layer 

it will show you the maximum collection size 

and it will ask you to enter any exclusions 

this is for layers that can not interact with each other 

has to be entered in this format layernumber traitname, layernumber traitname, layernumber traitname

this means these three items will never inteact with eachother 

if you want to exclude a whole layer from intercting with 1 trait you can do this also by just using this format

layernumber (of the one you dont want to intearct with the trait ) followed by layernumber traitname (thats you dont want the layer to interact with)

you can enter both formats into the one line alsons as there is a comma 

layernumber traitname, layernumber traitname, layernumber traitname,layernumber layernumber traitname, 

press etnter and it will update the new colleciton size based on the exclusions

then it will ask if you want to generate select y/n 

yes will continue 

n will exit 

if you have  made any mistakes at any time you can type exit and it will stop the script

if you continue it will ask you how many you want to generate 

you can type max and it will do the whole collection

if you select any number lower than the max it will randomize the generation with no duplicates

once you put a number in and press enter it will generate that number and put them in subfolder collection - labeled in the right format for the autointer 

it will also spit out 2 formtted jsons one for OW and one for DM you will just need to add the inscription numbers to this once the files are inscribed 

voila 

dogecoins first recursive doginals collection builder
recursive doginal builder and randomiser interface (generatehtml.py, metadata.py) built by heimdall-dev @heimdall_bull on x my doge tips welcome 
master file creation and meta data embedding and reading (imageSticher.py, metaReader.py) built by martinseeger2002 @martinseeger2002 on x my doge tips welcome 

have fun with this 

dont use it as an excuse to upload blurry crappy shit to the chain use this to strive to put higher and higher masters on chain that we can make awesome collections recusrivley 
