from django.shortcuts import render, get_object_or_404, redirect
from PIL import Image
import numpy as np
import os
import cv2
import keras
from keras.utils import np_utils
# import sequential model and all the required layers
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Dense,Flatten,Dropout
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .forms import *
from .models import animal
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
# Create your views here.


def define_model(request):
    data = []
    labels = []
    #animals_list = ['cats','dogs','birds','fishs','monkeys','lions','']
    #Code for making images into array -
    cats=os.listdir("media/cats")
    for cat in cats:
        #print(cat)
        imag = cv2.imread("media/cats/"+cat)
        #print(imag)
        img_from_ar = Image.fromarray(imag)
        resized_image = img_from_ar.resize((50, 50))
        data.append(np.array(resized_image))
        labels.append(0)

    dogs=os.listdir("media/dogs")
    for dog in dogs:
        imag=cv2.imread("media/dogs/"+dog)
        img_from_ar = Image.fromarray(imag, 'RGB')
        resized_image = img_from_ar.resize((50, 50))
        data.append(np.array(resized_image))
        labels.append(1)

    birds=os.listdir("media/birds")
    for bird in birds:
        imag=cv2.imread("media/birds/"+bird)
        img_from_ar = Image.fromarray(imag, 'RGB')
        resized_image = img_from_ar.resize((50, 50))
        data.append(np.array(resized_image))
        labels.append(2)

    fishs=os.listdir("media/fishs")
    for fish in fishs:
        imag=cv2.imread("media/fishs/"+fish)
        img_from_ar = Image.fromarray(imag, 'RGB')
        resized_image = img_from_ar.resize((50, 50))
        data.append(np.array(resized_image))
        labels.append(3)

    monkeys=os.listdir("media/monkeys")
    for monkey in monkeys:
        imag=cv2.imread("media/monkeys/"+monkey)
        img_from_ar = Image.fromarray(imag, 'RGB')
        resized_image = img_from_ar.resize((50, 50))
        data.append(np.array(resized_image))
        labels.append(4)

    lions=os.listdir("media/lions")
    for lion in lions:
        imag=cv2.imread("media/lions/"+lion)
        img_from_ar = Image.fromarray(imag, 'RGB')
        resized_image = img_from_ar.resize((50, 50))
        data.append(np.array(resized_image))
        labels.append(5)

    spinners=os.listdir("media/spinners")
    for spinner in spinners:
        imag=cv2.imread("media/spinners/"+spinner)
        img_from_ar = Image.fromarray(imag, 'RGB')
        resized_image = img_from_ar.resize((50, 50))
        data.append(np.array(resized_image))
        labels.append(6)

    #Since the “data” and “labels” are normal array , convert them to numpy arrays-
    animals=np.array(data)
    labels=np.array(labels)

    #Now save these numpy arrays so that you dont need to do this image manipulation again.
    np.save("animals",animals)
    np.save("labels",labels)

    #Load the arrays ( Optional : Required only if you have
    # closed your jupyter notebook after saving numpy array )
    animals=np.load("animals.npy")
    labels=np.load("labels.npy")

    #Now shuffle the “animals” and “labels” set so that you get
    # good mixture when you separate the dataset into train and test
    s=np.arange(animals.shape[0])
    np.random.shuffle(s)
    animals=animals[s]
    labels=labels[s]

    #Make a variable num_classes which is the total number of animal
    # categories and a variable data_length which is size of dataset
    num_classes=len(np.unique(labels))
    data_length=len(animals)

    #Divide data into test and train
    #Take 90% of data in train set and 10% in test set
    (x_train,x_test)=animals[(int)(0.1*data_length):],animals[:(int)(0.1*data_length)]
    x_train = x_train.astype('float32')/255
    x_test = x_test.astype('float32')/255
    train_length=len(x_train)
    test_length=len(x_test)

    #Divide labels into test and train
    (y_train,y_test)=labels[(int)(0.1*data_length):],labels[:(int)(0.1*data_length)]

    #Make labels into One Hot Encoding
    #One hot encoding
    y_train=keras.utils.to_categorical(y_train,num_classes)
    y_test=keras.utils.to_categorical(y_test,num_classes)

    #make model
    model=Sequential()
    model.add(Conv2D(filters=16,kernel_size=2,padding="same",activation="relu",input_shape=(50,50,3)))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Conv2D(filters=32,kernel_size=2,padding="same",activation="relu"))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Conv2D(filters=64,kernel_size=2,padding="same",activation="relu"))
    model.add(MaxPooling2D(pool_size=2))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(500,activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(7,activation="softmax"))
    model.summary()

    # compile the model
    model.compile(loss='categorical_crossentropy', optimizer='adam',
                      metrics=['accuracy'])

    #Step 4 — Train the model
    #Congrats on reaching upto this step. Your all work is over. Now just train the model and wait patiently.
    model.fit(x_train,y_train,batch_size=50
              ,epochs=100,verbose=1)

    #Step 5 — Test the model
    #Use model.evaluate to see how model work on test set
    score = model.evaluate(x_test, y_test, verbose=1)
    print('\n', 'Test accuracy:', score[1])

    return model
    #return render(request,'base.html')




def convert_to_array(img):
    im = cv2.imread("media/"+img)
    img = Image.fromarray(im, 'RGB')
    image = img.resize((50, 50))
    return np.array(image)

def get_animal_name(label):
    if label==0:
        return "cat"
    if label==1:
        return "dog"
    if label==2:
        return "bird"
    if label==3:
        return "fish"
    if label==4:
        return "monkey"
    if label==5:
        return "lion"
    if label==6:
        return "spinner"

def predict_animal(request,file):
    print("Predicting .................................")
    #messages.info(request,"Predicting .................................")
    ar=convert_to_array(file)
    ar=ar/255
    label=1
    a=[]
    a.append(ar)
    a=np.array(a)
    model = define_model(request)
    score=model.predict(a,verbose=1)
    print(score)
    label_index=np.argmax(score)
    print(label_index)
    acc=np.max(score)
    animal=get_animal_name(label_index)
    print(animal)
    #print("The predicted Animal is a "+animal+" with accuracy =    "+str(acc))

    messages.info(request,"The predicted Animal is a: "+animal)
    messages.info(request,"with accuracy: "+str(acc * 100) +" %")
    return ("The predicted Animal is a "+animal+" with accuracy =    "+str(acc))
    #return render(file,'index.html')


def predict_anim(request):
    if request.method == 'POST' :
        myfile = request.FILES['sentFile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        #os.listdir("cats")
        #file = os.listdir("media/")+myfile
        #print(file)
        print(filename)
        predict_animal(request,filename)
        form = AnimalsForm(request.POST,request.FILES['sentFile'])

        #image = form.cleaned_data['image']
        #return render(request, 'index.html', {
        #    'uploaded_file_url': uploaded_file_url
        #})
        return render(request, 'base.html')
    return render(request, 'index.html')

def create_animal(request):

    messages.success(request, 'Detect Terminate With Success')