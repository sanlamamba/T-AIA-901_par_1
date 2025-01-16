# Models

There are 2 systems which can be used to make inferences:
- A first one with an unique model used for a 4000 classes classification problem
- A second one made out of 2 models used to find the name of a city / train station and then classify these entities one by one.

The second one is by far the best model, since it's able to detect not only train stations, but also regions, departments and cities in a sentence. Not only can it do this, it can also detect the intermediaries and entities which are not outside of the itinary. The first model is only capable of detecting train station names for departures and arrivals.

# Setup

The following section will focus on setting-up the 2nd system. Every commands will be made from the ./model folder.

We will start by downloading most dependencies needed.

``` bash
    conda env update -f ./environment.yaml
```

Once done, head to the [PyTorch website](https://pytorch.org/) and download the right PyTorch configuration with a stable version and conda package. You don't need to download a GPU configuration for this project if you don't intend on running on a GPU the models. A CPU one is plenty enough.

Install Spacy's pipeline:

```bash
    python -m spacy download fr_core_news_sm
```

Ask for permission from [@DanyLeguy](https://www.github.com/LeguyDany) the access to the Azure bucket in order to download the models. Once granted, create a .env file in the project's root while filling in your connection string:

```
AZURE_CONNECTION_STRING="YOUR_CONNECTION_STRING"
```

Make sure that a new conda virtual environment has been setup:

```bash
    conda info --envs
```

Your should see an environment named "myenv". If that's the case, activate it:

```bash
    conda activate myenv
```

Once done, you are now going to download the models. There are two models that you need to be aware of:

- NER_model.pth
- model.pth

Both are needed in order to run this project. To download both of them, head to ./model/src/bin and run this command:

```bash
    python ./download_model.py
```

Once done, run this command to see if everything has been installed correctly:

```bash
    python ./prompt_model.py
```

# Prompting the models

Every happens with the ./model/src/bin/prompt_model.py file. Feel free to change the sentence in that file to get different itinaries:

```python
sentence = f"Je souhaite aller de l'{city_6} à {city_4}."
```

This sentence will be sent to the NER first, then to the classification model.

# How these models work

This section will explain how both models work for the 2nd system.

## Custom NER with BERT

This model is a fine-tuned BERT specialized in french. Its goal is mainly to identify specific entities (city, regions, departments and train station names) without further classification and put these entities in a list.

A lot of names are made of several words (i.e. "Île de France"), which means it needs to be able to recognize where a composite name starts and where it ends. In order to achieve this, this pretrained BERT model has been further fine-tuned with the IOB tagging system in mind.

IOB tagging correspond to tag each word in a sentence with:
- B for beginning, to indicate that it's the first word of a composite name.
- I for inside, to indicate that it's a word in a composite name.
- O for outside, to indicate that it's not a word to care for.

This model is going to run on every single word from your prompts to classify each one of them with these tag. Each tag will then be place right after your words, for instance:

```
Je[O] vais[O] de[O] Cergy[B] Saint-Christophe[I] à[O] Marseille[B].
```

From this string, a python script is going to concatenate the composite words of a name, remove the tags and put all of these names into a single list. This list will then serve as a starting point to the next classification model.

## Status classification with BERT

This second model is yet again another fine-tuned pretrained BERT model specialized in french. In fact, both this status classification model and the NER have the same base pretrained model, but are fine-tuned through different dataset.

This model is simpler than the previous one, since it won't be tagging every single word. Therer are 4 classes which need to be assigned for the names taken out from the sentence:

- departure
- arrival
- intermediary
- none

This is going to be the main focus of this model. To achieve this, we are pre-processing the sentence to make it focus on tagged words. Tagged words are put in between brackets in the following manner:

```
Je souhaite aller de [[Paris]] à Marseille.
```

This will indicate the model to focus on this word to make its inference. Once the inference made, we just need to remove these brackets and place them onto the next name:

```
Je souhaite aller de Paris à [[Marseille]].
```

This is done for every names in the model up until none of them remain.

While doing all of this, a class will be assigned to these names, and we will then end-up with a list of dictionnaries following this format:

```python
[
    {
        'status': 'departure', 
        'place': 'île de france',
    },
    {
        'status': 'arrival',
        'place': 'marseille',
    }
]
```

This is fine and all, but these are names of cities, and not train stations. Some further processing are needed to aquire this information.

## Post-processing script

A dataset has been specifically created in order to associate each place to a train station (i.e. ./data/cities_and_train_stations.csv). The associated train station has been calculated using the latitude and longitude of the place, compared to the latitude and longitude of every single train station through the Haversine formula.

Cities have their own latitude and longitude, but regions and departments do not. To circumvent this issue, each regions and departments will be associated to a train station depending on the number of cities under the regions / department. We will pick the train station with the highest number of nearby cities in these areas.

Some fuzzy search has been implemented, allowing for mis-spelling to some degrees by the user for the names of the places. Every word is stripped from their hyphens and is entirely put in lower case.

We end up with a list of dictionnaries looking like this from this point:

```python
[
    {
        'status': 'departure', 
        'place': 'île de france',
        'train_station': 'Moret-Veneux-les-Sablons'
    },
    {
        'status': 'arrival',
        'place': 'marseille',
        'train_station': 'Marseille-St-Charles'
    }
]
```
