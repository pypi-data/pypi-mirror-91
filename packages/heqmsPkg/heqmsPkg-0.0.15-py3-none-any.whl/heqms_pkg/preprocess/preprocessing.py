import pandas as pd
from nltk.tokenize import RegexpTokenizer
from gensim.models.doc2vec import TaggedDocument
import os
import heqms_pkg.rel_db.from_db as fdb
import heqms_pkg.config as cf

class Preprocessing:
    def __init__(self):
        # 파싱된 교과목, 직업 정보 불러오기
        # self.file_path='C:/Users/dirty/python/Jupyter/dldoc2vec/input/job_subject.txt'
        self.fdb = fdb.MysqlController()

    # 토큰화 함수 생성
    def nltk_tokenizer(self, _wd):
        return RegexpTokenizer(r'\w+').tokenize(_wd.lower())

    # 폴더 생성
    def createFolder(self, directory):
        try:
            #if not os.path.exists(directory):
            if not os.path.isdir(directory):
                os.makedirs(directory)
        except OSError:
            print('에러: 해당 경로로 폴더를 생성할 수 없습니다 : ' + directory)

    # 전처리 과정
    def from_df(self, part1, part2, deptNm):
        # 파싱된 교과목, 직업 정보 텍스트 파일 가져오기
        ma1 = self.fdb.select_ma(part1, deptNm)
        ma2 = self.fdb.select_ma(part2, deptNm)

        ma1_token = pd.DataFrame(columns=['cd', 'token_description'])  # 통합 입력할 교과목 데이터프레임 생성
        ma2_token = pd.DataFrame(columns=['cd', 'token_description'])  # 통합 입력할 직업 데이터프레임 생성

        # description 및 task 컬럼 단어들을 토큰화하여 'token_description' 변수로 통합
        ma1_token['cd'] = ma1['code']
        ma1_token['token_description'] = ma1['ma'].apply(self.nltk_tokenizer)

        ma2_token['cd'] = ma2['code']
        ma2_token['token_description'] = ma2['ma'].apply(self.nltk_tokenizer)

        # 두 데이터 통합
        data = pd.concat([ma1_token, ma2_token], ignore_index=True)

        pr = cf.PriorConfig()
        name, mdf_part1, mdf_part2 = pr.priority(part1, part2)
        deptNo = cf.UnivConfig.deptNo[deptNm]

        input_path = cf.linuxPath.input_path
        model_path = cf.linuxPath.model_path
        output_path = cf.linuxPath.output_path

        self.createFolder(input_path)
        self.createFolder(model_path)
        self.createFolder(output_path)

        # 데이터 저장
        finalName = str(deptNo) + '_DL_HEQM_' + name.upper() + '_INPUT' + ".csv"
        data.to_csv(input_path+"/"+finalName, mode='w')

        return data

    def ma_code(self, part, deptNm):
        ma = self.fdb.select_ma(part, deptNm)
        ma_name = pd.DataFrame(columns=['code'])
        ma_name['code'] = ma['code']

        return ma_name

    def to_tag(self, part1, part2, deptNm):
        data = self.from_df(part1, part2, deptNm)

        # 태그문서로 변환
        doc_data = data[['cd', 'token_description']].values.tolist()
        tagged_data = [TaggedDocument(words=_d, tags=[uid]) for uid, _d in doc_data]

        return tagged_data
