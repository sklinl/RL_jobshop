observation = env.reset()
action = RL.choose_action(observation)
observation_, reward, done, info = env.step(action)
observation = observation_
