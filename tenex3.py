import tensorflow.keras
import numpy as np
import cv2

# 모델 위치
model_filename ='/home/mingyu/ten/keras_model.h5'

# 케라스 모델 가져오기
model = tensorflow.keras.models.load_model(model_filename)

# 카메라를 제어할 수 있는 객체
capture = cv2.VideoCapture(3)

# 카메라 길이 너비 조절
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# 이미지 처리하기
def preprocessing(frame):
    #frame_fliped = cv2.flip(frame, 1)
    # 사이즈 조정 티쳐블 머신에서 사용한 이미지 사이즈로 변경해준다.
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    
    # 이미지 정규화
    # astype : 속성
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

    # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
    # keras 모델에 공급할 올바른 모양의 배열 생성
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    #print(frame_reshaped)
    return frame_reshaped

# 예측용 함수
def predict(frame):
    prediction = model.predict(frame)
    return prediction

while True:
    ret, frame = capture.read()

    if cv2.waitKey(100) > 0: 
        break

    preprocessed = preprocessing(frame)
    prediction = predict(preprocessed)

  

    print(prediction[0])

    if (prediction[0,0]>0.5):
        print('tetrapod')
        cv2.putText(frame, 'tetrapod', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

    elif (prediction[0,1]>0.5):
         print('ocean tetra')
         cv2.putText(frame, 'ocean tetra', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

    elif (prediction[0,2]>0.5):
         print('road tetra')
         cv2.putText(frame, 'road tetra', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

    elif (prediction[0,3]>0.5):
         print('ocean road tetra')
         cv2.putText(frame, 'ocean road tetra', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

    elif (prediction[0,4]>0.5):
         print('rock')
         cv2.putText(frame, 'rock', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

    elif (prediction[0,5]>0.5):
         print('sea')
         cv2.putText(frame, 'sea', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

 

    else:
        print('error')
        cv2.putText(frame, 'error', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))


    cv2.imshow("VideoFrame", frame)