import os
import heqms_pkg.machine_learning.ml_pvdm as ml
import heqms_pkg.rel_db.save_result as sr
import heqms_pkg.rel_db.to_db as tdb
import heqms_pkg.config as cf


def require():
    export = 'pip install -r requirements.txt'
    os.system(export)


def learning(part1, part2, deptNm):
    machine = ml.ml_pvdm()
    machine.learning(part1, part2, deptNm)  # 학습 (처음 1번만 사용하면 됌)


def save_result(part1, part2, deptNm):
    # 결과값 출력 및 csv 저장
    save = sr.save_result()
    save.result(part1, part2, deptNm)  # 학습한 모델로 결과값 저장


def to_db(part1, part2, deptNm):
    # DB테이블 생성 및 저장
    toDB = tdb.to_db()
    toDB.to_sql(part1, part2, deptNm)  # DB 입력


def run(part1, part2, deptNm):
    if deptNm not in cf.UnivConfig.deptNm:
        print('입력한 학과가 없습니다. 함수를 다시 호출하십시오.')
    else:
        if part1 not in cf.UnivConfig.partNm or part2 not in cf.UnivConfig.partNm:
            print('입력한 파트인자가 없습니다. 함수를 다시 호출하십시오.')
        else:
            choose = int(input('1. 패키지 설치 + 학습 + 결과 저장 + DB 입력 \n'
                               '2. 학습 + 결과 저장 + DB 입력 \n'
                               '3. 학습 + 결과 저장 \n'
                               '4. 결과 저장 + DB 입력 \n'
                               '5. 결과 저장만 \n'
                               '6. DB 입력만 \n'
                               '1, 2, 3, 4, 5, 6 중 선택하십시오. \n'
                               ))

            if choose == 1:
                require()
                print('==================')
                print('필수 패키지 설치 완료')
                print('==================')
                learning(part1, part2, deptNm)
                print('===============')
                print('머신러닝 학습 완료')
                print('===============')
                save_result(part1, part2, deptNm)
                print('================')
                print('결과 csv 저장 완료')
                print('================')
                to_db(part1, part2, deptNm)
                print('===========')
                print('DB 저장 완료')
                print('===========')

            elif choose == 2:
                learning(part1, part2, deptNm)
                print('===============')
                print('머신러닝 학습 완료')
                print('===============')
                save_result(part1, part2, deptNm)
                print('================')
                print('결과 csv 저장 완료')
                print('================')
                to_db(part1, part2, deptNm)
                print('===========')
                print('DB 저장 완료')
                print('===========')

            elif choose == 3:
                learning(part1, part2, deptNm)
                print('===============')
                print('머신러닝 학습 완료')
                print('===============')
                save_result(part1, part2, deptNm)
                print('================')
                print('결과 csv 저장 완료')
                print('================')

            elif choose == 4:
                save_result(part1, part2, deptNm)
                print('================')
                print('결과 csv 저장 완료')
                print('================')
                to_db(part1, part2, deptNm)
                print('===========')
                print('DB 저장 완료')
                print('===========')

            elif choose == 5:
                save_result(part1, part2, deptNm)
                print('================')
                print('결과 csv 저장 완료')
                print('================')

            elif choose == 6:
                to_db(part1, part2, deptNm)
                print('===========')
                print('DB 저장 완료')
                print('===========')

            else:
                print('입력한 숫자 : ' + str(choose))
                print('숫자가 다릅니다. 함수를 다시 호출하십시오.')

