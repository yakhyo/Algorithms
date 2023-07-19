# copy weights
def copy_weights(model1, model2):
    model1.eval()
    model2.eval()
    with torch.no_grad():
        m1_std = model1.state_dict().values()
        m2_std = model2.state_dict().values()
        for m1, m2 in zip(m1_std, m2_std):
            m1.copy_(m2)

# script to copy model weights one to another

keys1 = old_model.state_dict().keys()
values1 = old_model.state_dict().values()

keys2 = new_model.state_dict().keys()
values2 = new_model.state_dict().values()

old_state_dict = {}
new_state_dict = {}

for k1, v1, k2 in zip(keys1, values1, keys2):
    new_state_dict[k2] = v1
    old_state_dict[k1] = v1


torch.save(new_state_dict, "new.pt")
torch.save(old_state_dict, "old.pt")


old_model.load_state_dict(torch.load("bbb.pt"), strict=True)
new_model.load_state_dict(torch.load("ccc.pt"), strict=True)
