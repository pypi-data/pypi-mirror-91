# Concepts

## MSONable

One challenge in building complex data-transformation codes is keeping track of all the settings necessary to make some output database. One bad solution is to hard-code these settings, but then any modification is difficult to keep track of.

Maggma solves this by putting the configuration with the pipeline definition in JSON or YAML files. This is done using the `MSONable` pattern, which requires that any Maggma object (the databases and transformation steps) can convert itself to a python dictionary with it's configuration parameters in a process called serialization. These dictionaries can then be converted back to the origianl Maggma object without having to know what class it belonged. `MSONable` does this by injecting in `@class` and `@module` keys that tell it where to find the original python code for that Maggma object.

## Store

Another challenge is dealing with all the different types of databases out there. Maggma was originally built off MongoDB, so it's interface looks a lot like `PyMongo`. Still, there are a number of usefull new `object` databases that can be used to store large quantities of data you don't need to search in such as Amazon S3 and Google Cloud. It would be nice to have a single interface to all of these so you could write your datapipeline only once.

Stores are databases containing organized document-based data. They represent either a data source or a data sink. They are modeled around the MongoDB collection although they can represent more complex data sources that auto-alias keys without the user knowing, or even providing concatenation or joining of Stores. Stores implement methods to `connect`, `query`, find `distinct` values, `groupby` fields, `update` documents, and `remove` documents. Stores also implement a number of critical fields for Maggma that help in efficient document processing: the `key` and the `last_updated_field`. `key` is the field that is used to uniquely index the underlying data source. `last_updated_field` is the timestamp of when that document was last modified.

## Builder

Builders represent a data processing step. Builders break down each transformation into 3 phases: `get_items`, `process_item`, and `update_targets`:

1. `get_items`: Retrieve items from the source Store(s) for processing by the next phase
2. `process_item`: Manipulate the input item and create an output document that is sent to the next phase for storage.
3. `update_target`: Add the processed item to the target Store(s).

Both `get_items` and `update_targets` can perform IO (input/output) to the data stores. `process_item` is expected to not perform any IO so that it can be parallelized by Maggma. Builders can be chained together into an array and then saved as a JSON file to be run on a production system.

## Drone
Drone is a standardized class to synchronize local files and data in your database. It breaks down the process in 4 steps:

1. `get_items`
    - Given a folder path to a data folder, read all the files, and return a dictionary
        that maps each RecordKey -> List of `RecordIdentifier`
2. `should_update_records`
    - Given a list of `RecordIdentifier`, it query the database return a list of `RecordIdentifier` that requires update
3. `process_item` (from `Builder`)
    - Given a single `RecordIdentifier`, return the data that it refers to and add meta data
4. `update_targets`
    - updates the database given a list of data
