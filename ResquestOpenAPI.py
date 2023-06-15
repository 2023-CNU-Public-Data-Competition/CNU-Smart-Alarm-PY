import mysql.connector
import secret
import requests
import json


def call_openAPI(total_board_list, user_selected_board_id_list):

    # borad 별 업데이트 내용
    update_list = []
    update_list_item = {
        "category_no" : "",
        "update_cnt" : 0,
        "update_article" : []
    }
    # open api 호출
    url = "https://api.cnu.ac.kr/svc/offcam/pub/homepageboardContents"
    # 요청 파라미터
    request_data = {
        "P_board_no": "board_no",
        "AUTH_KEY": secret.api_auth_key
    }

    for board_item in total_board_list:
        category_no = board_item[0]
        board_no = board_item[1]
        db_article_last_no = board_item[2]

        # board 별 open api 호출
        request_data['P_board_no'] = board_no
        try:
            response = requests.post(url, data=json.dumps(request_data))
        except:
            print("API SERVER ERROR : NOT CONNECTED")


        else:
            print("api SERVER ERROR")
    return update_list, total_board_list