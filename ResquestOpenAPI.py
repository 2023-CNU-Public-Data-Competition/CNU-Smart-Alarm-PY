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

        if response.status_code == 200:
            data = response.json()
            if data['OutBlock'][0]['MSG'] == 'N':
                print("API SERVER DATA NULL")
                continue
            # api 응답 데이터의 최신 article_no
            api_article_last_no = (int)(data['RESULT'][0]['article_no'])
            # 보드 별로 업데이트 할 게시글이 있는지 확인 category_board_number의 last_board_no 이용
            if api_article_last_no != db_article_last_no:
                # 추후 category_board_number table update 위해 last_board_no update
                board_item[2] = api_article_last_no
                print(board_no, 'update')


        else:
            print("api SERVER ERROR")
    return update_list, total_board_list