import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors


def RecommendDoctor(problem=None):
    df_appointment = pd.read_csv('MentalHealthPlatform\healthplatform\data.csv')
    df_doctor = pd.read_csv('MentalHealthPlatform\healthplatform\Doctor_Data.csv')

    df = df_appointment

    df.drop('Patient ID', axis = 1, inplace = True)
    df.drop('Problem', axis = 1, inplace = True)
    average_doctor_rating = pd.DataFrame(df.groupby(['Doctor_id']).mean())
    average_doctor_rating.rename(columns = {'Appointment Rating':'AverageRating'}, inplace = True)

    df = df.drop_duplicates(subset=["Doctor_id",])

    average_rating = average_doctor_rating.merge(df_doctor, on='Doctor_id')

    # df= pd.merge(right= df, left = average_doctor_rating, on="Doctor ID")
    average_rating = average_rating[average_rating['AverageRating']>2.5]

    # preprossing doctor data
    doc_data = pd.read_csv('MentalHealthPlatform\healthplatform\Doctor_Data.csv')

    doc_data.rename(columns = {'Doctor_id':'Doctor_id'}, inplace = True)

    # read appointment data
    do  =pd.read_csv('MentalHealthPlatform\healthplatform\data.csv')
    df = pd.merge(right=doc_data, left = do, on="Doctor_id")
    df = df.drop_duplicates(subset=["Doctor_id", "Problem"])
    piv = df.pivot(index = 'Problem', columns = 'Doctor_id',  values = 'Appointment Rating')
    piv = piv.fillna(0)

    # Build NearestNeighbors Object
    model_nn = NearestNeighbors(metric='cosine' , algorithm='auto', n_neighbors=10)

    # Fit the NearestNeighbor
    model_nn.fit(piv)

    if problem is not None:
        problem = problem
    else:
        problem="Unknown"

    X = piv[piv.index == problem ]
    X = X.to_numpy().reshape(1,-1)
    distances, indices = model_nn.kneighbors(X,n_neighbors=10)
    recommended_doctors = []
    for i in range(0, len(distances.flatten())):
        if i == 0:
            recommended_doctors.append(piv.index[indices.flatten()[0]])
        else:
            recommended_doctors.append(piv.index[indices.flatten()[i]])

    rec = [Problem for Problem in recommended_doctors]
    return rec