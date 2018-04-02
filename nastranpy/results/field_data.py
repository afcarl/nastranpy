import numpy as np


class FieldData(object):

    def __init__(self, name, data_by_LID, data_by_EID, LIDs, EIDs,
                 LID_name='LID', EID_name='EID'):
        self._name = name
        self._data_by_LID = data_by_LID
        self._data_by_EID = data_by_EID
        self._LIDs = np.array(LIDs, dtype=np.int64)
        self._EIDs = np.array(EIDs, dtype=np.int64)
        self._LID_name = LID_name
        self._EID_name = EID_name
        self._iLIDs = {LID: i for i, LID in enumerate(self._LIDs)}
        self._iEIDs = {EID: i for i, EID in enumerate(self._EIDs)}
        self._n_LIDs = len(self._LIDs)
        self._n_EIDs = len(self._EIDs)
        self._dtype = self._data_by_LID.dtype
        self._item_size = np.dtype(self._dtype).itemsize

    @property
    def name(self):
        return self._name

    @property
    def index_labels(self):
        return (self._LID_name, self._EID_name)

    @property
    def LIDs(self):
        return np.array(self._LIDs)

    @property
    def EIDs(self):
        return np.array(self._EIDs)

    @property
    def dtype(self):
        return self._dtype

    @property
    def shape(self):
        return self._data_by_LID.shape

    @property
    def size(self):
        return self._data_by_LID.size

    def close(self):
        self._data_by_LID = None
        self._data_by_EID = None

    def read(self, LIDs=None, EIDs=None, out=None):
        LIDs_queried = self._LIDs if LIDs is None else LIDs
        EIDs_queried = self._EIDs if EIDs is None else EIDs

        if out is None:
            out = np.empty((len(LIDs_queried), len(EIDs_queried)), dtype=self._dtype)

        array = out

        is_combination = isinstance(LIDs, dict)

        if is_combination:
            LIDs_queried = [LID for LID, seq in LIDs.items() if not seq]
            LIDs_requested = set(LIDs_queried)
            LIDs_queried += list({LID for seq in LIDs.values() for _, LID in seq if
                                  LID not in LIDs_requested and LID in self._iLIDs})
            LIDs_combined_used = list({LID for seq in LIDs.values() for _, LID in seq if
                                       LID not in self._iLIDs})
            LIDs_queried_index = {LID: i for i, LID in enumerate(LIDs_queried + LIDs_combined_used)}
            LID_combinations = [(LIDs_queried_index[LID] if LID in LIDs_queried_index else None,
                                 np.array([LIDs_queried_index[LID] for _, LID in seq]),
                                 np.array([coeff for coeff, _ in seq])) for LID, seq in LIDs.items()]
            array = np.empty((len(LIDs_queried) + len(LIDs_combined_used), len(EIDs_queried)), dtype=self._dtype)

        if len(LIDs_queried) < len(EIDs_queried):
            iEIDs = slice(None) if EIDs is None else np.array([self._iEIDs[EID] for EID in EIDs_queried])

            for i, LID in enumerate(LIDs_queried):
                array[i, :] = self._data_by_LID[self._iLIDs[LID], :][iEIDs]

        else:
            iLIDs = slice(None) if LIDs is None else np.array([self._iLIDs[LID] for LID in LIDs_queried])

            for i, EID in enumerate(EIDs_queried):
                array[:len(LIDs_queried), i] = self._data_by_EID[self._iEIDs[EID], :][iLIDs].T

        if is_combination:

            for i, (index, indexes, coeffs) in enumerate(LID_combinations):

                if len(coeffs):
                    out[i, :] = np.dot(array[indexes, :].T, coeffs)

                    if index:
                        array[index, :] = out[i, :]

                else:
                    out[i, :] = array[index, :]

        return out
