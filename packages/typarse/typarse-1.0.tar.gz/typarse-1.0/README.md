# Typarse

This is a small project born out of my frustration with simple argument parsing in Python.

Not only do I have to instantiate some object whose name I can never remember, then I get way too many 
function parameters to get them right... It's a mess. And I don't even need half the features.

So this is an attempt at streamlining this process while simultaneously promoting some better type safety, by using the
magic of Python type hints!

Really all the magic here is happening in the BaseParser class. You just need to subclass it, add a few typed parameters,
perhaps with some extra information in dictionaries... and you're done! For examples, just look at, well, examples.