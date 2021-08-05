import glob
import pickle
import sys

print(sys.argv)
print(len(sys.argv))

if len(sys.argv) == 2 :
    for f in glob.glob("./{}".format(sys.argv[1])):
        with open(f,"rb") as fp:
            content = pickle.load(fp)
    print(content)

else:
    for f in glob.glob("./*dict"):
        with open(f,"rb") as fp:
            content = pickle.load(fp)
            print(content)
    
