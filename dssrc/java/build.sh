#javac -d ./classes -cp ./lib/*:/usr/local/cuda/lib64/* ./src/*.java
javac -d ./classes -cp ./lib1/* ./src/Test.java
java -cp ./classes:./lib1/* Test
