# Pokemon Image Repository

## Introduction

This api is an image repository for Pokemon! Currently only
generation 1 pokemon are supported.


## Endpoints

This api has 2 endpoints. Text search and Reverse image search.
Text search is fuzzy so don't worry about misspelling!

**Further documentation can be found [here](https://shopify-backend-4wd24tlmta-uc.a.run.app/swagger-ui/)**

**Front-end url to play with this api [here](https://shopify-backend-challenge-frontend.vercel.app/)** *please use Chrome on desktop*

Front-end Repository (code) found [here](https://github.com/alacwong/shopify-backend-challenge-frontend)

* Front-end UI components were inspired by this [website](https://h-richard.com/)
* Note api may have ~2s cold start since cloud run is serverless
* Note reverse image search depends on classification performance which works better/worse on different pokemon, eg does pretty well with charmander/charizard, but doesn't work as well with Eevee

## Running locally

Make sure you have Python 3.7 installed to run locally

```
$ pip install -r requirements.txt
$ flask run
```

## Methodology 

The search function seemed to be the most interesting problem to crack, so I
decided tackle it. Obviously building a "Google Image" clone would be very difficult. Even 
for text search, without data labels it would difficult to implement let alone reverse image search.

To solve this, I needed labeled data! Luckily I found a large Pokemon dataset on [kaggle](https://www.kaggle.com/thedagger/pokemon-generation-one).
I then created a bucket on google cloud to store these images. I then setup a MongoDB table to map the pokemon
names to the url found on the cloud for easy querying. For more interesting querying, I introduced fuzzy string
matching which uses the edit distance to determine closest pokemon name. Since my dataset was already on google, I decided
to use auto-ml to quickly train an image classifier that would later be used for reverse image search. The classifier
would classifier new images as a generation 1 pokemon, I would then output pokemon of that result.

I used the Flask framework for this Api. Flask api-spec provided good documentation with swagger.
For deployment I dockerized this application and deployed on Cloud run as a microservice which makes
this highly scalable.

## Next steps/ Future Improvements

1. Edit distance threshold, eg entering a search term like 'weiugnowegn', would 
still yield results since we find the closest pokemon name, maybe it would be
better to output no results.

2. More query terms, such as pokemon type (fire, flying, water ... ). This could be possible
but would require more preprocessing to determine additional tags for pokemon and update current table
to include these tags as well.

3. AutoML is expensive. I used around 30 node hours to train this model which was not cheap.
AutoML is very good for quick proto-typing, but does not always provide the best hyper-parameters
and is expensive so not very scalable. I would fix this by implementing my own image classifier 
that I can train whenever I want probably using a framework like Tensorflow or Pytorch. However
this would be difficult and would require quite a bit of time.

4. Reverse image search was only possible for this problem, because I limited 
the number of label/outputs for this problem. Therefore it would not work for a general case
(eg any image). To solve this, I would probably need to do more research on this topic.
This does seem like a clustering /un-supervised learning problem, however I would need to pick 
good features to do this. Perhaps, I could engineer good feature maps with a convolutional neural network?



