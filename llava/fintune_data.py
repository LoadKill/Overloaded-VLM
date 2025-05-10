import json
import os
import uuid

def generate_conversation_json(box_dict, image_folder, output_path):
    results = []

    for filename, annotations in box_dict.items():
        image_name = os.path.basename(filename)
        image_path = os.path.join(image_folder, image_name)
        image_id = os.path.splitext(image_name)[0]

        if not os.path.exists(image_path):
            print(f"[경고] 이미지 없음: {image_path}")
            continue

        for ann in annotations:
            if ann.get("DRAWING") == "Box":
                설명 = f"""이 사진에 나온 {ann.get("SEGMENT", "차량")}는 짐을 제대로 싣지 않고 {ann.get("COVER", "덮개 미설치")} 상태야. 이런 {ann.get("CLASS", "적재 문제")}은 주행 중에 물건이 떨어질 수도 있어서 위험하고, 특히 {ann.get("COURSE", "측면")}에서 보면 상태가 딱 보여. 이건 {ann.get("PACKAGE", "문제 차량")}으로 분류돼서 단속 대상입니다."""

                entry = {
                    "id": image_id,
                    "image": f"{image_folder}/{image_name}",
                    "conversations": [
                        {
                            "from": "human",
                            "value": "<image>\n사진 속 과적차량을 설명해줘"
                        },
                        {
                            "from": "gpt",
                            "value": 설명
                        }
                    ]
                }

                results.append(entry)
                break  # 하나의 박스만 사용하고 넘어감

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"[완료] {output_path}에 JSON 저장됨!")


if __name__ == "__main__":
    with open("data_final.json", "r", encoding="utf-8") as f:
        box_dict = json.load(f)

    generate_conversation_json(box_dict, image_folder="output_cv2", output_path="output_conversations.json")
