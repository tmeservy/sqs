## https://github.com/kunalgupta777/Moustache-Adder-/blob/master/moustache.py
## this script adds a brown moustache to all detected faces in a photograph!
## Using Haar Cascade Classifier
## @author :- Kunal Gupta ( cite as kg777)

import sys
import mustache

source_image_path = sys.argv[1]  ## Add the image name here
mustache.add_mustache(source_image_path)
