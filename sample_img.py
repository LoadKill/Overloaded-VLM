import cv2
import os
import json

def draw_boxes_with_cv2_raw_coords(box_dict, img_folder, save_folder="output_cv2"):
    os.makedirs(save_folder, exist_ok=True)

    for filename, annotations in box_dict.items():
        img_path = os.path.join(img_folder, filename)

        if not os.path.exists(img_path):
            print(f"[오류] 이미지 파일 없음: {img_path}")
            print(f"[경고] 이미지 없음: {filename}")
            continue

        img = cv2.imread(img_path)
        if img is None:
            print(f"[오류] 이미지 로딩 실패: {filename}")
            continue

        for ann in annotations:
            if ann.get("DRAWING") == "Box":
                try:
                    x1, y1, x2, y2 = map(float, ann["BOX"].split(","))
                    pt1 = (int(x1), int(y1))
                    pt2 = (int(x2), int(y2))

                    # 빨간색(BGR), 두께 3
                    cv2.rectangle(img, pt1, pt2, (0, 0, 255), thickness=3)

                except Exception as e:
                    print(f"[오류] 박스 좌표 오류 ({filename}): {ann['BOX']} -> {e}")

        out_path = os.path.join(save_folder, filename)
        cv2.imwrite(out_path, img)

    print(f"[완료] 결과 이미지가 '{save_folder}'에 저장되었습니다.")

# 사용 예시
if __name__ == "__main__":
    with open("data_final.json", "r", encoding="utf-8") as f:
        box_dict = json.load(f)

    draw_boxes_with_cv2_raw_coords(box_dict, img_folder="./raw/big_truck/x/")
