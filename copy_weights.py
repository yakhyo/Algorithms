# copy weights
def copy_weights(model1, model2):
    model1.eval()
    model2.eval()
    with torch.no_grad():
        m1_std = model1.state_dict().values()
        m2_std = model2.state_dict().values()
        for m1, m2 in zip(m1_std, m2_std):
            m1.copy_(m2)
