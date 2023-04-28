import torch.nn as nn
import torch
from utils.math import *

#policy with number of neurons
#maybe need to make smaller for mountain car? takes a while to run
class DiscretePolicy(nn.Module):
    def __init__(self, state_dim, action_num, hidden_size=(100, 100), activation='tanh'):
        super().__init__()
        self.is_disc_action = True
        #hyperbolic tangent
        if activation == 'tanh':
            self.activation = torch.tanh
        elif activation == 'relu':
            self.activation = torch.relu
        elif activation == 'sigmoid':
            self.activation = torch.sigmoid

        #all contained nodes connect to all nodes of the subsequent layer
        self.affine_layers = nn.ModuleList()
        last_dim = state_dim
        for nh in hidden_size:
            self.affine_layers.append(nn.Linear(last_dim, nh))
            last_dim = nh

        self.action_head = nn.Linear(last_dim, action_num)
        self.action_head.weight.data.mul_(0.1)
        self.action_head.bias.data.mul_(0.0)

    #make predictions, defines structure
    def forward(self, x):
        for affine in self.affine_layers:
            x = self.activation(affine(x))

        action_prob = torch.softmax(self.action_head(x), dim=1)
        return action_prob

    #select action based on probabilities
    def select_action(self, x):
        print(x)
        action_prob = self.forward(x)
        action = action_prob.multinomial(1)
        return action

    #returns kl divergence - measures the probability difference of two policies
    def get_kl(self, x):
        action_prob1 = self.forward(x)
        action_prob0 = action_prob1.detach()
        kl = action_prob0 * (torch.log(action_prob0) - torch.log(action_prob1))
        return kl.sum(1, keepdim=True)

    #return log of the action probabilities
    def get_log_prob(self, x, actions):
        action_prob = self.forward(x)
        return torch.log(action_prob.gather(1, actions.long().unsqueeze(1)))

    #fisher information matrix - 2nd order derivative of kl divergence
    #metric tensor(distance function) between two points in the policy space
    def get_fim(self, x):
        action_prob = self.forward(x)
        M = action_prob.pow(-1).view(-1).detach()
        return M, action_prob, {}

