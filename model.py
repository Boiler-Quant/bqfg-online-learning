from vowpalwabbit import pyvw

def train_model(model, data, loss_function='logistic'):
    for row in data:
        model.learn(row)
    model.save('model.vw')    
    return model

def predict(model, data):
    predictions = []
    for row in data:
        predictions.append(model.predict(row))
    model.finish()
    return predictions

def train_and_predict(data):
    model = pyvw.Workspace()
    model = train_model(model, data)
    predictions = predict(model, data)
    model.finish()
    return predictions