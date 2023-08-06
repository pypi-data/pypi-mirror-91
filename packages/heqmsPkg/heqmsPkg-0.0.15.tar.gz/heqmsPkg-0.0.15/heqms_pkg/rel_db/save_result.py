import pandas as pd
from gensim.models.doc2vec import Doc2Vec
import heqms_pkg.config as cf
import heqms_pkg.preprocess.preprocessing as pre
import heqms_pkg.rel_db.from_db as fdb


class save_result:
    def __init__(self):
        # 교과목, 직업 리스트 불러오기
        self.part = cf.UnivConfig().partNm
        self.dbconfig = cf.DBConfig_Dev()
        # self.deptNm = cf.UnivConfig().deptNm
        # self.subject = pre.Preprocessing().ma_name('subj', self.deptNm)
        # self.job = pre.Preprocessing().ma_name('job', self.deptNm)
        # self.subject_path = 'C:/Users/dirty/python/Jupyter/dldoc2vec/subject_name.txt'
        # self.subject = pd.read_csv(self.subject_path, names=['subject_name'])
        #
        # self.job_path = 'C:/Users/dirty/python/Jupyter/dldoc2vec/job_name.txt'
        # self.job = pd.read_csv(self.job_path, names=['job_name'])
        #
        # # 교과목 테이블 전처리
        # self.subject = self.subject.drop_duplicates(['subject_name'])
        # self.subject = self.subject.astype(str)
        # self.subject = self.subject.drop(self.subject.index[0])
        # self.subject = self.subject.reset_index(drop=True)
        # self.subject['subject_name'] = self.subject['subject_name'].str.lstrip()
        # self.subject['subject_name'] = self.subject['subject_name'].str.rstrip()
        #
        # # 직업 테이블 전처리
        # self.job = self.job.drop_duplicates(['job_name'])
        # self.job = self.job.astype(str)
        # self.job = self.job.drop(self.job.index[0])
        # self.job = self.job.reset_index(drop=True)
        # self.job['job_name'] = self.job['job_name'].str.lstrip()
        # self.job['job_name'] = self.job['job_name'].str.rstrip()

        # self.model = Doc2Vec.load('C:/Users/dirty/python/Jupyter/dldoc2vec/model/d2v.model')

    def result(self, part1, part2, deptNm):
        # 직무,직업,교과 순서 변경
        pr = cf.PriorConfig()
        name, mdf_part1, mdf_part2 = pr.priority(part1, part2)

        # 불러오기
        doc_list = pre.Preprocessing().from_df(mdf_part1, mdf_part2, deptNm)['token_description']
        nm_list = pre.Preprocessing().from_df(mdf_part1, mdf_part2, deptNm)['cd']

        # 학과명 -> 학과번호
        deptNum = cf.UnivConfig.deptNo[deptNm]
        model_path = cf.linuxPath.model_path
        fileName = str(deptNum) + '_' + name + '_d2v.model'

        model = Doc2Vec.load(model_path + "/" + fileName)
        model.random.seed(42)  # 값 고정

        # 직업명 리스트 불러오기
        part2_nm = pre.Preprocessing().ma_code(mdf_part2, deptNm)['code']  # 코드 불러오기

        final = pd.DataFrame(columns=[str(mdf_part1), str(mdf_part2), 'similarity'])  # 최종 데이터프레임 형식 생성

        for i in range(len(doc_list)):
            inferred_vector = model.infer_vector(doc_list[i])

            try:
                return_docs = model.docvecs.most_similar(positive=[inferred_vector], topn=1000)

            except TypeError as e:
                print(e)

                continue;

            # 결과 리스트 -> 테이블로 변형
            result_docs = pd.DataFrame(return_docs, columns=[str(mdf_part2), 'similarity'])
            result_docs[str(mdf_part1)] = nm_list[i]

            # for j in range(len(return_docs)):
            #     result_docs.loc[j, str(mdf_part1)] = part1_nm[i]
            #     result_docs.loc[j, str(mdf_part2)] = return_docs[j][0]
            #     result_docs.loc[j, 'similarity'] = return_docs[j][1]

            # 테이블 필터링으로 '직업'을 제외한 '교과목'만 출력
            final_docs = pd.merge(result_docs, part2_nm, left_on=str(mdf_part2), right_on='code', how='inner')
            final_docs = final_docs.drop(['code'], axis=1)

            final = final.append(final_docs[:30])

        # 파트별 코드-파트이름 가져오기
        cdnm = fdb.MysqlController().select_cdName
        cdnm_part1 = cdnm(mdf_part1, deptNm)
        cdnm_part2 = cdnm(mdf_part2, deptNm)

        # 코드에 맞는 파트이름 합치기
        final = pd.merge(final, cdnm_part1, left_on=str(mdf_part1), right_on=str(mdf_part1) + '_cd', how='inner')
        final = final.drop([str(mdf_part1) + '_cd'], axis=1)
        final = pd.merge(final, cdnm_part2, left_on=str(mdf_part2), right_on=str(mdf_part2) + '_cd', how='inner')
        final = final.drop([str(mdf_part2) + '_cd'], axis=1)

        # 기존 테이블 양식으로 변환
        hanbat_job_subject = pd.DataFrame(
            columns=[str(mdf_part1).upper() + '_NM', str(mdf_part1).upper() + '_CD', str(mdf_part2).upper() + '_NM',
                     str(mdf_part2).upper() + '_CD', 'RELEVANCE', 'DEPARTMENT_CD'])
        hanbat_job_subject[str(mdf_part1).upper() + "_CD"] = final[str(mdf_part1)]
        hanbat_job_subject[str(mdf_part2).upper() + "_CD"] = final[str(mdf_part2)]
        hanbat_job_subject['RELEVANCE'] = final['similarity']
        hanbat_job_subject['DEPARTMENT_CD'] = cf.UnivConfig.deptNo[deptNm]

        hanbat_job_subject[str(mdf_part1).upper() + '_NM'] = final[str(mdf_part1) + '_name']
        hanbat_job_subject[str(mdf_part2).upper() + '_NM'] = final[str(mdf_part2) + '_name']
        hanbat_job_subject.reset_index(drop=True, inplace=True)

        hanbat_job_subject.sort_values(by=[str(mdf_part1).upper() + '_NM', 'RELEVANCE'], axis=0,
                                       ascending=[True, False], inplace=True)
        hanbat_job_subject.reset_index(drop=True, inplace=True)

        # csv파일로 저장

        output_path = cf.linuxPath.output_path
        finalName = str(deptNum) + '_DL_HEQM_' + name.upper() + '_RESULT.csv'
        path = output_path + "/" + finalName
        hanbat_job_subject.to_csv(path, mode='w')


