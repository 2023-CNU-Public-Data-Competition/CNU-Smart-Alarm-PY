def tag_classification(article_title):
    TAG = ""
    category_dict = {
        'CONTEST': ['대회', '공모전'],
        'INTERN_JOB': ['인턴', '채용', '인턴쉽', '인턴십'],
        'SCHOLARSHIP': ['장학', '장학금'],
        'SCHEDULE': ['계절학기'],
        'GRADUATION': ['졸업'],
        'LECTURE': ['교육', '특강', '포럼']
    }
    category_scores = {}
    for category, keywords in category_dict.items():
        score = sum(keyword in article_title for keyword in keywords)
        if score > 0:
            category_scores[category] = score
        if score == 0:
            TAG = "NOTICE"

    if category_scores:
        max_score = max(category_scores.values())
        top_categories = [category for category, score in category_scores.items() if score == max_score]
        TAG = top_categories[0]

    return TAG