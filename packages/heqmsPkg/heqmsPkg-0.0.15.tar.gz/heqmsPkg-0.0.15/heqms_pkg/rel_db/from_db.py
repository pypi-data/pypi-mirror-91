import pymysql
import pandas as pd
import heqms_pkg.config as cf

class MysqlController:
    def __init__(self):
        self.config = cf.DBConfig_Dev()
        self.conn = pymysql.connect(host=self.config.host, port=self.config.port, user=self.config.user,
                                    password=self.config.password, db=self.config.db, charset='utf8')
        self.curs = self.conn.cursor()

    def select_subject(self, deptNm):
        sql = 'SELECT courseNm, lectGoalConcat_P, lectIntro_P, lectDescConcat_P FROM ai_subject_dictionary_cg WHERE deptNm LIKE ' + '"%' + deptNm + '%"'
        self.curs.execute(sql)
        res = self.curs.fetchall()

        subject_ma = pd.DataFrame(columns=['sub_nm', 'ma1', 'ma2', 'ma3'])
        sub_col = subject_ma.columns

        for i in range(len(sub_col)):
            for j in range(len(res)):
                subject_ma.loc[j, sub_col[i]] = str(res[j][i]).replace(" ", "_").replace("\\/", ",").replace(",", " ")

        return subject_ma

        self.conn.commit()
        self.conn.close()

    def select_job(self, deptNm):
        sql = 'SELECT job_name, parsing_job_overview, parsing_job_task FROM ontology_heqm_job_dictionary WHERE job_choice LIKE ' + '"%' + deptNm + '%"'
        self.curs.execute(sql)
        res = self.curs.fetchall()

        job_ma = pd.DataFrame(columns=['job_nm', 'ma1', 'ma2'])
        job_col = job_ma.columns

        for i in range(len(job_col)):
            for j in range(len(res)):
                job_ma.loc[j, job_col[i]] = str(res[j][i]).replace(" ", "_").replace("\\/", ",").replace(",", " ")

        return job_ma

        self.conn.commit()
        self.conn.close()

    def select_ma(self, part, deptNm):
        config = cf.UnivConfig.deptNo
        sql = 'SELECT ' + part + '_code, ' + part + '_ai_data FROM DL_HEQM_' + part.upper() +'_DICTIONARY' + ' WHERE '+ part +'_choice_deptCd LIKE ' + '"%' + config[deptNm] + '%"'
        self.curs.execute(sql)
        res = self.curs.fetchall()

        ma = pd.DataFrame(res, columns=['code', 'ma'])

        for i in range(len(ma)) :
            ma['ma'][i] = str(ma["ma"][i]).replace(" ", "_").replace("\\/", ",").replace(",", " ")

        return ma

        self.conn.commit()
        self.conn.close()


    def select_cdName(self, part, deptNm):
        config = cf.UnivConfig.deptNo
        sql = 'SELECT ' + part + '_code, ' + part + '_name FROM DL_HEQM_' + part.upper() +'_DICTIONARY' + ' WHERE '+ part +'_choice_deptCd LIKE ' + '"%' + config[deptNm] + '%"'
        self.curs.execute(sql)
        res = self.curs.fetchall()

        cd = pd.DataFrame(res, columns=[str(part)+'_cd', str(part)+'_name'])

        return cd

        self.conn.commit()
        self.conn.close()

def method():
    print("method executed")