import pandas as pd


class LabelMap():
    """
    LabelMap

    This class is a map between labels and ids.

    Parameters
    ----------
    labels_csv : str
        The path to the csv file containing the labels and ids.
    labels_col_name : str
        The name of the column containing the labels.
    ids_col_name : str
        The name of the column containing the ids.
    id_type : type
        The type of the ids.

    Attributes
    ----------
    label_map : dict
        The map between labels and ids.
    label_map_inv : dict
        The map between ids and labels.
    label_count : int
        The number of labels.
    label_data : pandas.DataFrame
        The dataframe containing the labels and ids.

    Methods
    -------
    add(label)
        Add a label to the label map.
    force_get(label)
        Get the id of a label or if id not found then add the label and get.
    to_text(id)
        Get the label of an id.
    to_id(label)
        Get the id of a label.
    map()
        Get the label map as dict.
    labels()
        Get the list of labels.
    print()
        Print the label map as table.
    count()
        Get the number of labels.
    get_csv()
        Get the data in the provided csv file.

    """
    __label_map__ = {}
    __label_map_inv__ = None
    __label_count__ = 0
    __label_data__ = None
    __cache_outdated__ = False

    def __init__(self, labels_csv=None, labels_col_name=None, ids_col_name=None, id_type=int):
        if labels_csv != None:
            if id_type != float and id_type != int:
                raise ValueError("id_type must be a int or float type")
            self.__type__ = id_type
            self.__label_data__ = pd.read_csv(labels_csv)
            self.__from_csv__(self.__label_data__,
                              labels_col_name, ids_col_name)

    def __from_csv__(self, label_data, labels_col_name, ids_col_name):
        self.__cache_outdated__ = True
        if labels_col_name == None:
            raise ValueError(
                "lable_col_name can't be None if labels_csv is not None")
        for i in range(0, len(label_data)):
            row = label_data.iloc[i]
            if self.__label_map__.get(row[labels_col_name]) == None:
                _id = self.__type__(self.__label_count__)
                if ids_col_name != None:
                    _id = row[ids_col_name]
                self.__label_map__[row[labels_col_name]] = _id
                self.__label_count__ += 1

    def add(self, label):
        """
        Add a label to the label map.

        Args
        ----------
        label -> string
        """
        if self.__label_map__.get(label) == None:
            self.__label_map__[label] = self.__type__(self.__label_count__)
            self.__cache_outdated__ = True
            self.__label_count__ += 1

    def force_get(self, label) -> int:
        """
        Get the id of the given label, if id of the label is None then add the label and return id.

        Args
        ----------
        label -> string
        """
        if self.__label_map__.get(label) == None:
            self.add(label)
        return self.__label_map__.get(label)

    def to_text(self, id) -> str:
        """
        Get the label of an id.

        Args
        ----------
        id -> int/ float
        """
        if(self.__label_map_inv__ == None or self.__cache_outdated__):
            self.__label_map_inv__ = {v: k for k,
                                      v in self.__label_map__.items()}
            self.__cache_outdated__ = False
        return self.__label_map_inv__[id]

    def to_id(self, label) -> int:
        """
        Get the id of the given label.

        Args
        ----------
        label -> string
        """
        return self.__label_map__[label]

    def map(self) -> dict:
        """
        Get the label map as dict.

        Args
        ----------
        None
        """
        return self.__label_map__

    def labels(self) -> list:
        """
        Get the list of lables

        Args
        ----------
        None
        """
        lst = []
        for label in self.__label_map__:
            lst.append(label)
        return lst

    def print(self) -> None:
        """
        Print the label map as table

        Args
        ----------
        None
        """
        print("{:>7} | {:<50}".format("ID", "LABEL"))
        print("{:>7}+{:<50}".format("--------",
              "----------------------------------------------"))
        for label in self.__label_map__:
            print("{:>7} | {:<50}".format(self.to_id(label), label))

    def count(self) -> int:
        """
        Get the number of labels.

        Args
        ----------
        None
        """
        return len(self.__label_map__)

    def get_csv(self) -> pd.DataFrame:
        """
        Get the data in the provided csv file.

        Args
        ----------
        None
        """
        return self.__label_data__
