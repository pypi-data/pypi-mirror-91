from gensim.models.doc2vec import Doc2Vec
import heqms_pkg.preprocess.preprocessing as pre
import heqms_pkg.config as cf
import multiprocessing

class ml_pvdm:
    def __init__(self):
        self.max_epochs = 2
        self.cores = multiprocessing.cpu_count()
        self.model = Doc2Vec(
            epochs=100,
            window=4,
            vector_size=1024,
            alpha=0.025,
            min_alpha=0.025,
            min_count=0,
            dm=1,
            negative=2,
            workers=self.cores,
            seed=42)

    def learning(self, part1, part2, deptNm):
        # 우선순위 변경
        name, mdf_part1, mdf_part2 = cf.PriorConfig().priority(part1, part2)

        # 불러오기
        prepro = pre.Preprocessing()
        tagged_data = prepro.to_tag(mdf_part1, mdf_part2, deptNm)
        max_epochs = self.max_epochs
        model = self.model

        model.build_vocab(tagged_data)

        # 머신러닝 학습
        for epoch in range(max_epochs):
            print('iteration {0}'.format(epoch))
            model.train(tagged_data,
                        total_examples=model.corpus_count,
                        epochs=model.iter)
            # 학습률 감소시킴
            model.alpha -= 0.002
            # 학습률 조정
            model.min_alpha = model.alpha

        deptNum = cf.UnivConfig.deptNo[deptNm] # 학과이름 -> 학과번호로 교체

        # 모델 저장
        model_path = cf.linuxPath.model_path
        fileName = str(deptNum) + '_' + name + '_d2v.model'
        model.save(model_path + "/" + fileName)
        print("Model Saved")

        return model

