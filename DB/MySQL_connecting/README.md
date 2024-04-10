## main.py
reset, select, insert, delete, update 함수 작동확인

## ranking_defs.py

ranking_db - ranking 테이블

![image](https://github.com/chhc0505/SP_5/assets/70686425/6c9ed331-3895-4530-a317-8c0f3d69323e)

rank는 웹 상에서 출력할 때 score을 내림차순해서 얻을 수 있으므로 ranking 테이블에서 삭제

* ranking_reset 함수 : ranking table 초기화

* select_ranking_table : ranking table을 순회, 내림차순으로 출력

* ranking_insert : id(str), score을 입력받아 ranking table 내에 삽입

* ranking_delete : id를 key로 ranking table에서 제거

* ranking_update : id를 key로 score update

## user_defs.py

user_db - user 테이블

![image](https://github.com/chhc0505/SP_5/assets/70686425/e6121e16-cc90-4ccb-a590-b23a2737fcc0)

* user_reset 함수 : user table 초기화

* select_user_table : user table 순회, 출력

* user_insert : id(str), user name(str), password(str)을 입력받아 user table에 삽입

* user_delete : id를 key로 user table에서 제거

* user_update : id를 key로 user name(str), password(str) update


## etc..

1. id를 key로 받아서 id 변경 불가

2. id가 key이므로 중복 불가, 예외처리 필요 (백엔드 코드와 합칠 때 예외처리 할 예정입니다!)

