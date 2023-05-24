This repository is heavily based off of this CPO implementation by the Github user SapanaChaudary: https://github.com/SapanaChaudhary/PyTorch-CPO.
I used the code from this repo and edited it to fix some bugs/issues and ran some experiments with OpenAI Gym environments like the cartpole and
mountain car(discrete and continuous). These environments didn't provide costs so I wrote a constraint cost function. I ran experiments with these
environments and a cost of 0 at all times as well as a cost of 1 when safety was violated (for example, going past a certain angle with cartpole).
The graphs of cumulative rewards/costs for my experiment with the cartpole environment and costs of 0/1 are available. I then edited the code 
significantly to get it to work with a car yaw environment on a reposity not yet public for my Spring 2023 research project(commits after April 21st). 
My final code as well as the data from the various experiments I ran (safety violations per episode, cumulative rewards/costs) is on this github: 
https://github.com/ritabrata-ray. Since it is currently private, the data is not yet available.

