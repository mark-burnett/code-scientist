# code-scientist

## Requirements

sqlalchemy

## Testing

To run unit tests you need the discover module:

python -m discover -s tests

## Architecture

### Model

The model is a collection of sqlalchemy ORM objects that represent the various
metrics collected on each file.

### Views

Views will be textual reports and figures derived from analysis done on the
model.
