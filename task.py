import mysql.connector
import secret
import ResquestOpenAPI, tag_classification

def get_total_board_number():
    # database 연결
    DB = mysql.connector.connect(
        host=secret.db_host,
        user=secret.db_user,
        password=secret.db_password,
        database=secret.db_name
    )
    cursor = DB.cursor()

    # open api 호출할 전체 board number load
    query = "SELECT category_no, board_no, last_update_no FROM category_board_number;"
    cursor.execute(query)

    # (카테고리 넘버, 보드 넘버, 최신 업데이트 게시글 넘버)
    result = cursor.fetchall()

    total_board_list = [list(row) for row in result]

    cursor.close()
    DB.close()

    return total_board_list


def get_selected_board_number():
    # database 연결
    DB = mysql.connector.connect(
        host=secret.db_host,
        user=secret.db_user,
        password=secret.db_password,
        database=secret.db_name
    )
    cursor = DB.cursor()

    query = "SELECT cbn.board_no FROM liked_category l " \
            "JOIN category_board_number cbn " \
            "ON l.category_no = cbn.category_no " \
            "GROUP BY l.category_no, cbn.board_no;"
    cursor.execute(query)
    result = cursor.fetchall()

    user_selected_board_id_list = [row[0] for row in result]

    cursor.close()
    DB.close()

    return user_selected_board_id_list


def update_last_board_id(total_board_list):
    # database 연결
    DB = mysql.connector.connect(
        host=secret.db_host,
        user=secret.db_user,
        password=secret.db_password,
        database=secret.db_name
    )
    cursor = DB.cursor()

    for index in total_board_list:
        board_id = index[1]
        update_last_no = index[2]

        query = "UPDATE category_board_number SET last_update_no = %s WHERE board_no = %s"
        cursor.execute(query, (update_last_no, board_id))
        DB.commit()

    cursor.close()
    DB.close()


if __name__ == "__main__":
    # category별 total board id list
    # (카테고리 넘버, 보드 넘버, 최신 업데이트 게시글 넘버)
    total_board_list = get_total_board_number()
    # user들이 선택한 board id list
    user_selected_board_id_list = get_selected_board_number()
    # open API 호출
    update_list, total_board_list = ResquestOpenAPI.call_openAPI(total_board_list, user_selected_board_id_list)
    # 전체 board의 최근 업데이트 보드 넘버 update
    update_last_board_id(total_board_list)
