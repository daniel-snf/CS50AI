import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    ) # 60% para entrenar y 40% para validar

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []

    mes = dict(Jan=0, Feb=1, Mar=2, Apr=3, May=4, June=5, Jul=6, Aug=7, Sep=8, Oct=9, Nov=10, Dec=11)

    with open(filename, 'r') as archivo:
        reader = csv.reader(archivo)
        next(reader)
        for fila in reader:

            if fila[-1] == "TRUE":
                labels.append(1)
            else:
                labels.append(0)

            evidence.append(
                int(fila[0]), # Administrative como Int
                float(fila[1]), # Administrative_Duration como float
                int(fila[2]), # Informational como int
                float(fila[3]), # Informational_Duration como float
                int(fila[4]), # ProductRelated como int
                float(fila(5)), # ProductRelated_Duration como float
                float(fila(6)), # BounceRates como float
                float(fila(7)), # ExitRates como float
                float(fila(8)), # PageValues como float
                float(fila(9)), # SpecialDay como float
                mes(fila(10)), # Month como int
                int(fila(11)), # OperatingSystems como int
                int(fila(12)), # Browser como int
                int(fila(13)), # Region como int
                int(fila(14)), # TrafficType como int
                1 if fila[15] == "Visitante que Regresa" else 0,
                1 if fila[16] == "Verdadero" else 0
                )
            

    return evidence, labels



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    # Implementación basado en la libreria scikit-learn

    modelo = KNeighborsClassifier(n_neighbors = 1)
    modelo.fit(evidence, labels)
    return modelo


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

# Contadores
    positivos_verdaderos = 0
    positivos_actuales = 0
    negativos_verdaderos = 0
    negativos_actuales = 0
    
    for i in range(len(labels)):
        if labels[i] ==1:
            positivos_actuales +=1
            if predictions[i] == 1:
                positivos_verdaderos +=1
        else:
            negativos_actuales +=1
            if predictions[i] == 0:
                negativos_verdaderos +=1
        

    sensitividad = positivos_verdaderos / positivos_actuales
    especificidad = negativos_verdaderos / negativos_actuales

    return sensitividad, especificidad


if __name__ == "__main__":
    main()