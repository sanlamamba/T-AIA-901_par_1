# Models

There are 2 systems which can be used to make inferences:
- A first one with an unique model used for a 4000 classes classification problem
- A second one made out of 2 models used to find the name of a city / train station and then classify these entities one by one.

The second one is by far the best model, since it's able to detect not only train stations, but also regions, departments and cities in a sentence. Not only can it do this, it can also detect the intermediaries and entities which are not outside of the itinary. The first model is only capable of detecting train station names for departures and arrivals.

# Setup
