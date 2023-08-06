class Config:
    APP_NAME = 'myapp'
    SECRET_KEY = 'secret-key-of-myapp'
    ADMIN_NAME = 'administrator'

    AWS_DEFAULT_REGION = 'ap-northeast-2'

    STATIC_PREFIX_PATH = 'static'
    ALLOWED_IMAGE_FORMATS = ['jpg', 'jpeg', 'png', 'gif']
    MAX_IMAGE_SIZE = 5242880  # 5MB


class DBConfig_Dev(Config):
    host = '125.132.25.172'
    port = 3307
    user = 'heqms'
    password = 'heqms_00!!'
    db = 'HEQMS'


class UnivConfig(Config):
    partName = {
        '직업': 'job',
        '직무': 'au',
        '교과': 'subj',
        'job': 'job',
        'au': 'au',
        'subj': 'subj'
        }
    deptNm = ['기계공학과',
              '신소재공학과',
              '화학생명공학과',
              '산업경영공학과',
              '설비공학과',
              '창의융합학과',
              '전기공학과',
              '전자·제어공학과',
              '컴퓨터공학과',
              '정보통신공학과',
              '건설환경공학과',
              '도시공학과',
              '건축공학과',
              '건축학과',
              '시각디자인학과',
              '산업디자인학과',
              '영어영문학과',
              '중국어과',
              '일본어과',
              '공공행정학과',
              '경영회계학과',
              '경제학과'
              ]

    deptNo = {'기계공학과': '81001001',
              '신소재공학과': '81001002',
              '화학생명공학과': '81001003',
              '산업경영공학과': '81001004',
              '설비공학과': '81001005',
              '창의융합학과': '81001006',
              '전기공학과': '82002001',
              '전자·제어공학과': '82002002',
              '컴퓨터공학과': '82002003',
              '정보통신공학과': '82002004',
              '건설환경공학과': '83003001',
              '도시공학과': '83003002',
              '건축공학과': '83003003',
              '건축학과': '83003004',
              '시각디자인학과': '83003005',
              '산업디자인학과': '83003008',
              '영어영문학과': '84004001',
              '중국어과': '84004002',
              '일본어과': '84004003',
              '공공행정학과': '84004004',
              '경영회계학과': '85005001',
              '경제학과': '85005002'
              }

    partNm = ['job', 'au', 'subj']

class PriorConfig(Config):
    def __init__(self):
        pass

    def priority(self, part1, part2):
        name = str(part1) + '_' + str(part2)
        mdf_name = name
        mdf_part1 = part1
        mdf_part2 = part2

        if name == 'au_job':
            mdf_name = 'job_au'
            mdf_part1 = 'au'
            mdf_part2 = 'job'

        elif name == 'subj_job':
            mdf_name = 'job_subj'
            mdf_part1 = 'job'
            mdf_part2 = 'subj'

        elif name == 'subj_au':
            mdf_name = 'au_subj'
            mdf_part1 = 'au'
            mdf_part2 = 'subj'

        else:
            pass

        return mdf_name, mdf_part1, mdf_part2

class linuxPath(Config):
    input_path = '/opt/heqms/heqms_test/input'
    model_path = '/opt/heqms/heqms_test/model'
    output_path = '/opt/heqms/heqms_test/output'
