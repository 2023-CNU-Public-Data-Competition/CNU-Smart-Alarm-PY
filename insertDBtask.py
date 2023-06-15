import mysql.connector
import secret
import tag_classification

def insert_new_post(update_list):
    # database 연결
    DB = mysql.connector.connect(
        host=secret.db_host,
        user=secret.db_user,
        password=secret.db_password,
        database=secret.db_name
    )
    cursor = DB.cursor()
    print("시작")

    for item in update_list:
        for _item in item['update_article']:
            print(_item['article_title'])
            tag = tag_classification(_item['article_title'])
            print(tag)
            import datetime
            current_date = datetime.date.today()
            query = "INSERT INTO post (article_no, category_no, article_title, article_text, writer_nm, click_cnt, attach_cnt, update_dt, tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (int(_item['article_no']), int(item['category_no']), _item['article_title'], _item['article_text'],
                    _item['writer_nm'], int(_item['click_cnt']), int(_item['attach_cnt']), current_date, tag)
            cursor.execute(query, data)
            DB.commit()
    cursor.close()
    DB.close()


def insert_new_alarm(update_list):
    category_nos = [item['category_no'] for item in update_list]

    DB = mysql.connector.connect(
        host=secret.db_host,
        user=secret.db_user,
        password=secret.db_password,
        database=secret.db_name
    )
    cursor = DB.cursor()

    cursor.execute("SELECT user_id FROM user")
    results = cursor.fetchall()
    total_user_list = [list(row) for row in results]

    for _user in total_user_list:
        # 사용자가 설정해둔 알람 목록 가져옴(keyword, category, tag 알람)
        user_selected_alarm_list = get_user_check_alarm(_user)

        user_alarm_category_list = [item for item in user_selected_alarm_list['CATEGORY']]
        # 사용자가 선택한 카테고리에서 update 된 글 alarm_list에 추가
        alarm_list = []
        for item in update_list:
            if item['category_no'] in user_alarm_category_list:
                alarm_list.append(item)

        # 1) KEYWORD 알람
        user_keyword = [item for item in user_selected_alarm_list['KEYWORD']]

        for item in alarm_list:
            update_article = item['update_article']
            for article in update_article:
                for keyword in user_keyword:
                    if keyword in (article['article_text'] or article['article_title']):
                        query = "INSERT INTO alarm (alarm_nm, alarm_type, article_no, article_title, update_dt) VALUES (?, ?, ?, ?, ?)"
                        data = (keyword, "KEYWORD", article['article_no'], article['article_title'], article['update_dt'])
                        cursor.execute(query, data)
                        DB.commit()
            alarm_list.remove(item)

        #TAG 알람
        user_TAG = [item for item in user_selected_alarm_list['TAG']]

        for item in alarm_list:
            update_article = item['update_article']
            for article in update_article:
                if article['TAG'] in user_TAG:
                    query = "INSERT INTO alarm (alarm_nm, alarm_type, article_no, article_title, update_dt) VALUES (?, ?, ?, ?, ?)"
                    data = (keyword, "TAG", article['article_no'], article['article_title'], article['update_dt'])
                    cursor.execute(query, data)
                    DB.commit()
            alarm_list.remove(item)

            # CATEGORY 알람
            user_CATEGORY = [item for item in user_selected_alarm_list['CATEGORY']]

            for item in alarm_list:
                update_article = item['update_article']
                for article in update_article:
                    if article['CATEGORY'] in user_CATEGORY:
                        query = "INSERT INTO alarm (alarm_nm, alarm_type, article_no, article_title, update_dt) VALUES (?, ?, ?, ?, ?)"
                        data = (keyword, "CATEGORY", article['article_no'], article['article_title'], article['update_dt'])
                        cursor.execute(query, data)
                        DB.commit()
                alarm_list.remove(item)