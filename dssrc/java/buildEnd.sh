javac -d ./classes -cp ./lib4/*:/usr/local/cuda/lib64/*:./classes ./src/TestEnd.java
#javac -d ./classes -cp ./lib/* ./src/*.java
java -cp ./classes:/usr/local/cuda/lib64/*:./lib4/* TestEnd
