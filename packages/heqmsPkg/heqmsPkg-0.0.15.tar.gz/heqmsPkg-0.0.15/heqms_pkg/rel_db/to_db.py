import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy
import heqms_pkg.config as cf


class to_db:
    def __init__(self):
        self.dbconfig = cf.DBConfig_Dev()

    def to_sql(self, part1, part2, deptNm):
        con = self.dbconfig
        pr = cf.PriorConfig()
        name, mdf_part1, mdf_part2 = pr.priority(part1, part2)
        deptNo = cf.UnivConfig.deptNo[deptNm]
        finalName = str(deptNo) + '_DL_HEQM_' + name.upper() + '_RESULT.csv'
        output_path = cf.linuxPath.output_path
        path = output_path + "/" + finalName

        # 결과 csv 읽어오기
        input_data = pd.read_csv(path, index_col=0)
        input_data.index = input_data.index + 1
        input_data['RELEVANCE'] = round(input_data['RELEVANCE'], 3)

        # engine = sqlalchemy.create_engine("postgresql://user:password@host:port/database")
        url = "mysql+mysqldb://" + con.user + ":" + con.password + "@" + con.host + ":" + str(con.port) + "/" + con.db + '?charset=utf8'
        print(url) # url 확인

        engine = create_engine(url, encoding='utf-8')
        conn = engine.connect()

        # DB입력
        input_data.to_sql(name=finalName, con=engine, if_exists='replace', index=True, index_label='id',
                          dtype={

                              'id': sqlalchemy.types.INTEGER(),

                              str(mdf_part1).upper() + '_NM': sqlalchemy.VARCHAR(255),

                              str(mdf_part1).upper() + '_CD': sqlalchemy.types.VARCHAR(255),

                              str(mdf_part2).upper() + '_NM': sqlalchemy.types.VARCHAR(255),

                              str(mdf_part2).upper() + '_CD': sqlalchemy.types.VARCHAR(255),

                              'RELEVANCE': sqlalchemy.types.FLOAT(),

                              'DEPARTMENT_CD': sqlalchemy.types.VARCHAR(255)

                          })
