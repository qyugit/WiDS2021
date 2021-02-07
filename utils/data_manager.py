"""Utils for WiDS2021 datasets."""

import json
import os
import pandas as pd

from typing import Dict
from typing import Tuple


class DataManager(object):
    """Manages datasets for WiDS2021 competition."""

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.ontology = self.GetOntology()

    def LoadRawData(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load raw datasets.

        Retuns:
            train_raw: <pd.DataFrame> Raw training data.
            test_raw: <pd.DataFrame> Raw test data.
        """
        train_raw = pd.read_csv(self.data_dir+"TrainingWiDS2021.csv.zip")
        test_raw = pd.read_csv(self.data_dir+"UnlabeledWiDS2021.csv.zip")

        return train_raw, test_raw

    def GetOntology(self) -> Dict:
        """Create ontology from the DataDictionaryWiDS2021.

        Retuns:
            ontology: <Dict> contains the information of variables.
        """
        if os.path.exists(self.data_dir+"ontology.josn"):
            with open(self.data_dir+"ontology.josn", "r") as f:
                ontology = json.load(f)
        else:
            raw_data_dict = pd.read_csv(
                self.data_dir+"/DataDictionaryWiDS2021.csv.zip")
            ontology = {}
            for _, row in raw_data_dict.iterrows():
                variable_info = {"dtype": row["Data Type"],
                                 "unit": row["Unit of Measure"],
                                 "description": row["Description"]}
                if row["Category"] not in ontology:
                    ontology[row["Category"]] = {}
                ontology[row["Category"]][row["Variable Name"]] = variable_info

            with open(self.data_dir+"ontology.josn", "w") as f:
                json.dump(ontology, f)

        return ontology
