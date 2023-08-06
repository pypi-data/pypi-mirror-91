from pathlib import Path
from typing import List

import pandas as pd

from sktmls.autogluon import TabularPrediction as task, __version__

MLS_MODEL_DIR = Path.home().joinpath("models")


class MLSTrainable:
    """
    AutoGluon을 통한 학습을 지원하는 클래스입니다.

    이 클래스는 단독으로 상속될 수 없으며 MLSModel과 함께 상속되어야 정상 동작합니다.

    `sktmls.models.contrib.GenericLogicModel`에서 실사용 가능합니다.
    """

    def fit(
        self,
        train_data: pd.DataFrame,
        label: str,
        test_data: pd.DataFrame = None,
        eval_metric: str = "roc_auc",
        non_training_features: List[str] = [],
    ) -> None:
        """
        AutoGluon을 통해 모델을 학습합니다.

        모델 학습이 완료되면 `self.models[0]`에 자동으로 할당되며, 이후 `predict` 함수에서 참조될 수 있습니다.

        ## 참고 사항

        - Inference 성능을 고려하여 LightGBM의 앙상블 모델만을 지원합니다.
        - AutoGluon이 자동으로 분류 문제인지 회귀 문제인지 판단합니다.
        - 성능 지표를 설정할 수 있으나, 분류 문제의 경우 기본값인 `roc_auc` 사용을 권장합니다.
        - 회귀 문제에 분류 성능 지표를 세팅하거나 분류 문제에 회귀 성능 지표를 세팅하면 에러가 발생합니다.

        ## Args

        - train_data: (`pandas.DataFrame`) 학습에 사용할 데이터 프레임
        - label: (str) train_data 내 라벨 컬럼 이름
        - test_data: (optional) (`pandas.DataFrame`) 모델 성능 측정을 위한 테스트 데이터 프레임 (기본값: None)
        - eval_metric: (optional) (str) 성능 지표 (기본값: `roc_auc`)
            - 분류 모델의 경우 가능한 값: `accuracy`|`balanced_accuracy`|`f1`|`f1_macro`|`f1_micro`|`f1_weighted`|`roc_auc`|`average_precision`|`precision`|`precision_macro`|`precision_micro`|`precision_weighted`|`recall`|`recall_macro`|`recall_micro`|`recall_weighted`|`log_loss`|`pac_score`
            - 회귀 모델의 경우 가능한 값: `root_mean_squared_error`|`mean_squared_error`|`mean_absolute_error`|`median_absolute_error`|`r2`
        - non_training_features: (optional) (str) 학습에서 제외할 피쳐 이름 리스트. 후처리 전용 피쳐 등을 명세할 때 사용 가능 (기본값: [])

        ## Example

        features = [...]
        preprocess_logic = {...}
        postprocess_logic = {...}

        # 학습을 직접 할 것이므로 `model`을 `None`으로 할당합니다.
        my_model_v1 = GenericLogicModel(
            model=None,
            model_name="my_model",
            model_version="v1",
            features=features,
            preprocess_logic=preprocess_logic,
            postprocess_logic=postprocess_logic,
            predict_fn="predict_proba"
        )

        # 학습 및 테스트 데이터 준비
        train_data, test_data = train_test_split(df, test_size=0.2, random_state=0)

        # 학습
        my_model_v1.fit(
            train_data=train_data,
            test_data=test_data,
            label="some_label"
        )

        # 성능 확인
        print(my_model_v1.performance)
        print(my_model_v1.feature_importance)

        # predict 테스트
        print(my_model_v1.predict(test_feature_values, pf_client=pf_client))

        # 배포
        model_registry = ModelRegistry(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE)
        model_registry.save(my_model_v1)
        """

        self.model_lib = "autogluon"
        self.model_lib_version = __version__
        self.metric = eval_metric
        self.label = label
        self.non_training_features = non_training_features
        self.preprocess_logic = {"merge": [{"var": f} for f in self.features if f not in non_training_features]}

        self.models[0] = self._fit(train_data, eval_metric)
        if test_data is not None:
            feature_importance = self.get_feature_importance(test_data)
            positive_features = feature_importance[feature_importance > 0].index.tolist()
            while len(self.features) > len(positive_features):
                self.features = positive_features + non_training_features
                self.preprocess_logic = {"merge": [{"var": f} for f in positive_features]}
                self.models[0] = self._fit(train_data, eval_metric)
                feature_importance = self.get_feature_importance(test_data)
                positive_features = feature_importance[feature_importance > 0].index.tolist()

            self.performance = self.evaluate(test_data)
            self.feature_importance = feature_importance.to_dict()

        self.model_info = self.models[0].info()
        self.models[0].delete_models(models_to_keep="best", dry_run=False)
        self.models[0].save_space(remove_data=True, remove_fit_stack=False, requires_save=False, reduce_children=False)
        self.models[0]._trainer.reset_paths = True

    def _fit(self, train_data: pd.DataFrame, eval_metric: str):
        columns = [f for f in self.features if f not in self.non_training_features] + [self.label]
        return task.fit(
            train_data=train_data[columns],
            label=self.label,
            presets=["good_quality_faster_inference_only_refit"],
            hyperparameters={"GBM": {}, "CAT": {}},
            eval_metric=eval_metric,
            output_directory=MLS_MODEL_DIR.joinpath(self.model_name, self.model_version),
        )

    def evaluate(self, test_data: pd.DataFrame) -> float:
        """
        AutoGluon을 통해 학습한 모델의 성능을 계산합니다.

        ## 참고 사항

        - `fit` 함수를 통해 학습이 된 경우에만 정상적으로 동작합니다.
        - `fit` 함수에서는 모델 학습 후 한 차례 본 함수를 실행하여 `self.performace`에 저장합니다.

        ## Args

        - test_data: (optional) (`pandas.DataFrame`) 모델 성능 측정을 위한 테스트 데이터 프레임 (기본값: None)

        ## Example

        # 학습 및 테스트 데이터 준비
        train_data, test_data = train_test_split(df, test_size=0.2, random_state=0)

        # 학습
        my_model_v1.fit(
            train_data=train_data,
            test_data=test_data,
            label="some_label"
        )

        # 성능 계산
        print(my_model_v1.evaluate(test_data))
        """
        columns = [f for f in self.features if f not in self.non_training_features] + [self.label]
        return self.models[0].evaluate(test_data[columns], silent=True).tolist()

    def get_feature_importance(self, test_data: pd.DataFrame) -> pd.Series:
        """
        AutoGluon을 통해 학습한 모델의 피쳐 중요도를 계산하여 `pandas.Series` 형식으로 리턴합니다.

        ## 참고 사항

        - `fit` 함수를 통해 학습이 된 경우에만 정상적으로 동작합니다.
        - `fit` 함수에서는 모델 학습 후 한 차례 본 함수를 실행하여 `self.feature_importance`에 저장합니다.

        ## Args

        - test_data: (optional) (`pandas.DataFrame`) 모델 성능 측정을 위한 테스트 데이터 프레임 (기본값: None)

        ## Example

        # 학습 및 테스트 데이터 준비
        train_data, test_data = train_test_split(df, test_size=0.2, random_state=0)

        # 학습
        my_model_v1.fit(
            train_data=train_data,
            test_data=test_data,
            label="some_label"
        )

        # 성능 계산
        print(my_model_v1.get_feature_importance(test_data))
        """
        columns = [f for f in self.features if f not in self.non_training_features] + [self.label]
        return self.models[0].feature_importance(test_data[columns], silent=True)

    def set_mms_path(self) -> None:
        """
        MMS에서의 정상적인 inference를 위한 path 업데이트 함수로 내부 호출 용도입니다.
        """
        trainer = self.models[0]._trainer
        for model_name in trainer.get_model_names_all():
            trainer.set_model_attribute(
                model_name, "path", f"/models/{self.model_name}/{self.model_version}/models/{model_name}/"
            )

    def set_local_path(self) -> None:
        """
        로컬 환경에서의 정상적인 inference를 위한 path 업데이트 함수로 내부 호출 용도입니다.
        """
        trainer = self.models[0]._trainer
        for model_name in trainer.get_model_names_all():
            trainer.set_model_attribute(
                model_name, "path", f"{MLS_MODEL_DIR}/{self.model_name}/{self.model_version}/models/{model_name}/"
            )

    def persist_models(self) -> None:
        """
        모델 캐시를 위한 함수로 내부 호출 용도입니다.
        """
        self.models[0].persist_models()

    def unpersist_models(self) -> None:
        """
        모델 캐시 만료를 위한 함수로 내부 호출 용도입니다.
        """
        self.models[0].unpersist_models()

    def get_model_names_persisted(self) -> List[str]:
        """
        캐시된 모델 이름 조회를 위한 함수로 내부 호출 용도입니다.
        """
        return self.models[0].get_model_names_persisted()
