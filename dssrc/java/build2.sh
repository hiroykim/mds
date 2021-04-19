javac -d ./classes -cp ./lib2/*:/usr/local/cuda/lib64/* ./src/Test2.java
#javac -d ./classes -cp ./lib/* ./src/*.java
java -cp ./classes:/usr/local/cuda/lib64/:./lib2/* Test2
