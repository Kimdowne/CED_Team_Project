import time
from ultralytics import YOLO
import cv2

## test = YOD() 라고 가정할 때
## 게이지 == test.gayG 변수 (gayG 변수가 올라가거나 내려감에 따라 게이지가 올라가거나 내려간다고 생각하면 됨)
## 작동 방식 | capture_frame 으로 순간 장면 읽기 -> process_predictions 로 읽은 장면 분석 후 return objects (객체 : 신뢰도) -> gay 로 objects 분석 및 게이지 +1 or -0.5 해줌
## gay 에 트리거가 있음. (gayG >= 10 일 때 return ary(인식된 객체 str)) 


class YOD :
    def __init__(self, model_path = "yolov8s", frame_width = 320, frame_height = 240) :
        self.model = YOLO(model_path) # YOLOv8s 모델 로드

        self.capture = cv2.VideoCapture(0) # 카메라 프레임 세팅
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        self.gayG = 0

    def capture_frame(self) : 
        ret, frame = self.capture.read()  # 카메라에서 프레임 읽기
        if not ret:
            print("Failed to grab frame. Exiting...")
            return None
        return frame
      
    def process_predictions(self,frame):
        detected_objects = []
        results = self.model.predict(source=frame, verbose=False)

        for box in results[0].boxes:
            confidence = round(box.conf.item() * 100)  # 신뢰도
            if confidence > 65:  # 신뢰도가 70% 이상일 때만 필터링
                cls_index = int(box.cls)  # 클래스 인덱스
                obj_name = self.model.names[cls_index]  # 객체 이름
                detected_objects.append({obj_name: confidence})
        return detected_objects
    
    def gay(self, objects) :
        ## 사물 인식 후 생긴 objects 리스트에서 특정 사물 (eg.person) 이 있는지 확인 후 게이지 ++
        ## 사람일 경우 + 많이, 아닐경우 + 조금
        o_key = []
        ary = ""
        for i in objects :
            swtich = next(iter(i.keys()))
            o_key.append(swtich)
        # print(o_key)

        if 'person' in o_key :
            # print("게이지 + 1")
            if self.gayG <= 10 :
                self.gayG += 1
            else :
                pass
        else :
            if self.gayG > 0 :
                # print("게이지 - 0.5")
                self.gayG -= 0.5
            else :
                pass

        # print(self.gayG)
        for i in o_key :
            ary += f"({i}) "

        if self.gayG >= 10 :  
            return ary

    
    

# YOLO 객체 감지 실행
test = YOD()

while True :
    frame = test.capture_frame() ## 캡쳐한 순간 프레임 저장
    predict = test.process_predictions(frame) ## 인식한 프레임을 기반으로 분석
    gay = test.gay(predict) ## 분석한 값을 게이지 함수에 대입 후 게이지 +1 or -0.5
    time.sleep(0.2) ## 감지되는 시간 설정
    if test.gayG >= 10 :
        print(gay)
        break
